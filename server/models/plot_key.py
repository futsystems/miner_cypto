#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.db import models


class PlotKey(models.Model):
    """
    plot key
    """
    name = models.CharField('Name', max_length=50, default='Config Name')
    farmer_pk = models.CharField('Farmer Key', max_length=250, default='')
    pool_key = models.CharField('Pool Key', max_length=250, default='')
    description = models.CharField('Description', max_length=1000, default='', blank=True)

    class Meta:
        app_label = 'server'

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.__unicode__()