from api.exchange_client import client
import math
from indicators.ema import *
from data.data_fetcher import get_1hour_candles
import ta

# Method to adjust quantity
def adjust_quantity(symbol, quantity):
    info = client.get_symbol_info(symbol)
    for f in info['filters']:
        if f['filterType'] == 'LOT_SIZE':
            step_size = float(f['stepSize'])
            break
    precision = int(round(-math.log(step_size, 10), 0))
    return round(quantity, precision)

# Method to get tick size and precision
def get_price_filter(symbol):
    info = client.get_symbol_info(symbol)
    for f in info['filters']:
        if f['filterType'] == 'PRICE_FILTER':
            tick_size = float(f['tickSize'])
            precision = int(round(-math.log(tick_size, 10), 0))
            return tick_size, precision
        
def adjust_price(symbol, price, direction='down'):
    tick_size, precision = get_price_filter(symbol)

    if direction == 'down':
        price -= tick_size
    else:
        price += tick_size

    return round(price, precision)

def adjust_stop_price(symbol, price):
    _, precision = get_price_filter(symbol)
    return round(price, precision)

def get_valid_stop_limit_prices(symbol, raw_price):
    stop_price = adjust_stop_price(symbol, raw_price)
    limit_price = adjust_price(symbol, stop_price, direction='down')

    # Ensure limitPrice < stopPrice
    if limit_price >= stop_price:
        limit_price = adjust_price(symbol, limit_price, direction='down')

    return stop_price, limit_price


def stoploss_ratio(r,bp,ll):
    trade_risk = bp-ll
    sp = 0
    for i in range(r):
        sp = sp + trade_risk
    return (sp+bp)
    
