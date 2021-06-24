#!/usr/bin/python
# -*- coding: utf-8 -*-


from django.db import models
from django.utils import timezone
from datetime import datetime
from .settings import HARVESTER_GATEWAY_DOMAIN
from common.helper import obj_attr_change



class HarvesterServiceManager(models.Manager):
    def add_or_update(self, harvester, data):
        index = data['index']
        service = data['service']
        local_power = data['local_power']
        remote_power = data['remote_power']
        remote_power_unit = data['remote_power_unit']
        status = data['status']
        harvester_service = self.filter(index=index, harvester__server_number=harvester.server_number).first()
        if harvester_service is None:
            harvester_service = HarvesterService()
            harvester_service.index = index
            harvester_service.service = service
            harvester_service.harvester = harvester

        harvester_service.local_power = local_power
        harvester_service.remote_power = remote_power
        harvester_service.remote_power_unit = remote_power_unit
        harvester_service.status = status

        if harvester_service.status is None:
            harvester_service.status=''
        harvester_service.save()


class HarvesterService(models.Model):
    """
    harvester Service
    """
    index = models.IntegerField('Index', default=0)
    service = models.CharField('Service Name', max_length=50, default='001')
    local_power = models.FloatField('Local Power', default=0)
    remote_power = models.FloatField('Remote Power', default=0)
    remote_unit = models.CharField('Remote Unit', max_length=20, default='TB', blank=True)
    status = models.CharField('Status', max_length=100, default='', blank=True)

    harvester = models.ForeignKey('Harvester', related_name='services', verbose_name='PlotConfig', on_delete=models.SET_NULL,
                      default=None,
                      blank=True, null=True)

    objects = HarvesterServiceManager()


    class Meta:
        app_label = 'server'
        ordering = ['index', ]

    def __unicode__(self):
        return u'service-%s' % self.service

    def __str__(self):
        return self.__unicode__()

