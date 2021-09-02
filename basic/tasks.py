#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals
from celery import shared_task

import logging, traceback
logger = logging.getLogger(__name__)

from .models import Token
from common.market import MarketAPI

@shared_task
def sync_price():
    logger.info('sync price')
    tokens = Token.objects.all()
    symbols = {}
    for token in tokens:
        data_set = None
        if token.price_source in symbols:
            data_set = symbols[token.price_source]
            data_set.append(token.price_symbol)
        else:
            data_set = []
            symbols[token.price_source] = data_set
            data_set.append(token.price_symbol)
    #print(symbols)
    api = MarketAPI()
    for source in symbols:
        result = api.get_price(symbols[source], source)
        for symbol in result:
            try:
                token = Token.objects.get(price_source=source,price_symbol=symbol)
                token.current_price = result[symbol]
                token.save(update_fields=['current_price'])
            except Exception as e:
                logger.error(traceback.format_exc())


