#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.db import models


class Account(models.Model):
    """
    Game Account
    """
    account_id = models.CharField('ID', max_length=50, default='0')
    address = models.CharField('Address', max_length=100, default='')
    chain_token_balance = models.FloatField('Chain Token', default=0)
    game_token_balance = models.FloatField('Game Token', default=0)

    description = models.CharField('Description', max_length=1000, default='', blank=True)

    class Meta:
        app_label = 'gamefi'

    def __unicode__(self):
        return 'ACC-%s' % self.id

    def __str__(self):
        return self.__unicode__()