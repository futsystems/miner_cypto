#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.db import models

from .game import Game

class Account(models.Model):
    """
    BlockChain Account
    """
    account_id = models.CharField('ID', max_length=50, default='0')
    game = models.ForeignKey(Game, related_name='accounts', verbose_name='Game',
                                  on_delete=models.SET_NULL,
                                  default=None,
                                  blank=True, null=True)

    address = models.CharField('Address', max_length=100, default='')
    is_main = models.BooleanField('Main Account', default=False)
    chain_token_balance = models.FloatField('Chain Token', default=0)
    game_token_balance = models.FloatField('Game Token', default=0)
    game_token_balance_not_claimed = models.FloatField('Game Token Not Claimed', default=0)
    description = models.CharField('Description', max_length=1000, default='', blank=True)

    class Meta:
        app_label = 'gamefi'
        ordering = ['account_id', ]

    def __unicode__(self):
        return 'Address-%s' % self.account_id

    def __str__(self):
        return self.__unicode__()

    def total_game_token_balance(self):
        return  self.game_token_balance + self.game_token_balance_not_claimed