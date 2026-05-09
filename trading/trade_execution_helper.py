from indicators.ema import *
from data.data_fetcher import get_1hour_candles
from data.data_fetcher import *
from indicators.trend import trend_check
from indicators.candlestick_details import *
from orders.exchange_orders import place_one_hour_stop_limit_buy_order, place_one_hour_stop_limit_sell_order

def last_close(df):
    c = 2
    last_candle = df.iloc[-c]
    lc = last_candle['Close']
    return lc


def last_open(df):
    c = 2
    last_candle = df.iloc[-c]
    lo = last_candle['Open']
    return lo


def last_high(df):
    c = 2
    last_candle = df.iloc[-c]
    lh = last_candle['High']
    return lh


def last_low(df):
    c = 2
    last_candle = df.iloc[-c]
    ll = last_candle['Low']
    return ll

def buy_trade_status(df):
    ema = ema_check(df)
    ema_buy = ema_buy_check(df)
    ema_100 = ema_last(df)
    c = 2
    last_candle = df.iloc[-c]
    lh = last_candle['High']
    ll = last_candle['Low']

    if((ema_buy>lh or ema_buy<ll) and (ema_100>lh or ema_100<ll) and (ema>lh or ema<ll)):
        return 'ok'
    elif((ema>ll and ema<lh) and (ema_buy>lh or ema_buy<ll) and (ema_100>lh or ema_100<ll)):
        return 'ok'
    elif((ema_buy>ll and ema_buy<lh) and (ema_100>lh or ema_100<ll) and (ema>lh or ema<ll)):
        return 'ok'
    elif((ema_100>ll and ema_100<lh) and (ema>lh or ema<ll) and (ema_buy>lh or ema_buy<ll)):
        return 'ok'
    elif((ema_buy>ll and ema_buy<lh) and (ema>ll and ema<lh) and (ema_100>lh or ema_100<ll)):
        return 'ok'
    elif((ema_100>ll and ema_100<lh) and (ema>ll and ema<lh) and (ema_buy>lh or ema_buy<ll)):
        return 'ok'
    elif((ema_100>ll and ema_100<lh) and (ema_buy>ll and ema_buy<lh) and (ema>lh or ema <ll)):
        return 'ok'
    else:
        return 'not'


def emaBuy_buy_status(tdf):
    ema_buy = ema_buy_check(tdf)
    c = 2
    last_candle = tdf.iloc[-c]
    lh = last_candle['High']

    # Second Last candle
    previous_candle_1 = tdf.iloc[-(c+1)]
    ph1 = previous_candle_1['High']
    
    # 3rd Last candle
    previous_candle_2 = tdf.iloc[-(c+2)]
    ph2 = previous_candle_2['High']

    # 4th Last candle
    previous_candle_3 = tdf.iloc[-(c+3)]
    ph3 = previous_candle_3['High']
    pc3 = previous_candle_3['Close']
    
    # 5th Last candle
    previous_candle_4 = tdf.iloc[-(c+4)]
    ph4 = previous_candle_4['High']
    pc4 = previous_candle_4['Close']

    # 6th Last candle
    previous_candle_5 = tdf.iloc[-(c+5)]
    ph5 = previous_candle_5['High']
    pc5 = previous_candle_5['Close']

    # 7th Last candle
    previous_candle_6 = tdf.iloc[-(c+6)]
    ph6 = previous_candle_6['High']
    pc6 = previous_candle_6['Close']

    # bearish_candles = 0
    # bullish_candles = 0
    # is_14_candles_below_emaBuy = False
    # is_bullish_candles_greater = False

    # for i in range(16,3,-1):
    #     high = df.iloc[-(i)]['High']
    #     if(high<ema_buy):
    #         is_14_candles_below_emaBuy = True
    #     elif(high>ema_buy):
    #         is_14_candles_below_emaBuy = False
    #         break

    # if(is_14_candles_below_emaBuy):
    #     for i in range(16,3,-1):
    #         open = df.iloc[-(i)]['Open']
    #         close = df.iloc[-(i)]['Close']
    #         if(close<open):
    #             bearish_candles = bearish_candles + 1
    #         elif(close>open):
    #             bullish_candles = bullish_candles + 1

    #     if(bullish_candles>bearish_candles):
    #         is_bullish_candles_greater = True

    # if(is_bullish_candles_greater):
    #     return 'ok'
    # elif(is_14_candles_below_emaBuy==False):
    if((ph4<ema_buy and ph3<ema_buy and ph2<ema_buy and ph1<ema_buy and lh<ema_buy) or ((pc4>(ema_buy+0.05)) or (pc5>(ema_buy+0.05)) or (pc6>(ema_buy+0.05)))):
        return 'ok'
    else:
        return 'not'

def is_one_hour_candle_down():
    df = get_1hour_candles()
    ema = ema_check(df)
    ema_buy = ema_buy_check(df)
    ema_100 = ema_last(df)

    c = 2
    last_candle = df.iloc[-c]
    lo = last_candle['Open']
    lc = last_candle['Close']
    lh = last_candle['High']
    ll = last_candle['Low']

    if(lh<ema and lh<ema_buy and lh<ema_100):
        return True
    else:
        return False
    

