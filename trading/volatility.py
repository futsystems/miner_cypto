#!/usr/bin/python
# -*- coding: utf-8 -*-

import numpy as np
from scipy import stats

import py_vollib
#from py_vollib.black_scholes  import black_scholes as bs
#from py_vollib.black_scholes.implied_volatility import implied_volatility as iv
#from py_vollib.black_scholes.greeks.analytical import delta
#from py_vollib.black_scholes.greeks.analytical import gamma
#from py_vollib.black_scholes.greeks.analytical import rho
#from py_vollib.black_scholes.greeks.analytical import theta
#from py_vollib.black_scholes.greeks.analytical import vega


def calc_real_vol(price, window=15):
    """
    :param price: price data frame
    :param window: trading days in rolling window
    :return:
    """

    days_per_year = 365  # trading days per year
    ann_factor = days_per_year / window

    #使用np函数直接计算
    #log_rtn = np.log(price / price.shift())
    #std = log_rtn.std()
    #vol = std*np.sqrt(days_per_year)

    #生成数组数据
    #log_rtn = np.diff(np.log(price))
    #rtn_mean = np.mean(log_rtn)
    #diff_square = [(log_rtn[i] - rtn_mean) ** 2 for i in range(0, len(log_rtn))]
    #std = np.sqrt(sum(diff_square) * (1.0 / (len(log_rtn) - 1)))
    #vol = std * np.sqrt(days_per_year)

    log_rtn = np.log(price).diff()

    # Var Swap (returns are not demeaned)
    #real_var = np.square(log_rtn).rolling(window).sum() * ann_factor
    #real_vol = np.sqrt(real_var)

    # Classical (returns are demeaned, dof=1)
    real_vol = log_rtn.rolling(window).std()*np.sqrt(days_per_year)
    return real_vol


