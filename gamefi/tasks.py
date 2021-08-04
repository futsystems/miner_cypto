#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals
from celery import shared_task
from django.utils import timezone
from common.mail import get_stuff_emails
from common.mail import send_email as _send_email

import time
import logging
logger = logging.getLogger(__name__)

from common.bsc import BSCAPI
from common.market import MarketAPI
from .models import Game, GameSettlement


@shared_task
def sync_account_balance():
    logger.info('sync account balance')
    for game in Game.objects.all():
        if game.chain == 'BSC':
            api = BSCAPI()
            for account in game.accounts.all():
                chain_token_balance = api.get_chain_balance(account.address)
                game_token_balance = api.get_token_balance(account.address, game.token)
                account.chain_token_balance = round(chain_token_balance,4)
                account.game_token_balance = round(game_token_balance,4)
                account.save()

                logger.info('account address:%s balance:%s token:%s token balance:%s' % (account.address, chain_token_balance, game.token, game_token_balance))
                time.sleep(0.5)



@shared_task
def settle_game_balance():
    logger.info('settle game')
    for game in Game.objects.all():
        if game.chain == 'BSC':
            api = BSCAPI()
            for account in game.accounts.all():
                chain_token_balance = api.get_chain_balance(account.address)
                game_token_balance = api.get_token_balance(account.address, game.token)
                account.chain_token_balance = round(chain_token_balance,4)
                account.game_token_balance = round(game_token_balance,4)
                account.save()

                logger.info('account address:%s balance:%s token:%s token balance:%s' % (account.address, chain_token_balance, game.token, game_token_balance))
                time.sleep(0.5)


        # do settlement for game
        last_game_token_balance = game.last_game_token_balance
        game_token_balance = game.game_balance()
        game_token_income = game_token_balance - last_game_token_balance

        settlement = GameSettlement()
        settlement.game = game
        settlement.last_game_token_balance = last_game_token_balance
        settlement.game_token_income = game_token_income
        settlement.game_token_payout = 0
        settlement.game_token_balance = game_token_balance
        settlement.settle_time = timezone.now()
        settlement.save()

        game.last_game_token_balance = game_token_balance
        game.save()


@shared_task
def query_price():
    logger.info('query price')
    market = MarketAPI()
    for game in Game.objects.all():
        game.token_price = market.get_token_price(game.token)
        if game.chain == 'BSC':
            game.chain_price = market.get_token_price('BNB')
        game.save()








