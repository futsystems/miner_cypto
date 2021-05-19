#!/usr/bin/python
# -*- coding: utf-8 -*-

from datetime import datetime

from django.db import models
from .settings import GATEWAY_DOMAIN

from .plot_config import PlotConfig
from .harvester import Harvester

from .choices import CACHE_TYPE



class Plotter(models.Model):
    """
    plotter server
    """
    server_number = models.CharField('Server Id', max_length=50, default='001')
    plot_config = models.ForeignKey(PlotConfig, verbose_name='PlotConfig', on_delete=models.SET_NULL, default=None,
                                    blank=True, null=True)
    plot_config_applied = models.BooleanField('Plot Config Applied', default=False)

    cache_type = models.CharField('Cache Type', max_length=20, choices=CACHE_TYPE, default='3.2*1')

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

    def output(self):
        return "%s / %s" % (self.st_plot_process_cnt, self.st_plot_output)

    def time(self):
        return round((self.st_avg_plot_time + self.st_avg_copy_time)/3600, 2)

    def statistic(self):
        avg_plot_hour = (self.st_avg_plot_time + self.st_avg_copy_time)/3600
        out_put_process = 24/avg_plot_hour if avg_plot_hour>0 else 0
        out_put = self.st_plot_process_cnt * out_put_process
        stagger = 0
        if self.plot_config is not  None:
            stagger = self.plot_config.global_stagger_m
        else:
            stagger = 48

        return '%s-%s / %s' % (round(out_put_process, 2), round(out_put, 2), round(float(24*60)/stagger,2))

    def update_statistic(self, data):
        self.st_plot_process_cnt = data['plot_process_cnt']
        self.st_plot_output = data['plot_output']
        self.st_avg_plot_time = data['avg_plot_time']
        self.st_avg_copy_time = data['avg_copy_time']
        self.st_update_time = datetime.now()
        self.save()

    def update_local_info(self,data):
        self.is_sending_run = data['is_sending_run']
        self.internal_ip = data['internal_ip']
        self.save()

    def get_info(self):
        return {
            'name': self.server_name(),
            'is_plotting_run': self.is_plotting_run
        }

    def server_name(self):
        return u'plotter-%s' % self.server_number

    def get_plot_config_dict(self):
        if self.plot_config is None:
            # return default dict
            return {
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
        }
        else:
            return self.plot_config.to_dict()

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