def bsm_price(option_type, sigma, s, k, r, T, q):
    """
    calculate the bsm price of European call and put options
    :param option_type:
    :param sigma: volatility
    :param s: spot price
    :param k: strike price
    :param r: interest rate
    :param T: time
    :param q: continuous dividend rate
    :return:
    """
    sigma = float(sigma)
    d1 = (np.log(s / k) + (r - q + sigma ** 2 * 0.5) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    if option_type == 'c':
        price = np.exp(-r*T) * (s * np.exp((r - q)*T) * stats.norm.cdf(d1) - k *  stats.norm.cdf(d2))
        return price
    elif option_type == 'p':
        price = np.exp(-r*T) * (k * stats.norm.cdf(-d2) - s * np.exp((r - q)*T) *  stats.norm.cdf(-d1))
        return price
    else:
        print('No such option type %s') % option_type


def calc_implied_vol_1(option_type, option_price, s, k, T, r=0, q=0):
    """
    apply bisection method to get the implied volatility by solving the BSM function
    :param option_type:
    :param option_price:
    :param s: spot price
    :param k: strike price
    :param r: interest rate
    :param T: time
    :param q: continuous dividend rate
    :return:
    """
    precision = 0.00001
    upper_vol = 500.0
    max_vol = 500.0
    min_vol = 0.0001
    lower_vol = 0.0001
    iteration = 0

    while 1:
        iteration +=1
        mid_vol = (upper_vol + lower_vol)/2.0
        price = bsm_price(option_type, mid_vol, s, k, r, T, q)
        if option_type == 'c':
            lower_price = bsm_price(option_type, lower_vol, s, k, r, T, q)
            if (lower_price - option_price) * (price - option_price) > 0:
                lower_vol = mid_vol
            else:
                upper_vol = mid_vol
            if abs(price - option_price) < precision:
                break
            if iteration > 50:
                break
            #if mid_vol > max_vol - 5:
            #    mid_vol = 0.000001
            #    break

        elif option_type == 'p':
            upper_price = bsm_price(option_type, upper_vol, s, k, r, T, q)
            if (upper_price - option_price) * (price - option_price) > 0:
                upper_vol = mid_vol
            else:
                lower_vol = mid_vol
            if abs(price - option_price) < precision:
                break
            if iteration > 50:
                break

    return mid_vol


def bs_call(S, K, T, r, vol):
    d1 = (np.log(S/K) + (r + 0.5*vol**2)*T) / (vol*np.sqrt(T))
    d2 = d1 - vol * np.sqrt(T)
    return S * stats.norm.cdf(d1) - np.exp(-r * T) * K * stats.norm.cdf(d2)


def bs_put(S, K, T, r, vol):
    d1 = (np.log(S / K) + (r + 0.5 * vol ** 2) * T) / (vol * np.sqrt(T))
    d2 = d1 - vol * np.sqrt(T)
    return np.exp(-r * T) * K * stats.norm.cdf(d2) - S * stats.norm.cdf(d1)


def bs_vega(S, K, T, r, sigma):
    d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    return S * stats.norm.pdf(d1) * np.sqrt(T)

def implied_vol_1(option_price, S, K, T, r=0):
    """
    vega 隐含波动率单位变动引起的价格变动
    :param target_value:
    :param S:
    :param K:
    :param T:
    :param r:
    :param args:
    :return:
    """
    MAX_ITERATIONS = 200
    PRECISION = 1.0e-5
    sigma = 0.5
    for i in range(0, MAX_ITERATIONS):
        price = bs_call(S, K, T, r, sigma)
        vega = bs_vega(S, K, T, r, sigma)
        diff = option_price - price  # our root
        if abs(diff) < PRECISION:
            return sigma
        sigma = sigma + diff/vega # f(x) / f'(x)
    return sigma # value wasn't found, return best guess so far


"""
price (float) – the Black-Scholes option price
S (float) – underlying asset price
sigma (float) – annualized standard deviation, or volatility
K (float) – strike price
t (float) – time to expiration in years
r (float) – risk-free interest rate
flag (str) – ‘c’ or ‘p’ for call or put.
"""
def greek_val(flag, S, K, t, r, sigma):
    price = bs(flag, S, K, t, r, sigma)
    imp_v = iv(price, S, K, t, r, flag)
    delta_calc = delta(flag, S, K, t, r, sigma)
    gamma_calc = gamma(flag, S, K, t, r, sigma)
    rho_calc = rho(flag, S, K, t, r, sigma)
    theta_calc = theta(flag, S, K, t, r, sigma)
    vega_calc = vega(flag, S, K, t, r, sigma)
    return np.array([ price, imp_v ,theta_calc, delta_calc ,rho_calc ,vega_calc ,gamma_calc])


def implied_vol_2(option_type, option_price, s, k, t, r=0):
    """

    :param option_type:
    :param option_price:
    :param s:
    :param k:
    :param t:
    :param r:
    :return:
    """
    imp_v = iv(option_price, s, k, t, r, option_type)
    return imp_v



class RealVolatilityCalculator(object):
    """
    波动率计算器
    用于储存一定数量的价格序列，并计算波动率
    """
    def __init__(self, price_array, days_per_year=365):
        self.data = price_array
        self.days_per_year = days_per_year
        self.current_date = None

    def calc_vol(self):
        log_rtn = np.diff(np.log(self.data))
        rtn_mean = np.mean(log_rtn)
        diff_square = [(log_rtn[i] - rtn_mean) ** 2 for i in range(0, len(log_rtn))]
        std = np.sqrt(sum(diff_square) * (1.0 / (len(log_rtn) - 1)))
        vol = std * np.sqrt(self.days_per_year)
        return vol

    def update_price(self, date, price):
        if self.current_date != date:
            self.current_date = date
            if len(self.data) > 0:
                self.data.remove(self.data[0])
            self.data.append(price)
        else:
            self.data[-1] = price










if __name__ == "__main__":
    vol = implied_vol('c', 85, 42870, 50000, 3.2 / 365)
    print('implied vol:%s' % vol)
    #S = 42590
    #K = 50000
    #T = 11
    #r = 0
    #vol = 1
    #print('~~~~~~~~~~')
    #V_market = bs_call(S, K, T, r, vol)
    #print(V_market)
    #implied_vol = implied_vol_1(85, 42590, 5000, 30, 0)

    #print('Implied vol: %.2f%%' % (implied_vol * 100))
    #print('Market price = %.2f' % V_market)
    #print('Model price = %.2f' % bs_call(S, K, T, r, implied_vol))
    pass



