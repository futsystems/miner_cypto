#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
BTC-12FEB21-31500-P

"""

from qfin.options import BlackScholesCall
from qfin.options import BlackScholesPut
from .instrument import Instrument
from .volatility import calc_implied_vol_1, implied_vol_1


class Option(object):
    def __init__(self, symbol):
        self.instrument = Instrument(symbol)
        print(self.instrument.option_type)

    def get_data(self, underlying_price, underlying_vol):
        if self.instrument.option_type == 'c':
            return BlackScholesCall(underlying_price, underlying_vol, self.instrument.strike, self.instrument.time_to_expire(), 0)
        elif self.instrument.option_type == 'p':
            return BlackScholesPut(underlying_price, underlying_vol, self.instrument.strike, self.instrument.time_to_expire(), 0)

    def implied_vol(self, option_price, underlying_price):
        #return implied_vol_1(option_price, underlying_price, self.instrument.strike, self.instrument.time_to_expire())
        return calc_implied_vol_1(self.instrument.option_type, option_price, underlying_price, self.instrument.strike, self.instrument.time_to_expire())


