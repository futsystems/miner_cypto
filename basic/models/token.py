#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.db import models
from datetime import datetime

price_source = (
    ('CoinGecko', 'CoinGecko'),
)

chain_type = (
    ('MAIN', 'MAIN'),
    ('ETH', 'ETH'),
    ('BSC', 'BSC'),
)


class Token(models.Model):
    """
    Token
    """
    name = models.CharField('Name', max_length=50, default='Token')
    symbol = models.CharField('Symbol', max_length=50, default='Symbol')
    chain_type = models.CharField(
        max_length=10,
        choices=chain_type,
        default='MAIN',
    )
    price_source = models.CharField(
        max_length=10,
        choices=price_source,
        default='CoinGecko',
    )
    contract_address = models.CharField('Contract Address', max_length=50, default='Contract')

    price_symbol = models.CharField('Price Symbol', max_length=50, default='Symbol')
    current_price = models.FloatField('Current Price', default=0)

    description = models.CharField('Description', max_length=1000, default='', blank=True)

    class Meta:
        app_label = 'basic'
        ordering = ['symbol', ]

    def __unicode__(self):
        return 'Token-%s' % self.symbol

    def __str__(self):
        return self.__unicode__()
