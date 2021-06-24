#!/usr/bin/python
# -*- coding: utf-8 -*-


from django.db import models
from datetime import datetime


class HarvesterServiceRestart(models.Model):
    """
    harvester Service Restart
    """
    service = models.CharField('Service Name', max_length=50, default='001')
    reason = models.CharField('Reason', max_length=50, default='001')
    harvester = models.ForeignKey('Harvester', verbose_name='Harvester', on_delete=models.SET_NULL,
                      default=None,
                      blank=True, null=True)

    time = models.DateTimeField('Restart Time', default=datetime.now, blank=True)

    class Meta:
        app_label = 'server'
        ordering = ['time', ]