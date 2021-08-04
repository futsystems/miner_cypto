#!/usr/bin/python
# -*- coding: utf-8 -*-

from pycoingecko import CoinGeckoAPI


class MarketAPI(object):
    def __init__(self):
        self._cg = CoinGeckoAPI()

    def get_token_price(self, token):
        if token =='BTC':
            return self._get_price('bitcoin')
        if token == 'ETH':
            return self._get_price('ethereum')
        if token == 'SKILL':
            return self._get_price('cryptoblades')
        if token == 'ZOON':
            return self._get_price('cryptozoon')
        if token == 'BNB':
            return self._get_price('binancecoin')
        return 0

    def _get_price(self, currency_id):
        data = self._cg.get_price(ids=currency_id, vs_currencies='usd')
        return data[currency_id]['usd']
