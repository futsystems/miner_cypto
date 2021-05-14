#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.db import models
from .settings import GATEWAY_DOMAIN

class PlotConfig(models.Model):
    """
    plot config
    """
    name = models.CharField('Name', max_length=50, default='Config Name')
    k = models.CharField('K Size', max_length=10, default='32')
    e = models.BooleanField('Bitfield', default=True)
    n_threads = models.IntegerField('Threads', default=3)
    n_buckets = models.IntegerField('Buckets', default=128)
    job_buffer = models.IntegerField('Job Buffer', default=4200)

    global_max_jobs = models.IntegerField('Global Max Jobs', default=12)
    global_stagger_m = models.IntegerField('Global Stagger Time', default=24)
    tmpdir_max_jobs = models.IntegerField('Tmp Max Jobs', default=12)

    tmpdir_stagger_phase_major = models.IntegerField('Tmp Stagger Phase Major', default=2)
    tmpdir_stagger_phase_minor = models.IntegerField('Tmp Stagger Phase Minor', default=1)
    tmpdir_stagger_phase_limit = models.IntegerField('Tmp Stagger Phase Limit', default=5)

    description = models.CharField('Description', max_length=1000, default='', blank=True)

    class Meta:
        app_label = 'server'

    def __unicode__(self):
        return u'plot config[%s]' % self.name

