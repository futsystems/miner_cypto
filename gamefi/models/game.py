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
    input = models.FloatField('Input', default=0)
    token = models.CharField('Token', max_length=100, default='')
    chain = models.CharField(
        max_length=10,
        choices=CHAIN_TYPE,
        default='BSC',
    )

    token_price = models.FloatField('Token Price', default=0)
    chain_price = models.FloatField('Chain Price', default=0)
    last_game_token_balance = models.FloatField('Game Token Balance(Last)', default=0)
    description = models.CharField('Description', max_length=1000, default='', blank=True)


    class Meta:
        app_label = 'gamefi'

    def chain_balance(self):
        return round(sum([account.chain_token_balance for account in self.accounts.filter(is_main=False).all()]), 2)

    def game_balance(self):
        return round(sum([account.total_game_token_balance() for account in self.accounts.all()]), 2)

    def game_balance_usd(self):
        return round(self.game_balance()* self.token_price, 2)

    def game_balance_chain(self):
        if self.chain_price == 0:
            return 0
        return round(self.game_balance() * self.token_price / self.chain_price, 2)

    def ratio(self):
        return "{0:.2%}".format(self.game_balance_chain()/ (self.input - self.chain_balance()))

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.__unicode__()