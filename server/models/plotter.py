#!/usr/bin/python
# -*- coding: utf-8 -*-

from datetime import datetime
from django.utils import timezone
from django.db import models
from .settings import GATEWAY_DOMAIN

from .plot_config import PlotConfig
from .harvester import Harvester
import logging,traceback,json
logger = logging.getLogger(__name__)
from .choices import CACHE_TYPE
from common.helper import get_human_readable_size



class Plotter(models.Model):
    """
    plotter server
    """
    server_number = models.CharField('Id', max_length=50, default='001')
    plot_config = models.ForeignKey(PlotConfig, verbose_name='PlotConfig', on_delete=models.SET_NULL, default=None,
                                    blank=True, null=True)
    plot_config_applied = models.BooleanField('Plot Config Applied', default=False)

    description = models.CharField('Description', max_length=1000, default='', blank=True)

    st_plot_process_cnt = models.IntegerField('Process', default=0)
    st_plot_output = models.IntegerField('Output', default=0)
    st_avg_plot_time = models.FloatField('Plot Time', default=0)
    st_avg_copy_time = models.FloatField('Copy Time', default=0)

    st_update_time = models.DateTimeField('UpdateTime', default=datetime.now, blank=True)


    internal_ip = models.CharField('Internal IP', max_length=20, default='', blank=True)
    is_sending_run = models.BooleanField('Sending', default=False)

    harvester = models.ForeignKey(Harvester, verbose_name='Harvester', on_delete=models.SET_NULL, default=None,
                                    blank=True, null=True)

    is_plotting_run = models.BooleanField('Plotting', default=False)

    boot_time = models.DateTimeField('Boot Time', default=datetime.now, blank=True)#server boot at this time
    uptime = models.IntegerField('Uptime', default=0, blank=True)

    cpu_model = models.CharField('CPU', max_length=100, default='', blank=True)
    cpu_cnt = models.IntegerField('CPU Count', default=0)
    cpu_used_percent = models.FloatField('CPU Used Percent', default=0)
    memory_total = models.BigIntegerField('Memory Total', default=0)
    memory_used = models.BigIntegerField('Memory Used', default=0)

    nvme_size = models.FloatField('NVME Size', default=0)
    nvme_cnt = models.IntegerField('NVME Count', default=1)

    plot_cnt = models.IntegerField('Plot Count', default=0)

    is_cache_raid = models.BooleanField('Cache Raid', default=False)
    exclude_plot_dst_path = models.CharField('Exclude Dst Paths', max_length=1000, default='', blank=True)
    plot_file_path = models.CharField('Plot File Path', max_length=1000, default='', blank=True)

    last_heartbeat = models.DateTimeField('HeartBeat', default=timezone.now, blank=True)

    data_interface = models.CharField('Data Network Card', max_length=100, default='', blank=True)

    __original_plot_config = None

    def __init__(self, *args, **kwargs):
        super(Plotter, self).__init__(*args, **kwargs)
        self.__original_plot_config = self.plot_config

    class Meta:
        app_label = 'server'

    def __unicode__(self):
        return u'plotter-%s' % self.server_number

    def __str__(self):
        return self.__unicode__()

    def cache(self):
        if self.is_cache_raid:
            return '%s*%s-R' % (self.nvme_size, self.nvme_cnt)
        return '%s*%s' % (self.nvme_size, self.nvme_cnt)

    cache.short_description = 'nvme/raid'

    def dest_nas(self):
        if self.harvester is None:
            return '---'
        else:
            return self.harvester.server_number

    dest_nas.short_description = 'NAS'

    def job_plot(self):
        avg_plot_hour = (self.st_avg_plot_time + self.st_avg_copy_time) / 3600
        return "%s / %s" % (self.st_plot_process_cnt, self.st_plot_output)
    job_plot.short_description = 'Job/Plot'

    def time_round(self):
        avg_plot_hour = (self.st_avg_plot_time + self.st_avg_copy_time) / 3600
        round_process = round(24 / avg_plot_hour if avg_plot_hour > 0 else 0,2)
        return '%s/%s' % (round((self.st_avg_plot_time + self.st_avg_copy_time)/3600, 2), round_process)
    time_round.short_description = 'Time/Round'

    def output(self):
        avg_plot_hour = (self.st_avg_plot_time + self.st_avg_copy_time)/3600
        round_process = 24/avg_plot_hour if avg_plot_hour > 0 else 0
        out_put = self.st_plot_process_cnt * round_process
        stagger = 0
        if self.plot_config is not  None:
            stagger = self.plot_config.global_stagger_m
        else:
            stagger = 48

        return round(out_put, 2)

    def cpu(self):
        return '{:.0f}%'.format(round(self.cpu_used_percent, 2))

    def up_time(self):
        if self.uptime < 3600:
            return '%sm' % round(self.uptime/60,2)
        else:
            return '%sh' % round(self.uptime/3600,2)

    def cache_raid(self):
        return self.is_cache_raid

    def mem(self):
        return '{:.0f}%'.format(round((float(self.memory_used*100)/self.memory_total),2) if self.memory_total>0 else 0)

    def thread(self):
        if self.plot_config is not None:
            real_cache_cnt = self.nvme_cnt
            if self.is_cache_raid :
                real_cache_cnt = 1
            return (self.plot_config.global_max_jobs - self.plot_config.tmpdir_stagger_phase_limit * real_cache_cnt) + (real_cache_cnt * self.plot_config.tmpdir_stagger_phase_limit *  self.plot_config.n_threads)
        else:
            return '--'

    def _is_online(self):
        """
        if server do not receive info in 3 minutes, we think it is gone
        :return:
        """
        now = timezone.now()
        if (now - self.last_heartbeat).total_seconds() > 60*3:
            return False
        return True

    _is_online.boolean = True
    _is_online.short_description = 'Online'
    is_online = property(_is_online)


    def _update_heartbeat(self, need_save=False):
        self.last_heartbeat = timezone.now()
        if need_save:
            self.save()

    def update_statistic(self, data):
        self.st_plot_process_cnt = data['plot_process_cnt']
        self.st_plot_output = data['plot_output']
        self.st_avg_plot_time = data['avg_plot_time']
        self.st_avg_copy_time = data['avg_copy_time']
        self.st_update_time = datetime.now()
        self._update_heartbeat()
        self.save()

    def update_register(self,data):
        self.boot_time = data['boot_time']

        if 'cpu' in data:
            self.cpu_model = data['cpu']['brand']
            self.cpu_cnt = data['cpu']['count']
            self.cpu_used_percent = data['cpu']['used_percent']

        if 'memory' in data:
            self.memory_total = data['memory']['total']
            self.memory_used = data['memory']['used']

        if 'nvme' in data:
            self.nvme_size = data['nvme']['nvme_size']
            self.nvme_cnt = data['nvme']['nvme_cnt']
            if 'is_cache_raid' in data['nvme']:
                self.is_cache_raid = data['nvme']['is_cache_raid']
        self._update_heartbeat()
        self.save()

    def update_local_info(self, data):
        if 'info' in data:
            self.is_sending_run = data['info']['is_sending_run']
            self.internal_ip = data['info']['internal_ip']
            self.uptime = data['info']['uptime']
            self.plot_cnt = data['info']['plot_cnt']

        if 'cpu' in data:
            self.cpu_model = data['cpu']['brand']
            self.cpu_cnt = data['cpu']['count']
            self.cpu_used_percent = data['cpu']['used_percent']

        if 'memory' in data:
            self.memory_total = data['memory']['total']
            self.memory_used = data['memory']['used']
        self._update_heartbeat()
        self.save()

    def get_info(self):
        return {
            'name': self.server_name(),
            'is_plotting_run': self.is_plotting_run
        }

    def server_name(self):
        return u'plotter-%s' % self.server_number

    def update_system(self):
        from server.plotter_api import PlotterAPI
        api = PlotterAPI(self)
        result = api.update_system()
        logging.info('update plotter:%s result:%s' % (self.server_name(), result))


    def get_plot_config_dict(self):
        if self.plot_config is None:
            # return default dict
            return {
            'name': 'default',
            'k': 32,
            'e': True,
            'n_threads': 4,
            'n_buckets': 128,
            'job_buffer': 4000,

            'global_max_jobs': 10,
            'global_stagger_m': 48,
            'tmpdir_max_jobs': 10,
            'tmpdir_stagger_phase_major': 2,
            'tmpdir_stagger_phase_minor': 1,
            'tmpdir_stagger_phase_limit': 6,
            'exclude_plot_dst_path': self.exclude_plot_dst_path,
            'plot_file_path': self.plot_file_path,
            'data_interface': self.data_interface,
        }
        else:
            data =  self.plot_config.to_dict()
            data['exclude_plot_dst_path'] = self.exclude_plot_dst_path,
            data['plot_file_path'] = self.plot_file_path,
            data['data_interface'] = self.data_interface

            return data

    @property
    def plot_config_content(self):
        if self.plot_config is None:
            return '[10/10 | 6-2:1 | 48] [-e:True -r:4 -b:4000 ] default'
        else:
            return self.plot_config.content

    @property
    def api_host(self):
        return '%s.%s' % (self.server_number,GATEWAY_DOMAIN)

    @property
    def api_port(self):
        return 8080

    def save(self, force_insert=False, force_update=False, *args, **kwargs):
        config_change = False
        if self.plot_config != self.__original_plot_config:
            self.plot_config_applied = False
            #fire_event = True
        super(Plotter, self).save(force_insert, force_update, *args, **kwargs)
        self.__original_plot_config = self.plot_config

        #if config_change:
        #    #call gateway to apply config

