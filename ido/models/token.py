#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.db import models
from datetime import datetime
from .choices import main_token, ido_platform_type

class Token(models.Model):
    """
    Token
    """
    name = models.CharField('Name', max_length=50, default='Project Name')
    token = models.CharField('Token', max_length=50, default='Token')
    platform =  models.CharField(
        max_length=10,
        choices=ido_platform_type,
        default='CoinList',
    )

    date = models.DateTimeField('Date', default=datetime.now, blank=True)
    price = models.FloatField('Price', default=0)
    quantity = models.FloatField('Quantity', default=0)

    project_type = models.CharField('Project Type', max_length=50,  default='', blank=True)

    token_used = models.FloatField('Token Used', default=0)
    token_type = models.CharField(
        max_length=10,
        choices=main_token,
        default='ETH',
    )
    vesting = models.CharField('Vest', max_length=1000, default='', blank=True)
    current_price = models.FloatField('Current Price', default=0)
    description = models.CharField('Description', max_length=1000, default='', blank=True)

    class Meta:
        app_label = 'ido'
        ordering = ['date', ]

    def __unicode__(self):
        return 'Token-%s' % self.token

    def __str__(self):
        return self.__unicode__()