def down_percentage_check(df):
    c = 2
    # Second Last candle
    previous_candle_1 = df.iloc[-(c+1)]
    po1 = previous_candle_1['Open']
    pc1 = previous_candle_1['Close']
    
    # 3rd Last candle
    previous_candle_2 = df.iloc[-(c+2)]
    po2 = previous_candle_2['Open']
    pc2 = previous_candle_2['Close']

    # 4th Last candle
    previous_candle_3 = df.iloc[-(c+3)]
    po3 = previous_candle_3['Open']
    pc3 = previous_candle_3['Close']
    
    # 5th Last candle
    previous_candle_4 = df.iloc[-(c+4)]
    po4 = previous_candle_4['Open']
    pc4 = previous_candle_4['Close']
    
    max_open = 0
    min_close = 0

    if(po1>po2 and po1>po3 and pc1<po1):
        max_open = po1
    elif(po2>po1 and po2>po3 and pc2<po2):
        max_open = po2
    elif(po3>po1 and po3>po2 and pc3<po3):
        max_open = po3
    

    if(pc1<pc2 and pc1<pc3 and pc1<po1):
        min_close = pc1
    elif(pc2<pc1 and pc2<pc3 and pc2<po2):
        min_close = pc2
    elif(pc3<pc1 and pc3<pc2 and pc3<po3):
        min_close = pc3

    print(f'Max:{max_open}')
    print(f'Min:{min_close}')

    if(max_open==0 or min_close==0):
        return 0
    else:
        s = min_close/max_open
        s = s * 100
        s = 100 - s
        return s
    

