#!/usr/bin/python
# -*- coding: utf-8 -*-

from datetime import datetime

from django.db import models
from .settings import GATEWAY_DOMAIN

from .plot_config import PlotConfig
from .harvester import Harvester

from .choices import CACHE_TYPE



class PlotTransfer(models.Model):
    """
    plot transfer record
    """
    plot_file_name = models.CharField('Plot File', max_length=254, default='default name')

    plotter_server = models.CharField('Plotter Server', max_length=50, default='plotter-001')
    plotter_ip = models.CharField('Plotter IP', max_length=20, default='', blank=True)
    plotter_path = models.CharField('Path', max_length=254, default='', blank=True)

    harvester_server = models.CharField('Harvester Server', max_length=50, default='harvester-001')
    harvester_ip = models.CharField('Harvester IP', max_length=20, default='', blank=True)
    harvester_path = models.CharField('Path', max_length=254, default='', blank=True)

    nc_pid = models.CharField('NC pid', max_length=10, default='', blank=True)
    nc_port = models.CharField('NC port', max_length=10, default='', blank=True)

    txn_start_time = models.DateTimeField('Start Time', default=datetime.now, blank=True)
    txn_stop_time = models.DateTimeField('Start Time', default=datetime.now, blank=True)

    plot_check = models.BooleanField('Plot Check', default=False)
    plot_check_fail_reason = models.BooleanField('Plot Check Fail Reason', default=False)

    class Meta:
        app_label = 'server'

    def __unicode__(self):
        return u'plot-transfer_%s' % self.id

    def __str__(self):
        return self.__unicode__()

    def get_file_title(self):
        return '%s.....%s' % (self.plot_file_name[0:40],self.plot_file_name[-10:])


