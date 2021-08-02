#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals
from celery import shared_task

from common.mail import get_stuff_emails
from common.mail import send_email as _send_email

import time
import logging
logger = logging.getLogger(__name__)

from common.bsc import BSCAPI
from .models import Game
@shared_task
def sync_account_balance():
    logger.info('sync account balance')
    for game in Game.objects.all():
        if game.chain == 'BSC':
            api = BSCAPI()
            for account in game.accounts.all():
                chain_token_balance = api.get_chain_balance(account.address)
                game_token_balance = api.get_token_balance(account.address, game.token)
                account.chain_token_balance = chain_token_balance
                account.game_token_balance = game_token_balance
                account.save()

                #logger.info('account address:%s balance:%s' % (account.address, chain_token_balance))
                time.sleep(0.5)





