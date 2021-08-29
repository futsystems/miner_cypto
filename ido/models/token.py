#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.db import models
from datetime import datetime
from .choices import main_token

class Token(models.Model):
    """
    Token
    """
    name = models.CharField('Name', max_length=50, default='token')
    token = models.CharField('Token', max_length=50, default='token')

    date = models.DateTimeField('Date', default=datetime.now, blank=True)
    price = models.FloatField('Price', default=0)
    quantity = models.FloatField('Quantity', default=0)

    token_used = models.FloatField('Token Used', default=0)
    token_type = models.CharField(
        max_length=10,
        choices=main_token,
        default='ETH',
    )

    current_price = models.FloatField('Current Price', default=0)
    description = models.CharField('Description', max_length=1000, default='', blank=True)

    class Meta:
        app_label = 'ido'
        ordering = ['date', ]

    def __unicode__(self):
        return 'Token-%s' % self.token

    def __str__(self):
        return self.__unicode__()
