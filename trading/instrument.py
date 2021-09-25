#!/usr/bin/python
# -*- coding: utf-8 -*-


import pytz
from datetime import datetime
from qfin.options import BlackScholesCall


class Instrument(object):
    def __init__(self, symbol):
        """
        BTC-12FEB21-31500-P
        :param symbol:
        """
        self.symbol = symbol
        args = self.symbol.split('-')
        self.underlying = args[0]
        self.expire = get_option_expire_deribit(args[1])
        self.strike = float(args[2])
        if args[3] == 'P':
            self.option_type = 'p'
        elif args[3] == 'C':
            self.option_type = 'c'

    def time_to_expire(self):
        return float((self.expire - datetime.now(pytz.timezone('UTC'))).total_seconds())/3600/24/365




def parse_option_date(date):
    """
    12FEB21 parser
    :param date:
    :return:
    """
    year = 2000 + int(date[-2:])
    month = get_month_num(date[-5:-2])
    day = int(date[:-5])
    return [year, month, day]


def get_month_num(month):
    if month == 'JAN':
        return 1
    elif month == 'FEB':
        return 2
    elif month == 'MAR':
        return 3
    elif month == 'APR':
        return 4
    elif month == 'MAY':
        return 5
    elif month == 'JUN':
        return 6
    elif month == 'JUL':
        return 7
    elif month == 'AUG':
        return 8
    elif month == 'SEP':
        return 9
    elif month == 'OCT':
        return 10
    elif month == 'NOV':
        return 11
    elif month == 'DEC':
        return 12
    return 1


def get_option_expire_deribit(date):
    """
    get option expire time time to maturity
    :return:
    UTC-8 settletime
    """
    args = parse_option_date(date)
    print(args)
    return datetime(args[0], args[1], args[2], 8, 0, 0, 0, tzinfo=pytz.timezone('UTC'))

if __name__ == "__main__":
    print('test')
    dt = (get_option_expire_deribit('24SEP21') - datetime.now(pytz.timezone('UTC')))
    #print(dt)
    #print(float(dt.total_seconds())/3600/24/365)
    #print(float(4)/365)

    option = Instrument('BTC-24SEP21-50000-C')
    print(option.option_type)
    data= BlackScholesCall(47390, 0.647, option.strike, option.time_to_expire(), 0)
    print(data.price)
    #print(option.symbol)
    #print(option.option_type)
    #print(option.strike)
    #print(option.time_to_expire())


