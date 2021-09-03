#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.db import models

from .game import Game
from .account import Account


class GameAccount(models.Model):
    """
    Game Account
    """
    account_id = models.CharField('ID', max_length=50, default='0')
    game = models.ForeignKey(Game, related_name='game_accounts', verbose_name='Game',
                                  on_delete=models.SET_NULL,
                                  default=None,
                                  blank=True, null=True)
    address = models.ForeignKey(Account, related_name='game_accounts', verbose_name='Address',
                                  on_delete=models.SET_NULL,
                                  default=None,
                                  blank=True, null=True)

    game_token_balance = models.FloatField('Game Token', default=0)
    game_token_balance_not_claimed = models.FloatField('Game Token Not Claimed', default=0)
    description = models.CharField('Description', max_length=1000, default='', blank=True)

    class Meta:
        app_label = 'gamefi'
        ordering = ['account_id', ]

    def __unicode__(self):
        return 'ACC-%s' % self.id

    def __str__(self):
        return self.__unicode__()

    def total_game_token_balance(self):
        return self.game_token_balance + self.game_token_balance_not_claimed
