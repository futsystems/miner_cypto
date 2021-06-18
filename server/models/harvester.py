#!/usr/bin/python
# -*- coding: utf-8 -*-


from django.db import models
from django.utils import timezone
from datetime import datetime
from .settings import HARVESTER_GATEWAY_DOMAIN
from common.helper import obj_attr_change

class Harvester(models.Model):
    """
    harvester server
    """
    server_number = models.CharField('Server Id', max_length=50, default='001')
    internal_ip = models.CharField('Internal IP', max_length=20, default='', blank=True)
    data_tx_ip = models.CharField('Data Transfer IP', max_length=20, default='', blank=True)
    total_current_plots = models.IntegerField('Plots', default=0)
    space_free_plots = models.IntegerField('Free Plots', default=0)
    file_cnt = models.IntegerField('Files', default=0)
    driver_cnt = models.IntegerField('Drivers', default=0)
    description = models.CharField('Description', max_length=1000, default='', blank=True)

    last_heartbeat = models.DateTimeField('Heartbeat', default=datetime.now, blank=True)

    boot_time = models.DateTimeField('Boot Time', default=datetime.now, blank=True)#server boot at this time
    uptime = models.IntegerField('Uptime', default=0, blank=True)

    cpu_model = models.CharField('CPU', max_length=100, default='', blank=True)
    cpu_cnt = models.IntegerField('CPU Count', default=0)
    cpu_used_percent = models.FloatField('CPU Used Percent', default=0)
    memory_total = models.BigIntegerField('Memory Total', default=0)
    memory_used = models.BigIntegerField('Memory Used', default=0)

    auto_scan_plot = models.BooleanField('Auto Scan', default=False)

    class Meta:
        app_label = 'server'

    def __unicode__(self):
        return u'harvester-%s' % self.server_number

    def __str__(self):
        return self.__unicode__()

    def server_name(self):
        return u'harvester-%s' % self.server_number

    @property
    def api_host(self):
        return '%s.%s' % (self.server_number,HARVESTER_GATEWAY_DOMAIN)

    @property
    def api_port(self):
        return 8080

    def _update_heartbeat(self, need_save=False):
        self.last_heartbeat = timezone.now()
        if need_save:
            self.save()

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

    def up_time(self):
        if self.uptime < 3600:
            return '%sm' % round(self.uptime/60,2)
        else:
            return '%sh' % round(self.uptime/3600,2)

    def power(self):
        """
        1gib = 0.0009765625 tib
        :return:
        """
        return round(self.file_cnt * 101.4 * 0.0009765625, 2)

    def get_harvester_dict(self):
        ip = self.internal_ip
        if self.data_tx_ip is not None and self.data_tx_ip != '':
            ip = self.data_tx_ip

        return {
            'name': self.server_name(),
            'ip': ip
        }

    def update_register(self,data):
        self.boot_time = data['boot_time']

        if 'cpu' in data:
            self.cpu_model = data['cpu']['brand']
            self.cpu_cnt = data['cpu']['count']
            self.cpu_used_percent = data['cpu']['used_percent']

        if 'memory' in data:
            self.memory_total = data['memory']['total']
            self.memory_used = data['memory']['used']
        self._update_heartbeat()
        self.save()

    def update_local_info(self, data):
        if 'info' in data:
            self.internal_ip = data['info']['internal_ip']
            self.uptime = data['info']['uptime']
            self.total_current_plots = data['info']['total_current_plots']
            self.driver_cnt = data['info']['driver_cnt']
            self.file_cnt = data['info']['space_free_plots']
            self.file_cnt = data['info']['file_cnt']

        if 'cpu' in data:
            self.cpu_model = data['cpu']['brand']
            self.cpu_cnt = data['cpu']['count']
            self.cpu_used_percent = data['cpu']['used_percent']

        if 'memory' in data:
            self.memory_total = data['memory']['total']
            self.memory_used = data['memory']['used']
        self._update_heartbeat()
        self.save()

    def get_harvester_config_dict(self):
        return {
            'auto_scan_plot': self.auto_scan_plot
        }

    def save(self, force_insert=False, force_update=False, *args, **kwargs):
        config_change=False
        old = Harvester.objects.filter(pk=getattr(self, 'pk', None)).first()
        if old:
            if obj_attr_change(old, self, 'auto_scan_plot'):
                config_change = True
        super(Harvester, self).save(force_insert, force_update, *args, **kwargs)
        if config_change:
            from ..harvester_api import HarvesterAPI
            api = HarvesterAPI(self)
            api.config_change()