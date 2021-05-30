#!/usr/bin/python
# -*- coding: utf-8 -*-


from django.db import models
from django.utils import timezone
from datetime import datetime
from .settings import HARVESTER_GATEWAY_DOMAIN

class Harvester(models.Model):
    """
    harvester server
    """
    server_number = models.CharField('Server Id', max_length=50, default='001')
    internal_ip = models.CharField('Internal IP', max_length=20, default='', blank=True)
    plot_cnt = models.IntegerField('Plot Count', default=0)
    driver_cnt = models.IntegerField('Driver Count', default=0)
    description = models.CharField('Description', max_length=1000, default='', blank=True)

    last_heartbeat = models.DateTimeField('Heartbeat', default=datetime.now, blank=True)

    boot_time = models.DateTimeField('Boot Time', default=datetime.now, blank=True)#server boot at this time
    uptime = models.IntegerField('Uptime', default=0, blank=True)

    cpu_model = models.CharField('CPU', max_length=100, default='', blank=True)
    cpu_cnt = models.IntegerField('CPU Count', default=0)
    cpu_used_percent = models.FloatField('CPU Used Percent', default=0)
    memory_total = models.BigIntegerField('Memory Total', default=0)
    memory_used = models.BigIntegerField('Memory Used', default=0)

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
            self.is_sending_run = data['info']['is_sending_run']
            self.internal_ip = data['info']['internal_ip']
            self.uptime = data['info']['uptime']

        if 'cpu' in data:
            self.cpu_model = data['cpu']['brand']
            self.cpu_cnt = data['cpu']['count']
            self.cpu_used_percent = data['cpu']['used_percent']

        if 'memory' in data:
            self.memory_total = data['memory']['total']
            self.memory_used = data['memory']['used']
        self._update_heartbeat()
        self.save()