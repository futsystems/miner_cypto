#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.db import models


class Game(models.Model):
    """
    Game
    """
    name = models.CharField('Name', max_length=50, default='Game')
    url = models.CharField('Url', max_length=250, default='')
    token = models.CharField('Token', max_length=100, default='')
    description = models.CharField('Description', max_length=1000, default='', blank=True)

    class Meta:
        app_label = 'gamefi'

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.__unicode__()