def is_30_min_allow_buy():
    df3 = get_30min_candles()
    candle_Typ = candle_type(df3)
    candle = detect_candlestick_pattern(df3)
    ema = ema_check(df3)
    ema_buy = ema_buy_check(df3)
    ema_100 = ema_last(df3)
    upper_ema_diff = ema_buy-ema
    lower_ema_diff = ema-ema_buy
    trend = trend_check(df3)
    upper_ema = ema_check(df3) + (ema_check(df3) * 0.0015)
    lower_ema = ema_check(df3) - (ema_check(df3) * 0.0015)
    upper_exceed_ema = ema_check(df3) + (ema_check(df3) * 0.0015)
    lower_exceed_ema = ema_check(df3) - (ema_check(df3) * 0.0015)
    trade_status = buy_trade_status(df3)
    emaBuy_status = emaBuy_buy_status(df3)
    return_true = False
    # down_percentage = down_percentage_check(df2)
    signal = None
    # stoploss_set = False
    # is_15min_done = False

    c = 2
    last_candle = df3.iloc[-c]
    lo = last_candle['Open']
    lc = last_candle['Close']
    lh = last_candle['High']
    ll = last_candle['Low']

    previous_candle_1 = df3.iloc[-(c+1)]
    po = previous_candle_1['Open']
    pc = previous_candle_1['Close']
    ph = previous_candle_1['High']
    pl = previous_candle_1['Low']

    previous_candle_2 = df3.iloc[-(c+2)]
    po2 = previous_candle_2['Open']
    pc2 = previous_candle_2['Close']
    ph2 = previous_candle_2['High']
    pl2 = previous_candle_2['Low']

    print("EmaBuy status:" + emaBuy_status)


    # For buy order
    if(candle == 'Bullish Engulfing' and candle_Typ == 'Bullish candle' and trend == 'Down_trend' and trade_status == 'ok'):
        if(ema_buy<ema and ema_buy<ema_100 and emaBuy_status =='ok' and lh<ema_buy):
            signal = 'Buy'
        elif(ema_buy>ema and ema_buy>ema_100):
            # 
            if(((ll>lower_ema and ll<=upper_exceed_ema)) and (lo<(ema_buy+ema)/2 or lc<(ema_buy+ema)/2)):
                # 
                signal = 'Buy'
            elif(((ema_buy>ll and ema_buy<lh) or ((ll<ema_buy and ll>ema) and (lc>(ema+ema_buy)/2))) and ll>ema):
                signal = 'Buy'
        # Buy trade
        if (signal == 'Buy'):
            return_true = True

    elif(candle == 'Right Hammer' and candle_Typ == 'Bullish candle' and trend == 'Down_trend' and trade_status == 'ok'):
        if(ema_buy<ema and ema_buy<ema_100 and emaBuy_status=='ok' and lh<ema_buy):
            signal = 'Buy'
        elif(ema_buy>ema and ema_buy>ema_100):
            if((ll>lower_ema and ll<=upper_exceed_ema) and (lo<(ema_buy+ema)/2 or lc<(ema_buy+ema)/2)):
                signal = 'Buy'
            elif(((ema_buy>ll and ema_buy<lh) or ((ll<ema_buy and ll>ema) and (lc>(ema+ema_buy)/2))) and ll>ema):
                # lo<(ema_buy+ema)/2 or 
                signal = 'Buy'
        # Buy trade
        if (signal == 'Buy'):
            return_true = True

    elif(candle == 'Inverted hammer' and candle_Typ == 'Bullish candle' and trend == 'Down_trend' and trade_status == 'ok'):
        if(ema_buy<ema and ema_buy<ema_100 and emaBuy_status=='ok' and lh<ema_buy):
            signal = 'Buy'
        elif(ema_buy>ema and ema_buy>ema_100):
            if((ll>lower_ema and ll<=upper_exceed_ema) and (lo<(ema_buy+ema)/2 or lc<(ema_buy+ema)/2)):
                signal = 'Buy'
            elif(((ema_buy>ll and ema_buy<lh) or ((ll<ema_buy and ll>ema) and (lc>(ema+ema_buy)/2))) and ll>ema):
                signal = 'Buy'
        # Buy trade
        if (signal == 'Buy'):
            return_true = True

    elif(candle == 'Right Hammer' and candle_Typ == 'Bearish candle' and trend == 'Down_trend' and trade_status == 'ok'):
        if(ema_buy<ema and ema_buy<ema_100 and emaBuy_status=='ok' and lh<ema_buy):
            signal = 'Buy'
        elif(ema_buy>ema and ema_buy>ema_100):
            if((ll>lower_ema and ll<=upper_exceed_ema) and (lo<(ema_buy+ema)/2 or lc<(ema_buy+ema)/2)):
                signal = 'Buy'
            elif(((ema_buy>ll and ema_buy<lh) or ((ll<ema_buy and ll>ema) and (lo>(ema+ema_buy)/2))) and ll>ema):
                signal = 'Buy'
        # Buy trade
        if (signal == 'Buy'):
            return_true = True

    elif(candle == 'Inverted hammer' and candle_Typ == 'Bearish candle' and trend == 'Down_trend' and trade_status == 'ok'):
        if(ema_buy<ema and ema_buy<ema_100 and emaBuy_status=='ok' and lh<ema_buy):
            signal = 'Buy'
        elif(ema_buy>ema and ema_buy>ema_100):
            if((ll>lower_ema and ll<=upper_exceed_ema) and (lo<(ema_buy+ema)/2 or lc<(ema_buy+ema)/2)):
                signal = 'Buy'
            elif(((ema_buy>ll and ema_buy<lh) or ((ll<ema_buy and ll>ema) and (lo>(ema+ema_buy)/2))) and ll>ema):
                signal = 'Buy'
        # Buy trade
        if (signal == 'Buy'):
            return_true = True

    elif(candle == 'Spinning Top' and (candle_Typ == 'Bullish candle' or candle_Typ == 'Bearish candle') and trend == 'Down_trend' and trade_status == 'ok'):
        if(ema_buy<ema and ema_buy<ema_100 and emaBuy_status=='ok' and lh<ema_buy):
            signal = 'Buy'
        elif(ema_buy>ema and ema_buy>ema_100):
            if((ll>lower_ema and ll<=upper_exceed_ema) and (lo<(ema_buy+ema)/2 or lc<(ema_buy+ema)/2)):
                signal = 'Buy'
            elif(((ema_buy>ll and ema_buy<lh) or ((ll<ema_buy and ll>ema) and (lc>(ema+ema_buy)/2))) and ll>ema):
                signal = 'Buy'
        # Buy trade
        if (signal == 'Buy'):
            return_true = True

    elif(candle == 'Dragonfly doji' and trend == 'Down_trend' and ll<=pl and (candle_Typ == 'Bullish candle' or candle_Typ == 'Bearish candle' or candle_Typ == 'Doji') and trade_status == 'ok'):
        if(ema_buy<ema and ema_buy<ema_100 and emaBuy_status=='ok' and lh<ema_buy):
            signal = 'Buy'
        elif(ema_buy>ema and ema_buy>ema_100):
            if((ll>lower_ema and ll<=upper_exceed_ema) and (lo<(ema_buy+ema)/2 or lc<(ema_buy+ema)/2)):
                signal = 'Buy'
            elif(((ema_buy>ll and ema_buy<lh) or ((ll<ema_buy and ll>ema) and (lc>(ema+ema_buy)/2))) and ll>ema):
                signal = 'Buy'
        # Buy trade
        if (signal == 'Buy'):
            return_true = True

    elif(candle == 'Gravestone Doji' and trend == 'Down_trend' and ll<=pl and (candle_Typ == 'Bullish candle' or candle_Typ == 'Bearish candle' or candle_Typ == 'Doji') and trade_status == 'ok'):
        if(ema_buy<ema and ema_buy<ema_100 and emaBuy_status=='ok' and lh<ema_buy):
            signal = 'Buy'
        elif(ema_buy>ema and ema_buy>ema_100):
            if((ll>lower_ema and ll<=upper_exceed_ema) and (lo<(ema_buy+ema)/2 or lc<(ema_buy+ema)/2)):
                signal = 'Buy'
            elif(((ema_buy>ll and ema_buy<lh) or ((ll<ema_buy and ll>ema) and (lc>(ema+ema_buy)/2))) and ll>ema):
                signal = 'Buy'
        # Buy trade
        if (signal == 'Buy'):
            return_true = True

    elif(candle == 'Simple Doji' and trend == 'Down_trend' and ll<=pl and (candle_Typ == 'Bullish candle' or candle_Typ == 'Bearish candle' or candle_Typ == 'Doji') and trade_status == 'ok'):
        if(ema_buy<ema and ema_buy<ema_100 and emaBuy_status=='ok' and lh<ema_buy):
            signal = 'Buy'
        elif(ema_buy>ema and ema_buy>ema_100):
            if((ll>lower_ema and ll<=upper_exceed_ema) and (lo<(ema_buy+ema)/2 or lc<(ema_buy+ema)/2)):
                signal = 'Buy'
            elif(((ema_buy>ll and ema_buy<lh) or ((ll<ema_buy and ll>ema) and (lc>(ema+ema_buy)/2))) and ll>ema):
                signal = 'Buy'
        # Buy trade
        if (signal == 'Buy'):
            return_true = True

    elif(candle == 'Reversal' and candle_Typ == 'Bullish candle' and trend == 'Down_trend' and trade_status == 'ok'):
        if(ema_buy<ema and ema_buy<ema_100 and emaBuy_status=='ok' and lh<ema_buy):
            signal = 'Buy'
        elif(ema_buy>ema and ema_buy>ema_100):
            if((ll>lower_ema and ll<=upper_exceed_ema) and (lo<(ema_buy+ema)/2 or lc<(ema_buy+ema)/2)):
                signal = 'Buy'
            elif(((ema_buy>ll and ema_buy<lh) or ((ll<ema_buy and ll>ema) and (lc>(ema+ema_buy)/2))) and ll>ema):
                signal = 'Buy'
        # Buy trade
        if (signal == 'Buy'):
            return_true = True

    elif(candle == 'Reversal' and candle_Typ == 'Bearish candle' and trend == 'Down_trend' and trade_status == 'ok'):
        if(ema_buy<ema and ema_buy<ema_100 and emaBuy_status=='ok' and lh<ema_buy):
            signal = 'Buy'
        elif(ema_buy>ema and ema_buy>ema_100):
            if((ll>lower_ema and ll<=upper_exceed_ema) and (lo<(ema_buy+ema)/2 or lc<(ema_buy+ema)/2)):
                signal = 'Buy'
            elif(((ema_buy>ll and ema_buy<lh) or ((ll<ema_buy and ll>ema) and (lo>(ema+ema_buy)/2))) and ll>ema):
                signal = 'Buy'
        # Buy trade
        if (signal == 'Buy'):
            return_true = True

    elif(candle == 'Bullish Marubuzu' and candle_Typ == 'Bullish candle' and trend == 'Down_trend' and trade_status == 'ok'):
        if(ema_buy<ema and ema_buy<ema_100 and emaBuy_status=='ok' and lh<ema_buy):
            signal = 'Buy'
        elif(ema_buy>ema and ema_buy>ema_100):
            if(((ll>lower_ema and ll<=upper_exceed_ema)) and (lo<(ema_buy+ema)/2 or lc<(ema_buy+ema)/2)):
                signal = 'Buy'
            elif(((ema_buy>ll and ema_buy<lh) or ((ll<ema_buy and ll>ema) and (lc>(ema+ema_buy)/2))) and ll>ema):
                signal = 'Buy'
        # Buy trade
        if (signal == 'Buy'):
            return_true = True
    
    # Second Condition
    if(ema_100<ema and trend == 'Down_trend' and ema_100 < ema_buy and 
        ((ema_100<=lh and ema_100>=ll) or (ll<=((ema+ema_100)/2 -((ema-ema_100)/6)))) and (lc<(ema+ema_100)/2 or lo<(ema+ema_100)/2) and trade_status == 'ok'):

        if(candle == 'Bullish Engulfing' and candle_Typ == 'Bullish candle'):
            return_true = True
        elif(candle == 'Right Hammer' and candle_Typ == 'Bullish candle'):
            return_true = True
        elif(candle == 'Right Hammer' and candle_Typ == 'Bearish candle'):
            return_true = True
        elif(candle == 'Inverted hammer' and candle_Typ == 'Bullish candle'):
            return_true = True
        elif(candle == 'Inverted hammer' and candle_Typ == 'Bearish candle'):
            return_true = True
        elif(candle == 'Spinning Top' and (candle_Typ == 'Bullish candle' or candle_Typ == 'Bearish candle')):
            return_true = True
        elif(candle == 'Dragonfly doji' and (candle_Typ == 'Bullish candle' or candle_Typ == 'Bearish candle' or candle_Typ == 'Doji') and ll<=pl):
            return_true = True
        elif(candle == 'Gravestone Doji' and ll<=pl and (candle_Typ == 'Bullish candle' or candle_Typ == 'Bearish candle' or candle_Typ == 'Doji')):
            return_true = True
        elif(candle == 'Simple Doji' and ll<=pl and (candle_Typ == 'Bullish candle' or candle_Typ == 'Bearish candle' or candle_Typ == 'Doji')):
            return_true = True
        elif(candle == 'Reversal' and candle_Typ == 'Bullish candle'):
            return_true = True
        elif(candle == 'Reversal' and candle_Typ == 'Bearish candle'):
            return_true = True
        elif(candle == 'Bullish Marubuzu' and candle_Typ == 'Bullish candle'):
            return_true = True

    if(return_true):
        print("30 minutes candle allow buy!")
        return True
    else:
        print("30 minutes candle does not allow buy")
        return False
    

