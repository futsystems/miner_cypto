#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.db import models
from .choices import CHAIN_TYPE

class Game(models.Model):
    """
    Game
    """
    name = models.CharField('Name', max_length=50, default='Game')
    url = models.CharField('Url', max_length=250, default='')
    token = models.CharField('Token', max_length=100, default='')
    chain = models.CharField(
        max_length=10,
        choices=CHAIN_TYPE,
        default='BSC',
    )
    description = models.CharField('Description', max_length=1000, default='', blank=True)


    class Meta:
        app_label = 'gamefi'

    def chain_balance(self):
        return round(sum([account.chain_token_balance for account in self.accounts.all()]), 2)

    def game_balance(self):
        return round(sum([account.game_token_balance for account in self.accounts.all()]), 2)

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.__unicode__()