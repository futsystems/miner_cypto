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
        return  self.content

    @property
    def content(self):
        return u'%s[-k %s -e:%s -r:%s -b:%s -u:%s] [max:%s / %s stagger:%s  tmpdir: %s-%s:%s]' % (self.name, self.k,
                      self.e, self.n_threads, self.job_buffer, self.n_buckets, self.global_max_jobs, self.tmpdir_max_jobs, self.global_stagger_m,self.tmpdir_stagger_phase_limit
                                                                                      ,self.tmpdir_stagger_phase_major,self.tmpdir_stagger_phase_minor)


    def to_dict(self):
        return {
            'k': self.k,
            'e': self.e,
            'n_threads': self.n_threads,
            'n_buckets': self.n_buckets,
            'job_buffer': self.job_buffer,

            'global_max_jobs': self.global_max_jobs,
            'global_stagger_m': self.global_stagger_m,
            'tmpdir_max_jobs': self.tmpdir_max_jobs,
            'tmpdir_stagger_phase_major': self.tmpdir_stagger_phase_major,
            'tmpdir_stagger_phase_minor': self.tmpdir_stagger_phase_minor,
            'tmpdir_stagger_phase_limit': self.tmpdir_stagger_phase_limit,
        }