def check_one_hour_trade():
    print('         -------------------')
    print('          Pre 1 hour setup')
    df2 = get_1hour_candles()
    candle_Typ = candle_type(df2)
    candle = detect_candlestick_pattern(df2)
    ema = ema_check(df2)
    ema_buy = ema_buy_check(df2)
    ema_100 = ema_last(df2)
    upper_ema_diff = ema_buy-ema
    lower_ema_diff = ema-ema_buy
    trend = trend_check(df2,1)
    upper_ema = ema_check(df2) + (ema_check(df2) * 0.0015)
    lower_ema = ema_check(df2) - (ema_check(df2) * 0.0015)
    upper_exceed_ema = ema_check(df2) + (ema_check(df2) * 0.0015)
    lower_exceed_ema = ema_check(df2) - (ema_check(df2) * 0.0015)
    trade_status = buy_trade_status(df2)
    signal = None
    oneHour_orderId = None
    oneHour_buy_price = None
    is_oneHour_trade_done = False

    c = 2
    last_candle = df2.iloc[-c]
    lo = last_candle['Open']
    lc = last_candle['Close']
    lh = last_candle['High']
    ll = last_candle['Low']

    previous_candle_1 = df2.iloc[-(c+1)]
    po = previous_candle_1['Open']
    pc = previous_candle_1['Close']
    ph = previous_candle_1['High']
    pl = previous_candle_1['Low']

    previous_candle_2 = df2.iloc[-(c+2)]
    po2 = previous_candle_2['Open']
    pc2 = previous_candle_2['Close']
    ph2 = previous_candle_2['High']
    pl2 = previous_candle_2['Low']

    print(candle_Typ)
    print(candle)
    print(trend_check(df2))
    can_one_hour_buy = False
    if(ll<pl or ll<pl2):
        can_one_hour_buy = True
    # -----------------------------------------------------------------------------------------------------------
    # For buy order
    if(candle == 'Bullish Engulfing' and candle_Typ == 'Bullish candle' and trend == 'Down_trend' and trade_status == 'ok'):
        if(ema_buy<ema and ema_buy<ema_100 and lh<ema_buy):
            signal = 'Buy'
        elif(ema_buy>ema and ema_buy>ema_100):
            # 
            if(((ll>lower_ema and ll<=upper_exceed_ema)) and (lo<(ema_buy+ema)/2 or lc<(ema_buy+ema)/2)):
                # 
                signal = 'Buy'
            elif(((ema_buy>ll and ema_buy<lh) or ((ll<ema_buy and ll>ema) and (lc>(ema+ema_buy)/2))) and ll>ema):
                signal = 'Buy'
        # Buy trade
        if (signal == 'Buy'and can_one_hour_buy):
            if(lh>ph):
                buy_price = (lh+0.05)
                # Stop market buy
                oneHour_orderId = place_one_hour_stop_limit_buy_order(buy_price)
                if oneHour_orderId:
                    oneHour_buy_price = buy_price
                    is_oneHour_trade_done = True
            else:
                buy_price = (ph+0.05)
                # Stop market buy
                oneHour_orderId = place_one_hour_stop_limit_buy_order(buy_price)
                if oneHour_orderId:
                    oneHour_buy_price = buy_price
                    is_oneHour_trade_done = True

    elif(candle == 'Right Hammer' and candle_Typ == 'Bullish candle' and trend == 'Down_trend' and trade_status == 'ok'):
        if(ema_buy<ema and ema_buy<ema_100 and lh<ema_buy):
            signal = 'Buy'
        elif(ema_buy>ema and ema_buy>ema_100):
            if((ll>lower_ema and ll<=upper_exceed_ema) and (lo<(ema_buy+ema)/2 or lc<(ema_buy+ema)/2)):
                signal = 'Buy'
            elif(((ema_buy>ll and ema_buy<lh) or ((ll<ema_buy and ll>ema) and (lc>(ema+ema_buy)/2))) and ll>ema):
                # lo<(ema_buy+ema)/2 or 
                signal = 'Buy'
        # Buy trade
        if (signal == 'Buy'and can_one_hour_buy):
            if((lh-lc)<0.02):
                buy_price = lh+(lc-lo)/3
                # stop limit buy
                oneHour_orderId = place_one_hour_stop_limit_buy_order(buy_price)
                if oneHour_orderId:
                    oneHour_buy_price = buy_price
                    is_oneHour_trade_done = True
            else:
                buy_price = (lh+0.05)
                # Stop limit order
                oneHour_orderId = place_one_hour_stop_limit_buy_order(buy_price)
                if oneHour_orderId:
                    oneHour_buy_price = buy_price
                    is_oneHour_trade_done = True

    elif(candle == 'Inverted hammer' and candle_Typ == 'Bullish candle' and trend == 'Down_trend' and trade_status == 'ok'):
        if(ema_buy<ema and ema_buy<ema_100 and lh<ema_buy):
            signal = 'Buy'
        elif(ema_buy>ema and ema_buy>ema_100):
            if((ll>lower_ema and ll<=upper_exceed_ema) and (lo<(ema_buy+ema)/2 or lc<(ema_buy+ema)/2)):
                signal = 'Buy'
            elif(((ema_buy>ll and ema_buy<lh) or ((ll<ema_buy and ll>ema) and (lc>(ema+ema_buy)/2))) and ll>ema):
                signal = 'Buy'
        # Buy trade
        if (signal == 'Buy' and can_one_hour_buy):
            buy_price = (lh+0.05)
            # Stop limit buy
            oneHour_orderId = place_one_hour_stop_limit_buy_order(buy_price)
            if oneHour_orderId:
                oneHour_buy_price = buy_price
                is_oneHour_trade_done = True

    elif(candle == 'Spinning Top' and candle_Typ == 'Bullish candle' and trend == 'Down_trend' and trade_status == 'ok'):
        if(ema_buy<ema and ema_buy<ema_100 and lh<ema_buy):
            signal = 'Buy'
        elif(ema_buy>ema and ema_buy>ema_100):
            if((ll>lower_ema and ll<=upper_exceed_ema) and (lo<(ema_buy+ema)/2 or lc<(ema_buy+ema)/2)):
                signal = 'Buy'
            elif(((ema_buy>ll and ema_buy<lh) or ((ll<ema_buy and ll>ema) and (lc>(ema+ema_buy)/2))) and ll>ema):
                signal = 'Buy'
        # Buy trade
        if (signal == 'Buy' and can_one_hour_buy):
            buy_price = (lh+0.05)
            # Stop limit buy
            oneHour_orderId = place_one_hour_stop_limit_buy_order(buy_price)
            if oneHour_orderId:
                oneHour_buy_price = buy_price
                is_oneHour_trade_done = True

    elif(candle == 'Reversal' and candle_Typ == 'Bullish candle' and trend == 'Down_trend' and trade_status == 'ok'):
        if(ema_buy<ema and ema_buy<ema_100 and lh<ema_buy):
            signal = 'Buy'
        elif(ema_buy>ema and ema_buy>ema_100):
            if((ll>lower_ema and ll<=upper_exceed_ema) and (lo<(ema_buy+ema)/2 or lc<(ema_buy+ema)/2)):
                signal = 'Buy'
            elif(((ema_buy>ll and ema_buy<lh) or ((ll<ema_buy and ll>ema) and (lc>(ema+ema_buy)/2))) and ll>ema):
                signal = 'Buy'
        # Buy trade
        if (signal == 'Buy' and can_one_hour_buy):
            buy_price = (lh+0.05)
            # Stop limit buy
            oneHour_orderId = place_one_hour_stop_limit_buy_order(buy_price)
            if oneHour_orderId:
                oneHour_buy_price = buy_price
                is_oneHour_trade_done = True

    elif(candle == 'Bullish Marubuzu' and candle_Typ == 'Bullish candle' and trend == 'Down_trend' and trade_status == 'ok'):
        if(ema_buy<ema and ema_buy<ema_100 and lh<ema_buy):
            signal = 'Buy'
        elif(ema_buy>ema and ema_buy>ema_100):
            if(((ll>lower_ema and ll<=upper_exceed_ema)) and (lo<(ema_buy+ema)/2 or lc<(ema_buy+ema)/2)):
                signal = 'Buy'
            elif(((ema_buy>ll and ema_buy<lh) or ((ll<ema_buy and ll>ema) and (lc>(ema+ema_buy)/2))) and ll>ema):
                signal = 'Buy'
        # Buy trade
        if (signal == 'Buy' and can_one_hour_buy):
            if(lh>ph):
                buy_price = (lh+0.05)
                # Stop market buy
                oneHour_orderId = place_one_hour_stop_limit_buy_order(buy_price)
                if oneHour_orderId:
                    oneHour_buy_price = buy_price
                    is_oneHour_trade_done = True
            else:
                buy_price = (ph+0.05)
                # Stop market buy
                oneHour_orderId = place_one_hour_stop_limit_buy_order(buy_price)
                if oneHour_orderId:
                    oneHour_buy_price = buy_price
                    is_oneHour_trade_done = True
            
    # Second Condition
    if(ema_100<ema and trend == 'Down_trend' and ema_100 < ema_buy and 
        ((ema_100<=lh and ema_100>=ll) or (ll<=((ema+ema_100)/2 -((ema-ema_100)/6)))) and (lc<(ema+ema_100)/2 or lo<(ema+ema_100)/2) and trade_status == 'ok' and can_one_hour_buy):

        if(candle == 'Bullish Engulfing' and candle_Typ == 'Bullish candle'):
            if(lh>ph):
                buy_price = (lh+0.05)
                # Stop market buy
                oneHour_orderId = place_one_hour_stop_limit_buy_order(buy_price)
                if oneHour_orderId:
                    oneHour_buy_price = buy_price
                    is_oneHour_trade_done = True
            else:
                buy_price = (ph+0.05)
                # Stop market buy
                oneHour_orderId = place_one_hour_stop_limit_buy_order(buy_price)
                if oneHour_orderId:
                    oneHour_buy_price = buy_price
                    is_oneHour_trade_done = True
        elif(candle == 'Right Hammer' and candle_Typ == 'Bullish candle'):
            if((lh-lc)<0.02):
                buy_price = lh+(lc-lo)/3
                # stop limit buy
                oneHour_orderId = place_one_hour_stop_limit_buy_order(buy_price)
                if oneHour_orderId:
                    oneHour_buy_price = buy_price
                    is_oneHour_trade_done = True
            else:
                buy_price = (lh+0.05)
                # Stop limit order
                oneHour_orderId = place_one_hour_stop_limit_buy_order(buy_price)
                if oneHour_orderId:
                    oneHour_buy_price = buy_price
                    is_oneHour_trade_done = True
        elif(candle == 'Inverted hammer' and candle_Typ == 'Bullish candle'):
            buy_price = lh
            # Stop limit buy
            oneHour_orderId = place_one_hour_stop_limit_buy_order(buy_price)
            if oneHour_orderId:
                oneHour_buy_price = buy_price
                is_oneHour_trade_done = True
        elif(candle == 'Spinning Top' and candle_Typ == 'Bullish candle'):
            buy_price = (lh+0.05)
            # Stop limit buy
            oneHour_orderId = place_one_hour_stop_limit_buy_order(buy_price)
            if oneHour_orderId:
                oneHour_buy_price = buy_price
                is_oneHour_trade_done = True
        elif(candle == 'Reversal' and candle_Typ == 'Bullish candle'):
            buy_price = (lh+0.05)
            # Stop limit buy
            oneHour_orderId = place_one_hour_stop_limit_buy_order(buy_price)
            if oneHour_orderId:
                oneHour_buy_price = buy_price
                is_oneHour_trade_done = True
        elif(candle == 'Bullish Marubuzu' and candle_Typ == 'Bullish candle'):
            if(lh>ph):
                buy_price = (lh+0.05)
                # Stop market buy
                oneHour_orderId = place_one_hour_stop_limit_buy_order(buy_price)
                if oneHour_orderId:
                    oneHour_buy_price = buy_price
                    is_oneHour_trade_done = True
            else:
                buy_price = (ph+0.05)
                # Stop market buy
                oneHour_orderId = place_one_hour_stop_limit_buy_order(buy_price)
                if oneHour_orderId:
                    oneHour_buy_price = buy_price
                    is_oneHour_trade_done = True
    # -----------------------------------------------------------------------------------------------------------
    # For Selling
    if(candle == 'Bearish Engulfing' and candle_Typ == 'Bearish candle' and trend == 'Up_trend'):
        if(ema_buy>ema and ll>ema_buy):
            signal = 'Sell'
        elif(ema_buy<ema):
            if(((lh<upper_ema and lh>=lower_exceed_ema))):
                signal = 'Sell'
            elif(((ema_buy>ll and ema_buy<lh) or (lh>ema_buy and lh<ema)) and lh<ema):
                signal = 'Sell'
        # Sell trade
        if (signal == 'Sell'):
            if(ll<pl):
                sell_price = ll-0.05
                # Stop limit sell
                oneHour_orderId = place_one_hour_stop_limit_sell_order(sell_price)
                if(oneHour_orderId):
                    is_oneHour_trade_done = True
            else:
                sell_price = pl-0.05
                # Stop limit sell
                oneHour_orderId = place_one_hour_stop_limit_sell_order(sell_price)
                if(oneHour_orderId):
                    is_oneHour_trade_done = True

    elif(candle == 'Right Hammer' and candle_Typ == 'Bearish candle' and trend == 'Up_trend'):
        if(ema_buy>ema and ll>ema_buy):
            signal = 'Sell'
        elif(ema_buy<ema):
            if((lh<upper_ema and lh>=lower_exceed_ema)):
                signal = 'Sell'
            elif(((ema_buy>ll and ema_buy<lh) or (lh>ema_buy and lh<ema)) and lh<ema):
                signal = 'Sell'
        # Sell trade
        if (signal == 'Sell'):
            sell_price = (ll-0.05)
            # Stop limit sell
            oneHour_orderId = place_one_hour_stop_limit_sell_order(sell_price)
            if(oneHour_orderId):
                is_oneHour_trade_done = True

    elif(candle == 'Inverted hammer' and candle_Typ == 'Bearish candle' and trend == 'Up_trend'):
        if(ema_buy>ema and ll>ema_buy):
            signal = 'Sell'
        elif(ema_buy<ema):
            if((lh<upper_ema and lh>=lower_exceed_ema)):
                signal = 'Sell'
            elif(((ema_buy>ll and ema_buy<lh) or (lh>ema_buy and lh<ema)) and lh<ema):
                signal = 'Sell'
        # Sell trade
        if (signal == 'Sell'):
            if((lc-ll)<0.02):
                sell_price = ll-(lo-lc)/3
                # Stop limit sell
                oneHour_orderId = place_one_hour_stop_limit_sell_order(sell_price)
                if(oneHour_orderId):
                    is_oneHour_trade_done = True
            else:
                sell_price = (ll-0.05)
                # Stop limit sell
                oneHour_orderId = place_one_hour_stop_limit_sell_order(sell_price)
                if(oneHour_orderId):
                    is_oneHour_trade_done = True

    elif(candle == 'Spinning Top' and candle_Typ == 'Bearish candle' and trend == 'Up_trend'):
        if(ema_buy>ema and ll>ema_buy):
            signal = 'Sell'
        elif(ema_buy<ema):
            if((lh<upper_ema and lh>=lower_exceed_ema)):
                signal = 'Sell'
            elif(((ema_buy>ll and ema_buy<lh) or (lh>ema_buy and lh<ema)) and lh<ema):
                signal = 'Sell'
        # Sell trade
        if (signal == 'Sell'):
            sell_price = (ll-0.05)
            # Stop limit sell
            oneHour_orderId = place_one_hour_stop_limit_sell_order(sell_price)
            if(oneHour_orderId):
                is_oneHour_trade_done = True

    elif(candle == 'Reversal' and candle_Typ == 'Bearish candle' and trend == 'Up_trend'):
        if(ema_buy>ema and ll>ema_buy):
            signal = 'Sell'
        elif(ema_buy<ema):
            if((lh<upper_ema and lh>=lower_exceed_ema)):
                signal = 'Sell'
            elif(((ema_buy>ll and ema_buy<lh) or (lh>ema_buy and lh<ema)) and lh<ema):
                signal = 'Sell'
        # Sell trade
        if (signal == 'Sell'):
            sell_price = (ll-0.05)
            # Stop limit sell
            oneHour_orderId = place_one_hour_stop_limit_sell_order(sell_price)
            if(oneHour_orderId):
                is_oneHour_trade_done = True

    elif(candle == 'Bearish Marubuzu' and candle_Typ == 'Bearish candle' and trend == 'Up_trend'):
        if(ema_buy>ema and ll>ema_buy):
            signal = 'Sell'
        elif(ema_buy<ema):
            if((lh<upper_ema and lh>=lower_exceed_ema)):
                signal = 'Sell'
            elif(((ema_buy>ll and ema_buy<lh) or (lh>ema_buy and lh<ema)) and lh<ema):
                signal = 'Sell'
        # Sell trade
        if (signal == 'Sell'):
            if(ll<pl):
                sell_price = ll-0.05
                # Stop limit sell
                oneHour_orderId = place_one_hour_stop_limit_sell_order(sell_price)
                if(oneHour_orderId):
                    is_oneHour_trade_done = True
            else:
                sell_price = pl-0.05
                # Stop limit sell
                oneHour_orderId = place_one_hour_stop_limit_sell_order(sell_price)
                if(oneHour_orderId):
                    is_oneHour_trade_done = True

    # Second Condition
    if(ema_100>ema and trend == 'Up_trend' and ema_100 > ema_buy and 
        ((ema_100<=lh and ema_100>=ll) or (lh>=((ema+ema_100)/2 + ((ema-ema_100)/6)))) and (lo>(ema+ema_100)/2 or lc>(ema+ema_100)/2)):
        
        if(candle == 'Bearish Engulfing' and candle_Typ == 'Bearish candle'):
            if(ll<pl):
                sell_price = ll-0.05
                # Stop limit sell
                oneHour_orderId = place_one_hour_stop_limit_sell_order(sell_price)
                if(oneHour_orderId):
                    is_oneHour_trade_done = True
            else:
                sell_price = pl-0.05
                # Stop limit sell
                oneHour_orderId = place_one_hour_stop_limit_sell_order(sell_price)
                if(oneHour_orderId):
                    is_oneHour_trade_done = True
        elif(candle == 'Right Hammer' and candle_Typ == 'Bearish candle'):
            sell_price = (ll-0.05)
            # Stop limit sell
            oneHour_orderId = place_one_hour_stop_limit_sell_order(sell_price)
            if(oneHour_orderId):
                is_oneHour_trade_done = True
        elif(candle == 'Inverted hammer' and candle_Typ == 'Bearish candle'):
            if((lc-ll)<0.02):
                sell_price = ll-(lo-lc)/3
                # Stop limit sell
                oneHour_orderId = place_one_hour_stop_limit_sell_order(sell_price)
                if(oneHour_orderId):
                    is_oneHour_trade_done = True
            else:
                sell_price = (ll-0.05)
                # Stop limit sell
                oneHour_orderId = place_one_hour_stop_limit_sell_order(sell_price)
                if(oneHour_orderId):
                    is_oneHour_trade_done = True
        elif(candle == 'Spinning Top' and candle_Typ == 'Bearish candle'):
            sell_price = (ll-0.05)
            # Stop limit sell
            oneHour_orderId = place_one_hour_stop_limit_sell_order(sell_price)
            if(oneHour_orderId):
                is_oneHour_trade_done = True
        elif(candle == 'Reversal' and candle_Typ == 'Bearish candle'):
            sell_price = (ll-0.05)
            # Stop limit sell
            oneHour_orderId = place_one_hour_stop_limit_sell_order(sell_price)
            if(oneHour_orderId):
                is_oneHour_trade_done = True
        elif(candle == 'Bearish Marubuzu' and candle_Typ == 'Bearish candle'):
            if(ll<pl):
                sell_price = ll-0.05
                # Stop limit sell
                oneHour_orderId = place_one_hour_stop_limit_sell_order(sell_price)
                if(oneHour_orderId):
                    is_oneHour_trade_done = True
            else:
                sell_price = pl-0.05
                # Stop limit sell
                oneHour_orderId = place_one_hour_stop_limit_sell_order(sell_price)
                if(oneHour_orderId):
                    is_oneHour_trade_done = True

    print('          ------------------')
    
    return oneHour_orderId, oneHour_buy_price, is_oneHour_trade_done