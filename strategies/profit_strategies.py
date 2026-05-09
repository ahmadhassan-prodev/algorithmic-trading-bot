from orders.exchange_orders import place_oco_sell_order, place_profit_stop_limit_sell_order
from indicators.ema import *

def set_profit_1(df,buy_price,stoploss):
    ema_buy = ema_buy_check(df)
    prof_difference = ema_buy-buy_price
    one_percent = buy_price/100
    one_and_half_percent = 1.5 * one_percent
    two_percent = 2 * one_percent
    calculated_profit_price = None
    latest_ema = ema_last(df)
    ema_20th = ema_last(df,22)
    ema_difference = latest_ema - ema_20th
    if(ema_difference>0):
        ema_percent = (ema_difference/ema_20th)*100
    else:
        ema_percent = 0
    
    if(latest_ema>ema_20th):
        if(ema_percent > 2):
            calculated_profit_price = buy_price + two_percent
        else:
            calculated_profit_price = buy_price + one_and_half_percent
    else:
        if(prof_difference>one_percent):
            calculated_profit_price = ema_buy
        else:
            calculated_profit_price = buy_price + one_percent

    # Place stop limit order
    # place_profit_stop_limit_sell_order(calculated_profit_price)
    stoploss_orderId = place_oco_sell_order(calculated_profit_price, stoploss)
    return stoploss_orderId
    
def set_one_hour_profit(buy_price):
    two_percent = 2 * (buy_price/100)
    calculated_profit = buy_price + two_percent
    place_profit_stop_limit_sell_order(calculated_profit)
