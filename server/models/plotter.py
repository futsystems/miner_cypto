#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.db import models
from .settings import GATEWAY_DOMAIN

class Plotter(models.Model):
    """
    plotter server
    """
    server_number = models.CharField('Server Id', max_length=50, default='Consul')
    description = models.CharField('Description', max_length=1000, default='', blank=True)

    class Meta:
        app_label = 'server'

    def __unicode__(self):
        return u'plotter-%s' % self.server_number

    def server_name(self):
        return u'plotter-%s' % self.server_number

    @property
    def api_host(self):
        return '%s.%s' % (self.server_number,GATEWAY_DOMAIN)

    @property
    def api_port(self):
        return 8080

