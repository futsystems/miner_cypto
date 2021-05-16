#!/usr/bin/python
# -*- coding: utf-8 -*-


from django.db import models
from datetime import datetime

class Harvester(models.Model):
    """
    harvester server
    """
    server_number = models.CharField('Server Id', max_length=50, default='001')
    internal_ip = models.CharField('Internal IP', max_length=20, default='', blank=True)
    plot_cnt = models.IntegerField('Plot Count', default=0)
    driver_cnt = models.IntegerField('Driver Count', default=0)
    description = models.CharField('Description', max_length=1000, default='', blank=True)
    last_heartbeat_time = models.DateTimeField('Heartbeat', default=datetime.now, blank=True)

    class Meta:
        app_label = 'server'

    def __unicode__(self):
        return u'plotter-%s' % self.server_number

    def __str__(self):
        return self.__unicode__()



    def server_name(self):
        return u'plotter-%s' % self.server_number

    def update_local_info(self, data):
        self.internal_ip = data['internal_ip']
        self.plots_cnt = data['plots_cnt']
        self.driver_cnt = data['driver_cnt']
        self.last_heartbeat_time = datetime.now()
        self.save()