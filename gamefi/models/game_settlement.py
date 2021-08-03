#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.db import models
from django.utils import timezone
from datetime import datetime
from .game import Game


class GameSettlement(models.Model):
    """
    Game
    """
    game = models.ForeignKey(Game, related_name='settlements', verbose_name='Game',
                             on_delete=models.SET_NULL,
                             default=None,
                             blank=True, null=True)
    last_game_token_balance = models.FloatField('Game Token Balance(Last)', default=0)
    game_token_income = models.FloatField('Income', default=0)
    game_token_payout = models.FloatField('Payout', default=0)
    game_token_balance = models.FloatField('Game Token Balance', default=0)
    settle_time = models.DateTimeField('SettleTime', default=datetime.now, blank=True)

    class Meta:
        app_label = 'gamefi'

    def chain_balance(self):
        return round(sum([account.chain_token_balance for account in self.accounts.filter(is_main=False).all()]), 2)

    def game_balance(self):
        return round(sum([account.game_token_balance for account in self.accounts.all()]), 2)

    def __unicode__(self):
        return '%s-%s' % (self.game, self.settle_time)

    def __str__(self):
        return self.__unicode__()