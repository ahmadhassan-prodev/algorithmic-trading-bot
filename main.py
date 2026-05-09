from utils.wait_time import *
from assets.exchange_assets import *
from data.data_fetcher import *
from indicators.candlestick_details import *
from indicators.ema import *
from indicators.rsi import *
from indicators.trend import *
from indicators.volume import *
from strategies.profit_strategies import *
from trading.trade_execution_helper import *
from utils.exchange_helpers import *
from orders.exchange_orders import *


# Main Program
trade_combination = int(input("Choose the trend:\n1.Uptrend\n2.Downtrend\n"))
is_PL_and_H = False
is_PH_and_L = False
one_hour_trade_input = None
if trade_combination==1:
    is_PL_and_H = True
    one_hour_trade_input = 1
elif trade_combination==2:
    is_PH_and_L = True
    one_hour_trade_input = 2

high = None
low = None
prev_high = None
prev_low = None

prev_low = float(input("Enter the value of previous low: "))
prev_high = float(input("Enter the value of previous high: "))
high = float(input("Enter the value of high: "))
low = float(input("Enter the value of low: "))

is_oneHour_above_high = False
is_oneHour_below_low = False
if one_hour_trade_input == 1:
    is_oneHour_above_high = True
elif one_hour_trade_input == 2: 
    is_oneHour_below_low = True

isHighConfirm = False
isLowConfirm = False
temp_high = None
temp_low = None

sleep_until_next_15min()
stoploss = 0
is_30_min_signal_found = False
is_15_min_signal_found = False
is_one_hour_signal_found = False
is_15_min_buy_done = False
hours_after_15_min_buy = 0
is_oneHour_done = False
is_oneHour_trade_done = False
oneHour_buy_price = None
oneHour_orderId = None
oneHour_trade_time = None
is_buy_waiting_active = False
is_afterbuy_stoploss_active = False
is_one_candle_wait_activated = False
is_check_for_30_min = False
check_30_min_buy_price = None
check_30_min_stoploss = None
candle_number = None
candles_wait = None
signal_candle = None
signal_high = None
signal_low = None
signal_close = None
signal_open = None
is_shift_towards_30_min = False
is_buy_signal_found_between_30_min = False
is_combination_of_15_and_30_min = False
wh = None
wl = None
wc = None
wo = None
sl = None
flo3 = None
flc3 = None
flh3 = None
fll3 = None
one_h = None
candle_number = 0
stoploss_orderId = None
stoploss_buy_price = None
stoploss_low_price = None
is_trade_shift_one_hour_signal_found = False
is_looking_for_one_hour_signal = False
is_check_for_one_candle_stoploss = False
is_check_for_one_candle_stoploss = False
while (True):
    try:
        if(oneHour_buy_price):
            status = get_order_status(oneHour_orderId)
            if(status == 'FILLED'):
                cancel_limit_sell_order()
                # need to change order
                stoploss_orderId = place_stoploss_sell_order(stoploss,1)
                if stoploss_orderId:
                    stoploss_buy_price = oneHour_buy_price
                    stoploss_low_price = stoploss
                is_shift_towards_30_min = True
                is_oneHour_trade_done = False
                oneHour_buy_price = None
                oneHour_orderId = None
                print("sell trade is shifted towards 30 min")
            elif(status == 'CANCELED'):
                oneHour_buy_price = None
                is_oneHour_trade_done = False
                oneHour_orderId = None
    # --------------------------------------------------------------------------------------------
        # Deciding time for trade
        one_df = get_1hour_candles()
        last_candle_one = one_df.iloc[-2]
        one_lh = last_candle_one['High']
        one_ll = last_candle_one['Low']

        previous_candle_one = one_df.iloc[-3]
        one_ph = previous_candle_one['High']
        one_pl = previous_candle_one['Low']

        if(one_lh>high and one_lh>one_ph):
            temp_high = one_lh
        elif temp_high:
            if temp_high-one_ll > temp_high*0.03:
                isHighConfirm = True

        if(one_ll<low and one_ll<one_pl):
            temp_low = one_ll
        elif temp_low:
            if one_lh - temp_low > temp_low*0.03:
                isLowConfirm = True

        if(isHighConfirm):
            high = temp_high
            temp_high = None
            prev_low = low 
            low = one_ll
            temp_low = low
            isHighConfirm = False
        elif(isLowConfirm):
            low = temp_low
            temp_low = None
            prev_high = high
            high = one_lh
            temp_high = high
            isLowConfirm = False

        if is_PL_and_H and is_oneHour_above_high:
            if(one_ll<prev_low):
                is_oneHour_above_high = False
                is_oneHour_below_low = True
                is_PL_and_H = False
                is_PH_and_L = True
        elif is_PH_and_L and is_oneHour_below_low:
            if(one_lh>prev_high):
                is_oneHour_above_high = True
                is_oneHour_below_low = False
                is_PL_and_H = True
                is_PH_and_L = False

        if is_oneHour_above_high:
            print("Price is moving in uptrend")
            print("High:",high)
            print("Low:",prev_low)
        elif is_oneHour_below_low:
            print("Price is moving in downtrend")
            print("High:",prev_high)
            print("Low:",low)
        print('--------------------------------------')
    # -----------------------------------------------------------------------------------------

        print("           15 minutes setup")
        df = get_15min_candles()
        candle_Typ = candle_type(df)
        candle = detect_candlestick_pattern(df)
        ema = ema_check(df)
        ema_buy = ema_buy_check(df)
        ema_100 = ema_last(df)
        upper_ema_diff = ema_buy-ema
        lower_ema_diff = ema-ema_buy
        trend = trend_check(df)
        upper_ema = ema_check(df) + (ema_check(df) * 0.0015)
        lower_ema = ema_check(df) - (ema_check(df) * 0.0015)
        upper_exceed_ema = ema_check(df) + (ema_check(df) * 0.0015)
        lower_exceed_ema = ema_check(df) - (ema_check(df) * 0.0015)
        upper_ema_buy = ema_buy + (ema_buy * 0.0011)
        lower_ema_buy = ema_buy - (ema_buy * 0.0011)
        trade_status = buy_trade_status(df)
        emaBuy_status = emaBuy_buy_status(df)
        down_percentage = down_percentage_check(df)
        signal = None
        stoploss_set = False
        is_15min_done = False
        is_pre_order_done = False
        is_now_30 = False
        status = None
        order_time = None

        c = 2
        last_candle = df.iloc[-c]
        lo = last_candle['Open']
        lc = last_candle['Close']
        lh = last_candle['High']
        ll = last_candle['Low']

        previous_candle_1 = df.iloc[-(c+1)]
        po = previous_candle_1['Open']
        pc = previous_candle_1['Close']
        ph = previous_candle_1['High']
        pl = previous_candle_1['Low']

        previous_candle_2 = df.iloc[-(c+2)]
        po2 = previous_candle_2['Open']
        pc2 = previous_candle_2['Close']
        ph2 = previous_candle_2['High']
        pl2 = previous_candle_2['Low']

        print(candle_Typ)
        print(candle)
        print(trend_check(df))
        print(down_percentage)

    # -----------------------------------------------------------------------------------------
        now = datetime.now()
        if now.minute == 0 or now.minute == 30:
            is_now_30 = True

        if(is_check_for_one_candle_stoploss):
            if candle_Typ == 'Bearish candle':
                print("One candle stoploss activated!")
                sell_price = stoploss - 0.05
                status, order_time = place_stop_market_sell_order(sell_price)
                if(status == 'FILLED'):
                    stoploss = 0
                    is_15_min_buy_done = False
                else:
                    print("One candle stoploss de-activated!")
                if(is_15min_wait_completed(order_time)):
                    is_15min_done = True
                is_check_for_one_candle_stoploss = False
            else:
                is_check_for_one_candle_stoploss = False

        if(is_one_candle_wait_activated):
            if(lc>ph and lc>ph2):
                buy_price = lh + 0.05
                # Stop market buy
                status, order_time = place_stop_market_buy_order(buy_price)
                if status:
                    if(status == 'FILLED'):
                        stoploss = pl
                        stoploss_set = True
                        if(is_combination_of_15_and_30_min):
                            stoploss_orderId = place_stoploss_sell_order(stoploss,1)
                            if stoploss_orderId:
                                stoploss_buy_price = buy_price
                                stoploss_low_price = stoploss
                        else:
                            stoploss_orderId = set_profit_1(df,buy_price,stoploss)
                            if stoploss_orderId:
                                stoploss_buy_price = buy_price
                                stoploss_low_price = stoploss
                        is_15_min_buy_done = True
                        is_check_for_one_candle_stoploss = True
                        is_combination_of_15_and_30_min = False
                    else:
                        is_buy_waiting_active = True
                        wh = buy_price
                        wl = ll
                        wc = lc
                        wo = lo
                        print(f"Buy waiting activated!\nwh:{wh}\nwl:{wl}")
                        is_combination_of_15_and_30_min = True
                    if(is_15min_wait_completed(order_time)):
                        is_15min_done = True
                is_one_candle_wait_activated = False
            else:
                is_one_candle_wait_activated = False
                is_combination_of_15_and_30_min = False
                print("One candle wait deactivated!")

        if(is_one_hour_signal_found):
            if(lc>one_h):
                cancel_limit_sell_order()
                market_buy_order(lc)
                stoploss_orderId = place_stoploss_sell_order(stoploss,1)
                if stoploss_orderId:
                    stoploss_buy_price = one_h
                    stoploss_low_price = stoploss
                is_shift_towards_30_min = True
                is_one_hour_signal_found = False
                one_h = None
                print("sell trade is shifted towards 30 min")

        # Need to delete
        if is_check_for_30_min:
            if is_30_min_allow_buy():
                print("It is safe to place order for previous 15 min signal")
                if(lc>check_30_min_buy_price):
                    cp = current_SOL()
                    buy_price = cp
                    # Market buy
                    is_check_for_30_min = False
                    if market_buy_order(buy_price):
                        stoploss = check_30_min_stoploss
                        stoploss_orderId = place_stoploss_sell_order(stoploss, 1)
                        if stoploss_orderId:
                            stoploss_buy_price = buy_price
                            stoploss_low_price = stoploss
                        is_15_min_buy_done = True
                    check_30_min_buy_price = None
                    check_30_min_stoploss = None
                elif(lh>check_30_min_buy_price and lc<check_30_min_buy_price):
                    buy_price = lh+0.05
                    # Stop limit buy
                    is_buy_waiting_active = True
                    wh = buy_price
                    wl = check_30_min_stoploss
                    wo = po
                    wc = pc
                    print(f"Buy waiting activated!\nwh:{wh}\nwl:{wl}")
                    is_check_for_30_min = False
                    check_30_min_buy_price = None
                    check_30_min_stoploss = None
                elif(lh<check_30_min_buy_price):
                    if(ll<pl or (lc<lo and (lo-lc)>(pc-po)/2)):
                        is_check_for_30_min = False
                        check_30_min_buy_price = None
                        check_30_min_stoploss = None
                    else:
                        is_buy_waiting_active = True
                        wh = check_30_min_buy_price
                        wl = check_30_min_stoploss
                        wc = pc
                        wo = po
                        print(f"Buy waiting activated!\nwh:{wh}\nwl:{wl}")
                        is_check_for_30_min = False
                        check_30_min_buy_price = None
                        check_30_min_stoploss = None
            else:
                is_check_for_30_min = False
                check_30_min_buy_price = None
                check_30_min_stoploss = None
            print('          ------------------')        
# ----------------------------------------------------------------------------------------------------------------

        if is_oneHour_above_high:
                if(candle == 'Bullish Engulfing' and candle_Typ == 'Bullish candle' and trend == 'Down_trend' and trade_status == 'ok'):
                    if(ema_buy<ema and ema_buy<ema_100 and emaBuy_status=='ok' and lh<ema_buy):
                        signal = 'Buy'
                    elif(ema_buy>ema and ema_buy>ema_100):
                        # 
                        if(((ll>lower_ema and ll<=upper_exceed_ema) or ((ema>ll and ema<lh) and (lc>ema and lo>ema))) and (lo<(ema_buy+ema)/2 or lc<(ema_buy+ema)/2)):
                            # 
                            signal = 'Buy'
                        elif(((ema_buy>ll and ema_buy<lh) or ((ll<ema_buy and ll>ema) and (lc>(ema+ema_buy)/2)) or (upper_ema_buy>ll and upper_ema_buy<lh)) and ll>ema):
                            signal = 'Buy'
                    # Buy trade
                    if (signal == 'Buy'):
                        if(lh>ph):
                            buy_price = (lh+0.05)
                            # Stop market buy
                            status, order_time = place_stop_market_buy_order(buy_price)
                            if status:
                                if(status == 'FILLED'):
                                    if(pl<ll):
                                        stoploss = pl
                                        stoploss_set = True
                                    else:
                                        stoploss = ll
                                        stoploss_set = True
                                    # print('Buy Signal')
                                    # print(buy_price)
                                    stoploss_orderId = set_profit_1(df,buy_price,stoploss)
                                    if stoploss_orderId:
                                        stoploss_buy_price = buy_price
                                        stoploss_low_price = stoploss
                                    is_15_min_buy_done = True
                                    is_check_for_one_candle_stoploss = True
                                else:
                                    is_buy_waiting_active = True
                                    wh = buy_price
                                    wl = ll
                                    wc = lc
                                    wo = lo
                                    print(f"Buy waiting activated!\nwh:{wh}\nwl:{wl}")
                                if(is_15min_wait_completed(order_time)):
                                    is_15min_done = True
                        else:
                            buy_price = (ph+0.05)
                            # Stop market buy
                            status, order_time = place_stop_market_buy_order(buy_price)
                            if status:
                                if(status == 'FILLED'):
                                    if(pl<ll):
                                        stoploss = pl
                                        stoploss_set = True
                                    else:
                                        stoploss = ll
                                        stoploss_set = True
                                    # print('Buy Signal')
                                    # print(buy_price)
                                    stoploss_orderId = set_profit_1(df,buy_price,stoploss)
                                    if stoploss_orderId:
                                        stoploss_buy_price = buy_price
                                        stoploss_low_price = stoploss
                                    is_15_min_buy_done = True
                                    is_check_for_one_candle_stoploss = True
                                else:
                                    is_buy_waiting_active = True
                                    wh = buy_price
                                    wl = ll
                                    wc = lc
                                    wo = lo
                                    print(f"Buy waiting activated!\nwh:{wh}\nwl:{wl}")
                                if(is_15min_wait_completed(order_time)):
                                    is_15min_done = True

                elif(candle == 'Right Hammer' and candle_Typ == 'Bullish candle' and trend == 'Down_trend' and trade_status == 'ok'):
                    if(ema_buy<ema and ema_buy<ema_100 and emaBuy_status=='ok' and lh<ema_buy):
                        signal = 'Buy'
                    elif(ema_buy>ema and ema_buy>ema_100):
                        if(((ll>lower_ema and ll<=upper_exceed_ema)) and (lo<(ema_buy+ema)/2 or lc<(ema_buy+ema)/2)):
                            signal = 'Buy'
                        elif(((ema_buy>ll and ema_buy<lh) or ((ll<ema_buy and ll>ema) and (lc>(ema+ema_buy)/2)) or (upper_ema_buy>ll and upper_ema_buy<lh)) and ll>ema):
                            # lo<(ema_buy+ema)/2 or 
                            signal = 'Buy'
                    # Buy trade
                    if (signal == 'Buy' and is_volume_filter_pass(df)):
                        if((lh-lc)<0.02):
                            buy_price = lh+(lc-lo)/3
                            # stop limit buy
                            status, order_time = place_stop_market_buy_order(buy_price)
                            if status:
                                if(status == 'FILLED'):
                                    stoploss = ll
                                    stoploss_set = True
                                    stoploss_orderId = set_profit_1(df,buy_price,stoploss)
                                    if stoploss_orderId:
                                        stoploss_buy_price = buy_price
                                        stoploss_low_price = stoploss
                                    is_15_min_buy_done = True
                                    is_check_for_one_candle_stoploss = True
                                    # print('Buy Signal')
                                    # print(buy_price)
                                else:
                                    is_buy_waiting_active = True
                                    wh = buy_price
                                    wl = ll
                                    wc = lc
                                    wo = lo
                                    print(f"Buy waiting activated!\nwh:{wh}\nwl:{wl}")
                                if(is_15min_wait_completed(order_time)):
                                    is_15min_done = True
                        else:
                            buy_price = (lh+0.05)
                            # Stop limit order
                            status, order_time = place_stop_market_buy_order(buy_price)
                            if status:
                                if(status == 'FILLED'):
                                    stoploss = ll
                                    stoploss_set = True
                                    stoploss_orderId = set_profit_1(df,buy_price,stoploss)
                                    if stoploss_orderId:
                                        stoploss_buy_price = buy_price
                                        stoploss_low_price = stoploss
                                    is_15_min_buy_done = True
                                    is_check_for_one_candle_stoploss = True
                                    # print('Buy Signal')
                                    # print(buy_price)
                                else:
                                    is_buy_waiting_active = True
                                    wh = buy_price
                                    wl = ll
                                    wc = lc
                                    wo = lo
                                    print(f"Buy waiting activated!\nwh:{wh}\nwl:{wl}")
                                if(is_15min_wait_completed(order_time)):
                                    is_15min_done = True

                elif(candle == 'Inverted hammer' and candle_Typ == 'Bullish candle' and trend == 'Down_trend' and trade_status == 'ok'):
                    if(ema_buy<ema and ema_buy<ema_100 and emaBuy_status=='ok' and lh<ema_buy):
                        signal = 'Buy'
                    elif(ema_buy>ema and ema_buy>ema_100):
                        if(((ll>lower_ema and ll<=upper_exceed_ema) or ((ema>ll and ema<lh) and (lc>ema and lo>ema))) and (lo<(ema_buy+ema)/2 or lc<(ema_buy+ema)/2)):
                            signal = 'Buy'
                        elif(((ema_buy>ll and ema_buy<lh) or ((ll<ema_buy and ll>ema) and (lc>(ema+ema_buy)/2)) or (upper_ema_buy>ll and upper_ema_buy<lh)) and ll>ema):
                            signal = 'Buy'
                    # Buy trade
                    if (signal == 'Buy' and is_volume_filter_pass(df)):
                        buy_price = (lh+0.05)
                        # Stop limit buy
                        status, order_time = place_stop_market_buy_order(buy_price)
                        if status:
                            if(status == 'FILLED'):
                                stoploss = ll
                                stoploss_set = True
                                stoploss_orderId = set_profit_1(df,buy_price,stoploss)
                                if stoploss_orderId:
                                    stoploss_buy_price = buy_price
                                    stoploss_low_price = stoploss
                                is_15_min_buy_done = True
                                is_check_for_one_candle_stoploss = True
                                # print('Buy Signal')
                                # print(buy_price)
                            else:
                                is_buy_waiting_active = True
                                wh = buy_price
                                wl = ll
                                wc = lc
                                wo = lo
                                print(f"Buy waiting activated!\nwh:{wh}\nwl:{wl}")
                            if(is_15min_wait_completed(order_time)):
                                is_15min_done = True

                elif(candle == 'Right Hammer' and candle_Typ == 'Bearish candle' and trend == 'Down_trend' and trade_status == 'ok'):
                    if(ema_buy<ema and ema_buy<ema_100 and emaBuy_status=='ok' and lh<ema_buy):
                        signal = 'Buy'
                    elif(ema_buy>ema and ema_buy>ema_100):
                        if(((ll>lower_ema and ll<=upper_exceed_ema) or ((ema>ll and ema<lh) and (lc>ema and lo>ema))) and (lo<(ema_buy+ema)/2 or lc<(ema_buy+ema)/2)):
                            signal = 'Buy'
                        elif(((ema_buy>ll and ema_buy<lh) or ((ll<ema_buy and ll>ema) and (lo>(ema+ema_buy)/2)) or (upper_ema_buy>ll and upper_ema_buy<lh)) and ll>ema):
                            signal = 'Buy'
                    # Buy trade
                    if (signal == 'Buy'):
                        # In between one hour check
                        now = datetime.now()
                        if(now.minute == 0):
                            oneHour_orderId, oneHour_buy_price, is_oneHour_trade_done = check_one_hour_trade()
                            is_pre_order_done = True

                        is_trade_ok = False
                        if(is_volume_filter_pass(df)):
                            is_trade_ok = True
                        ch = lh
                        cl = ll
                        sleep_until_next_15min()
                        df = get_15min_candles()
                        lc = last_close(df)
                        lh = last_high(df)
                        lo = last_open(df)
                        ll = last_low(df)
                        if(is_volume_filter_pass(df)):
                            is_trade_ok = True
                        if(is_trade_ok):
                            if((lc>=ch) and (lh-lc)>0.02):
                                buy_price = lh+0.05
                                # stop limit buy
                                status, order_time = place_stop_market_buy_order(buy_price)
                                if status:
                                    if(status == 'FILLED'):
                                        stoploss = cl
                                        stoploss_set = True
                                        stoploss_orderId = set_profit_1(df,buy_price,stoploss)
                                        if stoploss_orderId:
                                            stoploss_buy_price = buy_price
                                            stoploss_low_price = stoploss
                                        is_15_min_buy_done = True
                                        is_check_for_one_candle_stoploss = True
                                        # print('Buy Signal')
                                        # print(buy_price)
                                    else:
                                        is_buy_waiting_active = True
                                        wh = buy_price
                                        wl = ll
                                        wc = lc
                                        wo = lo
                                        print(f"Buy waiting activated!\nwh:{wh}\nwl:{wl}")
                                    if(is_15min_wait_completed(order_time)):
                                        is_15min_done = True
                            elif(lc>lo and (lh-lc)>0.02):
                                is_one_candle_wait_activated = True
                                print("One candle wait activated!")
                            

                elif(candle == 'Inverted hammer' and candle_Typ == 'Bearish candle' and trend == 'Down_trend' and trade_status == 'ok'):
                    if(ema_buy<ema and ema_buy<ema_100 and emaBuy_status=='ok' and lh<ema_buy):
                        signal = 'Buy'
                    elif(ema_buy>ema and ema_buy>ema_100):
                        if(((ll>lower_ema and ll<=upper_exceed_ema) or ((ema>ll and ema<lh) and (lc>ema and lo>ema))) and (lo<(ema_buy+ema)/2 or lc<(ema_buy+ema)/2)):
                            signal = 'Buy'
                        elif(((ema_buy>ll and ema_buy<lh) or ((ll<ema_buy and ll>ema) and (lo>(ema+ema_buy)/2)) or (upper_ema_buy>ll and upper_ema_buy<lh)) and ll>ema):
                            signal = 'Buy'
                    # Buy trade
                    if (signal == 'Buy'):
                        # In between one hour check
                        now = datetime.now()
                        if(now.minute == 0):
                            oneHour_orderId, oneHour_buy_price, is_oneHour_trade_done = check_one_hour_trade()
                            is_pre_order_done = True

                        is_trade_ok = False
                        if(is_volume_filter_pass(df)):
                            is_trade_ok = True
                        ch = lh
                        cl = ll
                        sleep_until_next_15min()
                        df = get_15min_candles()
                        lc = last_close(df)
                        lh = last_high(df)
                        lo = last_open(df)
                        ll = last_low(df)
                        if(is_volume_filter_pass(df)):
                            is_trade_ok = True
                        if(is_trade_ok):
                            if((lc>=ch) and (lh-lc)>0.02):
                                buy_price = lh+0.05
                                # stop limit buy
                                status, order_time = place_stop_market_buy_order(buy_price)
                                if status:
                                    if(status == 'FILLED'):
                                        stoploss = cl
                                        stoploss_set = True
                                        stoploss_orderId = set_profit_1(df,buy_price,stoploss)
                                        if stoploss_orderId:
                                            stoploss_buy_price = buy_price
                                            stoploss_low_price = stoploss
                                        is_15_min_buy_done = True
                                        is_check_for_one_candle_stoploss = True
                                        # print('Buy Signal')
                                        # print(buy_price)
                                    else:
                                        is_buy_waiting_active = True
                                        wh = buy_price
                                        wl = ll
                                        wc = lc
                                        wo = lo
                                        print(f"Buy waiting activated!\nwh:{wh}\nwl:{wl}")
                                    if(is_15min_wait_completed(order_time)):
                                        is_15min_done = True
                            elif(lc>lo and (lh-lc)>0.02):
                                is_one_candle_wait_activated = True
                                print("One candle wait activated!")
                        # else:
                        #     is_15min_done = True
                            # print('--------------------------------------')
                            # continue
                elif(candle == 'Spinning Top' and candle_Typ == 'Bullish candle' and trend == 'Down_trend' and trade_status == 'ok'):
                    if(ema_buy<ema and ema_buy<ema_100 and emaBuy_status=='ok' and lh<ema_buy):
                        signal = 'Buy'
                    elif(ema_buy>ema and ema_buy>ema_100):
                        if(((ll>lower_ema and ll<=upper_exceed_ema) or ((ema>ll and ema<lh) and (lc>ema and lo>ema))) and (lo<(ema_buy+ema)/2 or lc<(ema_buy+ema)/2)):
                            signal = 'Buy'
                        elif(((ema_buy>ll and ema_buy<lh) or ((ll<ema_buy and ll>ema) and (lc>(ema+ema_buy)/2)) or (upper_ema_buy>ll and upper_ema_buy<lh)) and ll>ema):
                            signal = 'Buy'
                    # Buy trade
                    if (signal == 'Buy' and is_volume_filter_pass(df)):
                        buy_price = (lh+0.05)
                        # Stop limit buy
                        status, order_time = place_stop_market_buy_order(buy_price)
                        if status:
                            if(status == 'FILLED'):
                                stoploss = ll
                                stoploss_set = True
                                stoploss_orderId = set_profit_1(df,buy_price,stoploss)
                                if stoploss_orderId:
                                    stoploss_buy_price = buy_price
                                    stoploss_low_price = stoploss
                                is_15_min_buy_done = True
                                is_check_for_one_candle_stoploss = True
                                # print('Buy Signal')
                                # print(buy_price)
                            else:
                                is_buy_waiting_active = True
                                wh = buy_price
                                wl = ll
                                wc = lc
                                wo = lo
                                print(f"Buy waiting activated!\nwh:{wh}\nwl:{wl}")
                            if(is_15min_wait_completed(order_time)):
                                is_15min_done = True

                elif(candle == 'Spinning Top' and candle_Typ == 'Bearish candle' and trend == 'Down_trend' and trade_status == 'ok'):
                    if(ema_buy<ema and ema_buy<ema_100 and emaBuy_status=='ok' and lh<ema_buy):
                        signal = 'Buy'
                    elif(ema_buy>ema and ema_buy>ema_100):
                        if(((ll>lower_ema and ll<=upper_exceed_ema) or ((ema>ll and ema<lh) and (lc>ema and lo>ema))) and (lo<(ema_buy+ema)/2 or lc<(ema_buy+ema)/2)):
                            signal = 'Buy'
                        elif(((ema_buy>ll and ema_buy<lh) or ((ll<ema_buy and ll>ema) and (lc>(ema+ema_buy)/2)) or (upper_ema_buy>ll and upper_ema_buy<lh)) and ll>ema):
                            signal = 'Buy'
                    # Buy trade
                    if (signal == 'Buy'):
                        # In between one hour check
                        now = datetime.now()
                        if(now.minute == 0):
                            oneHour_orderId, oneHour_buy_price, is_oneHour_trade_done = check_one_hour_trade()
                            is_pre_order_done = True

                        is_trade_ok = False
                        if(is_volume_filter_pass(df)):
                            is_trade_ok = True
                        ch = lh
                        cl = ll
                        sleep_until_next_15min()
                        df = get_15min_candles()
                        lc = last_close(df)
                        lh = last_high(df)
                        lo = last_open(df)
                        ll = last_low(df)
                        if(is_volume_filter_pass(df)):
                            is_trade_ok = True
                        if(is_trade_ok):
                            if((lc>=ch) and (lh-lc)>0.02):
                                buy_price = lh+0.05
                                # stop limit buy
                                status, order_time = place_stop_market_buy_order(buy_price)
                                if status:
                                    if(status == 'FILLED'):
                                        stoploss = cl
                                        stoploss_set = True
                                        stoploss_orderId = set_profit_1(df,buy_price,stoploss)
                                        if stoploss_orderId:
                                            stoploss_buy_price = buy_price
                                            stoploss_low_price = stoploss
                                        is_15_min_buy_done = True
                                        is_check_for_one_candle_stoploss = True
                                        # print('Buy Signal')
                                        # print(buy_price)
                                    else:
                                        is_buy_waiting_active = True
                                        wh = buy_price
                                        wl = ll
                                        wc = lc
                                        wo = lo
                                        print(f"Buy waiting activated!\nwh:{wh}\nwl:{wl}")
                                    if(is_15min_wait_completed(order_time)):
                                        is_15min_done = True
                            elif(lc>lo and (lh-lc)>0.02):
                                is_one_candle_wait_activated = True
                                print("One candle wait activated!")
                        # else:
                        #     is_15min_done = True

                elif(candle == 'Dragonfly doji' and  trend == 'Down_trend' and ll<=pl and (candle_Typ == 'Bullish candle' or candle_Typ == 'Bearish candle' or candle_Typ == 'Doji') and trade_status == 'ok'):
                    if(ema_buy<ema and ema_buy<ema_100 and emaBuy_status=='ok' and lh<ema_buy):
                        signal = 'Buy'
                    elif(ema_buy>ema and ema_buy>ema_100):
                        if(((ll>lower_ema and ll<=upper_exceed_ema) or ((ema>ll and ema<lh) and (lc>ema and lo>ema))) and (lo<(ema_buy+ema)/2 or lc<(ema_buy+ema)/2)):
                            signal = 'Buy'
                        elif(((ema_buy>ll and ema_buy<lh) or ((ll<ema_buy and ll>ema) and (lc>(ema+ema_buy)/2)) or (upper_ema_buy>ll and upper_ema_buy<lh)) and ll>ema):
                            signal = 'Buy'
                    # Buy trade
                    if (signal == 'Buy'):
                        # In between one hour check
                        now = datetime.now()
                        if(now.minute == 0):
                            oneHour_orderId, oneHour_buy_price, is_oneHour_trade_done = check_one_hour_trade()
                            is_pre_order_done = True

                        is_trade_ok = False
                        if(is_volume_filter_pass(df)):
                            is_trade_ok = True
                        ch = lh
                        cl = ll
                        sleep_until_next_15min()
                        df = get_15min_candles()
                        lc = last_close(df)
                        lh = last_high(df)
                        lo = last_open(df)
                        ll = last_low(df)
                        if(is_volume_filter_pass(df)):
                            is_trade_ok = True
                        if(is_trade_ok):
                            if((lc>=ch) and (lh-lc)>0.02):
                                buy_price = lh+0.05
                                # stop limit buy
                                status, order_time = place_stop_market_buy_order(buy_price)
                                if status:
                                    if(status == 'FILLED'):
                                        stoploss = cl
                                        stoploss_set = True
                                        stoploss_orderId = set_profit_1(df,buy_price,stoploss)
                                        if stoploss_orderId:
                                            stoploss_buy_price = buy_price
                                            stoploss_low_price = stoploss
                                        is_15_min_buy_done = True
                                        is_check_for_one_candle_stoploss = True
                                        # print('Buy Signal')
                                        # print(buy_price)
                                    else:
                                        is_buy_waiting_active = True
                                        wh = buy_price
                                        wl = ll
                                        wc = lc
                                        wo = lo
                                        print(f"Buy waiting activated!\nwh:{wh}\nwl:{wl}")
                                    if(is_15min_wait_completed(order_time)):
                                        is_15min_done = True
                            elif(lc>lo and (lh-lc)>0.02):
                                is_one_candle_wait_activated = True
                                print("One candle wait activated!")

                elif(candle == 'Gravestone Doji' and trend == 'Down_trend' and ll<=pl and (candle_Typ == 'Bullish candle' or candle_Typ == 'Bearish candle' or candle_Typ == 'Doji') and trade_status == 'ok'):
                    if(ema_buy<ema and ema_buy<ema_100 and emaBuy_status=='ok' and lh<ema_buy):
                        signal = 'Buy'
                    elif(ema_buy>ema and ema_buy>ema_100):
                        if(((ll>lower_ema and ll<=upper_exceed_ema) or ((ema>ll and ema<lh) and (lc>ema and lo>ema))) and (lo<(ema_buy+ema)/2 or lc<(ema_buy+ema)/2)):
                            signal = 'Buy'
                        elif(((ema_buy>ll and ema_buy<lh) or ((ll<ema_buy and ll>ema) and (lc>(ema+ema_buy)/2)) or (upper_ema_buy>ll and upper_ema_buy<lh)) and ll>ema):
                            signal = 'Buy'
                    # Buy trade
                    if (signal == 'Buy'):
                        # In between one hour check
                        now = datetime.now()
                        if(now.minute == 0):
                            oneHour_orderId, oneHour_buy_price, is_oneHour_trade_done = check_one_hour_trade()
                            is_pre_order_done = True

                        is_trade_ok = False
                        if(is_volume_filter_pass(df)):
                            is_trade_ok = True
                        ch = lh
                        cl = ll
                        sleep_until_next_15min()
                        df = get_15min_candles()
                        lc = last_close(df)
                        lh = last_high(df)
                        lo = last_open(df)
                        ll = last_low(df)
                        if(is_volume_filter_pass(df)):
                            is_trade_ok = True
                        if(is_trade_ok):
                            if((lc>=ch) and (lh-lc)>0.02):
                                buy_price = lh+0.05
                                # stop limit buy
                                status, order_time = place_stop_market_buy_order(buy_price)
                                if status:
                                    if(status == 'FILLED'):
                                        stoploss = cl
                                        stoploss_set = True
                                        stoploss_orderId = set_profit_1(df,buy_price,stoploss)
                                        if stoploss_orderId:
                                            stoploss_buy_price = buy_price
                                            stoploss_low_price = stoploss
                                        is_15_min_buy_done = True
                                        is_check_for_one_candle_stoploss = True
                                        # print('Buy Signal')
                                        # print(buy_price)
                                    else:
                                        is_buy_waiting_active = True
                                        wh = buy_price
                                        wl = ll
                                        wc = lc
                                        wo = lo
                                        print(f"Buy waiting activated!\nwh:{wh}\nwl:{wl}")
                                    if(is_15min_wait_completed(order_time)):
                                        is_15min_done = True
                            elif(lc>lo and (lh-lc)>0.02):
                                is_one_candle_wait_activated = True
                                print("One candle wait activated!")

                elif(candle == 'Simple Doji' and trend == 'Down_trend' and ll<=pl and (candle_Typ == 'Bullish candle' or candle_Typ == 'Bearish candle' or candle_Typ == 'Doji') and trade_status == 'ok'):
                    if(ema_buy<ema and ema_buy<ema_100 and emaBuy_status=='ok' and lh<ema_buy):
                        signal = 'Buy'
                    elif(ema_buy>ema and ema_buy>ema_100):
                        if(((ll>lower_ema and ll<=upper_exceed_ema) or ((ema>ll and ema<lh) and (lc>ema and lo>ema))) and (lo<(ema_buy+ema)/2 or lc<(ema_buy+ema)/2)):
                            signal = 'Buy'
                        elif(((ema_buy>ll and ema_buy<lh) or ((ll<ema_buy and ll>ema) and (lc>(ema+ema_buy)/2)) or (upper_ema_buy>ll and upper_ema_buy<lh)) and ll>ema):
                            signal = 'Buy'
                    # Buy trade
                    if (signal == 'Buy'):
                        # In between one hour check
                        now = datetime.now()
                        if(now.minute == 0):
                            oneHour_orderId, oneHour_buy_price, is_oneHour_trade_done = check_one_hour_trade()
                            is_pre_order_done = True

                        is_trade_ok = False
                        if(is_volume_filter_pass(df)):
                            is_trade_ok = True
                        ch = lh
                        cl = ll
                        sleep_until_next_15min()
                        df = get_15min_candles()
                        lc = last_close(df)
                        lh = last_high(df)
                        lo = last_open(df)
                        ll = last_low(df)
                        if(is_volume_filter_pass(df)):
                            is_trade_ok = True
                        if(is_trade_ok):
                            if((lc>=ch) and (lh-lc)>0.02):
                                buy_price = lh+0.05
                                # stop limit buy
                                status, order_time = place_stop_market_buy_order(buy_price)
                                if status:
                                    if(status == 'FILLED'):
                                        stoploss = cl
                                        stoploss_set = True
                                        stoploss_orderId = set_profit_1(df,buy_price,stoploss)
                                        if stoploss_orderId:
                                            stoploss_buy_price = buy_price
                                            stoploss_low_price = stoploss
                                        is_15_min_buy_done = True
                                        is_check_for_one_candle_stoploss = True
                                        # print('Buy Signal')
                                        # print(buy_price)
                                    else:
                                        is_buy_waiting_active = True
                                        wh = buy_price
                                        wl = ll
                                        wc = lc
                                        wo = lo
                                        print(f"Buy waiting activated!\nwh:{wh}\nwl:{wl}")
                                    if(is_15min_wait_completed(order_time)):
                                        is_15min_done = True
                            elif(lc>lo and (lh-lc)>0.02):
                                is_one_candle_wait_activated = True
                                print("One candle wait activated!")

                elif(candle == 'Reversal' and candle_Typ == 'Bullish candle' and trend == 'Down_trend' and trade_status == 'ok'):
                    if(ema_buy<ema and ema_buy<ema_100 and emaBuy_status=='ok' and lh<ema_buy):
                        signal = 'Buy'
                    elif(ema_buy>ema and ema_buy>ema_100):
                        if((ll>lower_ema and ll<=upper_exceed_ema) and (lo<(ema_buy+ema)/2 or lc<(ema_buy+ema)/2)):
                            signal = 'Buy'
                        elif(((ema_buy>ll and ema_buy<lh) or ((ll<ema_buy and ll>ema) and (lc>(ema+ema_buy)/2)) or (upper_ema_buy>ll and upper_ema_buy<lh)) and ll>ema):
                            signal = 'Buy'
                    # Buy trade
                    if (signal == 'Buy'):
                        buy_price = (lh+0.05)
                        # Stop limit buy
                        status, order_time = place_stop_market_buy_order(buy_price)
                        if status:
                            if(status == 'FILLED'):
                                stoploss = ll
                                stoploss_set = True
                                stoploss_orderId = set_profit_1(df,buy_price,stoploss)
                                if stoploss_orderId:
                                    stoploss_buy_price = buy_price
                                    stoploss_low_price = stoploss
                                is_15_min_buy_done = True
                                is_check_for_one_candle_stoploss = True
                                # print('Buy Signal')
                                # print(buy_price)
                            else:
                                is_buy_waiting_active = True
                                wh = buy_price
                                wl = ll
                                wc = lc
                                wo = lo
                                print(f"Buy waiting activated!\nwh:{wh}\nwl:{wl}")
                            if(is_15min_wait_completed(order_time)):
                                is_15min_done = True

                elif(candle == 'Reversal' and candle_Typ == 'Bearish candle' and trend == 'Down_trend' and trade_status == 'ok'):
                    if(ema_buy<ema and ema_buy<ema_100 and emaBuy_status=='ok' and lh<ema_buy):
                        signal = 'Buy'
                    elif(ema_buy>ema and ema_buy>ema_100):
                        if((ll>lower_ema and ll<=upper_exceed_ema) and (lo<(ema_buy+ema)/2 or lc<(ema_buy+ema)/2)):
                            signal = 'Buy'
                        elif(((ema_buy>ll and ema_buy<lh) or ((ll<ema_buy and ll>ema) and (lo>(ema+ema_buy)/2)) or (upper_ema_buy>ll and upper_ema_buy<lh)) and ll>ema):
                            signal = 'Buy'
                    # Buy trade
                    if (signal == 'Buy'):
                        buy_price = (lo+lc)/2
                        # Stop limit buy
                        status, order_time = place_stop_market_buy_order(buy_price)
                        if status:
                            if(status == 'FILLED'):
                                stoploss = ll
                                stoploss_set = True
                                stoploss_orderId = set_profit_1(df,buy_price,stoploss)
                                if stoploss_orderId:
                                    stoploss_buy_price = buy_price
                                    stoploss_low_price = stoploss
                                is_15_min_buy_done = True
                                is_check_for_one_candle_stoploss = True
                                # print('Buy Signal')
                                # print(buy_price)
                            # else:
                            #     is_buy_waiting_active = True
                            #     wh = lh
                            #     wl = ll
                            #     print(f"Buy waiting activated!\nwh:{wh}\nwl:{wl}")
                            if(is_15min_wait_completed(order_time)):
                                is_15min_done = True

                elif(candle == 'Bullish Marubuzu' and candle_Typ == 'Bullish candle' and trend == 'Down_trend' and trade_status == 'ok'):
                    if(ema_buy<ema and ema_buy<ema_100 and emaBuy_status=='ok' and lh<ema_buy):
                        signal = 'Buy'
                    elif(ema_buy>ema and ema_buy>ema_100):
                        if(((ll>lower_ema and ll<=upper_exceed_ema)) and (lo<(ema_buy+ema)/2 or lc<(ema_buy+ema)/2)):
                            signal = 'Buy'
                        elif(((ema_buy>ll and ema_buy<lh) or ((ll<ema_buy and ll>ema) and (lc>(ema+ema_buy)/2)) or (upper_ema_buy>ll and upper_ema_buy<lh)) and ll>ema):
                            signal = 'Buy'
                    # Buy trade
                    if (signal == 'Buy'):
                        if(lh>ph):
                            buy_price = (lh+0.05)
                            # Stop market buy
                            status, order_time = place_stop_market_buy_order(buy_price)
                            if status:
                                if(status == 'FILLED'):
                                    if(pl<ll):
                                        stoploss = pl
                                        stoploss_set = True
                                    else:
                                        stoploss = ll
                                        stoploss_set = True
                                    # print('Buy Signal')
                                    # print(buy_price)
                                    stoploss_orderId = set_profit_1(df,buy_price,stoploss)
                                    if stoploss_orderId:
                                        stoploss_buy_price = buy_price
                                        stoploss_low_price = stoploss
                                    is_15_min_buy_done = True
                                    is_check_for_one_candle_stoploss = True
                                else:
                                    is_buy_waiting_active = True
                                    wh = buy_price
                                    wl = ll
                                    wc = lc
                                    wo = lo
                                    print(f"Buy waiting activated!\nwh:{wh}\nwl:{wl}")
                                if(is_15min_wait_completed(order_time)):
                                    is_15min_done = True
                        else:
                            buy_price = (ph+0.05)
                            # Stop market buy
                            status, order_time = place_stop_market_buy_order(buy_price)
                            if status:
                                if(status == 'FILLED'):
                                    if(pl<ll):
                                        stoploss = pl
                                        stoploss_set = True
                                    else:
                                        stoploss = ll
                                        stoploss_set = True
                                    # print('Buy Signal')
                                    # print(buy_price)
                                    stoploss_orderId = set_profit_1(df,buy_price,stoploss)
                                    if stoploss_orderId:
                                        stoploss_buy_price = buy_price
                                        stoploss_low_price = stoploss
                                    is_15_min_buy_done = True
                                    is_check_for_one_candle_stoploss = True
                                else:
                                    is_buy_waiting_active = True
                                    wh = buy_price
                                    wl = ll
                                    wc = lc
                                    wo = lo
                                    print(f"Buy waiting activated!\nwh:{wh}\nwl:{wl}")
                                if(is_15min_wait_completed(order_time)):
                                    is_15min_done = True

                # Second Condition
                if(ema_100<ema and trend == 'Down_trend' and ema_100 < ema_buy and 
                    ((ema_100<=lh and ema_100>=ll) or (ll<=((ema+ema_100)/2 -((ema-ema_100)/6)))) and (lc<(ema+ema_100)/2 or lo<(ema+ema_100)/2) and trade_status == 'ok'):
                    #  and lh<ema

                    if(candle == 'Bullish Engulfing' and candle_Typ == 'Bullish candle'):
                        if(lh>ph):
                            buy_price = (lh+0.05)
                            # Stop market buy
                            status, order_time = place_stop_market_buy_order(buy_price)
                            if status:
                                if(status == 'FILLED'):
                                    if(pl<ll):
                                        stoploss = pl
                                        stoploss_set = True
                                    else:
                                        stoploss = ll
                                        stoploss_set = True
                                    # print('Buy Signal')
                                    # print(buy_price)
                                    stoploss_orderId = set_profit_1(df,buy_price,stoploss)
                                    if stoploss_orderId:
                                        stoploss_buy_price = buy_price
                                        stoploss_low_price = stoploss
                                    is_15_min_buy_done = True
                                    is_check_for_one_candle_stoploss = True
                                else:
                                    is_buy_waiting_active = True
                                    wh = buy_price
                                    wl = ll
                                    wc = lc
                                    wo = lo
                                    print(f"Buy waiting activated!\nwh:{wh}\nwl:{wl}")
                                if(is_15min_wait_completed(order_time)):
                                    is_15min_done = True
                        else:
                            buy_price = (ph+0.05)
                            # Stop market buy
                            status, order_time = place_stop_market_buy_order(buy_price)
                            if status:
                                if(status == 'FILLED'):
                                    if(pl<ll):
                                        stoploss = pl
                                        stoploss_set = True
                                    else:
                                        stoploss = ll
                                        stoploss_set = True
                                    # print('Buy Signal')
                                    # print(buy_price)
                                    stoploss_orderId = set_profit_1(df,buy_price,stoploss)
                                    if stoploss_orderId:
                                        stoploss_buy_price = buy_price
                                        stoploss_low_price = stoploss
                                    is_15_min_buy_done = True
                                    is_check_for_one_candle_stoploss = True
                                else:
                                    is_buy_waiting_active = True
                                    wh = buy_price
                                    wl = ll
                                    wc = lc
                                    wo = lo
                                    print(f"Buy waiting activated!\nwh:{wh}\nwl:{wl}")
                                if(is_15min_wait_completed(order_time)):
                                    is_15min_done = True
                    elif(candle == 'Right Hammer' and candle_Typ == 'Bullish candle' and is_volume_filter_pass(df)):
                        if((lh-lc)<0.02):
                            buy_price = lh+(lc-lo)/3
                            # stop limit buy
                            status, order_time = place_stop_market_buy_order(buy_price)
                            if status:
                                if(status == 'FILLED'):
                                    stoploss = ll
                                    stoploss_set = True
                                    stoploss_orderId = set_profit_1(df,buy_price,stoploss)
                                    if stoploss_orderId:
                                        stoploss_buy_price = buy_price
                                        stoploss_low_price = stoploss
                                    is_15_min_buy_done = True
                                    is_check_for_one_candle_stoploss = True
                                    # print('Buy Signal')
                                    # print(buy_price)
                                else:
                                    is_buy_waiting_active = True
                                    wh = buy_price
                                    wl = ll
                                    wc = lc
                                    wo = lo
                                    print(f"Buy waiting activated!\nwh:{wh}\nwl:{wl}")
                                if(is_15min_wait_completed(order_time)):
                                    is_15min_done = True
                        else:
                            buy_price = (lh+0.05)
                            # Stop limit order
                            status, order_time = place_stop_market_buy_order(buy_price)
                            if status:
                                if(status == 'FILLED'):
                                    stoploss = ll
                                    stoploss_set = True
                                    stoploss_orderId = set_profit_1(df,buy_price,stoploss)
                                    if stoploss_orderId:
                                        stoploss_buy_price = buy_price
                                        stoploss_low_price = stoploss
                                    is_15_min_buy_done = True
                                    is_check_for_one_candle_stoploss = True
                                    # print('Buy Signal')
                                    # print(buy_price)
                                else:
                                    is_buy_waiting_active = True
                                    wh = buy_price
                                    wl = ll
                                    wc = lc
                                    wo = lo
                                    print(f"Buy waiting activated!\nwh:{wh}\nwl:{wl}")
                                if(is_15min_wait_completed(order_time)):
                                    is_15min_done = True
                    elif(candle == 'Right Hammer' and candle_Typ == 'Bearish candle'):
                        # In between one hour check
                        now = datetime.now()
                        if(now.minute == 0):
                            oneHour_orderId, oneHour_buy_price, is_oneHour_trade_done = check_one_hour_trade()
                            is_pre_order_done = True

                        is_trade_ok = False
                        if(is_volume_filter_pass(df)):
                            is_trade_ok = True
                        ch = lh
                        cl = ll
                        sleep_until_next_15min()
                        df = get_15min_candles()
                        lc = last_close(df)
                        lh = last_high(df)
                        lo = last_open(df)
                        ll = last_low(df)
                        if(is_volume_filter_pass(df)):
                            is_trade_ok = True
                        if(is_trade_ok):
                            if((lc>=ch) and (lh-lc)>0.02):
                                buy_price = lh+0.05
                                # stop limit buy
                                status, order_time = place_stop_market_buy_order(buy_price)
                                if status:
                                    if(status == 'FILLED'):
                                        stoploss = cl
                                        stoploss_set = True
                                        stoploss_orderId = set_profit_1(df,buy_price,stoploss)
                                        if stoploss_orderId:
                                            stoploss_buy_price = buy_price
                                            stoploss_low_price = stoploss
                                        is_15_min_buy_done = True
                                        is_check_for_one_candle_stoploss = True
                                        # print('Buy Signal')
                                        # print(buy_price)
                                    else:
                                        is_buy_waiting_active = True
                                        wh = buy_price
                                        wl = ll
                                        wc = lc
                                        wo = lo
                                        print(f"Buy waiting activated!\nwh:{wh}\nwl:{wl}")
                                    if(is_15min_wait_completed(order_time)):
                                        is_15min_done = True
                            elif(lc>lo and (lh-lc)>0.02):
                                is_one_candle_wait_activated = True
                                print("One candle wait activated!")
                        # else:
                        #     is_15min_done = True
                            # print('--------------------------------------')
                            # continue
                    elif(candle == 'Inverted hammer' and candle_Typ == 'Bullish candle'):
                        buy_price = (lh+0.05)
                        # Stop limit buy
                        status, order_time = place_stop_market_buy_order(buy_price)
                        if status:
                            if(status == 'FILLED'):
                                stoploss = ll
                                stoploss_set = True
                                stoploss_orderId = set_profit_1(df,buy_price,stoploss)
                                if stoploss_orderId:
                                    stoploss_buy_price = buy_price
                                    stoploss_low_price = stoploss
                                is_15_min_buy_done = True
                                is_check_for_one_candle_stoploss = True
                                # print('Buy Signal')
                                # print(buy_price)
                            else:
                                is_buy_waiting_active = True
                                wh = buy_price
                                wl = ll
                                wc = lc
                                wo = lo
                                print(f"Buy waiting activated!\nwh:{wh}\nwl:{wl}")
                            if(is_15min_wait_completed(order_time)):
                                is_15min_done = True
                    elif(candle == 'Inverted hammer' and candle_Typ == 'Bearish candle'):
                        # In between one hour check
                        now = datetime.now()
                        if(now.minute == 0):
                            oneHour_orderId, oneHour_buy_price, is_oneHour_trade_done = check_one_hour_trade()
                            is_pre_order_done = True

                        is_trade_ok = False
                        if(is_volume_filter_pass(df)):
                            is_trade_ok = True
                        ch = lh
                        cl = ll
                        sleep_until_next_15min()
                        df = get_15min_candles()
                        lc = last_close(df)
                        lh = last_high(df)
                        lo = last_open(df)
                        ll = last_low(df)
                        if(is_volume_filter_pass(df)):
                            is_trade_ok = True
                        if(is_trade_ok):
                            if((lc>=ch) and (lh-lc)>0.02):
                                buy_price = lh+0.05
                                # stop limit buy
                                status, order_time = place_stop_market_buy_order(buy_price)
                                if status:
                                    if(status == 'FILLED'):
                                        stoploss = cl
                                        stoploss_set = True
                                        stoploss_orderId = set_profit_1(df,buy_price,stoploss)
                                        if stoploss_orderId:
                                            stoploss_buy_price = buy_price
                                            stoploss_low_price = stoploss
                                        is_15_min_buy_done = True
                                        is_check_for_one_candle_stoploss = True
                                        # print('Buy Signal')
                                        # print(buy_price)
                                    else:
                                        is_buy_waiting_active = True
                                        wh = buy_price
                                        wl = ll
                                        wc = lc
                                        wo = lo
                                        print(f"Buy waiting activated!\nwh:{wh}\nwl:{wl}")
                                    if(is_15min_wait_completed(order_time)):
                                        is_15min_done = True
                            elif(lc>lo and (lh-lc)>0.02):
                                is_one_candle_wait_activated = True
                                print("One candle wait activated!")
                        # else:
                        #     is_15min_done = True
                            # print('--------------------------------------')
                            # continue
                    elif(candle == 'Spinning Top' and (candle_Typ == 'Bullish candle' or candle_Typ == 'Bearish candle')):
                        # In between one hour check
                        now = datetime.now()
                        if(now.minute == 0):
                            oneHour_orderId, oneHour_buy_price, is_oneHour_trade_done = check_one_hour_trade()
                            is_pre_order_done = True

                        is_trade_ok = False
                        if(is_volume_filter_pass(df)):
                            is_trade_ok = True
                        ch = lh
                        cl = ll
                        sleep_until_next_15min()
                        df = get_15min_candles()
                        lc = last_close(df)
                        lh = last_high(df)
                        lo = last_open(df)
                        ll = last_low(df)
                        if(is_volume_filter_pass(df)):
                            is_trade_ok = True
                        if(is_trade_ok):
                            if((lc>=ch) and (lh-lc)>0.02):
                                buy_price = lh+0.05
                                # stop limit buy
                                status, order_time = place_stop_market_buy_order(buy_price)
                                if status:
                                    if(status == 'FILLED'):
                                        stoploss = cl
                                        stoploss_set = True
                                        stoploss_orderId = set_profit_1(df,buy_price,stoploss)
                                        if stoploss_orderId:
                                            stoploss_buy_price = buy_price
                                            stoploss_low_price = stoploss
                                        is_15_min_buy_done = True
                                        is_check_for_one_candle_stoploss = True
                                        # print('Buy Signal')
                                        # print(buy_price)
                                    else:
                                        is_buy_waiting_active = True
                                        wh = buy_price
                                        wl = ll
                                        wc = lc
                                        wo = lo
                                        print(f"Buy waiting activated!\nwh:{wh}\nwl:{wl}")
                                    if(is_15min_wait_completed(order_time)):
                                        is_15min_done = True
                            elif(lc>lo and (lh-lc)>0.02):
                                is_one_candle_wait_activated = True
                                print("One candle wait activated!")
                        # else:
                        #     is_15min_done = True
                    elif(candle == 'Dragonfly doji' and (candle_Typ == 'Bullish candle' or candle_Typ == 'Bearish candle' or candle_Typ == 'Doji') and ll<=pl):
                        # In between one hour check
                        now = datetime.now()
                        if(now.minute == 0):
                            oneHour_orderId, oneHour_buy_price, is_oneHour_trade_done = check_one_hour_trade()
                            is_pre_order_done = True

                        is_trade_ok = False
                        if(is_volume_filter_pass(df)):
                            is_trade_ok = True
                        ch = lh
                        cl = ll
                        sleep_until_next_15min()
                        df = get_15min_candles()
                        lc = last_close(df)
                        lh = last_high(df)
                        lo = last_open(df)
                        ll = last_low(df)
                        if(is_volume_filter_pass(df)):
                            is_trade_ok = True
                        if(is_trade_ok):
                            if((lc>=ch) and (lh-lc)>0.02):
                                buy_price = lh+0.05
                                # stop limit buy
                                status, order_time = place_stop_market_buy_order(buy_price)
                                if status:
                                    if(status == 'FILLED'):
                                        stoploss = cl
                                        stoploss_set = True
                                        stoploss_orderId = set_profit_1(df,buy_price,stoploss)
                                        if stoploss_orderId:
                                            stoploss_buy_price = buy_price
                                            stoploss_low_price = stoploss
                                        is_15_min_buy_done = True
                                        is_check_for_one_candle_stoploss = True
                                        # print('Buy Signal')
                                        # print(buy_price)
                                    else:
                                        is_buy_waiting_active = True
                                        wh = buy_price
                                        wl = ll
                                        wc = lc
                                        wo = lo
                                        print(f"Buy waiting activated!\nwh:{wh}\nwl:{wl}")
                                    if(is_15min_wait_completed(order_time)):
                                        is_15min_done = True
                            elif(lc>lo and (lh-lc)>0.02):
                                is_one_candle_wait_activated = True
                                print("One candle wait activated!")
                    elif(candle == 'Gravestone Doji' and ll<=pl and (candle_Typ == 'Bullish candle' or candle_Typ == 'Bearish candle' or candle_Typ == 'Doji')):
                        # In between one hour check
                        now = datetime.now()
                        if(now.minute == 0):
                            oneHour_orderId, oneHour_buy_price, is_oneHour_trade_done = check_one_hour_trade()
                            is_pre_order_done = True

                        is_trade_ok = False
                        if(is_volume_filter_pass(df)):
                            is_trade_ok = True
                        ch = lh
                        cl = ll
                        sleep_until_next_15min()
                        df = get_15min_candles()
                        lc = last_close(df)
                        lh = last_high(df)
                        lo = last_open(df)
                        ll = last_low(df)
                        if(is_volume_filter_pass(df)):
                            is_trade_ok = True
                        if(is_trade_ok):
                            if((lc>=ch) and (lh-lc)>0.02):
                                buy_price = lh+0.05
                                # stop limit buy
                                status, order_time = place_stop_market_buy_order(buy_price)
                                if status:
                                    if(status == 'FILLED'):
                                        stoploss = cl
                                        stoploss_set = True
                                        stoploss_orderId = set_profit_1(df,buy_price,stoploss)
                                        if stoploss_orderId:
                                            stoploss_buy_price = buy_price
                                            stoploss_low_price = stoploss
                                        is_15_min_buy_done = True
                                        is_check_for_one_candle_stoploss = True
                                        # print('Buy Signal')
                                        # print(buy_price)
                                    else:
                                        is_buy_waiting_active = True
                                        wh = buy_price
                                        wl = ll
                                        wc = lc
                                        wo = lo
                                        print(f"Buy waiting activated!\nwh:{wh}\nwl:{wl}")
                                    if(is_15min_wait_completed(order_time)):
                                        is_15min_done = True
                            elif(lc>lo and (lh-lc)>0.02):
                                is_one_candle_wait_activated = True
                                print("One candle wait activated!")
                    elif(candle == 'Simple Doji' and ll<=pl and (candle_Typ == 'Bullish candle' or candle_Typ == 'Bearish candle' or candle_Typ == 'Doji')):
                        # In between one hour check
                        now = datetime.now()
                        if(now.minute == 0):
                            oneHour_orderId, oneHour_buy_price, is_oneHour_trade_done = check_one_hour_trade()
                            is_pre_order_done = True

                        is_trade_ok = False
                        if(is_volume_filter_pass(df)):
                            is_trade_ok = True
                        ch = lh
                        cl = ll
                        sleep_until_next_15min()
                        df = get_15min_candles()
                        lc = last_close(df)
                        lh = last_high(df)
                        lo = last_open(df)
                        ll = last_low(df)
                        if(is_volume_filter_pass(df)):
                            is_trade_ok = True
                        if(is_trade_ok):
                            if((lc>=ch) and (lh-lc)>0.02):
                                buy_price = lh+0.05
                                # stop limit buy
                                status, order_time = place_stop_market_buy_order(buy_price)
                                if status:
                                    if(status == 'FILLED'):
                                        stoploss = cl
                                        stoploss_set = True
                                        stoploss_orderId = set_profit_1(df,buy_price,stoploss)
                                        if stoploss_orderId:
                                            stoploss_buy_price = buy_price
                                            stoploss_low_price = stoploss
                                        is_15_min_buy_done = True
                                        is_check_for_one_candle_stoploss = True
                                        # print('Buy Signal')
                                        # print(buy_price)
                                    else:
                                        is_buy_waiting_active = True
                                        wh = buy_price
                                        wl = ll
                                        wc = lc
                                        wo = lo
                                        print(f"Buy waiting activated!\nwh:{wh}\nwl:{wl}")
                                    if(is_15min_wait_completed(order_time)):
                                        is_15min_done = True
                            elif(lc>lo and (lh-lc)>0.02):
                                is_one_candle_wait_activated = True
                                print("One candle wait activated!")
                    elif(candle == 'Reversal' and candle_Typ == 'Bullish candle'):
                        buy_price = (lh+0.05)
                        # Stop limit buy
                        status, order_time = place_stop_market_buy_order(buy_price)
                        if status:
                            if(status == 'FILLED'):
                                stoploss = ll
                                stoploss_set = True
                                stoploss_orderId = set_profit_1(df,buy_price,stoploss)
                                if stoploss_orderId:
                                    stoploss_buy_price = buy_price
                                    stoploss_low_price = stoploss
                                is_15_min_buy_done = True
                                is_check_for_one_candle_stoploss = True
                                # print('Buy Signal')
                                # print(buy_price)
                            else:
                                is_buy_waiting_active = True
                                wh = buy_price
                                wl = ll
                                wc = lc
                                wo = lo
                                print(f"Buy waiting activated!\nwh:{wh}\nwl:{wl}")
                            if(is_15min_wait_completed(order_time)):
                                is_15min_done = True
                    elif(candle == 'Reversal' and candle_Typ == 'Bearish candle'):
                        # buy_price = (lo+lc)/2
                        buy_price = lh + 0.05
                        # Stop limit buy
                        status, order_time = place_stop_market_buy_order(buy_price)
                        if status:
                            if(status == 'FILLED'):
                                stoploss = ll
                                stoploss_set = True
                                stoploss_orderId = set_profit_1(df,buy_price,stoploss)
                                if stoploss_orderId:
                                    stoploss_buy_price = buy_price
                                    stoploss_low_price = stoploss
                                is_15_min_buy_done = True
                                is_check_for_one_candle_stoploss = True
                                # print('Buy Signal')
                                # print(buy_price)
                            # else:
                            #     is_buy_waiting_active = True
                            #     wh = lh
                            #     wl = ll
                            #     print(f"Buy waiting activated!\nwh:{wh}\nwl:{wl}")
                            if(is_15min_wait_completed(order_time)):
                                is_15min_done = True
                    elif(candle == 'Bullish Marubuzu' and candle_Typ == 'Bullish candle'):
                        if(lh>ph):
                            buy_price = (lh+0.05)
                            # Stop market buy
                            status, order_time = place_stop_market_buy_order(buy_price)
                            if status:
                                if(status == 'FILLED'):
                                    if(pl<ll):
                                        stoploss = pl
                                        stoploss_set = True
                                    else:
                                        stoploss = ll
                                        stoploss_set = True
                                    # print('Buy Signal')
                                    # print(buy_price)
                                    stoploss_orderId = set_profit_1(df,buy_price,stoploss)
                                    if stoploss_orderId:
                                        stoploss_buy_price = buy_price
                                        stoploss_low_price = stoploss
                                    is_15_min_buy_done = True
                                    is_check_for_one_candle_stoploss = True
                                else:
                                    is_buy_waiting_active = True
                                    wh = buy_price
                                    wl = ll
                                    wc = lc
                                    wo = lo
                                    print(f"Buy waiting activated!\nwh:{wh}\nwl:{wl}")
                                if(is_15min_wait_completed(order_time)):
                                    is_15min_done = True
                        else:
                            buy_price = (ph+0.05)
                            # Stop market buy
                            status, order_time = place_stop_market_buy_order(buy_price)
                            if status:
                                if(status == 'FILLED'):
                                    if(pl<ll):
                                        stoploss = pl
                                        stoploss_set = True
                                    else:
                                        stoploss = ll
                                        stoploss_set = True
                                    # print('Buy Signal')
                                    # print(buy_price)
                                    stoploss_orderId = set_profit_1(df,buy_price,stoploss)
                                    if stoploss_orderId:
                                        stoploss_buy_price = buy_price
                                        stoploss_low_price = stoploss
                                    is_15_min_buy_done = True
                                    is_check_for_one_candle_stoploss = True
                                else:
                                    is_buy_waiting_active = True
                                    wh = buy_price
                                    wl = ll
                                    wc = lc
                                    wo = lo
                                    print(f"Buy waiting activated!\nwh:{wh}\nwl:{wl}")
                                if(is_15min_wait_completed(order_time)):
                                    is_15min_done = True
                    
                # Exceptional trade
                if(
                    (((((ema_buy-ema)<0.20 and (ema_buy-ema)>=0) or ((ema-ema_buy)<0.20 and (ema-ema_buy)>=0)) and (((ema_buy-ema_100)<0.20 and (ema_buy-ema_100)>=0) or ((ema_100-ema_buy)<0.20 and (ema_100-ema_buy)>=0)) and (((ema_100-ema)<0.20 and (ema_100-ema)>=0) or ((ema-ema_100)<0.20 and (ema-ema_100)>=0)) and 
                    trend == 'Down_trend') or 
                    ((((ema_buy-ema)<0.10 and (ema_buy-ema)>0) or ((ema-ema_buy)<0.10 and (ema-ema_buy)>0)) and (((ema_buy-ema_100)<0.10 and (ema_buy-ema_100)>0) or ((ema_100-ema_buy)<0.10 and (ema_100-ema_buy)>0)) and (((ema_100-ema)<0.10 and (ema_100-ema)>0) or ((ema-ema_100)<0.10 and (ema-ema_100)>0))))
                    and trade_status == 'ok' and ((lc<ema and lc<ema_buy and lc<ema_100) or (lo<ema and lo<ema_buy and lo<ema_100))):
                    print("Exceptional trade 0.20")
                    if(((ema_buy>=ll and ema_buy<=lh) or (ema>=ll and ema<=lh) or (ema_100>=ll and ema_100<=lh)) or (lh<ema and lh<ema_buy and lh<ema_100)):
                        if(candle == 'Bullish Engulfing' and candle_Typ == 'Bullish candle'):
                            if(lh>ph):
                                buy_price = (lh+0.05)
                                # Stop market buy
                                status, order_time = place_stop_market_buy_order(buy_price)
                                if status:
                                    if(status == 'FILLED'):
                                        if(pl<ll):
                                            stoploss = pl
                                            stoploss_set = True
                                        else:
                                            stoploss = ll
                                            stoploss_set = True
                                        # print('Buy Signal')
                                        # print(buy_price)
                                        stoploss_orderId = set_profit_1(df,buy_price,stoploss)
                                        if stoploss_orderId:
                                            stoploss_buy_price = buy_price
                                            stoploss_low_price = stoploss
                                        is_15_min_buy_done = True
                                        is_check_for_one_candle_stoploss = True
                                    else:
                                        is_buy_waiting_active = True
                                        wh = buy_price
                                        wl = ll
                                        wc = lc
                                        wo = lo
                                        print(f"Buy waiting activated!\nwh:{wh}\nwl:{wl}")
                                    if(is_15min_wait_completed(order_time)):
                                        is_15min_done = True
                            else:
                                buy_price = (ph+0.05)
                                # Stop market buy
                                status, order_time = place_stop_market_buy_order(buy_price)
                                if status:
                                    if(status == 'FILLED'):
                                        if(pl<ll):
                                            stoploss = pl
                                            stoploss_set = True
                                        else:
                                            stoploss = ll
                                            stoploss_set = True
                                        # print('Buy Signal')
                                        # print(buy_price)
                                        stoploss_orderId = set_profit_1(df,buy_price,stoploss)
                                        if stoploss_orderId:
                                            stoploss_buy_price = buy_price
                                            stoploss_low_price = stoploss
                                        is_15_min_buy_done = True
                                        is_check_for_one_candle_stoploss = True
                                    else:
                                        is_buy_waiting_active = True
                                        wh = buy_price
                                        wl = ll
                                        wc = lc
                                        wo = lo
                                        print(f"Buy waiting activated!\nwh:{wh}\nwl:{wl}")
                                    if(is_15min_wait_completed(order_time)):
                                        is_15min_done = True
                        elif(candle == 'Right Hammer' and candle_Typ == 'Bullish candle' and is_volume_filter_pass(df)):
                            if((lh-lc)<0.02):
                                buy_price = lh+(lc-lo)/3
                                # stop limit buy
                                status, order_time = place_stop_market_buy_order(buy_price)
                                if status:
                                    if(status == 'FILLED'):
                                        stoploss = ll
                                        stoploss_set = True
                                        stoploss_orderId = set_profit_1(df,buy_price,stoploss)
                                        if stoploss_orderId:
                                            stoploss_buy_price = buy_price
                                            stoploss_low_price = stoploss
                                        is_15_min_buy_done = True
                                        is_check_for_one_candle_stoploss = True
                                        # print('Buy Signal')
                                        # print(buy_price)
                                    else:
                                        is_buy_waiting_active = True
                                        wh = buy_price
                                        wl = ll
                                        wc = lc
                                        wo = lo
                                        print(f"Buy waiting activated!\nwh:{wh}\nwl:{wl}")
                                    if(is_15min_wait_completed(order_time)):
                                        is_15min_done = True
                            else:
                                buy_price = (lh+0.05)
                                # Stop limit order
                                status, order_time = place_stop_market_buy_order(buy_price)
                                if status:
                                    if(status == 'FILLED'):
                                        stoploss = ll
                                        stoploss_set = True
                                        stoploss_orderId = set_profit_1(df,buy_price,stoploss)
                                        if stoploss_orderId:
                                            stoploss_buy_price = buy_price
                                            stoploss_low_price = stoploss
                                        is_15_min_buy_done = True
                                        is_check_for_one_candle_stoploss = True
                                        # print('Buy Signal')
                                        # print(buy_price)
                                    else:
                                        is_buy_waiting_active = True
                                        wh = buy_price
                                        wl = ll
                                        wc = lc
                                        wo = lo
                                        print(f"Buy waiting activated!\nwh:{wh}\nwl:{wl}")
                                    if(is_15min_wait_completed(order_time)):
                                        is_15min_done = True
                        elif(candle == 'Right Hammer' and candle_Typ == 'Bearish candle'):
                            # In between one hour check
                            now = datetime.now()
                            if(now.minute == 0):
                                oneHour_orderId, oneHour_buy_price, is_oneHour_trade_done = check_one_hour_trade()
                                is_pre_order_done = True

                            is_trade_ok = False
                            if(is_volume_filter_pass(df)):
                                is_trade_ok = True
                            ch = lh
                            cl = ll
                            sleep_until_next_15min()
                            df = get_15min_candles()
                            lc = last_close(df)
                            lh = last_high(df)
                            lo = last_open(df)
                            ll = last_low(df)
                            if(is_volume_filter_pass(df)):
                                is_trade_ok = True
                            if(is_trade_ok):
                                if((lc>=ch) and (lh-lc)>0.02):
                                    buy_price = lh+0.05
                                    # stop limit buy
                                    status, order_time = place_stop_market_buy_order(buy_price)
                                    if status:
                                        if(status == 'FILLED'):
                                            stoploss = cl
                                            stoploss_set = True
                                            stoploss_orderId = set_profit_1(df,buy_price,stoploss)
                                            if stoploss_orderId:
                                                stoploss_buy_price = buy_price
                                                stoploss_low_price = stoploss
                                            is_15_min_buy_done = True
                                            is_check_for_one_candle_stoploss = True
                                            # print('Buy Signal')
                                            # print(buy_price)
                                        else:
                                            is_buy_waiting_active = True
                                            wh = buy_price
                                            wl = ll
                                            wc = lc
                                            wo = lo
                                            print(f"Buy waiting activated!\nwh:{wh}\nwl:{wl}")
                                        if(is_15min_wait_completed(order_time)):
                                            is_15min_done = True
                                elif(lc>lo and (lh-lc)>0.02):
                                    is_one_candle_wait_activated = True
                                    print("One candle wait activated!")
                            # else:
                            #     is_15min_done = True
                                # print('--------------------------------------')
                                # continue
                        elif(candle == 'Inverted hammer' and candle_Typ == 'Bullish candle'):
                            buy_price = (lh+0.05)
                            # Stop limit buy
                            status, order_time = place_stop_market_buy_order(buy_price)
                            if status:
                                if(status == 'FILLED'):
                                    stoploss = ll
                                    stoploss_set = True
                                    stoploss_orderId = set_profit_1(df,buy_price,stoploss)
                                    if stoploss_orderId:
                                        stoploss_buy_price = buy_price
                                        stoploss_low_price = stoploss
                                    is_15_min_buy_done = True
                                    is_check_for_one_candle_stoploss = True
                                    # print('Buy Signal')
                                    # print(buy_price)
                                else:
                                    is_buy_waiting_active = True
                                    wh = buy_price
                                    wl = ll
                                    wc = lc
                                    wo = lo
                                    print(f"Buy waiting activated!\nwh:{wh}\nwl:{wl}")
                                if(is_15min_wait_completed(order_time)):
                                    is_15min_done = True
                        elif(candle == 'Inverted hammer' and candle_Typ == 'Bearish candle'):
                            # In between one hour check
                            now = datetime.now()
                            if(now.minute == 0):
                                oneHour_orderId, oneHour_buy_price, is_oneHour_trade_done = check_one_hour_trade()
                                is_pre_order_done = True

                            is_trade_ok = False
                            if(is_volume_filter_pass(df)):
                                is_trade_ok = True
                            ch = lh
                            cl = ll
                            sleep_until_next_15min()
                            df = get_15min_candles()
                            lc = last_close(df)
                            lh = last_high(df)
                            lo = last_open(df)
                            ll = last_low(df)
                            if(is_volume_filter_pass(df)):
                                is_trade_ok = True
                            if(is_trade_ok):
                                if((lc>=ch) and (lh-lc)>0.02):
                                    buy_price = lh+0.05
                                    # stop limit buy
                                    status, order_time = place_stop_market_buy_order(buy_price)
                                    if status:
                                        if(status == 'FILLED'):
                                            stoploss = cl
                                            stoploss_set = True
                                            stoploss_orderId = set_profit_1(df,buy_price,stoploss)
                                            if stoploss_orderId:
                                                stoploss_buy_price = buy_price
                                                stoploss_low_price = stoploss
                                            is_15_min_buy_done = True
                                            is_check_for_one_candle_stoploss = True
                                            # print('Buy Signal')
                                            # print(buy_price)
                                        else:
                                            is_buy_waiting_active = True
                                            wh = buy_price
                                            wl = ll
                                            wc = lc
                                            wo = lo
                                            print(f"Buy waiting activated!\nwh:{wh}\nwl:{wl}")
                                        if(is_15min_wait_completed(order_time)):
                                            is_15min_done = True
                                elif(lc>lo and (lh-lc)>0.02):
                                    is_one_candle_wait_activated = True
                                    print("One candle wait activated!")
                            # else:
                            #     is_15min_done = True
                                # print('--------------------------------------')
                                # continue
                        elif(candle == 'Spinning Top' and (candle_Typ == 'Bullish candle' or candle_Typ == 'Bearish candle')):
                            # In between one hour check
                            now = datetime.now()
                            if(now.minute == 0):
                                oneHour_orderId, oneHour_buy_price, is_oneHour_trade_done = check_one_hour_trade()
                                is_pre_order_done = True

                            is_trade_ok = False
                            if(is_volume_filter_pass(df)):
                                is_trade_ok = True
                            ch = lh
                            cl = ll
                            sleep_until_next_15min()
                            df = get_15min_candles()
                            lc = last_close(df)
                            lh = last_high(df)
                            lo = last_open(df)
                            ll = last_low(df)
                            if(is_volume_filter_pass(df)):
                                is_trade_ok = True
                            if(is_trade_ok):
                                if((lc>=ch) and (lh-lc)>0.02):
                                    buy_price = lh+0.05
                                    # stop limit buy
                                    status, order_time = place_stop_market_buy_order(buy_price)
                                    if status:
                                        if(status == 'FILLED'):
                                            stoploss = cl
                                            stoploss_set = True
                                            stoploss_orderId = set_profit_1(df,buy_price,stoploss)
                                            if stoploss_orderId:
                                                stoploss_buy_price = buy_price
                                                stoploss_low_price = stoploss
                                            is_15_min_buy_done = True
                                            is_check_for_one_candle_stoploss = True
                                            # print('Buy Signal')
                                            # print(buy_price)
                                        else:
                                            is_buy_waiting_active = True
                                            wh = buy_price
                                            wl = ll
                                            wc = lc
                                            wo = lo
                                            print(f"Buy waiting activated!\nwh:{wh}\nwl:{wl}")
                                        if(is_15min_wait_completed(order_time)):
                                            is_15min_done = True
                                elif(lc>lo and (lh-lc)>0.02):
                                    is_one_candle_wait_activated = True
                                    print("One candle wait activated!")
                                # else:
                                #     is_15min_done = True
                        elif(candle == 'Dragonfly doji' and ll<=pl and (candle_Typ == 'Bullish candle' or candle_Typ == 'Bearish candle' or candle_Typ == 'Doji')):
                            # In between one hour check
                            now = datetime.now()
                            if(now.minute == 0):
                                oneHour_orderId, oneHour_buy_price, is_oneHour_trade_done = check_one_hour_trade()
                                is_pre_order_done = True

                            is_trade_ok = False
                            if(is_volume_filter_pass(df)):
                                is_trade_ok = True
                            ch = lh
                            cl = ll
                            sleep_until_next_15min()
                            df = get_15min_candles()
                            lc = last_close(df)
                            lh = last_high(df)
                            lo = last_open(df)
                            ll = last_low(df)
                            if(is_volume_filter_pass(df)):
                                is_trade_ok = True
                            if(is_trade_ok):
                                if((lc>=ch) and (lh-lc)>0.02):
                                    buy_price = lh+0.05
                                    # stop limit buy
                                    status, order_time = place_stop_market_buy_order(buy_price)
                                    if status:
                                        if(status == 'FILLED'):
                                            stoploss = cl
                                            stoploss_set = True
                                            stoploss_orderId = set_profit_1(df,buy_price,stoploss)
                                            if stoploss_orderId:
                                                stoploss_buy_price = buy_price
                                                stoploss_low_price = stoploss
                                            is_15_min_buy_done = True
                                            is_check_for_one_candle_stoploss = True
                                            # print('Buy Signal')
                                            # print(buy_price)
                                        else:
                                            is_buy_waiting_active = True
                                            wh = buy_price
                                            wl = ll
                                            wc = lc
                                            wo = lo
                                            print(f"Buy waiting activated!\nwh:{wh}\nwl:{wl}")
                                        if(is_15min_wait_completed(order_time)):
                                            is_15min_done = True
                                elif(lc>lo and (lh-lc)>0.02):
                                    is_one_candle_wait_activated = True
                                    print("One candle wait activated!")
                        elif(candle == 'Gravestone Doji' and ll<=pl and (candle_Typ == 'Bullish candle' or candle_Typ == 'Bearish candle' or candle_Typ == 'Doji')):
                            # In between one hour check
                            now = datetime.now()
                            if(now.minute == 0):
                                oneHour_orderId, oneHour_buy_price, is_oneHour_trade_done = check_one_hour_trade()
                                is_pre_order_done = True

                            is_trade_ok = False
                            if(is_volume_filter_pass(df)):
                                is_trade_ok = True
                            ch = lh
                            cl = ll
                            sleep_until_next_15min()
                            df = get_15min_candles()
                            lc = last_close(df)
                            lh = last_high(df)
                            lo = last_open(df)
                            ll = last_low(df)
                            if(is_volume_filter_pass(df)):
                                is_trade_ok = True
                            if(is_trade_ok):
                                if((lc>=ch) and (lh-lc)>0.02):
                                    buy_price = lh+0.05
                                    # stop limit buy
                                    status, order_time = place_stop_market_buy_order(buy_price)
                                    if status:
                                        if(status == 'FILLED'):
                                            stoploss = cl
                                            stoploss_set = True
                                            stoploss_orderId = set_profit_1(df,buy_price,stoploss)
                                            if stoploss_orderId:
                                                stoploss_buy_price = buy_price
                                                stoploss_low_price = stoploss
                                            is_15_min_buy_done = True
                                            is_check_for_one_candle_stoploss = True
                                            # print('Buy Signal')
                                            # print(buy_price)
                                        else:
                                            is_buy_waiting_active = True
                                            wh = buy_price
                                            wl = ll
                                            wc = lc
                                            wo = lo
                                            print(f"Buy waiting activated!\nwh:{wh}\nwl:{wl}")
                                        if(is_15min_wait_completed(order_time)):
                                            is_15min_done = True
                                elif(lc>lo and (lh-lc)>0.02):
                                    is_one_candle_wait_activated = True
                                    print("One candle wait activated!")
                        elif(candle == 'Simple Doji' and ll<=pl and (candle_Typ == 'Bullish candle' or candle_Typ == 'Bearish candle' or candle_Typ == 'Doji')):
                            # In between one hour check
                            now = datetime.now()
                            if(now.minute == 0):
                                oneHour_orderId, oneHour_buy_price, is_oneHour_trade_done = check_one_hour_trade()
                                is_pre_order_done = True

                            is_trade_ok = False
                            if(is_volume_filter_pass(df)):
                                is_trade_ok = True
                            ch = lh
                            cl = ll
                            sleep_until_next_15min()
                            df = get_15min_candles()
                            lc = last_close(df)
                            lh = last_high(df)
                            lo = last_open(df)
                            ll = last_low(df)
                            if(is_volume_filter_pass(df)):
                                is_trade_ok = True
                            if(is_trade_ok):
                                if((lc>=ch) and (lh-lc)>0.02):
                                    buy_price = lh+0.05
                                    # stop limit buy
                                    status, order_time = place_stop_market_buy_order(buy_price)
                                    if status:
                                        if(status == 'FILLED'):
                                            stoploss = cl
                                            stoploss_set = True
                                            stoploss_orderId = set_profit_1(df,buy_price,stoploss)
                                            if stoploss_orderId:
                                                stoploss_buy_price = buy_price
                                                stoploss_low_price = stoploss
                                            is_15_min_buy_done = True
                                            is_check_for_one_candle_stoploss = True
                                            # print('Buy Signal')
                                            # print(buy_price)
                                        else:
                                            is_buy_waiting_active = True
                                            wh = buy_price
                                            wl = ll
                                            wc = lc
                                            wo = lo
                                            print(f"Buy waiting activated!\nwh:{wh}\nwl:{wl}")
                                        if(is_15min_wait_completed(order_time)):
                                            is_15min_done = True
                                elif(lc>lo and (lh-lc)>0.02):
                                    is_one_candle_wait_activated = True
                                    print("One candle wait activated!")
                        elif(candle == 'Reversal' and candle_Typ == 'Bullish candle'):
                            buy_price = (lh+0.05)
                            # Stop limit buy
                            status, order_time = place_stop_market_buy_order(buy_price)
                            if status:
                                if(status == 'FILLED'):
                                    stoploss = ll
                                    stoploss_set = True
                                    stoploss_orderId = set_profit_1(df,buy_price,stoploss)
                                    if stoploss_orderId:
                                        stoploss_buy_price = buy_price
                                        stoploss_low_price = stoploss
                                    is_15_min_buy_done = True
                                    is_check_for_one_candle_stoploss = True
                                    # print('Buy Signal')
                                    # print(buy_price)
                                else:
                                    is_buy_waiting_active = True
                                    wh = buy_price
                                    wl = ll
                                    wc = lc
                                    wo = lo
                                    print(f"Buy waiting activated!\nwh:{wh}\nwl:{wl}")
                                if(is_15min_wait_completed(order_time)):
                                    is_15min_done = True
                        elif(candle == 'Reversal' and candle_Typ == 'Bearish candle'):
                            buy_price = (lo+lc)/2
                            # Stop limit buy
                            status, order_time = place_stop_market_buy_order(buy_price)
                            if status:
                                if(status == 'FILLED'):
                                    stoploss = ll
                                    stoploss_set = True
                                    stoploss_orderId = set_profit_1(df,buy_price,stoploss)
                                    if stoploss_orderId:
                                        stoploss_buy_price = buy_price
                                        stoploss_low_price = stoploss
                                    is_15_min_buy_done = True
                                    is_check_for_one_candle_stoploss = True
                                    # print('Buy Signal')
                                    # print(buy_price)
                                # else:
                                #     is_buy_waiting_active = True
                                #     wh = lh
                                #     wl = ll
                                #     print(f"Buy waiting activated!\nwh:{wh}\nwl:{wl}")
                                if(is_15min_wait_completed(order_time)):
                                    is_15min_done = True

                        elif(candle == 'Bullish Marubuzu' and candle_Typ == 'Bullish candle'):
                            if(lh>ph):
                                buy_price = (lh+0.05)
                                # Stop market buy
                                status, order_time = place_stop_market_buy_order(buy_price)
                                if status:
                                    if(status == 'FILLED'):
                                        if(pl<ll):
                                            stoploss = pl
                                            stoploss_set = True
                                        else:
                                            stoploss = ll
                                            stoploss_set = True
                                        # print('Buy Signal')
                                        # print(buy_price)
                                        stoploss_orderId = set_profit_1(df,buy_price,stoploss)
                                        if stoploss_orderId:
                                            stoploss_buy_price = buy_price
                                            stoploss_low_price = stoploss
                                        is_15_min_buy_done = True
                                        is_check_for_one_candle_stoploss = True
                                    else:
                                        is_buy_waiting_active = True
                                        wh = buy_price
                                        wl = ll
                                        wc = lc
                                        wo = lo
                                        print(f"Buy waiting activated!\nwh:{wh}\nwl:{wl}")
                                    if(is_15min_wait_completed(order_time)):
                                        is_15min_done = True
                            else:
                                buy_price = (ph+0.05)
                                # Stop market buy
                                status, order_time = place_stop_market_buy_order(buy_price)
                                if status:
                                    if(status == 'FILLED'):
                                        if(pl<ll):
                                            stoploss = pl
                                            stoploss_set = True
                                        else:
                                            stoploss = ll
                                            stoploss_set = True
                                        # print('Buy Signal')
                                        # print(buy_price)
                                        stoploss_orderId = set_profit_1(df,buy_price,stoploss)
                                        if stoploss_orderId:
                                            stoploss_buy_price = buy_price
                                            stoploss_low_price = stoploss
                                        is_15_min_buy_done = True
                                        is_check_for_one_candle_stoploss = True
                                    else:
                                        is_buy_waiting_active = True
                                        wh = buy_price
                                        wl = ll
                                        wc = lc
                                        wo = lo
                                        print(f"Buy waiting activated!\nwh:{wh}\nwl:{wl}")
                                    if(is_15min_wait_completed(order_time)):
                                        is_15min_done = True
                        
                # EMA exceptional trade
                if((((((ema_100-ema_buy)<0.10 and ((ema_100-ema_buy)>=0)) or (((ema_buy-ema_100)<0.10) and ((ema_buy-ema_100)>=0))) and ema<ema_buy and ema<ema_100 and ((ema<=lh and ema>=ll) or lh<ema)) or 
                    (((((ema-ema_buy)<0.10 and ((ema-ema_buy)>=0)) or ((ema_buy-ema)<0.10 and ((ema_buy-ema)>=0)))) and ema_100>ema and ema_100>ema_buy and lh<ema_100)) and 
                    trade_status == 'ok' and trend == 'Down_trend'):
                    if(candle == 'Bullish Engulfing' and candle_Typ == 'Bullish candle'):
                        if(lh>ph):
                            buy_price = (lh+0.05)
                            # Stop market buy
                            if (now.minute == 0 or now.minute == 30) and is_30_min_allow_buy():
                                status, order_time = place_stop_market_buy_order(buy_price)
                                if status:
                                    if(status == 'FILLED'):
                                        if(pl<ll):
                                            stoploss = pl
                                            stoploss_set = True
                                        else:
                                            stoploss = ll
                                            stoploss_set = True
                                        # print('Buy Signal')
                                        # print(buy_price)
                                        stoploss_orderId = set_profit_1(df,buy_price,stoploss)
                                        if stoploss_orderId:
                                            stoploss_buy_price = buy_price
                                            stoploss_low_price = stoploss
                                        is_15_min_buy_done = True
                                        is_check_for_one_candle_stoploss = True
                                    else:
                                        is_buy_waiting_active = True
                                        wh = buy_price
                                        wl = ll
                                        wc = lc
                                        wo = lo
                                        print(f"Buy waiting activated!\nwh:{wh}\nwl:{wl}")
                                    if(is_15min_wait_completed(order_time)):
                                        is_15min_done = True
                            else:
                                is_check_for_30_min = True
                                check_30_min_buy_price = buy_price
                                if(pl<ll):
                                    check_30_min_stoploss = pl
                                else:
                                    check_30_min_stoploss = ll
                        else:
                            buy_price = (ph+0.05)
                            # Stop market buy
                            if (now.minute == 0 or now.minute == 30) and is_30_min_allow_buy():
                                status, order_time = place_stop_market_buy_order(buy_price)
                                if status:
                                    if(status == 'FILLED'):
                                        if(pl<ll):
                                            stoploss = pl
                                            stoploss_set = True
                                        else:
                                            stoploss = ll
                                            stoploss_set = True
                                        # print('Buy Signal')
                                        # print(buy_price)
                                        stoploss_orderId = set_profit_1(df,buy_price,stoploss)
                                        if stoploss_orderId:
                                            stoploss_buy_price = buy_price
                                            stoploss_low_price = stoploss
                                        is_15_min_buy_done = True
                                        is_check_for_one_candle_stoploss = True
                                    else:
                                        is_buy_waiting_active = True
                                        wh = buy_price
                                        wl = ll
                                        wc = lc
                                        wo = lo
                                        print(f"Buy waiting activated!\nwh:{wh}\nwl:{wl}")
                                    if(is_15min_wait_completed(order_time)):
                                        is_15min_done = True
                            else:
                                is_check_for_30_min = True
                                check_30_min_buy_price = buy_price
                                if(pl<ll):
                                    check_30_min_stoploss = pl
                                else:
                                    check_30_min_stoploss = ll

                    elif(candle == 'Right Hammer' and candle_Typ == 'Bullish candle' and is_volume_filter_pass(df)):
                        if((lh-lc)<0.02):
                            buy_price = lh+(lc-lo)/3
                            # stop limit buy
                            status, order_time = place_stop_market_buy_order(buy_price)
                            if status:
                                if(status == 'FILLED'):
                                    stoploss = ll
                                    stoploss_set = True
                                    # print('Buy Signal')
                                    # print(buy_price)
                                    stoploss_orderId = set_profit_1(df,buy_price,stoploss)
                                    if stoploss_orderId:
                                        stoploss_buy_price = buy_price
                                        stoploss_low_price = stoploss
                                    is_15_min_buy_done = True
                                    is_check_for_one_candle_stoploss = True
                                else:
                                    is_buy_waiting_active = True
                                    wh = buy_price
                                    wl = ll
                                    wc = lc
                                    wo = lo
                                    print(f"Buy waiting activated!\nwh:{wh}\nwl:{wl}")
                                if(is_15min_wait_completed(order_time)):
                                    is_15min_done = True
                        else:
                            buy_price = (lh+0.05)
                            # Stop limit order
                            status, order_time = place_stop_market_buy_order(buy_price)
                            if status:
                                if(status == 'FILLED'):
                                    stoploss = ll
                                    stoploss_set = True
                                    # print('Buy Signal')
                                    # print(buy_price)
                                    stoploss_orderId = set_profit_1(df,buy_price,stoploss)
                                    if stoploss_orderId:
                                        stoploss_buy_price = buy_price
                                        stoploss_low_price = stoploss
                                    is_15_min_buy_done = True
                                    is_check_for_one_candle_stoploss = True
                                else:
                                    is_buy_waiting_active = True
                                    wh = buy_price
                                    wl = ll
                                    wc = lc
                                    wo = lo
                                    print(f"Buy waiting activated!\nwh:{wh}\nwl:{wl}")
                                if(is_15min_wait_completed(order_time)):
                                    is_15min_done = True
                    elif(candle == 'Right Hammer' and candle_Typ == 'Bearish candle'):
                        # In between one hour check
                        now = datetime.now()
                        if(now.minute == 0):
                            oneHour_orderId, oneHour_buy_price, is_oneHour_trade_done = check_one_hour_trade()
                            is_pre_order_done = True

                        is_trade_ok = False
                        if(is_volume_filter_pass(df)):
                            is_trade_ok = True
                        ch = lh
                        cl = ll
                        sleep_until_next_15min()
                        df = get_15min_candles()
                        lc = last_close(df)
                        lh = last_high(df)
                        lo = last_open(df)
                        ll = last_low(df)
                        if(is_volume_filter_pass(df)):
                            is_trade_ok = True
                        if(is_trade_ok):
                            if((lc>=ch) and (lh-lc)>0.02):
                                buy_price = lh+0.05
                                # stop limit buy
                                status, order_time = place_stop_market_buy_order(buy_price)
                                if status:
                                    if(status == 'FILLED'):
                                        stoploss = cl
                                        stoploss_set = True
                                        stoploss_orderId = set_profit_1(df,buy_price,stoploss)
                                        if stoploss_orderId:
                                            stoploss_buy_price = buy_price
                                            stoploss_low_price = stoploss
                                        is_15_min_buy_done = True
                                        is_check_for_one_candle_stoploss = True
                                        # print('Buy Signal')
                                        # print(buy_price)
                                    else:
                                        is_buy_waiting_active = True
                                        wh = buy_price
                                        wl = ll
                                        wc = lc
                                        wo = lo
                                        print(f"Buy waiting activated!\nwh:{wh}\nwl:{wl}")
                                    if(is_15min_wait_completed(order_time)):
                                        is_15min_done = True
                            elif(lc>lo and (lh-lc)>0.02):
                                is_one_candle_wait_activated = True
                                print("One candle wait activated!")
                        # else:
                        #     is_15min_done = True
                            # print('--------------------------------------')
                            # continue
                    elif(candle == 'Inverted hammer' and candle_Typ == 'Bullish candle'):
                        buy_price = (lh+0.05)
                        # Stop limit buy
                        status, order_time = place_stop_market_buy_order(buy_price)
                        if status:
                            if(status == 'FILLED'):
                                stoploss = ll
                                stoploss_set = True
                                # print('Buy Signal')
                                # print(buy_price)
                                stoploss_orderId = set_profit_1(df,buy_price,stoploss)
                                if stoploss_orderId:
                                    stoploss_buy_price = buy_price
                                    stoploss_low_price = stoploss
                                is_15_min_buy_done = True
                                is_check_for_one_candle_stoploss = True
                            else:
                                is_buy_waiting_active = True
                                wh = buy_price
                                wl = ll
                                wc = lc
                                wo = lo
                                print(f"Buy waiting activated!\nwh:{wh}\nwl:{wl}")
                            if(is_15min_wait_completed(order_time)):
                                is_15min_done = True
                    elif(candle == 'Inverted hammer' and candle_Typ == 'Bearish candle'):
                        # In between one hour check
                        now = datetime.now()
                        if(now.minute == 0):
                            oneHour_orderId, oneHour_buy_price, is_oneHour_trade_done = check_one_hour_trade()
                            is_pre_order_done = True

                        is_trade_ok = False
                        if(is_volume_filter_pass(df)):
                            is_trade_ok = True
                        ch = lh
                        cl = ll
                        sleep_until_next_15min()
                        df = get_15min_candles()
                        lc = last_close(df)
                        lh = last_high(df)
                        lo = last_open(df)
                        ll = last_low(df)
                        if(is_volume_filter_pass(df)):
                            is_trade_ok = True
                        if(is_trade_ok):
                            if((lc>=ch) and (lh-lc)>0.02):
                                buy_price = lh+0.05
                                # stop limit buy
                                status, order_time = place_stop_market_buy_order(buy_price)
                                if status:
                                    if(status == 'FILLED'):
                                        stoploss = cl
                                        stoploss_set = True
                                        stoploss_orderId = set_profit_1(df,buy_price,stoploss)
                                        if stoploss_orderId:
                                            stoploss_buy_price = buy_price
                                            stoploss_low_price = stoploss
                                        is_15_min_buy_done = True
                                        is_check_for_one_candle_stoploss = True
                                        # print('Buy Signal')
                                        # print(buy_price)
                                    else:
                                        is_buy_waiting_active = True
                                        wh = buy_price
                                        wl = ll
                                        wc = lc
                                        wo = lo
                                        print(f"Buy waiting activated!\nwh:{wh}\nwl:{wl}")
                                    if(is_15min_wait_completed(order_time)):
                                        is_15min_done = True
                            elif(lc>lo and (lh-lc)>0.02):
                                is_one_candle_wait_activated = True
                                print("One candle wait activated!")
                        # else:
                        #     is_15min_done = True
                            # print('--------------------------------------')
                            # continue
                    elif(candle == 'Spinning Top' and (candle_Typ == 'Bullish candle' or candle_Typ == 'Bearish candle')):
                        # In between one hour check
                        now = datetime.now()
                        if(now.minute == 0):
                            oneHour_orderId, oneHour_buy_price, is_oneHour_trade_done = check_one_hour_trade()
                            is_pre_order_done = True

                        is_trade_ok = False
                        if(is_volume_filter_pass(df)):
                            is_trade_ok = True
                        ch = lh
                        cl = ll
                        sleep_until_next_15min()
                        df = get_15min_candles()
                        lc = last_close(df)
                        lh = last_high(df)
                        lo = last_open(df)
                        ll = last_low(df)
                        if(is_volume_filter_pass(df)):
                            is_trade_ok = True
                        if(is_trade_ok):
                            if((lc>=ch) and (lh-lc)>0.02):
                                buy_price = lh+0.05
                                # stop limit buy
                                status, order_time = place_stop_market_buy_order(buy_price)
                                if status:
                                    if(status == 'FILLED'):
                                        stoploss = cl
                                        stoploss_set = True
                                        stoploss_orderId = set_profit_1(df,buy_price,stoploss)
                                        if stoploss_orderId:
                                            stoploss_buy_price = buy_price
                                            stoploss_low_price = stoploss
                                        is_15_min_buy_done = True
                                        is_check_for_one_candle_stoploss = True
                                        # print('Buy Signal')
                                        # print(buy_price)
                                    else:
                                        is_buy_waiting_active = True
                                        wh = buy_price
                                        wl = ll
                                        wc = lc
                                        wo = lo
                                        print(f"Buy waiting activated!\nwh:{wh}\nwl:{wl}")
                                    if(is_15min_wait_completed(order_time)):
                                        is_15min_done = True
                            elif(lc>lo and (lh-lc)>0.02):
                                is_one_candle_wait_activated = True
                                print("One candle wait activated!")
                        # else:
                        #     is_15min_done = True
                    elif(candle == 'Dragonfly doji' and (candle_Typ == 'Bullish candle' or candle_Typ == 'Bearish candle' or candle_Typ == 'Doji') and ll<=pl):
                        # In between one hour check
                        now = datetime.now()
                        if(now.minute == 0):
                            oneHour_orderId, oneHour_buy_price, is_oneHour_trade_done = check_one_hour_trade()
                            is_pre_order_done = True

                        is_trade_ok = False
                        if(is_volume_filter_pass(df)):
                            is_trade_ok = True
                        ch = lh
                        cl = ll
                        sleep_until_next_15min()
                        df = get_15min_candles()
                        lc = last_close(df)
                        lh = last_high(df)
                        lo = last_open(df)
                        ll = last_low(df)
                        if(is_volume_filter_pass(df)):
                            is_trade_ok = True
                        if(is_trade_ok):
                            if((lc>=ch) and (lh-lc)>0.02):
                                buy_price = lh+0.05
                                # stop limit buy
                                status, order_time = place_stop_market_buy_order(buy_price)
                                if status:
                                    if(status == 'FILLED'):
                                        stoploss = cl
                                        stoploss_set = True
                                        stoploss_orderId = set_profit_1(df,buy_price,stoploss)
                                        if stoploss_orderId:
                                            stoploss_buy_price = buy_price
                                            stoploss_low_price = stoploss
                                        is_15_min_buy_done = True
                                        is_check_for_one_candle_stoploss = True
                                        # print('Buy Signal')
                                        # print(buy_price)
                                    else:
                                        is_buy_waiting_active = True
                                        wh = buy_price
                                        wl = ll
                                        wc = lc
                                        wo = lo
                                        print(f"Buy waiting activated!\nwh:{wh}\nwl:{wl}")
                                    if(is_15min_wait_completed(order_time)):
                                        is_15min_done = True
                            elif(lc>lo and (lh-lc)>0.02):
                                is_one_candle_wait_activated = True
                                print("One candle wait activated!")
                    elif(candle == 'Gravestone Doji' and ll<=pl and (candle_Typ == 'Bullish candle' or candle_Typ == 'Bearish candle' or candle_Typ == 'Doji')):
                        # In between one hour check
                        now = datetime.now()
                        if(now.minute == 0):
                            oneHour_orderId, oneHour_buy_price, is_oneHour_trade_done = check_one_hour_trade()
                            is_pre_order_done = True

                        is_trade_ok = False
                        if(is_volume_filter_pass(df)):
                            is_trade_ok = True
                        ch = lh
                        cl = ll
                        sleep_until_next_15min()
                        df = get_15min_candles()
                        lc = last_close(df)
                        lh = last_high(df)
                        lo = last_open(df)
                        ll = last_low(df)
                        if(is_volume_filter_pass(df)):
                            is_trade_ok = True
                        if(is_trade_ok):
                            if((lc>=ch) and (lh-lc)>0.02):
                                buy_price = lh+0.05
                                # stop limit buy
                                status, order_time = place_stop_market_buy_order(buy_price)
                                if status:
                                    if(status == 'FILLED'):
                                        stoploss = cl
                                        stoploss_set = True
                                        stoploss_orderId = set_profit_1(df,buy_price,stoploss)
                                        if stoploss_orderId:
                                            stoploss_buy_price = buy_price
                                            stoploss_low_price = stoploss
                                        is_15_min_buy_done = True
                                        is_check_for_one_candle_stoploss = True
                                        # print('Buy Signal')
                                        # print(buy_price)
                                    else:
                                        is_buy_waiting_active = True
                                        wh = buy_price
                                        wl = ll
                                        wc = lc
                                        wo = lo
                                        print(f"Buy waiting activated!\nwh:{wh}\nwl:{wl}")
                                    if(is_15min_wait_completed(order_time)):
                                        is_15min_done = True
                            elif(lc>lo and (lh-lc)>0.02):
                                is_one_candle_wait_activated = True
                                print("One candle wait activated!")
                    elif(candle == 'Simple Doji' and ll<=pl and (candle_Typ == 'Bullish candle' or candle_Typ == 'Bearish candle' or candle_Typ == 'Doji')):
                        # In between one hour check
                        now = datetime.now()
                        if(now.minute == 0):
                            oneHour_orderId, oneHour_buy_price, is_oneHour_trade_done = check_one_hour_trade()
                            is_pre_order_done = True

                        is_trade_ok = False
                        if(is_volume_filter_pass(df)):
                            is_trade_ok = True
                        ch = lh
                        cl = ll
                        sleep_until_next_15min()
                        df = get_15min_candles()
                        lc = last_close(df)
                        lh = last_high(df)
                        lo = last_open(df)
                        ll = last_low(df)
                        if(is_volume_filter_pass(df)):
                            is_trade_ok = True
                        if(is_trade_ok):
                            if((lc>=ch) and (lh-lc)>0.02):
                                buy_price = lh+0.05
                                # stop limit buy
                                status, order_time = place_stop_market_buy_order(buy_price)
                                if status:
                                    if(status == 'FILLED'):
                                        stoploss = cl
                                        stoploss_set = True
                                        stoploss_orderId = set_profit_1(df,buy_price,stoploss)
                                        if stoploss_orderId:
                                            stoploss_buy_price = buy_price
                                            stoploss_low_price = stoploss
                                        is_15_min_buy_done = True
                                        is_check_for_one_candle_stoploss = True
                                        # print('Buy Signal')
                                        # print(buy_price)
                                    else:
                                        is_buy_waiting_active = True
                                        wh = buy_price
                                        wl = ll
                                        wc = lc
                                        wo = lo
                                        print(f"Buy waiting activated!\nwh:{wh}\nwl:{wl}")
                                    if(is_15min_wait_completed(order_time)):
                                        is_15min_done = True
                            elif(lc>lo and (lh-lc)>0.02):
                                is_one_candle_wait_activated = True
                                print("One candle wait activated!")
                    elif(candle == 'Reversal' and candle_Typ == 'Bullish candle'):
                        buy_price = (lh+0.05)
                        # Stop limit buy
                        if (now.minute == 0 or now.minute == 30) and is_30_min_allow_buy():
                            status, order_time = place_stop_market_buy_order(buy_price)
                            if status:
                                if(status == 'FILLED'):
                                    stoploss = ll
                                    stoploss_set = True
                                    stoploss_orderId = set_profit_1(df,buy_price,stoploss)
                                    if stoploss_orderId:
                                        stoploss_buy_price = buy_price
                                        stoploss_low_price = stoploss
                                    is_15_min_buy_done = True
                                    is_check_for_one_candle_stoploss = True
                                    # print('Buy Signal')
                                    # print(buy_price)
                                else:
                                    is_buy_waiting_active = True
                                    wh = buy_price
                                    wl = ll
                                    wc = lc
                                    wo = lo
                                    print(f"Buy waiting activated!\nwh:{wh}\nwl:{wl}")
                                if(is_15min_wait_completed(order_time)):
                                    is_15min_done = True
                        else:
                            is_check_for_30_min = True
                            check_30_min_buy_price = buy_price
                            check_30_min_stoploss = ll
                    elif(candle == 'Reversal' and candle_Typ == 'Bearish candle'):
                        buy_price = (lo+lc)/2
                        # Stop limit buy
                        if (now.minute == 0 or now.minute == 30) and is_30_min_allow_buy():
                            status, order_time = place_stop_market_buy_order(buy_price)
                            if status:
                                if(status == 'FILLED'):
                                    stoploss = ll
                                    stoploss_set = True
                                    stoploss_orderId = set_profit_1(df,buy_price,stoploss)
                                    if stoploss_orderId:
                                        stoploss_buy_price = buy_price
                                        stoploss_low_price = stoploss
                                    is_15_min_buy_done = True
                                    is_check_for_one_candle_stoploss = True
                                    # print('Buy Signal')
                                    # print(buy_price)
                                # else:
                                #     is_buy_waiting_active = True
                                #     wh = lh
                                #     wl = ll
                                #     print(f"Buy waiting activated!\nwh:{wh}\nwl:{wl}")
                                if(is_15min_wait_completed(order_time)):
                                    is_15min_done = True
                        else:
                            is_check_for_30_min = True
                            check_30_min_buy_price = buy_price
                            check_30_min_stoploss = ll
                    elif(candle == 'Bullish Marubuzu' and candle_Typ == 'Bullish candle'):
                        if(lh>ph):
                            buy_price = (lh+0.05)
                            # Stop market buy
                            if (now.minute == 0 or now.minute == 30) and is_30_min_allow_buy():
                                status, order_time = place_stop_market_buy_order(buy_price)
                                if status:
                                    if(status == 'FILLED'):
                                        if(pl<ll):
                                            stoploss = pl
                                            stoploss_set = True
                                        else:
                                            stoploss = ll
                                            stoploss_set = True
                                        # print('Buy Signal')
                                        # print(buy_price)
                                        stoploss_orderId = set_profit_1(df,buy_price,stoploss)
                                        if stoploss_orderId:
                                            stoploss_buy_price = buy_price
                                            stoploss_low_price = stoploss
                                        is_15_min_buy_done = True
                                        is_check_for_one_candle_stoploss = True
                                    else:
                                        is_buy_waiting_active = True
                                        wh = buy_price
                                        wl = ll
                                        wc = lc
                                        wo = lo
                                        print(f"Buy waiting activated!\nwh:{wh}\nwl:{wl}")
                                    if(is_15min_wait_completed(order_time)):
                                        is_15min_done = True
                            else:
                                is_check_for_30_min = True
                                check_30_min_buy_price = buy_price
                                if(pl<ll):
                                    check_30_min_stoploss = pl
                                else:
                                    check_30_min_stoploss = ll
                        else:
                            buy_price = (ph+0.05)
                            # Stop market buy
                            if (now.minute == 0 or now.minute == 30) and is_30_min_allow_buy():
                                status, order_time = place_stop_market_buy_order(buy_price)
                                if status:
                                    if(status == 'FILLED'):
                                        if(pl<ll):
                                            stoploss = pl
                                            stoploss_set = True
                                        else:
                                            stoploss = ll
                                            stoploss_set = True
                                        # print('Buy Signal')
                                        # print(buy_price)
                                        stoploss_orderId = set_profit_1(df,buy_price,stoploss)
                                        if stoploss_orderId:
                                            stoploss_buy_price = buy_price
                                            stoploss_low_price = stoploss
                                        is_15_min_buy_done = True
                                        is_check_for_one_candle_stoploss = True
                                    else:
                                        is_buy_waiting_active = True
                                        wh = buy_price
                                        wl = ll
                                        wc = lc
                                        wo = lo
                                        print(f"Buy waiting activated!\nwh:{wh}\nwl:{wl}")
                                    if(is_15min_wait_completed(order_time)):
                                        is_15min_done = True
                            else:
                                is_check_for_30_min = True
                                check_30_min_buy_price = buy_price
                                if(pl<ll):
                                    check_30_min_stoploss = pl
                                else:
                                    check_30_min_stoploss = ll
                    
        # Percentage down trade
        if(down_percentage>2.5 and candle_Typ == 'Bullish candle' and trade_status == 'ok' and candle == None):
            buy_price = lh+((lc-lo)/4)
            # Stop limit buy
            status, order_time = place_stop_market_buy_order(buy_price)
            if status:
                if(status == 'FILLED'):
                    stoploss = ll
                    stoploss_set = True
                    # print('Buy Signal')
                    # print(buy_price)
                    stoploss_orderId = set_profit_1(df,buy_price,stoploss)
                    if stoploss_orderId:
                        stoploss_buy_price = buy_price
                        stoploss_low_price = stoploss
                    is_15_min_buy_done = True
                    is_check_for_one_candle_stoploss = True
                if(is_15min_wait_completed(order_time)):
                    is_15min_done = True

        if(lc>lo and pc<po and pc2<po2 and lc>po and lc>po2 and lh>ph and lh>ph2 and (pl2>pl or pl2>ll)):
            print("Double Bullish Engulfing")
            if(is_volume_filter_pass(df)):
                buy_price = lh + 0.05
                status, order_time = place_stop_market_buy_order(buy_price)
                if status:
                    if(status == 'FILLED'):
                        stoploss = ll
                        stoploss_set = True
                        stoploss_orderId = place_stoploss_sell_order(stoploss, 1)
                        if stoploss_orderId:
                            stoploss_buy_price = buy_price
                            stoploss_low_price = stoploss
                        is_15_min_buy_done = True
                        is_check_for_one_candle_stoploss = True
                    if(is_15min_wait_completed(order_time)):
                        is_15min_done = True

# -------------------------------------------------------------------------------------------------------------------

        # For Selling
        if(is_shift_towards_30_min == False):
            if(candle == 'Bearish Engulfing' and candle_Typ == 'Bearish candle' and trend == 'Up_trend'):
                if(ema_buy>ema and ll>ema_buy):
                    signal = 'Sell'
                elif(ema_buy<ema):
                    if(((lh<upper_ema and lh>=lower_exceed_ema)) and (lo>(ema_buy+ema)/2 or lc>(ema_buy+ema)/2)):
                        signal = 'Sell'
                    elif(((ema_buy>ll and ema_buy<lh) or ((lh>ema_buy and lh<ema) and (lo<(ema_buy+ema)/2 or lc<(ema_buy+ema)/2)) or (lower_ema_buy>ll and lower_ema_buy<lh)) and lh<ema):
                        signal = 'Sell'
                # Sell trade
                if (signal == 'Sell'):
                    if(ll<pl):
                        sell_price = ll-0.05
                        # Stop limit sell
                        # if(is_sol_available()):
                        status, order_time = place_stop_market_sell_order(sell_price)
                        if(status == 'FILLED'):
                            stoploss = 0
                            # print('Sell Signal')
                            # print(sell_price)
                        else:
                            stoploss = ll-0.05
                        if(is_15min_wait_completed(order_time)):
                            is_15min_done = True
                    else:
                        sell_price = pl-0.05
                        # Stop limit sell
                        # if(is_sol_available()):
                        status, order_time = place_stop_market_sell_order(sell_price)
                        if(status == 'FILLED'):
                            stoploss = 0
                            # print('Sell Signal')
                            # print(sell_price)
                        else:
                            stoploss = pl-0.05
                        if(is_15min_wait_completed(order_time)):
                            is_15min_done = True
                                
            elif(candle == 'Right Hammer' and candle_Typ == 'Bullish candle' and trend == 'Up_trend'):
                if(ema_buy>ema and ll>ema_buy):
                    signal = 'Sell'
                elif(ema_buy<ema):
                    if((lh<upper_ema and lh>=lower_exceed_ema) and (lo>(ema_buy+ema)/2 or lc>(ema_buy+ema)/2)):
                        signal = 'Sell'
                    elif(((ema_buy>ll and ema_buy<lh) or ((lh>ema_buy and lh<ema) and (lo<(ema_buy+ema)/2 or lc<(ema_buy+ema)/2)) or (lower_ema_buy>ll and lower_ema_buy<lh)) and lh<ema):
                        signal = 'Sell'
                # Sell trade
                if (signal == 'Sell'):
                    # In between one hour check
                    now = datetime.now()
                    if(now.minute == 0):
                        oneHour_orderId, oneHour_buy_price, is_oneHour_trade_done = check_one_hour_trade()
                        is_pre_order_done = True

                    cl = ll
                    ch = lh
                    sleep_until_next_15min()
                    df = get_15min_candles()
                    lc = last_close(df)
                    lo = last_open(df)
                    lh = last_high(df)
                    ll = last_low(df)
                    if((lc<=cl) and (lc-ll)>0.02):
                        sell_price = ll-0.05
                        # stop limit sell
                        # if(is_sol_available()):
                        status, order_time = place_stop_market_sell_order(sell_price)
                        if(status == 'FILLED'):
                            stoploss = 0
                            # print('Sell Signal')
                            # print(sell_price)
                        else:
                            stoploss = ll-0.05
                        if(is_15min_wait_completed(order_time)):
                            is_15min_done = True
                    elif(lc<lo):
                        if(ll<cl and ((lh-ll)<(ch-cl)*1.5)):
                            stoploss = ll
                        else:
                            stoploss = cl
                        is_15min_done = True
                    else:
                        stoploss = cl
                        is_15min_done = True
                        
            elif(candle == 'Inverted hammer' and candle_Typ == 'Bullish candle' and trend == 'Up_trend'):
                if(ema_buy>ema and ll>ema_buy):
                    signal = 'Sell'
                elif(ema_buy<ema):
                    if((lh<upper_ema and lh>=lower_exceed_ema) and (lo>(ema_buy+ema)/2 or lc>(ema_buy+ema)/2)):
                        signal = 'Sell'
                    elif(((ema_buy>ll and ema_buy<lh) or ((lh>ema_buy and lh<ema) and (lo<(ema_buy+ema)/2 or lc<(ema_buy+ema)/2)) or (lower_ema_buy>ll and lower_ema_buy<lh)) and lh<ema):
                        signal = 'Sell'
                # Sell trade
                if (signal == 'Sell'):
                    # In between one hour check
                    now = datetime.now()
                    if(now.minute == 0):
                        oneHour_orderId, oneHour_buy_price, is_oneHour_trade_done = check_one_hour_trade()
                        is_pre_order_done = True

                    cl = ll
                    ch = lh
                    sleep_until_next_15min()
                    df = get_15min_candles()
                    lc = last_close(df)
                    lo = last_open(df)
                    lh = last_high(df)
                    ll = last_low(df)
                    if((lc<=cl) and (lc-ll)>0.02):
                        sell_price = ll-0.05
                        # stop limit sell
                        # if(is_sol_available()):
                        status, order_time = place_stop_market_sell_order(sell_price)
                        if(status == 'FILLED'):
                            stoploss = 0
                            # print('Sell Signal')
                            # print(sell_price)
                        else:
                            stoploss = ll-0.05
                        if(is_15min_wait_completed(order_time)):
                            is_15min_done = True
                    elif(lc<lo):
                        if(ll<cl and ((lh-ll)<(ch-cl)*1.5)):
                            stoploss = ll
                        else:
                            stoploss = cl
                        is_15min_done = True
                    else:
                        stoploss = cl
                        is_15min_done = True
                        # print('--------------------------------------')
                        # continue

            elif(candle == 'Right Hammer' and candle_Typ == 'Bearish candle' and trend == 'Up_trend'):
                if(ema_buy>ema and ll>ema_buy):
                    signal = 'Sell'
                elif(ema_buy<ema):
                    if((lh<upper_ema and lh>=lower_exceed_ema) and (lo>(ema_buy+ema)/2 or lc>(ema_buy+ema)/2)):
                        signal = 'Sell'
                    elif(((ema_buy>ll and ema_buy<lh) or ((lh>ema_buy and lh<ema) and (lo<(ema_buy+ema)/2 or lc<(ema_buy+ema)/2)) or (lower_ema_buy>ll and lower_ema_buy<lh)) and lh<ema):
                        signal = 'Sell'
                # Sell trade
                if (signal == 'Sell'):
                    sell_price = (ll-0.05)
                    # Stop limit sell
                    # if(is_sol_available()):
                    status, order_time = place_stop_market_sell_order(sell_price)
                    if(status == 'FILLED'):
                        stoploss = 0
                        # print('Sell Signal')
                        # print(sell_price)
                    else:
                        stoploss = ll-0.05
                    if(is_15min_wait_completed(order_time)):
                        is_15min_done = True

            elif(candle == 'Inverted hammer' and candle_Typ == 'Bearish candle' and trend == 'Up_trend'):
                if(ema_buy>ema and ll>ema_buy):
                    signal = 'Sell'
                elif(ema_buy<ema):
                    if((lh<upper_ema and lh>=lower_exceed_ema) and (lo>(ema_buy+ema)/2 or lc>(ema_buy+ema)/2)):
                        signal = 'Sell'
                    elif(((ema_buy>ll and ema_buy<lh) or ((lh>ema_buy and lh<ema) and (lo<(ema_buy+ema)/2 or lc<(ema_buy+ema)/2)) or (lower_ema_buy>ll and lower_ema_buy<lh)) and lh<ema):
                        signal = 'Sell'
                # Sell trade
                if (signal == 'Sell'):
                    if((lc-ll)<0.02):
                        sell_price = ll-(lo-lc)/3
                        # Stop limit sell
                        # if(is_sol_available()):
                        status, order_time = place_stop_market_sell_order(sell_price)
                        if(status == 'FILLED'):
                            stoploss = 0
                            # print('Sell Signal')
                            # print(sell_price)
                        else:
                            stoploss = ll-(lo-lc)/3
                        if(is_15min_wait_completed(order_time)):
                            is_15min_done = True
                    else:
                        sell_price = (ll-0.05)
                        # Stop limit sell
                        # if(is_sol_available()):
                        status, order_time = place_stop_market_sell_order(sell_price)
                        if(status == 'FILLED'):
                            stoploss = 0
                            # print('Sell Signal')
                            # print(sell_price)
                        else:
                            stoploss = ll-0.05
                        if(is_15min_wait_completed(order_time)):
                            is_15min_done = True

            elif(candle == 'Spinning Top' and (candle_Typ == 'Bullish candle' or candle_Typ == 'Bearish candle') and trend == 'Up_trend'):
                if(ema_buy>ema and ll>ema_buy):
                    signal = 'Sell'
                elif(ema_buy<ema):
                    if((lh<upper_ema and lh>=lower_exceed_ema) and (lo>(ema_buy+ema)/2 or lc>(ema_buy+ema)/2)):
                        signal = 'Sell'
                    elif(((ema_buy>ll and ema_buy<lh) or ((lh>ema_buy and lh<ema) and (lo<(ema_buy+ema)/2 or lc<(ema_buy+ema)/2)) or (lower_ema_buy>ll and lower_ema_buy<lh)) and lh<ema):
                        signal = 'Sell'
                # Sell trade
                if (signal == 'Sell'):
                    # In between one hour check
                    now = datetime.now()
                    if(now.minute == 0):
                        oneHour_orderId, oneHour_buy_price, is_oneHour_trade_done = check_one_hour_trade()
                        is_pre_order_done = True

                    cl = ll
                    ch = lh
                    sleep_until_next_15min()
                    df = get_15min_candles()
                    lc = last_close(df)
                    lo = last_open(df)
                    lh = last_high(df)
                    ll = last_low(df)
                    if((lc<=cl) and (lc-ll)>0.02):
                        sell_price = ll-0.05
                        # stop limit sell
                        # if(is_sol_available()):
                        status, order_time = place_stop_market_sell_order(sell_price)
                        if(status == 'FILLED'):
                            stoploss = 0
                            # print('Sell Signal')
                            # print(sell_price)
                        else:
                            stoploss = ll-0.05
                        if(is_15min_wait_completed(order_time)):
                            is_15min_done = True
                    elif(lc<lo):
                        if(ll<cl and ((lh-ll)<(ch-cl)*1.5)):
                            stoploss = ll
                        else:
                            stoploss = cl
                        is_15min_done = True
                    else:
                        stoploss = cl
                        is_15min_done = True

            elif(candle == 'Dragonfly doji' and trend == 'Up_trend' and lh>=ph and (candle_Typ == 'Bullish candle' or candle_Typ == 'Bearish candle' or candle_Typ == 'Doji')):
                if(ema_buy>ema and ll>ema_buy):
                    signal = 'Sell'
                elif(ema_buy<ema):
                    if((lh<upper_ema and lh>=lower_exceed_ema) and (lo>(ema_buy+ema)/2 or lc>(ema_buy+ema)/2)):
                        signal = 'Sell'
                    elif(((ema_buy>ll and ema_buy<lh) or ((lh>ema_buy and lh<ema) and (lo<(ema_buy+ema)/2 or lc<(ema_buy+ema)/2)) or (lower_ema_buy>ll and lower_ema_buy<lh)) and lh<ema):
                        signal = 'Sell'
                # Sell trade
                if (signal == 'Sell'):
                    # In between one hour check
                    now = datetime.now()
                    if(now.minute == 0):
                        oneHour_orderId, oneHour_buy_price, is_oneHour_trade_done = check_one_hour_trade()
                        is_pre_order_done = True

                    cl = ll
                    ch = lh
                    sleep_until_next_15min()
                    df = get_15min_candles()
                    lc = last_close(df)
                    lo = last_open(df)
                    lh = last_high(df)
                    ll = last_low(df)
                    if((lc<=cl) and (lc-ll)>0.02):
                        sell_price = ll-0.05
                        # stop limit sell
                        # if(is_sol_available()):
                        status, order_time = place_stop_market_sell_order(sell_price)
                        if(status == 'FILLED'):
                            stoploss = 0
                            # print('Sell Signal')
                            # print(sell_price)
                        else:
                            stoploss = ll-0.05
                        if(is_15min_wait_completed(order_time)):
                            is_15min_done = True
                    elif(lc<lo):
                        if(ll<cl and ((lh-ll)<(ch-cl)*1.5)):
                            stoploss = ll
                        else:
                            stoploss = cl
                        is_15min_done = True
                    else:
                        stoploss = cl
                        is_15min_done = True

            elif(candle == 'Gravestone Doji' and lh>=ph and trend == 'Up_trend' and (candle_Typ == 'Bullish candle' or candle_Typ == 'Bearish candle' or candle_Typ == 'Doji')):
                if(ema_buy>ema and ll>ema_buy):
                    signal = 'Sell'
                elif(ema_buy<ema):
                    if((lh<upper_ema and lh>=lower_exceed_ema) and (lo>(ema_buy+ema)/2 or lc>(ema_buy+ema)/2)):
                        signal = 'Sell'
                    elif(((ema_buy>ll and ema_buy<lh) or ((lh>ema_buy and lh<ema) and (lo<(ema_buy+ema)/2 or lc<(ema_buy+ema)/2)) or (lower_ema_buy>ll and lower_ema_buy<lh)) and lh<ema):
                        signal = 'Sell'
                # Sell trade
                if (signal == 'Sell'):
                    # In between one hour check
                    now = datetime.now()
                    if(now.minute == 0):
                        oneHour_orderId, oneHour_buy_price, is_oneHour_trade_done = check_one_hour_trade()
                        is_pre_order_done = True

                    cl = ll
                    ch = lh
                    sleep_until_next_15min()
                    df = get_15min_candles()
                    lc = last_close(df)
                    lo = last_open(df)
                    lh = last_high(df)
                    ll = last_low(df)
                    if((lc<=cl) and (lc-ll)>0.02):
                        sell_price = ll-0.05
                        # stop limit sell
                        # if(is_sol_available()):
                        status, order_time = place_stop_market_sell_order(sell_price)
                        if(status == 'FILLED'):
                            stoploss = 0
                            # print('Sell Signal')
                            # print(sell_price)
                        else:
                            stoploss = ll-0.05
                        if(is_15min_wait_completed(order_time)):
                            is_15min_done = True
                    elif(lc<lo):
                        if(ll<cl and ((lh-ll)<(ch-cl)*1.5)):
                            stoploss = ll
                        else:
                            stoploss = cl
                        is_15min_done = True
                    else:
                        stoploss = cl
                        is_15min_done = True

            elif(candle == 'Simple Doji' and lh>=ph and trend == 'Up_trend' and (candle_Typ == 'Bullish candle' or candle_Typ == 'Bearish candle' or candle_Typ == 'Doji')):
                if(ema_buy>ema and ll>ema_buy):
                    signal = 'Sell'
                elif(ema_buy<ema):
                    if((lh<upper_ema and lh>=lower_exceed_ema) and (lo>(ema_buy+ema)/2 or lc>(ema_buy+ema)/2)):
                        signal = 'Sell'
                    elif(((ema_buy>ll and ema_buy<lh) or ((lh>ema_buy and lh<ema) and (lo<(ema_buy+ema)/2 or lc<(ema_buy+ema)/2)) or (lower_ema_buy>ll and lower_ema_buy<lh)) and lh<ema):
                        signal = 'Sell'
                # Sell trade
                if (signal == 'Sell'):
                    # In between one hour check
                    now = datetime.now()
                    if(now.minute == 0):
                        oneHour_orderId, oneHour_buy_price, is_oneHour_trade_done = check_one_hour_trade()
                        is_pre_order_done = True

                    cl = ll
                    ch = lh
                    sleep_until_next_15min()
                    df = get_15min_candles()
                    lc = last_close(df)
                    lo = last_open(df)
                    lh = last_high(df)
                    ll = last_low(df)
                    if((lc<=cl) and (lc-ll)>0.02):
                        sell_price = ll-0.05
                        # stop limit sell
                        # if(is_sol_available()):
                        status, order_time = place_stop_market_sell_order(sell_price)
                        if(status == 'FILLED'):
                            stoploss = 0
                            # print('Sell Signal')
                            # print(sell_price)
                        else:
                            stoploss = ll-0.05
                        if(is_15min_wait_completed(order_time)):
                            is_15min_done = True
                    elif(lc<lo):
                        if(ll<cl and ((lh-ll)<(ch-cl)*1.5)):
                            stoploss = ll
                        else:
                            stoploss = cl
                        is_15min_done = True
                    else:
                        stoploss = cl
                        is_15min_done = True

            elif(candle == 'Reversal' and candle_Typ == 'Bullish candle' and trend == 'Up_trend'):
                if(ema_buy>ema and ll>ema_buy):
                    signal = 'Sell'
                elif(ema_buy<ema):
                    if((lh<upper_ema and lh>=lower_exceed_ema) and (lo>(ema_buy+ema)/2 or lc>(ema_buy+ema)/2)):
                        signal = 'Sell'
                    elif(((ema_buy>ll and ema_buy<lh) or ((lh>ema_buy and lh<ema) and (lo<(ema_buy+ema)/2 or lc<(ema_buy+ema)/2)) or (lower_ema_buy>ll and lower_ema_buy<lh)) and lh<ema):
                        signal = 'Sell'
                # Sell trade
                if (signal == 'Sell'):
                    sell_price = (ll-0.05)
                    # sell_price = (lo+lc)/2
                    # Stop limit buy
                    # if(is_sol_available()):
                    status, order_time = place_stop_market_sell_order(sell_price)
                    if(status == 'FILLED'):
                        stoploss = 0
                        # print('Sell Signal')
                        # print(sell_price)
                    else:
                        df = get_15min_candles()
                        el = last_low(df)
                        if(el<(lo+lc)/2):
                            stoploss_orderId = place_stoploss_sell_order(sell_price)
                        else:
                            stoploss = ll
                    if(is_15min_wait_completed(order_time)):
                        is_15min_done = True

            elif(candle == 'Reversal' and candle_Typ == 'Bearish candle' and trend == 'Up_trend'):
                if(ema_buy>ema and ll>ema_buy):
                    signal = 'Sell'
                elif(ema_buy<ema):
                    if((lh<upper_ema and lh>=lower_exceed_ema) and (lo>(ema_buy+ema)/2 or lc>(ema_buy+ema)/2)):
                        signal = 'Sell'
                    elif(((ema_buy>ll and ema_buy<lh) or ((lh>ema_buy and lh<ema) and (lo<(ema_buy+ema)/2 or lc<(ema_buy+ema)/2)) or (lower_ema_buy>ll and lower_ema_buy<lh)) and lh<ema):
                        signal = 'Sell'
                # Sell trade
                if (signal == 'Sell'):
                    sell_price = (ll-0.05)
                    # Stop limit sell
                    # if(is_sol_available()):
                    status, order_time = place_stop_market_sell_order(sell_price)
                    if(status == 'FILLED'):
                        stoploss = 0
                        # print('Sell Signal')
                        # print(sell_price)
                    else:
                        stoploss = ll-0.05
                    if(is_15min_wait_completed(order_time)):
                        is_15min_done = True

            elif(candle == 'Bearish Marubuzu' and candle_Typ == 'Bearish candle' and trend == 'Up_trend'):
                if(ema_buy>ema and ll>ema_buy):
                    signal = 'Sell'
                elif(ema_buy<ema):
                    if((lh<upper_ema and lh>=lower_exceed_ema) and (lo>(ema_buy+ema)/2 or lc>(ema_buy+ema)/2)):
                        signal = 'Sell'
                    elif(((ema_buy>ll and ema_buy<lh) or ((lh>ema_buy and lh<ema) and (lo<(ema_buy+ema)/2 or lc<(ema_buy+ema)/2)) or (lower_ema_buy>ll and lower_ema_buy<lh)) and lh<ema):
                        signal = 'Sell'
                # Sell trade
                if (signal == 'Sell'):
                    if(ll<pl):
                        sell_price = ll-0.05
                        # Stop limit sell
                        # if(is_sol_available()):
                        status, order_time = place_stop_market_sell_order(sell_price)
                        if(status == 'FILLED'):
                            stoploss = 0
                            # print('Sell Signal')
                            # print(sell_price)
                        else:
                            stoploss = ll-0.05
                        if(is_15min_wait_completed(order_time)):
                            is_15min_done = True
                    else:
                        sell_price = pl-0.05
                        # Stop limit sell
                        # if(is_sol_available()):
                        status, order_time = place_stop_market_sell_order(sell_price)
                        if(status == 'FILLED'):
                            stoploss = 0
                            # print('Sell Signal')
                            # print(sell_price)
                        else:
                            stoploss = pl-0.05
                        if(is_15min_wait_completed(order_time)):
                            is_15min_done = True

            # Second Condition
            if(ema_100>ema and trend == 'Up_trend' and ema_100 > ema_buy and 
                ((ema_100<=lh and ema_100>=ll) or (lh>=((ema+ema_100)/2 + ((ema-ema_100)/6)))) and (lo>(ema+ema_100)/2 or lc>(ema+ema_100)/2)):
                
                if(candle == 'Bearish Engulfing' and candle_Typ == 'Bearish candle'):
                    if(ll<pl):
                        sell_price = ll-0.05
                        # Stop limit sell
                        # if(is_sol_available()):
                        status, order_time = place_stop_market_sell_order(sell_price)
                        if(status == 'FILLED'):
                            stoploss = 0
                            # print('Sell Signal')
                            # print(sell_price)
                        else:
                            stoploss = ll-0.05
                        if(is_15min_wait_completed(order_time)):
                            is_15min_done = True
                    else:
                        sell_price = pl-0.05
                        # Stop limit sell
                        # if(is_sol_available()):
                        status, order_time = place_stop_market_sell_order(sell_price)
                        if(status == 'FILLED'):
                            stoploss = 0
                            # print('Sell Signal')
                            # print(sell_price)
                        else:
                            stoploss = pl-0.05
                        if(is_15min_wait_completed(order_time)):
                            is_15min_done = True
                elif(candle == 'Right Hammer' and candle_Typ == 'Bullish candle'):
                    # In between one hour check
                    now = datetime.now()
                    if(now.minute == 0):
                        oneHour_orderId, oneHour_buy_price, is_oneHour_trade_done = check_one_hour_trade()
                        is_pre_order_done = True

                    cl = ll
                    ch = lh
                    sleep_until_next_15min()
                    df = get_15min_candles()
                    lc = last_close(df)
                    lo = last_open(df)
                    lh = last_high(df)
                    ll = last_low(df)
                    if((lc<=cl) and (lc-ll)>0.02):
                        sell_price = ll-0.05
                        # stop limit sell
                        # if(is_sol_available()):
                        status, order_time = place_stop_market_sell_order(sell_price)
                        if(status == 'FILLED'):
                            stoploss = 0
                            # print('Sell Signal')
                            # print(sell_price)
                        else:
                            stoploss = ll-0.05
                        if(is_15min_wait_completed(order_time)):
                            is_15min_done = True
                    elif(lc<lo):
                        if(ll<cl and ((lh-ll)<(ch-cl)*1.5)):
                            stoploss = ll
                        else:
                            stoploss = cl
                        is_15min_done = True
                    else:
                        stoploss = cl
                        is_15min_done = True
                        # print('--------------------------------------')
                        # continue
                elif(candle == 'Right Hammer' and candle_Typ == 'Bearish candle'):
                    sell_price = (ll-0.05)
                    # Stop limit sell
                    # if(is_sol_available()):
                    status, order_time = place_stop_market_sell_order(sell_price)
                    if(status == 'FILLED'):
                        stoploss = 0
                        # print('Sell Signal')
                        # print(sell_price)
                    else:
                        stoploss = ll-0.05
                    if(is_15min_wait_completed(order_time)):
                        is_15min_done = True
                elif(candle == 'Inverted hammer' and candle_Typ == 'Bullish candle'):
                    # In between one hour check
                    now = datetime.now()
                    if(now.minute == 0):
                        oneHour_orderId, oneHour_buy_price, is_oneHour_trade_done = check_one_hour_trade()
                        is_pre_order_done = True

                    cl = ll
                    ch = lh
                    sleep_until_next_15min()
                    df = get_15min_candles()
                    lc = last_close(df)
                    lo = last_open(df)
                    lh = last_high(df)
                    ll = last_low(df)
                    if((lc<=cl) and (lc-ll)>0.02):
                        sell_price = ll-0.05
                        # stop limit sell
                        # if(is_sol_available()):
                        status, order_time = place_stop_market_sell_order(sell_price)
                        if(status == 'FILLED'):
                            stoploss = 0
                            # print('Sell Signal')
                            # print(sell_price)
                        else:
                            stoploss = ll-0.05
                        if(is_15min_wait_completed(order_time)):
                            is_15min_done = True
                    elif(lc<lo):
                        if(ll<cl and ((lh-ll)<(ch-cl)*1.5)):
                            stoploss = ll
                        else:
                            stoploss = cl
                        is_15min_done = True
                    else:
                        stoploss = cl
                        is_15min_done = True
                elif(candle == 'Inverted hammer' and candle_Typ == 'Bearish candle'):
                    if((lc-ll)<0.02):
                        sell_price = ll-(lo-lc)/3
                        # Stop limit sell
                        # if(is_sol_available()):
                        status, order_time = place_stop_market_sell_order(sell_price)
                        if(status == 'FILLED'):
                            stoploss = 0
                            # print('Sell Signal')
                            # print(sell_price)
                        else:
                            stoploss = ll-(lo-lc)/3
                        if(is_15min_wait_completed(order_time)):
                            is_15min_done = True
                    else:
                        sell_price = (ll-0.05)
                        # Stop limit sell
                        # if(is_sol_available()):
                        status, order_time = place_stop_market_sell_order(sell_price)
                        if(status == 'FILLED'):
                            stoploss = 0
                            # print('Sell Signal')
                            # print(sell_price)
                        else:
                            stoploss = ll-0.05
                        if(is_15min_wait_completed(order_time)):
                            is_15min_done = True
                elif(candle == 'Spinning Top' and (candle_Typ == 'Bullish candle' or candle_Typ == 'Bearish candle')):
                    # In between one hour check
                    now = datetime.now()
                    if(now.minute == 0):
                        oneHour_orderId, oneHour_buy_price, is_oneHour_trade_done = check_one_hour_trade()
                        is_pre_order_done = True

                    cl = ll
                    ch = lh
                    sleep_until_next_15min()
                    df = get_15min_candles()
                    lc = last_close(df)
                    lo = last_open(df)
                    lh = last_high(df)
                    ll = last_low(df)
                    if((lc<=cl) and (lc-ll)>0.02):
                        sell_price = ll-0.05
                        # stop limit sell
                        # if(is_sol_available()):
                        status, order_time = place_stop_market_sell_order(sell_price)
                        if(status == 'FILLED'):
                            stoploss = 0
                            # print('Sell Signal')
                            # print(sell_price)
                        else:
                            stoploss = ll-0.05
                        if(is_15min_wait_completed(order_time)):
                            is_15min_done = True
                    elif(lc<lo):
                        if(ll<cl and ((lh-ll)<(ch-cl)*1.5)):
                            stoploss = ll
                        else:
                            stoploss = cl
                        is_15min_done = True
                    else:
                        stoploss = cl
                        is_15min_done = True
                elif(candle == 'Dragonfly doji' and lh>=ph and (candle_Typ == 'Bullish candle' or candle_Typ == 'Bearish candle' or candle_Typ == 'Doji')):
                    # In between one hour check
                    now = datetime.now()
                    if(now.minute == 0):
                        oneHour_orderId, oneHour_buy_price, is_oneHour_trade_done = check_one_hour_trade()
                        is_pre_order_done = True

                    cl = ll
                    ch = lh
                    sleep_until_next_15min()
                    df = get_15min_candles()
                    lc = last_close(df)
                    lo = last_open(df)
                    lh = last_high(df)
                    ll = last_low(df)
                    if((lc<=cl) and (lc-ll)>0.02):
                        sell_price = ll-0.05
                        # stop limit sell
                        # if(is_sol_available()):
                        status, order_time = place_stop_market_sell_order(sell_price)
                        if(status == 'FILLED'):
                            stoploss = 0
                            # print('Sell Signal')
                            # print(sell_price)
                        else:
                            stoploss = ll-0.05
                        if(is_15min_wait_completed(order_time)):
                            is_15min_done = True
                    elif(lc<lo):
                        if(ll<cl and ((lh-ll)<(ch-cl)*1.5)):
                            stoploss = ll
                        else:
                            stoploss = cl
                        is_15min_done = True
                    else:
                        stoploss = cl
                        is_15min_done = True
                elif(candle == 'Gravestone Doji' and lh>=ph and (candle_Typ == 'Bullish candle' or candle_Typ == 'Bearish candle' or candle_Typ == 'Doji')):
                    # In between one hour check
                    now = datetime.now()
                    if(now.minute == 0):
                        oneHour_orderId, oneHour_buy_price, is_oneHour_trade_done = check_one_hour_trade()
                        is_pre_order_done = True

                    cl = ll
                    ch = lh
                    sleep_until_next_15min()
                    df = get_15min_candles()
                    lc = last_close(df)
                    lo = last_open(df)
                    lh = last_high(df)
                    ll = last_low(df)
                    if((lc<=cl) and (lc-ll)>0.02):
                        sell_price = ll-0.05
                        # stop limit sell
                        # if(is_sol_available()):
                        status, order_time = place_stop_market_sell_order(sell_price)
                        if(status == 'FILLED'):
                            stoploss = 0
                            # print('Sell Signal')
                            # print(sell_price)
                        else:
                            stoploss = ll-0.05
                        if(is_15min_wait_completed(order_time)):
                            is_15min_done = True
                    elif(lc<lo):
                        if(ll<cl and ((lh-ll)<(ch-cl)*1.5)):
                            stoploss = ll
                        else:
                            stoploss = cl
                        is_15min_done = True
                    else:
                        stoploss = cl
                        is_15min_done = True
                elif(candle == 'Simple Doji' and lh>=ph and (candle_Typ == 'Bullish candle' or candle_Typ == 'Bearish candle' or candle_Typ == 'Doji')):
                    # In between one hour check
                    now = datetime.now()
                    if(now.minute == 0):
                        oneHour_orderId, oneHour_buy_price, is_oneHour_trade_done = check_one_hour_trade()
                        is_pre_order_done = True

                    cl = ll
                    ch = lh
                    sleep_until_next_15min()
                    df = get_15min_candles()
                    lc = last_close(df)
                    lo = last_open(df)
                    lh = last_high(df)
                    ll = last_low(df)
                    if((lc<=cl) and (lc-ll)>0.02):
                        sell_price = ll-0.05
                        # stop limit sell
                        # if(is_sol_available()):
                        status, order_time = place_stop_market_sell_order(sell_price)
                        if(status == 'FILLED'):
                            stoploss = 0
                            # print('Sell Signal')
                            # print(sell_price)
                        else:
                            stoploss = ll-0.05
                        if(is_15min_wait_completed(order_time)):
                            is_15min_done = True
                    elif(lc<lo):
                        if(ll<cl and ((lh-ll)<(ch-cl)*1.5)):
                            stoploss = ll
                        else:
                            stoploss = cl
                        is_15min_done = True
                    else:
                        stoploss = cl
                        is_15min_done = True
                elif(candle == 'Reversal' and candle_Typ == 'Bullish candle'):
                    sell_price = ll-0.05
                    # sell_price = (lo+lc)/2
                    # Stop limit sell
                    # if(is_sol_available()):
                    status, order_time = place_stop_market_sell_order(sell_price)
                    if(status == 'FILLED'):
                        stoploss = 0
                        # print('Sell Signal')
                        # print(sell_price)
                    else:
                        df = get_15min_candles()
                        el = last_low(df)
                        if(el<(lo+lc)/2):
                            stoploss_orderId = place_stoploss_sell_order(sell_price)
                        else:
                            stoploss = ll
                    if(is_15min_wait_completed(order_time)):
                        is_15min_done = True
                elif(candle == 'Reversal' and candle_Typ == 'Bearish candle'):
                    sell_price = (ll-0.05)
                    # Stop limit sell
                    # if(is_sol_available()):
                    status, order_time = place_stop_market_sell_order(sell_price)
                    if(status == 'FILLED'):
                        stoploss = 0
                        # print('Sell Signal')
                        # print(sell_price)
                    else:
                        stoploss = ll-0.05
                    if(is_15min_wait_completed(order_time)):
                        is_15min_done = True
                elif(candle == 'Bearish Marubuzu' and candle_Typ == 'Bearish candle'):
                    if(ll<pl):
                        sell_price = ll-0.05
                        # Stop limit sell
                        # if(is_sol_available()):
                        status, order_time = place_stop_market_sell_order(sell_price)
                        if(status == 'FILLED'):
                            stoploss = 0
                            # print('Sell Signal')
                            # print(sell_price)
                        else:
                            stoploss = ll-0.05
                        if(is_15min_wait_completed(order_time)):
                            is_15min_done = True
                    else:
                        sell_price = pl-0.05
                        # Stop limit sell
                        # if(is_sol_available()):
                        status, order_time = place_stop_market_sell_order(sell_price)
                        if(status == 'FILLED'):
                            stoploss = 0
                            # print('Sell Signal')
                            # print(sell_price)
                        else:
                            stoploss = pl-0.05
                        if(is_15min_wait_completed(order_time)):
                            is_15min_done = True

            # Exceptional Sell Trade
            if(((ema_100>ll and ema_100<lh) and (ema>ll and ema<lh) and (ema_buy>ll and ema_buy<lh)) and trend == 'Up_trend'):
                if(candle == 'Bearish Engulfing' and candle_Typ == 'Bearish candle'):
                    if(ll<pl):
                        sell_price = ll-0.05
                        # Stop limit sell
                        # if(is_sol_available()):
                        status, order_time = place_stop_market_sell_order(sell_price)
                        if(status == 'FILLED'):
                            stoploss = 0
                            # print('Sell Signal')
                            # print(sell_price)
                        else:
                            stoploss = ll-0.05
                        if(is_15min_wait_completed(order_time)):
                            is_15min_done = True
                    else:
                        sell_price = pl-0.05
                        # Stop limit sell
                        # if(is_sol_available()):
                        status, order_time = place_stop_market_sell_order(sell_price)
                        if(status == 'FILLED'):
                            stoploss = 0
                            # print('Sell Signal')
                            # print(sell_price)
                        else:
                            stoploss = pl-0.05
                        if(is_15min_wait_completed(order_time)):
                            is_15min_done = True
                elif(candle == 'Right Hammer' and candle_Typ == 'Bullish candle'):
                    # In between one hour check
                    now = datetime.now()
                    if(now.minute == 0):
                        oneHour_orderId, oneHour_buy_price, is_oneHour_trade_done = check_one_hour_trade()
                        is_pre_order_done = True

                    cl = ll
                    ch = lh
                    sleep_until_next_15min()
                    df = get_15min_candles()
                    lc = last_close(df)
                    lo = last_open(df)
                    lh = last_high(df)
                    ll = last_low(df)
                    if((lc<=cl) and (lc-ll)>0.02):
                        sell_price = ll-0.05
                        # stop limit sell
                        # if(is_sol_available()):
                        status, order_time = place_stop_market_sell_order(sell_price)
                        if(status == 'FILLED'):
                            stoploss = 0
                            # print('Sell Signal')
                            # print(sell_price)
                        else:
                            stoploss = ll-0.05
                        if(is_15min_wait_completed(order_time)):
                            is_15min_done = True
                    elif(lc<lo):
                        if(ll<cl and ((lh-ll)<(ch-cl)*1.5)):
                            stoploss = ll
                        else:
                            stoploss = cl
                        is_15min_done = True
                    else:
                        stoploss = cl
                        is_15min_done = True
                elif(candle == 'Right Hammer' and candle_Typ == 'Bearish candle'):
                    sell_price = (ll-0.05)
                    # Stop limit sell
                    # if(is_sol_available()):
                    status, order_time = place_stop_market_sell_order(sell_price)
                    if(status == 'FILLED'):
                        stoploss = 0
                        # print('Sell Signal')
                        # print(sell_price)
                    else:
                        stoploss = ll-0.05
                    if(is_15min_wait_completed(order_time)):
                        is_15min_done = True
                elif(candle == 'Inverted hammer' and candle_Typ == 'Bullish candle'):
                    # In between one hour check
                    now = datetime.now()
                    if(now.minute == 0):
                        oneHour_orderId, oneHour_buy_price, is_oneHour_trade_done = check_one_hour_trade()
                        is_pre_order_done = True

                    cl = ll
                    ch = lh
                    sleep_until_next_15min()
                    df = get_15min_candles()
                    lc = last_close(df)
                    lo = last_open(df)
                    lh = last_high(df)
                    ll = last_low(df)
                    if((lc<=cl) and (lc-ll)>0.02):
                        sell_price = ll-0.05
                        # stop limit sell
                        # if(is_sol_available()):
                        status, order_time = place_stop_market_sell_order(sell_price)
                        if(status == 'FILLED'):
                            stoploss = 0
                            # print('Sell Signal')
                            # print(sell_price)
                        else:
                            stoploss = ll-0.05
                        if(is_15min_wait_completed(order_time)):
                            is_15min_done = True
                    elif(lc<lo):
                        if(ll<cl and ((lh-ll)<(ch-cl)*1.5)):
                            stoploss = ll
                        else:
                            stoploss = cl
                        is_15min_done = True
                    else:
                        stoploss = cl
                        is_15min_done = True
                elif(candle == 'Inverted hammer' and candle_Typ == 'Bearish candle'):
                    if((lc-ll)<0.02):
                        sell_price = ll-(lo-lc)/3
                        # Stop limit sell
                        # if(is_sol_available()):
                        status, order_time = place_stop_market_sell_order(sell_price)
                        if(status == 'FILLED'):
                            stoploss = 0
                            # print('Sell Signal')
                            # print(sell_price)
                        else:
                            stoploss = ll-(lo-lc)/3
                        if(is_15min_wait_completed(order_time)):
                            is_15min_done = True
                    else:
                        sell_price = (ll-0.05)
                        # Stop limit sell
                        # if(is_sol_available()):
                        status, order_time = place_stop_market_sell_order(sell_price)
                        if(status == 'FILLED'):
                            stoploss = 0
                            # print('Sell Signal')
                            # print(sell_price)
                        else:
                            stoploss = ll-0.05
                        if(is_15min_wait_completed(order_time)):
                            is_15min_done = True
                elif(candle == 'Spinning Top' and (candle_Typ == 'Bullish candle' or candle_Typ == 'Bearish candle')):
                    # In between one hour check
                    now = datetime.now()
                    if(now.minute == 0):
                        oneHour_orderId, oneHour_buy_price, is_oneHour_trade_done = check_one_hour_trade()
                        is_pre_order_done = True

                    cl = ll
                    ch = lh
                    sleep_until_next_15min()
                    df = get_15min_candles()
                    lc = last_close(df)
                    lo = last_open(df)
                    lh = last_high(df)
                    ll = last_low(df)
                    if((lc<=cl) and (lc-ll)>0.02):
                        sell_price = ll-0.05
                        # stop limit sell
                        # if(is_sol_available()):
                        status, order_time = place_stop_market_sell_order(sell_price)
                        if(status == 'FILLED'):
                            stoploss = 0
                            # print('Sell Signal')
                            # print(sell_price)
                        else:
                            stoploss = ll-0.05
                        if(is_15min_wait_completed(order_time)):
                            is_15min_done = True
                    elif(lc<lo):
                        if(ll<cl and ((lh-ll)<(ch-cl)*1.5)):
                            stoploss = ll
                        else:
                            stoploss = cl
                        is_15min_done = True
                    else:
                        stoploss = cl
                        is_15min_done = True
                elif(candle == 'Dragonfly doji' and lh>=ph and (candle_Typ == 'Bullish candle' or candle_Typ == 'Bearish candle' or candle_Typ == 'Doji')):
                    # In between one hour check
                    now = datetime.now()
                    if(now.minute == 0):
                        oneHour_orderId, oneHour_buy_price, is_oneHour_trade_done = check_one_hour_trade()
                        is_pre_order_done = True

                    cl = ll
                    ch = lh
                    sleep_until_next_15min()
                    df = get_15min_candles()
                    lc = last_close(df)
                    lo = last_open(df)
                    lh = last_high(df)
                    ll = last_low(df)
                    if((lc<=cl) and (lc-ll)>0.02):
                        sell_price = ll-0.05
                        # stop limit sell
                        # if(is_sol_available()):
                        status, order_time = place_stop_market_sell_order(sell_price)
                        if(status == 'FILLED'):
                            stoploss = 0
                            # print('Sell Signal')
                            # print(sell_price)
                        else:
                            stoploss = ll-0.05
                        if(is_15min_wait_completed(order_time)):
                            is_15min_done = True
                    elif(lc<lo):
                        if(ll<cl and ((lh-ll)<(ch-cl)*1.5)):
                            stoploss = ll
                        else:
                            stoploss = cl
                        is_15min_done = True
                    else:
                        stoploss = cl
                        is_15min_done = True
                elif(candle == 'Gravestone Doji' and lh>=ph and (candle_Typ == 'Bullish candle' or candle_Typ == 'Bearish candle' or candle_Typ == 'Doji')):
                    # In between one hour check
                    now = datetime.now()
                    if(now.minute == 0):
                        oneHour_orderId, oneHour_buy_price, is_oneHour_trade_done = check_one_hour_trade()
                        is_pre_order_done = True

                    cl = ll
                    ch = lh
                    sleep_until_next_15min()
                    df = get_15min_candles()
                    lc = last_close(df)
                    lo = last_open(df)
                    lh = last_high(df)
                    ll = last_low(df)
                    if((lc<=cl) and (lc-ll)>0.02):
                        sell_price = ll-0.05
                        # stop limit sell
                        # if(is_sol_available()):
                        status, order_time = place_stop_market_sell_order(sell_price)
                        if(status == 'FILLED'):
                            stoploss = 0
                            # print('Sell Signal')
                            # print(sell_price)
                        else:
                            stoploss = ll-0.05
                        if(is_15min_wait_completed(order_time)):
                            is_15min_done = True
                    elif(lc<lo):
                        if(ll<cl and ((lh-ll)<(ch-cl)*1.5)):
                            stoploss = ll
                        else:
                            stoploss = cl
                        is_15min_done = True
                    else:
                        stoploss = cl
                        is_15min_done = True
                elif(candle == 'Simple Doji' and lh>=ph and (candle_Typ == 'Bullish candle' or candle_Typ == 'Bearish candle' or candle_Typ == 'Doji')):
                    # In between one hour check
                    now = datetime.now()
                    if(now.minute == 0):
                        oneHour_orderId, oneHour_buy_price, is_oneHour_trade_done = check_one_hour_trade()
                        is_pre_order_done = True

                    cl = ll
                    ch = lh
                    sleep_until_next_15min()
                    df = get_15min_candles()
                    lc = last_close(df)
                    lo = last_open(df)
                    lh = last_high(df)
                    ll = last_low(df)
                    if((lc<=cl) and (lc-ll)>0.02):
                        sell_price = ll-0.05
                        # stop limit sell
                        # if(is_sol_available()):
                        status, order_time = place_stop_market_sell_order(sell_price)
                        if(status == 'FILLED'):
                            stoploss = 0
                            # print('Sell Signal')
                            # print(sell_price)
                        else:
                            stoploss = ll-0.05
                        if(is_15min_wait_completed(order_time)):
                            is_15min_done = True
                    elif(lc<lo):
                        if(ll<cl and ((lh-ll)<(ch-cl)*1.5)):
                            stoploss = ll
                        else:
                            stoploss = cl
                        is_15min_done = True
                    else:
                        stoploss = cl
                        is_15min_done = True
                elif(candle == 'Reversal' and candle_Typ == 'Bullish candle'):
                    sell_price = ll-0.05
                    # sell_price = (lo+lc)/2
                    # Stop limit sell
                    # if(is_sol_available()):
                    status, order_time = place_stop_market_sell_order(sell_price)
                    if(status == 'FILLED'):
                        stoploss = 0
                        # print('Sell Signal')
                        # print(sell_price)
                    else:
                        df = get_15min_candles()
                        el = last_low(df)
                        if(el<(lo+lc)/2):
                            stoploss_orderId = place_stoploss_sell_order(sell_price)
                        else:
                            stoploss = ll
                    if(is_15min_wait_completed(order_time)):
                        is_15min_done = True
                elif(candle == 'Reversal' and candle_Typ == 'Bearish candle'):
                    sell_price = (ll-0.05)
                    # Stop limit sell
                    # if(is_sol_available()):
                    status, order_time = place_stop_market_sell_order(sell_price)
                    if(status == 'FILLED'):
                        stoploss = 0
                        # print('Sell Signal')
                        # print(sell_price)
                    else:
                        stoploss = ll-0.05
                    if(is_15min_wait_completed(order_time)):
                        is_15min_done = True
                elif(candle == 'Bearish Marubuzu' and candle_Typ == 'Bearish candle'):
                    if(ll<pl):
                        sell_price = ll-0.05
                        # Stop limit sell
                        # if(is_sol_available()):
                        status, order_time = place_stop_market_sell_order(sell_price)
                        if(status == 'FILLED'):
                            stoploss = 0
                            # print('Sell Signal')
                            # print(sell_price)
                        else:
                            stoploss = ll-0.05
                        if(is_15min_wait_completed(order_time)):
                            is_15min_done = True
                    else:
                        sell_price = pl-0.05
                        # Stop limit sell
                        # if(is_sol_available()):
                        status, order_time = place_stop_market_sell_order(sell_price)
                        if(status == 'FILLED'):
                            stoploss = 0
                            # print('Sell Signal')
                            # print(sell_price)
                        else:
                            stoploss = pl-0.05
                        if(is_15min_wait_completed(order_time)):
                            is_15min_done = True

            # EMA exceptional trade
            if((((ema-ema_buy)<0.05 and (ema-ema_buy)>0) or ((ema_buy-ema)<0.05 and (ema_buy-ema)>0)) and ema>ema_100 and ema_buy>ema_100 and trend == 'Up_trend' and ((ema>=ll and ema<=lh) or (ema_buy>=ll and ema_buy<=lh) or ll>ema or ll>ema_buy)):
                if(candle == 'Bearish Engulfing' and candle_Typ == 'Bearish candle'):
                    if(ll<pl):
                        sell_price = ll-0.05
                        # Stop limit sell
                        # if(is_sol_available()):
                        status, order_time = place_stop_market_sell_order(sell_price)
                        if(status == 'FILLED'):
                            stoploss = 0
                            # print('Sell Signal')
                            # print(sell_price)
                        else:
                            stoploss = ll-0.05
                        if(is_15min_wait_completed(order_time)):
                            is_15min_done = True
                    else:
                        sell_price = pl-0.05
                        # Stop limit sell
                        # if(is_sol_available()):
                        status, order_time = place_stop_market_sell_order(sell_price)
                        if(status == 'FILLED'):
                            stoploss = 0
                            # print('Sell Signal')
                            # print(sell_price)
                        else:
                            stoploss = pl-0.05
                        if(is_15min_wait_completed(order_time)):
                            is_15min_done = True
                elif(candle == 'Right Hammer' and candle_Typ == 'Bullish candle'):
                    # In between one hour check
                    now = datetime.now()
                    if(now.minute == 0):
                        oneHour_orderId, oneHour_buy_price, is_oneHour_trade_done = check_one_hour_trade()
                        is_pre_order_done = True

                    cl = ll
                    ch = lh
                    sleep_until_next_15min()
                    df = get_15min_candles()
                    lc = last_close(df)
                    lo = last_open(df)
                    lh = last_high(df)
                    ll = last_low(df)
                    if((lc<=cl) and (lc-ll)>0.02):
                        sell_price = ll-0.05
                        # stop limit sell
                        # if(is_sol_available()):
                        status, order_time = place_stop_market_sell_order(sell_price)
                        if(status == 'FILLED'):
                            stoploss = 0
                            # print('Sell Signal')
                            # print(sell_price)
                        else:
                            stoploss = ll-0.05
                        if(is_15min_wait_completed(order_time)):
                            is_15min_done = True
                    elif(lc<lo):
                        if(ll<cl and ((lh-ll)<(ch-cl)*1.5)):
                            stoploss = ll
                        else:
                            stoploss = cl
                        is_15min_done = True
                    else:
                        stoploss = cl
                        is_15min_done = True
                elif(candle == 'Right Hammer' and candle_Typ == 'Bearish candle'):
                    sell_price = (ll-0.05)
                    # Stop limit sell
                    # if(is_sol_available()):
                    status, order_time = place_stop_market_sell_order(sell_price)
                    if(status == 'FILLED'):
                        stoploss = 0
                        # print('Sell Signal')
                        # print(sell_price)
                    else:
                        stoploss = ll-0.05
                    if(is_15min_wait_completed(order_time)):
                        is_15min_done = True
                elif(candle == 'Inverted hammer' and candle_Typ == 'Bullish candle'):
                    # In between one hour check
                    now = datetime.now()
                    if(now.minute == 0):
                        oneHour_orderId, oneHour_buy_price, is_oneHour_trade_done = check_one_hour_trade()
                        is_pre_order_done = True

                    cl = ll
                    ch = lh
                    sleep_until_next_15min()
                    df = get_15min_candles()
                    lc = last_close(df)
                    lo = last_open(df)
                    lh = last_high(df)
                    ll = last_low(df)
                    if((lc<=cl) and (lc-ll)>0.02):
                        sell_price = ll-0.05
                        # stop limit sell
                        # if(is_sol_available()):
                        status, order_time = place_stop_market_sell_order(sell_price)
                        if(status == 'FILLED'):
                            stoploss = 0
                            # print('Sell Signal')
                            # print(sell_price)
                        else:
                            stoploss = ll-0.05
                        if(is_15min_wait_completed(order_time)):
                            is_15min_done = True
                    elif(lc<lo):
                        if(ll<cl and ((lh-ll)<(ch-cl)*1.5)):
                            stoploss = ll
                        else:
                            stoploss = cl
                        is_15min_done = True
                    else:
                        stoploss = cl
                        is_15min_done = True
                elif(candle == 'Inverted hammer' and candle_Typ == 'Bearish candle'):
                    if((lc-ll)<0.02):
                        sell_price = ll-(lo-lc)/3
                        # Stop limit sell
                        # if(is_sol_available()):
                        status, order_time = place_stop_market_sell_order(sell_price)
                        if(status == 'FILLED'):
                            stoploss = 0
                            # print('Sell Signal')
                            # print(sell_price)
                        else:
                            stoploss = ll-(lo-lc)/3
                        if(is_15min_wait_completed(order_time)):
                            is_15min_done = True
                    else:
                        sell_price = (ll-0.05)
                        # Stop limit sell
                        # if(is_sol_available()):
                        status, order_time = place_stop_market_sell_order(sell_price)
                        if(status == 'FILLED'):
                            stoploss = 0
                            # print('Sell Signal')
                            # print(sell_price)
                        else:
                            stoploss = ll-0.05
                        if(is_15min_wait_completed(order_time)):
                            is_15min_done = True
                elif(candle == 'Spinning Top' and (candle_Typ == 'Bullish candle' or candle_Typ == 'Bearish candle')):
                    # In between one hour check
                    now = datetime.now()
                    if(now.minute == 0):
                        oneHour_orderId, oneHour_buy_price, is_oneHour_trade_done = check_one_hour_trade()
                        is_pre_order_done = True

                    cl = ll
                    ch = lh
                    sleep_until_next_15min()
                    df = get_15min_candles()
                    lc = last_close(df)
                    lo = last_open(df)
                    lh = last_high(df)
                    ll = last_low(df)
                    if((lc<=cl) and (lc-ll)>0.02):
                        sell_price = ll-0.05
                        # stop limit sell
                        # if(is_sol_available()):
                        status, order_time = place_stop_market_sell_order(sell_price)
                        if(status == 'FILLED'):
                            stoploss = 0
                            # print('Sell Signal')
                            # print(sell_price)
                        else:
                            stoploss = ll-0.05
                        if(is_15min_wait_completed(order_time)):
                            is_15min_done = True
                    elif(lc<lo):
                        if(ll<cl and ((lh-ll)<(ch-cl)*1.5)):
                            stoploss = ll
                        else:
                            stoploss = cl
                        is_15min_done = True
                    else:
                        stoploss = cl
                        is_15min_done = True
                elif(candle == 'Dragonfly doji' and lh>=ph and (candle_Typ == 'Bullish candle' or candle_Typ == 'Bearish candle' or candle_Typ == 'Doji')):
                    # In between one hour check
                    now = datetime.now()
                    if(now.minute == 0):
                        oneHour_orderId, oneHour_buy_price, is_oneHour_trade_done = check_one_hour_trade()
                        is_pre_order_done = True

                    cl = ll
                    ch = lh
                    sleep_until_next_15min()
                    df = get_15min_candles()
                    lc = last_close(df)
                    lo = last_open(df)
                    lh = last_high(df)
                    ll = last_low(df)
                    if((lc<=cl) and (lc-ll)>0.02):
                        sell_price = ll-0.05
                        # stop limit sell
                        # if(is_sol_available()):
                        status, order_time = place_stop_market_sell_order(sell_price)
                        if(status == 'FILLED'):
                            stoploss = 0
                            # print('Sell Signal')
                            # print(sell_price)
                        else:
                            stoploss = ll-0.05
                        if(is_15min_wait_completed(order_time)):
                            is_15min_done = True
                    elif(lc<lo):
                        if(ll<cl and ((lh-ll)<(ch-cl)*1.5)):
                            stoploss = ll
                        else:
                            stoploss = cl
                        is_15min_done = True
                    else:
                        stoploss = cl
                        is_15min_done = True
                elif(candle == 'Gravestone Doji' and lh>=ph and (candle_Typ == 'Bullish candle' or candle_Typ == 'Bearish candle' or candle_Typ == 'Doji')):
                    # In between one hour check
                    now = datetime.now()
                    if(now.minute == 0):
                        oneHour_orderId, oneHour_buy_price, is_oneHour_trade_done = check_one_hour_trade()
                        is_pre_order_done = True

                    cl = ll
                    ch = lh
                    sleep_until_next_15min()
                    df = get_15min_candles()
                    lc = last_close(df)
                    lo = last_open(df)
                    lh = last_high(df)
                    ll = last_low(df)
                    if((lc<=cl) and (lc-ll)>0.02):
                        sell_price = ll-0.05
                        # stop limit sell
                        # if(is_sol_available()):
                        status, order_time = place_stop_market_sell_order(sell_price)
                        if(status == 'FILLED'):
                            stoploss = 0
                            # print('Sell Signal')
                            # print(sell_price)
                        else:
                            stoploss = ll-0.05
                        if(is_15min_wait_completed(order_time)):
                            is_15min_done = True
                    elif(lc<lo):
                        if(ll<cl and ((lh-ll)<(ch-cl)*1.5)):
                            stoploss = ll
                        else:
                            stoploss = cl
                        is_15min_done = True
                    else:
                        stoploss = cl
                        is_15min_done = True
                elif(candle == 'Simple Doji' and lh>=ph and (candle_Typ == 'Bullish candle' or candle_Typ == 'Bearish candle' or candle_Typ == 'Doji')):
                    # In between one hour check
                    now = datetime.now()
                    if(now.minute == 0):
                        oneHour_orderId, oneHour_buy_price, is_oneHour_trade_done = check_one_hour_trade()
                        is_pre_order_done = True

                    cl = ll
                    ch = lh
                    sleep_until_next_15min()
                    df = get_15min_candles()
                    lc = last_close(df)
                    lo = last_open(df)
                    lh = last_high(df)
                    ll = last_low(df)
                    if((lc<=cl) and (lc-ll)>0.02):
                        sell_price = ll-0.05
                        # stop limit sell
                        # if(is_sol_available()):
                        status, order_time = place_stop_market_sell_order(sell_price)
                        if(status == 'FILLED'):
                            stoploss = 0
                            # print('Sell Signal')
                            # print(sell_price)
                        else:
                            stoploss = ll-0.05
                        if(is_15min_wait_completed(order_time)):
                            is_15min_done = True
                    elif(lc<lo):
                        if(ll<cl and ((lh-ll)<(ch-cl)*1.5)):
                            stoploss = ll
                        else:
                            stoploss = cl
                        is_15min_done = True
                    else:
                        stoploss = cl
                        is_15min_done = True
                elif(candle == 'Reversal' and candle_Typ == 'Bullish candle'):
                    sell_price = ll-0.05
                    # sell_price = (lo+lc)/2
                    # Stop limit sell
                    # if(is_sol_available()):
                    status, order_time = place_stop_market_sell_order(sell_price)
                    if(status == 'FILLED'):
                        stoploss = 0
                        # print('Sell Signal')
                        # print(sell_price)
                    else:
                        df = get_15min_candles()
                        el = last_low(df)
                        if(el<(lo+lc)/2):
                            stoploss_orderId = place_stoploss_sell_order(sell_price)
                        else:
                            stoploss = ll
                    if(is_15min_wait_completed(order_time)):
                        is_15min_done = True
                elif(candle == 'Reversal' and candle_Typ == 'Bearish candle'):
                    sell_price = (ll-0.05)
                    # Stop limit sell
                    # if(is_sol_available()):
                    status, order_time = place_stop_market_sell_order(sell_price)
                    if(status == 'FILLED'):
                        stoploss = 0
                        # print('Sell Signal')
                        # print(sell_price)
                    else:
                        stoploss = ll-0.05
                    if(is_15min_wait_completed(order_time)):
                        is_15min_done = True
                elif(candle == 'Bearish Marubuzu' and candle_Typ == 'Bearish candle'):
                    if(ll<pl):
                        sell_price = ll-0.05
                        # Stop limit sell
                        # if(is_sol_available()):
                        status, order_time = place_stop_market_sell_order(sell_price)
                        if(status == 'FILLED'):
                            stoploss = 0
                            # print('Sell Signal')
                            # print(sell_price)
                        else:
                            stoploss = ll-0.05
                        if(is_15min_wait_completed(order_time)):
                            is_15min_done = True
                    else:
                        sell_price = pl-0.05
                        # Stop limit sell
                        # if(is_sol_available()):
                        status, order_time = place_stop_market_sell_order(sell_price)
                        if(status == 'FILLED'):
                            stoploss = 0
                            # print('Sell Signal')
                            # print(sell_price)
                        else:
                            stoploss = pl-0.05
                        if(is_15min_wait_completed(order_time)):
                            is_15min_done = True

        print('          ------------------')
# ------------------------------------------------------------------------------------------------------------------

        # Setup for 30 minute candle
        now = datetime.now()
        if (now.minute == 0 or now.minute == 30 or is_now_30):
            print('           30 minutes setup')
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

            flo3 = lo
            flc3 = lc
            flh3 = lh
            fll3 = ll

            print(candle_Typ)
            print(candle)
            print(trend_check(df3))
        # -----------------------------------------------------------------------------------------------------------
            if is_oneHour_above_high:
                if(is_one_hour_candle_down() == False):
                    # For buy order
                    if(candle == 'Bullish Engulfing' and candle_Typ == 'Bullish candle' and trend == 'Down_trend' and trade_status == 'ok'):
                        if(ema_buy<ema and ema_buy<ema_100 and emaBuy_status=='ok' and lh<ema_buy):
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
                            is_30_min_signal_found = True

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
                            is_30_min_signal_found = True

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
                            is_30_min_signal_found = True

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
                            is_30_min_signal_found = True

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
                            is_30_min_signal_found = True

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
                            is_30_min_signal_found = True

                    elif(candle == 'Dragonfly doji' and  trend == 'Down_trend' and ll<=pl and (candle_Typ == 'Bullish candle' or candle_Typ == 'Bearish candle' or candle_Typ == 'Doji') and trade_status == 'ok'):
                        if(ema_buy<ema and ema_buy<ema_100 and emaBuy_status=='ok' and lh<ema_buy):
                            signal = 'Buy'
                        elif(ema_buy>ema and ema_buy>ema_100):
                            if((ll>lower_ema and ll<=upper_exceed_ema) and (lo<(ema_buy+ema)/2 or lc<(ema_buy+ema)/2)):
                                signal = 'Buy'
                            elif(((ema_buy>ll and ema_buy<lh) or ((ll<ema_buy and ll>ema) and (lc>(ema+ema_buy)/2))) and ll>ema):
                                signal = 'Buy'
                        # Buy trade
                        if (signal == 'Buy'):
                            is_30_min_signal_found = True

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
                            is_30_min_signal_found = True

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
                            is_30_min_signal_found = True

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
                            is_30_min_signal_found = True

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
                            is_30_min_signal_found = True

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
                            is_30_min_signal_found = True
                    
                    # Second Condition
                    if(ema_100<ema and trend == 'Down_trend' and ema_100 < ema_buy and 
                        ((ema_100<=lh and ema_100>=ll) or (ll<=((ema+ema_100)/2 -((ema-ema_100)/6)))) and (lc<(ema+ema_100)/2 or lo<(ema+ema_100)/2) and trade_status == 'ok'):

                        if(candle == 'Bullish Engulfing' and candle_Typ == 'Bullish candle'):
                            is_30_min_signal_found = True
                        elif(candle == 'Right Hammer' and candle_Typ == 'Bullish candle'):
                            is_30_min_signal_found = True
                        elif(candle == 'Right Hammer' and candle_Typ == 'Bearish candle'):
                            is_30_min_signal_found = True
                        elif(candle == 'Inverted hammer' and candle_Typ == 'Bullish candle'):
                            is_30_min_signal_found = True
                        elif(candle == 'Inverted hammer' and candle_Typ == 'Bearish candle'):
                            is_30_min_signal_found = True
                        elif(candle == 'Spinning Top' and (candle_Typ == 'Bullish candle' or candle_Typ == 'Bearish candle')):
                            is_30_min_signal_found = True
                        elif(candle == 'Dragonfly doji' and (candle_Typ == 'Bullish candle' or candle_Typ == 'Bearish candle' or candle_Typ == 'Doji') and ll<=pl):
                            is_30_min_signal_found = True
                        elif(candle == 'Gravestone Doji' and ll<=pl and (candle_Typ == 'Bullish candle' or candle_Typ == 'Bearish candle' or candle_Typ == 'Doji')):
                            is_30_min_signal_found = True
                        elif(candle == 'Simple Doji' and ll<=pl and (candle_Typ == 'Bullish candle' or candle_Typ == 'Bearish candle' or candle_Typ == 'Doji')):
                            is_30_min_signal_found = True
                        elif(candle == 'Reversal' and candle_Typ == 'Bullish candle'):
                            is_30_min_signal_found = True
                        elif(candle == 'Reversal' and candle_Typ == 'Bearish candle'):
                            is_30_min_signal_found = True
                        elif(candle == 'Bullish Marubuzu' and candle_Typ == 'Bullish candle'):
                            is_30_min_signal_found = True

                    if(is_30_min_signal_found):
                        print("30 minutes buy signal found")

        # -----------------------------------------------------------------------------------------------------------
            # For selling
            if(is_shift_towards_30_min):
                if(candle == 'Bearish Engulfing' and candle_Typ == 'Bearish candle' and trend == 'Up_trend'):
                    if(ema_buy>ema and ll>ema_buy):
                        signal = 'Sell'
                    elif(ema_buy<ema):
                        if(((lh<upper_ema and lh>=lower_exceed_ema)) and (lo>(ema_buy+ema)/2 or lc>(ema_buy+ema)/2)):
                            signal = 'Sell'
                        elif(((ema_buy>ll and ema_buy<lh) or ((lh>ema_buy and lh<ema) and (lo<(ema_buy+ema)/2 or lc<(ema_buy+ema)/2))) and lh<ema):
                            signal = 'Sell'
                    # Sell trade
                    if (signal == 'Sell'):
                        if(ll<pl):
                            sell_price = ll-0.05
                            # Stop limit sell
                            # if(is_sol_available()):
                            status, order_time = place_stop_market_sell_order_30min(sell_price)
                            if(status == 'FILLED'):
                                stoploss = 0
                                is_shift_towards_30_min = False
                                # print('Sell Signal')
                                # print(sell_price)
                            else:
                                stoploss = ll-0.05
                            if(is_30min_wait_completed(order_time)):
                                is_15min_done = True
                        else:
                            sell_price = pl-0.05
                            # Stop limit sell
                            # if(is_sol_available()):
                            status, order_time = place_stop_market_sell_order_30min(sell_price)
                            if(status == 'FILLED'):
                                stoploss = 0
                                is_shift_towards_30_min = False
                                # print('Sell Signal')
                                # print(sell_price)
                            else:
                                stoploss = pl-0.05
                            if(is_30min_wait_completed(order_time)):
                                is_15min_done = True
                                    
                elif(candle == 'Right Hammer' and candle_Typ == 'Bullish candle' and trend == 'Up_trend'):
                    if(ema_buy>ema and ll>ema_buy):
                        signal = 'Sell'
                    elif(ema_buy<ema):
                        if((lh<upper_ema and lh>=lower_exceed_ema) and (lo>(ema_buy+ema)/2 or lc>(ema_buy+ema)/2)):
                            signal = 'Sell'
                        elif(((ema_buy>ll and ema_buy<lh) or ((lh>ema_buy and lh<ema) and (lo<(ema_buy+ema)/2 or lc<(ema_buy+ema)/2))) and lh<ema):
                            signal = 'Sell'
                    # Sell trade
                    if (signal == 'Sell'):
                        # In between one hour check
                        now = datetime.now()
                        if(now.minute == 0):
                            oneHour_orderId, oneHour_buy_price, is_oneHour_trade_done = check_one_hour_trade()
                            is_pre_order_done = True

                        cl = ll
                        ch = lh
                        sleep_until_next_30min()
                        df = get_30min_candles()
                        lc = last_close(df)
                        lo = last_open(df)
                        lh = last_high(df)
                        ll = last_low(df)
                        if((lc<=cl) and (lc-ll)>0.02):
                            sell_price = ll-0.05
                            # stop limit sell
                            # if(is_sol_available()):
                            status, order_time = place_stop_market_sell_order_30min(sell_price)
                            if(status == 'FILLED'):
                                stoploss = 0
                                is_shift_towards_30_min = False
                                # print('Sell Signal')
                                # print(sell_price)
                            else:
                                stoploss = ll-0.05
                            if(is_30min_wait_completed(order_time)):
                                is_15min_done = True
                        elif(lc<lo):
                            if(ll<cl and ((lh-ll)<(ch-cl)*1.5)):
                                stoploss = ll
                            else:
                                stoploss = cl
                            is_15min_done = True
                        else:
                            stoploss = cl
                            is_15min_done = True
                            # print('--------------------------------------')
                            # continue

                elif(candle == 'Inverted hammer' and candle_Typ == 'Bullish candle' and trend == 'Up_trend'):
                    if(ema_buy>ema and ll>ema_buy):
                        signal = 'Sell'
                    elif(ema_buy<ema):
                        if((lh<upper_ema and lh>=lower_exceed_ema) and (lo>(ema_buy+ema)/2 or lc>(ema_buy+ema)/2)):
                            signal = 'Sell'
                        elif(((ema_buy>ll and ema_buy<lh) or ((lh>ema_buy and lh<ema) and (lo<(ema_buy+ema)/2 or lc<(ema_buy+ema)/2))) and lh<ema):
                            signal = 'Sell'
                    # Sell trade
                    if (signal == 'Sell'):
                        # In between one hour check
                        now = datetime.now()
                        if(now.minute == 0):
                            oneHour_orderId, oneHour_buy_price, is_oneHour_trade_done = check_one_hour_trade()
                            is_pre_order_done = True

                        cl = ll
                        ch = lh
                        sleep_until_next_30min()
                        df = get_30min_candles()
                        lc = last_close(df)
                        lo = last_open(df)
                        lh = last_high(df)
                        ll = last_low(df)
                        if((lc<=cl) and (lc-ll)>0.02):
                            sell_price = ll-0.05
                            # stop limit sell
                            # if(is_sol_available()):
                            status, order_time = place_stop_market_sell_order_30min(sell_price)
                            if(status == 'FILLED'):
                                stoploss = 0
                                is_shift_towards_30_min = False
                                # print('Sell Signal')
                                # print(sell_price)
                            else:
                                stoploss = ll-0.05
                            if(is_30min_wait_completed(order_time)):
                                is_15min_done = True
                        elif(lc<lo):
                            if(ll<cl and ((lh-ll)<(ch-cl)*1.5)):
                                stoploss = ll
                            else:
                                stoploss = cl
                            is_15min_done = True
                        else:
                            stoploss = cl
                            is_15min_done = True

                elif(candle == 'Right Hammer' and candle_Typ == 'Bearish candle' and trend == 'Up_trend'):
                    if(ema_buy>ema and ll>ema_buy):
                        signal = 'Sell'
                    elif(ema_buy<ema):
                        if((lh<upper_ema and lh>=lower_exceed_ema) and (lo>(ema_buy+ema)/2 or lc>(ema_buy+ema)/2)):
                            signal = 'Sell'
                        elif(((ema_buy>ll and ema_buy<lh) or ((lh>ema_buy and lh<ema) and (lo<(ema_buy+ema)/2 or lc<(ema_buy+ema)/2))) and lh<ema):
                            signal = 'Sell'
                    # Sell trade
                    if (signal == 'Sell'):
                        sell_price = (ll-0.05)
                        # Stop limit sell
                        # if(is_sol_available()):
                        status, order_time = place_stop_market_sell_order_30min(sell_price)
                        if(status == 'FILLED'):
                            stoploss = 0
                            is_shift_towards_30_min = False
                            # print('Sell Signal')
                            # print(sell_price)
                        else:
                            stoploss = ll-0.05
                        if(is_30min_wait_completed(order_time)):
                            is_15min_done = True

                elif(candle == 'Inverted hammer' and candle_Typ == 'Bearish candle' and trend == 'Up_trend'):
                    if(ema_buy>ema and ll>ema_buy):
                        signal = 'Sell'
                    elif(ema_buy<ema):
                        if((lh<upper_ema and lh>=lower_exceed_ema) and (lo>(ema_buy+ema)/2 or lc>(ema_buy+ema)/2)):
                            signal = 'Sell'
                        elif(((ema_buy>ll and ema_buy<lh) or ((lh>ema_buy and lh<ema) and (lo<(ema_buy+ema)/2 or lc<(ema_buy+ema)/2))) and lh<ema):
                            signal = 'Sell'
                    # Sell trade
                    if (signal == 'Sell'):
                        if((lc-ll)<0.02):
                            sell_price = ll-(lo-lc)/3
                            # Stop limit sell
                            # if(is_sol_available()):
                            status, order_time = place_stop_market_sell_order_30min(sell_price)
                            if(status == 'FILLED'):
                                stoploss = 0
                                is_shift_towards_30_min = False
                                # print('Sell Signal')
                                # print(sell_price)
                            else:
                                stoploss = ll-(lo-lc)/3
                            if(is_30min_wait_completed(order_time)):
                                is_15min_done = True
                        else:
                            sell_price = (ll-0.05)
                            # Stop limit sell
                            # if(is_sol_available()):
                            status, order_time = place_stop_market_sell_order_30min(sell_price)
                            if(status == 'FILLED'):
                                stoploss = 0
                                is_shift_towards_30_min = False
                                # print('Sell Signal')
                                # print(sell_price)
                            else:
                                stoploss = ll-0.05
                            if(is_30min_wait_completed(order_time)):
                                is_15min_done = True

                elif(candle == 'Spinning Top' and (candle_Typ == 'Bullish candle' or candle_Typ == 'Bearish candle') and trend == 'Up_trend'):
                    if(ema_buy>ema and ll>ema_buy):
                        signal = 'Sell'
                    elif(ema_buy<ema):
                        if((lh<upper_ema and lh>=lower_exceed_ema) and (lo>(ema_buy+ema)/2 or lc>(ema_buy+ema)/2)):
                            signal = 'Sell'
                        elif(((ema_buy>ll and ema_buy<lh) or ((lh>ema_buy and lh<ema) and (lo<(ema_buy+ema)/2 or lc<(ema_buy+ema)/2))) and lh<ema):
                            signal = 'Sell'
                    # Sell trade
                    if (signal == 'Sell'):
                        # In between one hour check
                        now = datetime.now()
                        if(now.minute == 0):
                            oneHour_orderId, oneHour_buy_price, is_oneHour_trade_done = check_one_hour_trade()
                            is_pre_order_done = True
                        
                        cl = ll
                        ch = lh
                        sleep_until_next_30min()
                        df = get_30min_candles()
                        lc = last_close(df)
                        lo = last_open(df)
                        lh = last_high(df)
                        ll = last_low(df)
                        if((lc<=cl) and (lc-ll)>0.02):
                            sell_price = ll-0.05
                            # stop limit sell
                            # if(is_sol_available()):
                            status, order_time = place_stop_market_sell_order_30min(sell_price)
                            if(status == 'FILLED'):
                                stoploss = 0
                                is_shift_towards_30_min = False
                                # print('Sell Signal')
                                # print(sell_price)
                            else:
                                stoploss = ll-0.05
                            if(is_30min_wait_completed(order_time)):
                                is_15min_done = True
                        elif(lc<lo):
                            if(ll<cl and ((lh-ll)<(ch-cl)*1.5)):
                                stoploss = ll
                            else:
                                stoploss = cl
                            is_15min_done = True
                        else:
                            stoploss = cl
                            is_15min_done = True

                elif(candle == 'Dragonfly doji' and trend == 'Up_trend' and lh>=ph and (candle_Typ == 'Bullish candle' or candle_Typ == 'Bearish candle' or candle_Typ == 'Doji')):
                    if(ema_buy>ema and ll>ema_buy):
                        signal = 'Sell'
                    elif(ema_buy<ema):
                        if((lh<upper_ema and lh>=lower_exceed_ema) and (lo>(ema_buy+ema)/2 or lc>(ema_buy+ema)/2)):
                            signal = 'Sell'
                        elif(((ema_buy>ll and ema_buy<lh) or ((lh>ema_buy and lh<ema) and (lo<(ema_buy+ema)/2 or lc<(ema_buy+ema)/2))) and lh<ema):
                            signal = 'Sell'
                    # Sell trade
                    if (signal == 'Sell'):
                        # In between one hour check
                        now = datetime.now()
                        if(now.minute == 0):
                            oneHour_orderId, oneHour_buy_price, is_oneHour_trade_done = check_one_hour_trade()
                            is_pre_order_done = True
                        
                        cl = ll
                        ch = lh
                        sleep_until_next_30min()
                        df = get_30min_candles()
                        lc = last_close(df)
                        lo = last_open(df)
                        lh = last_high(df)
                        ll = last_low(df)
                        if((lc<=cl) and (lc-ll)>0.02):
                            sell_price = ll-0.05
                            # stop limit sell
                            # if(is_sol_available()):
                            status, order_time = place_stop_market_sell_order_30min(sell_price)
                            if(status == 'FILLED'):
                                stoploss = 0
                                is_shift_towards_30_min = False
                                # print('Sell Signal')
                                # print(sell_price)
                            else:
                                stoploss = ll-0.05
                            if(is_30min_wait_completed(order_time)):
                                is_15min_done = True
                        elif(lc<lo):
                            if(ll<cl and ((lh-ll)<(ch-cl)*1.5)):
                                stoploss = ll
                            else:
                                stoploss = cl
                            is_15min_done = True
                        else:
                            stoploss = cl
                            is_15min_done = True

                elif(candle == 'Gravestone Doji' and lh>=ph and trend == 'Up_trend' and (candle_Typ == 'Bullish candle' or candle_Typ == 'Bearish candle' or candle_Typ == 'Doji')):
                    if(ema_buy>ema and ll>ema_buy):
                        signal = 'Sell'
                    elif(ema_buy<ema):
                        if((lh<upper_ema and lh>=lower_exceed_ema) and (lo>(ema_buy+ema)/2 or lc>(ema_buy+ema)/2)):
                            signal = 'Sell'
                        elif(((ema_buy>ll and ema_buy<lh) or ((lh>ema_buy and lh<ema) and (lo<(ema_buy+ema)/2 or lc<(ema_buy+ema)/2))) and lh<ema):
                            signal = 'Sell'
                    # Sell trade
                    if (signal == 'Sell'):
                        # In between one hour check
                        now = datetime.now()
                        if(now.minute == 0):
                            oneHour_orderId, oneHour_buy_price, is_oneHour_trade_done = check_one_hour_trade()
                            is_pre_order_done = True
                        
                        cl = ll
                        ch = lh
                        sleep_until_next_30min()
                        df = get_30min_candles()
                        lc = last_close(df)
                        lo = last_open(df)
                        lh = last_high(df)
                        ll = last_low(df)
                        if((lc<=cl) and (lc-ll)>0.02):
                            sell_price = ll-0.05
                            # stop limit sell
                            # if(is_sol_available()):
                            status, order_time = place_stop_market_sell_order_30min(sell_price)
                            if(status == 'FILLED'):
                                stoploss = 0
                                is_shift_towards_30_min = False
                                # print('Sell Signal')
                                # print(sell_price)
                            else:
                                stoploss = ll-0.05
                            if(is_30min_wait_completed(order_time)):
                                is_15min_done = True
                        elif(lc<lo):
                            if(ll<cl and ((lh-ll)<(ch-cl)*1.5)):
                                stoploss = ll
                            else:
                                stoploss = cl
                            is_15min_done = True
                        else:
                            stoploss = cl
                            is_15min_done = True

                elif(candle == 'Simple Doji' and lh>=ph and trend == 'Up_trend' and (candle_Typ == 'Bullish candle' or candle_Typ == 'Bearish candle' or candle_Typ == 'Doji')):
                    if(ema_buy>ema and ll>ema_buy):
                        signal = 'Sell'
                    elif(ema_buy<ema):
                        if((lh<upper_ema and lh>=lower_exceed_ema) and (lo>(ema_buy+ema)/2 or lc>(ema_buy+ema)/2)):
                            signal = 'Sell'
                        elif(((ema_buy>ll and ema_buy<lh) or ((lh>ema_buy and lh<ema) and (lo<(ema_buy+ema)/2 or lc<(ema_buy+ema)/2))) and lh<ema):
                            signal = 'Sell'
                    # Sell trade
                    if (signal == 'Sell'):
                        # In between one hour check
                        now = datetime.now()
                        if(now.minute == 0):
                            oneHour_orderId, oneHour_buy_price, is_oneHour_trade_done = check_one_hour_trade()
                            is_pre_order_done = True
                        
                        cl = ll
                        ch = lh
                        sleep_until_next_30min()
                        df = get_30min_candles()
                        lc = last_close(df)
                        lo = last_open(df)
                        lh = last_high(df)
                        ll = last_low(df)
                        if((lc<=cl) and (lc-ll)>0.02):
                            sell_price = ll-0.05
                            # stop limit sell
                            # if(is_sol_available()):
                            status, order_time = place_stop_market_sell_order_30min(sell_price)
                            if(status == 'FILLED'):
                                stoploss = 0
                                is_shift_towards_30_min = False
                                # print('Sell Signal')
                                # print(sell_price)
                            else:
                                stoploss = ll-0.05
                            if(is_30min_wait_completed(order_time)):
                                is_15min_done = True
                        elif(lc<lo):
                            if(ll<cl and ((lh-ll)<(ch-cl)*1.5)):
                                stoploss = ll
                            else:
                                stoploss = cl
                            is_15min_done = True
                        else:
                            stoploss = cl
                            is_15min_done = True

                elif(candle == 'Reversal' and candle_Typ == 'Bullish candle' and trend == 'Up_trend'):
                    if(ema_buy>ema and ll>ema_buy):
                        signal = 'Sell'
                    elif(ema_buy<ema):
                        if((lh<upper_ema and lh>=lower_exceed_ema) and (lo>(ema_buy+ema)/2 or lc>(ema_buy+ema)/2)):
                            signal = 'Sell'
                        elif(((ema_buy>ll and ema_buy<lh) or ((lh>ema_buy and lh<ema) and (lo<(ema_buy+ema)/2 or lc<(ema_buy+ema)/2))) and lh<ema):
                            signal = 'Sell'
                    # Sell trade
                    if (signal == 'Sell'):
                        sell_price = ll-0.05
                        # sell_price = (lo+lc)/2
                        # Stop limit buy
                        # if(is_sol_available()):
                        status, order_time = place_stop_market_sell_order_30min(sell_price)
                        if(status == 'FILLED'):
                            stoploss = 0
                            is_shift_towards_30_min = False
                            # print('Sell Signal')
                            # print(sell_price)
                        else:
                            df = get_30min_candles()
                            el = last_low(df)
                            if(el<(lo+lc)/2):
                                stoploss_orderId = place_stoploss_sell_order(sell_price)
                            else:
                                stoploss = ll
                        if(is_30min_wait_completed(order_time)):
                            is_15min_done = True

                elif(candle == 'Reversal' and candle_Typ == 'Bearish candle' and trend == 'Up_trend'):
                    if(ema_buy>ema and ll>ema_buy):
                        signal = 'Sell'
                    elif(ema_buy<ema):
                        if((lh<upper_ema and lh>=lower_exceed_ema) and (lo>(ema_buy+ema)/2 or lc>(ema_buy+ema)/2)):
                            signal = 'Sell'
                        elif(((ema_buy>ll and ema_buy<lh) or ((lh>ema_buy and lh<ema) and (lo<(ema_buy+ema)/2 or lc<(ema_buy+ema)/2))) and lh<ema):
                            signal = 'Sell'
                    # Sell trade
                    if (signal == 'Sell'):
                        sell_price = (ll-0.05)
                        # Stop limit sell
                        # if(is_sol_available()):
                        status, order_time = place_stop_market_sell_order_30min(sell_price)
                        if(status == 'FILLED'):
                            stoploss = 0
                            is_shift_towards_30_min = False
                            # print('Sell Signal')
                            # print(sell_price)
                        else:
                            stoploss = ll-0.05
                        if(is_30min_wait_completed(order_time)):
                            is_15min_done = True

                elif(candle == 'Bearish Marubuzu' and candle_Typ == 'Bearish candle' and trend == 'Up_trend'):
                    if(ema_buy>ema and ll>ema_buy):
                        signal = 'Sell'
                    elif(ema_buy<ema):
                        if((lh<upper_ema and lh>=lower_exceed_ema) and (lo>(ema_buy+ema)/2 or lc>(ema_buy+ema)/2)):
                            signal = 'Sell'
                        elif(((ema_buy>ll and ema_buy<lh) or ((lh>ema_buy and lh<ema) and (lo<(ema_buy+ema)/2 or lc<(ema_buy+ema)/2))) and lh<ema):
                            signal = 'Sell'
                    # Sell trade
                    if (signal == 'Sell'):
                        if(ll<pl):
                            sell_price = ll-0.05
                            # Stop limit sell
                            # if(is_sol_available()):
                            status, order_time = place_stop_market_sell_order_30min(sell_price)
                            if(status == 'FILLED'):
                                stoploss = 0
                                is_shift_towards_30_min = False
                                # print('Sell Signal')
                                # print(sell_price)
                            else:
                                stoploss = ll-0.05
                            if(is_30min_wait_completed(order_time)):
                                is_15min_done = True
                        else:
                            sell_price = pl-0.05
                            # Stop limit sell
                            # if(is_sol_available()):
                            status, order_time = place_stop_market_sell_order_30min(sell_price)
                            if(status == 'FILLED'):
                                stoploss = 0
                                is_shift_towards_30_min = False
                                # print('Sell Signal')
                                # print(sell_price)
                            else:
                                stoploss = pl-0.05
                            if(is_30min_wait_completed(order_time)):
                                is_15min_done = True

                # Second Condition
                if(ema_100>ema and trend == 'Up_trend' and ema_100 > ema_buy and 
                    ((ema_100<=lh and ema_100>=ll) or (lh>=((ema+ema_100)/2 + ((ema-ema_100)/6)))) and (lo>(ema+ema_100)/2 or lc>(ema+ema_100)/2)):
                    
                    if(candle == 'Bearish Engulfing' and candle_Typ == 'Bearish candle'):
                        if(ll<pl):
                            sell_price = ll-0.05
                            # Stop limit sell
                            # if(is_sol_available()):
                            status, order_time = place_stop_market_sell_order_30min(sell_price)
                            if(status == 'FILLED'):
                                stoploss = 0
                                is_shift_towards_30_min = False
                                # print('Sell Signal')
                                # print(sell_price)
                            else:
                                stoploss = ll-0.05
                            if(is_30min_wait_completed(order_time)):
                                is_15min_done = True
                        else:
                            sell_price = pl-0.05
                            # Stop limit sell
                            # if(is_sol_available()):
                            status, order_time = place_stop_market_sell_order_30min(sell_price)
                            if(status == 'FILLED'):
                                stoploss = 0
                                is_shift_towards_30_min = False
                                # print('Sell Signal')
                                # print(sell_price)
                            else:
                                stoploss = pl-0.05
                            if(is_30min_wait_completed(order_time)):
                                is_15min_done = True
                    elif(candle == 'Right Hammer' and candle_Typ == 'Bullish candle'):
                        # In between one hour check
                        now = datetime.now()
                        if(now.minute == 0):
                            oneHour_orderId, oneHour_buy_price, is_oneHour_trade_done = check_one_hour_trade()
                            is_pre_order_done = True
                        
                        cl = ll
                        ch = lh
                        sleep_until_next_30min()
                        df = get_30min_candles()
                        lc = last_close(df)
                        lo = last_open(df)
                        lh = last_high(df)
                        ll = last_low(df)
                        if((lc<=cl) and (lc-ll)>0.02):
                            sell_price = ll-0.05
                            # stop limit sell
                            # if(is_sol_available()):
                            status, order_time = place_stop_market_sell_order_30min(sell_price)
                            if(status == 'FILLED'):
                                stoploss = 0
                                is_shift_towards_30_min = False
                                # print('Sell Signal')
                                # print(sell_price)
                            else:
                                stoploss = ll-0.05
                            if(is_30min_wait_completed(order_time)):
                                is_15min_done = True
                        elif(lc<lo):
                            if(ll<cl and ((lh-ll)<(ch-cl)*1.5)):
                                stoploss = ll
                            else:
                                stoploss = cl
                            is_15min_done = True
                        else:
                            stoploss = cl
                            is_15min_done = True
                    elif(candle == 'Right Hammer' and candle_Typ == 'Bearish candle'):
                        sell_price = (ll-0.05)
                        # Stop limit sell
                        # if(is_sol_available()):
                        status, order_time = place_stop_market_sell_order_30min(sell_price)
                        if(status == 'FILLED'):
                            stoploss = 0
                            is_shift_towards_30_min = False
                            # print('Sell Signal')
                            # print(sell_price)
                        else:
                            stoploss = ll-0.05
                        if(is_30min_wait_completed(order_time)):
                            is_15min_done = True
                    elif(candle == 'Inverted hammer' and candle_Typ == 'Bullish candle'):
                        # In between one hour check
                        now = datetime.now()
                        if(now.minute == 0):
                            oneHour_orderId, oneHour_buy_price, is_oneHour_trade_done = check_one_hour_trade()
                            is_pre_order_done = True
                        
                        cl = ll
                        ch = lh
                        sleep_until_next_30min()
                        df = get_30min_candles()
                        lc = last_close(df)
                        lo = last_open(df)
                        lh = last_high(df)
                        ll = last_low(df)
                        if((lc<=cl) and (lc-ll)>0.02):
                            sell_price = ll-0.05
                            # stop limit sell
                            # if(is_sol_available()):
                            status, order_time = place_stop_market_sell_order_30min(sell_price)
                            if(status == 'FILLED'):
                                stoploss = 0
                                is_shift_towards_30_min = False
                                # print('Sell Signal')
                                # print(sell_price)
                            else:
                                stoploss = ll-0.05
                            if(is_30min_wait_completed(order_time)):
                                is_15min_done = True
                        elif(lc<lo):
                            if(ll<cl and ((lh-ll)<(ch-cl)*1.5)):
                                stoploss = ll
                            else:
                                stoploss = cl
                            is_15min_done = True
                        else:
                            stoploss = cl
                            is_15min_done = True
                    elif(candle == 'Inverted hammer' and candle_Typ == 'Bearish candle'):
                        if((lc-ll)<0.02):
                            sell_price = ll-(lo-lc)/3
                            # Stop limit sell
                            # if(is_sol_available()):
                            status, order_time = place_stop_market_sell_order_30min(sell_price)
                            if(status == 'FILLED'):
                                stoploss = 0
                                is_shift_towards_30_min = False
                                # print('Sell Signal')
                                # print(sell_price)
                            else:
                                stoploss = ll-(lo-lc)/3
                            if(is_30min_wait_completed(order_time)):
                                is_15min_done = True
                        else:
                            sell_price = (ll-0.05)
                            # Stop limit sell
                            # if(is_sol_available()):
                            status, order_time = place_stop_market_sell_order_30min(sell_price)
                            if(status == 'FILLED'):
                                stoploss = 0
                                is_shift_towards_30_min = False
                                # print('Sell Signal')
                                # print(sell_price)
                            else:
                                stoploss = ll-0.05
                            if(is_30min_wait_completed(order_time)):
                                is_15min_done = True
                    elif(candle == 'Spinning Top' and (candle_Typ == 'Bullish candle' or candle_Typ == 'Bearish candle')):
                        # In between one hour check
                        now = datetime.now()
                        if(now.minute == 0):
                            oneHour_orderId, oneHour_buy_price, is_oneHour_trade_done = check_one_hour_trade()
                            is_pre_order_done = True
                        
                        cl = ll
                        ch = lh
                        sleep_until_next_30min()
                        df = get_30min_candles()
                        lc = last_close(df)
                        lo = last_open(df)
                        lh = last_high(df)
                        ll = last_low(df)
                        if((lc<=cl) and (lc-ll)>0.02):
                            sell_price = ll-0.05
                            # stop limit sell
                            # if(is_sol_available()):
                            status, order_time = place_stop_market_sell_order_30min(sell_price)
                            if(status == 'FILLED'):
                                stoploss = 0
                                is_shift_towards_30_min = False
                                # print('Sell Signal')
                                # print(sell_price)
                            else:
                                stoploss = ll-0.05
                            if(is_30min_wait_completed(order_time)):
                                is_15min_done = True
                        elif(lc<lo):
                            if(ll<cl and ((lh-ll)<(ch-cl)*1.5)):
                                stoploss = ll
                            else:
                                stoploss = cl
                            is_15min_done = True
                        else:
                            stoploss = cl
                            is_15min_done = True
                    elif(candle == 'Dragonfly doji' and lh>=ph and (candle_Typ == 'Bullish candle' or candle_Typ == 'Bearish candle' or candle_Typ == 'Doji')):
                        # In between one hour check
                        now = datetime.now()
                        if(now.minute == 0):
                            oneHour_orderId, oneHour_buy_price, is_oneHour_trade_done = check_one_hour_trade()
                            is_pre_order_done = True
                        
                        cl = ll
                        ch = lh
                        sleep_until_next_30min()
                        df = get_30min_candles()
                        lc = last_close(df)
                        lo = last_open(df)
                        lh = last_high(df)
                        ll = last_low(df)
                        if((lc<=cl) and (lc-ll)>0.02):
                            sell_price = ll-0.05
                            # stop limit sell
                            # if(is_sol_available()):
                            status, order_time = place_stop_market_sell_order_30min(sell_price)
                            if(status == 'FILLED'):
                                stoploss = 0
                                is_shift_towards_30_min = False
                                # print('Sell Signal')
                                # print(sell_price)
                            else:
                                stoploss = ll-0.05
                            if(is_30min_wait_completed(order_time)):
                                is_15min_done = True
                        elif(lc<lo):
                            if(ll<cl and ((lh-ll)<(ch-cl)*1.5)):
                                stoploss = ll
                            else:
                                stoploss = cl
                            is_15min_done = True
                        else:
                            stoploss = cl
                            is_15min_done = True
                    elif(candle == 'Gravestone Doji' and lh>=ph and (candle_Typ == 'Bullish candle' or candle_Typ == 'Bearish candle' or candle_Typ == 'Doji')):
                        # In between one hour check
                        now = datetime.now()
                        if(now.minute == 0):
                            oneHour_orderId, oneHour_buy_price, is_oneHour_trade_done = check_one_hour_trade()
                            is_pre_order_done = True
                        
                        cl = ll
                        ch = lh
                        sleep_until_next_30min()
                        df = get_30min_candles()
                        lc = last_close(df)
                        lo = last_open(df)
                        lh = last_high(df)
                        ll = last_low(df)
                        if((lc<=cl) and (lc-ll)>0.02):
                            sell_price = ll-0.05
                            # stop limit sell
                            # if(is_sol_available()):
                            status, order_time = place_stop_market_sell_order_30min(sell_price)
                            if(status == 'FILLED'):
                                stoploss = 0
                                is_shift_towards_30_min = False
                                # print('Sell Signal')
                                # print(sell_price)
                            else:
                                stoploss = ll-0.05
                            if(is_30min_wait_completed(order_time)):
                                is_15min_done = True
                        elif(lc<lo):
                            if(ll<cl and ((lh-ll)<(ch-cl)*1.5)):
                                stoploss = ll
                            else:
                                stoploss = cl
                            is_15min_done = True
                        else:
                            stoploss = cl
                            is_15min_done = True
                    elif(candle == 'Simple Doji' and lh>=ph and (candle_Typ == 'Bullish candle' or candle_Typ == 'Bearish candle' or candle_Typ == 'Doji')):
                        # In between one hour check
                        now = datetime.now()
                        if(now.minute == 0):
                            oneHour_orderId, oneHour_buy_price, is_oneHour_trade_done = check_one_hour_trade()
                            is_pre_order_done = True
                        
                        cl = ll
                        ch = lh
                        sleep_until_next_30min()
                        df = get_30min_candles()
                        lc = last_close(df)
                        lo = last_open(df)
                        lh = last_high(df)
                        ll = last_low(df)
                        if((lc<=cl) and (lc-ll)>0.02):
                            sell_price = ll-0.05
                            # stop limit sell
                            # if(is_sol_available()):
                            status, order_time = place_stop_market_sell_order_30min(sell_price)
                            if(status == 'FILLED'):
                                stoploss = 0
                                is_shift_towards_30_min = False
                                # print('Sell Signal')
                                # print(sell_price)
                            else:
                                stoploss = ll-0.05
                            if(is_30min_wait_completed(order_time)):
                                is_15min_done = True
                        elif(lc<lo):
                            if(ll<cl and ((lh-ll)<(ch-cl)*1.5)):
                                stoploss = ll
                            else:
                                stoploss = cl
                            is_15min_done = True
                        else:
                            stoploss = cl
                            is_15min_done = True
                    elif(candle == 'Reversal' and candle_Typ == 'Bullish candle'):
                        sell_price = (lo+lc)/2
                        # Stop limit sell
                        # if(is_sol_available()):
                        status, order_time = place_stop_market_sell_order_30min(sell_price)
                        if(status == 'FILLED'):
                            stoploss = 0
                            is_shift_towards_30_min = False
                            # print('Sell Signal')
                            # print(sell_price)
                        else:
                            stoploss = ll
                        if(is_30min_wait_completed(order_time)):
                            is_15min_done = True
                    elif(candle == 'Reversal' and candle_Typ == 'Bearish candle'):
                        sell_price = (ll-0.05)
                        # Stop limit sell
                        # if(is_sol_available()):
                        status, order_time = place_stop_market_sell_order_30min(sell_price)
                        if(status == 'FILLED'):
                            stoploss = 0
                            is_shift_towards_30_min = False
                            # print('Sell Signal')
                            # print(sell_price)
                        else:
                            stoploss = ll-0.05
                        if(is_30min_wait_completed(order_time)):
                            is_15min_done = True
                    elif(candle == 'Bearish Marubuzu' and candle_Typ == 'Bearish candle'):
                        if(ll<pl):
                            sell_price = ll-0.05
                            # Stop limit sell
                            # if(is_sol_available()):
                            status, order_time = place_stop_market_sell_order_30min(sell_price)
                            if(status == 'FILLED'):
                                stoploss = 0
                                is_shift_towards_30_min = False
                                # print('Sell Signal')
                                # print(sell_price)
                            else:
                                stoploss = ll-0.05
                            if(is_30min_wait_completed(order_time)):
                                is_15min_done = True
                        else:
                            sell_price = pl-0.05
                            # Stop limit sell
                            # if(is_sol_available()):
                            status, order_time = place_stop_market_sell_order_30min(sell_price)
                            if(status == 'FILLED'):
                                stoploss = 0
                                is_shift_towards_30_min = False
                                # print('Sell Signal')
                                # print(sell_price)
                            else:
                                stoploss = pl-0.05
                            if(is_30min_wait_completed(order_time)):
                                is_15min_done = True

            print('          ------------------')

# ----------------------------------------------------------------------------------------------------------------------
        # Buy decision for inbetween 30 minute signal
        now = datetime.now()
        if(is_buy_signal_found_between_30_min and (now.minute == 0 or now.minute == 30)):
            if(is_30_min_allow_buy()):
                print("     Buy decision for inbetween 30 minute signal")
                df5 = get_15min_candles()
                # stoploss_set = False
                # is_15min_done = False
                # print(candle_Typ)
                # print(candle)

                c = 2
                last_candle = df5.iloc[-c]
                lo = last_candle['Open']
                lc = last_candle['Close']
                lh = last_candle['High']
                ll = last_candle['Low']

                previous_candle_1 = df5.iloc[-(c+1)]
                po = previous_candle_1['Open']
                pc = previous_candle_1['Close']
                ph = previous_candle_1['High']
                pl = previous_candle_1['Low']

                if(lc>signal_high):
                    cp = current_SOL()
                    buy_price = cp
                    # Market buy
                    is_buy_signal_found_between_30_min = False
                    if market_buy_order(buy_price):
                        stoploss = pl
                        stoploss_orderId = place_stoploss_sell_order(stoploss, 1)
                        if stoploss_orderId:
                            stoploss_buy_price = buy_price
                            stoploss_low_price = stoploss
                        is_15_min_buy_done = True
                        # set_profit_1(df5,buy_price)
                elif(lh>signal_high and lc<signal_high):
                    buy_price = lh+0.05
                    # Stop limit buy
                    is_combination_of_15_and_30_min = True
                    is_buy_waiting_active = True
                    wh = buy_price
                    wl = signal_low
                    wo = signal_open
                    wc = signal_close
                    print(f"Buy waiting activated!\nwh:{wh}\nwl:{wl}")
                    is_combination_of_15_and_30_min = True
                    is_buy_signal_found_between_30_min = False
                elif(lh<signal_high):
                    if(ll<signal_low or (lc<lo and (lo-lc)>(signal_close-signal_open)/2)):
                        is_buy_signal_found_between_30_min = False
                    else:
                        is_combination_of_15_and_30_min = True
                        is_buy_waiting_active = True
                        wh = signal_high
                        wl = signal_low
                        wc = signal_close
                        wo = signal_open
                        print(f"Buy waiting activated!\nwh:{wh}\nwl:{wl}")
                        is_combination_of_15_and_30_min = True
                        is_buy_signal_found_between_30_min = False
            else:
                is_buy_signal_found_between_30_min = False
            print('          ------------------')
# ------------------------------------------------------------------------------------------------------------------
        # Buy condition when one hour candle is lower than ema's
        now = datetime.now()
        if is_oneHour_above_high:
            if(is_one_hour_candle_down()):
                print("Finding Buy signal...")
                df4 = get_15min_candles()
                candle_Typ = candle_type(df4)
                candle = detect_candlestick_pattern(df4)
                # stoploss_set = False
                # is_15min_done = False
                # print(candle_Typ)
                # print(candle)

                c = 2
                last_candle = df.iloc[-c]
                lo = last_candle['Open']
                lc = last_candle['Close']
                lh = last_candle['High']
                ll = last_candle['Low']

                previous_candle_1 = df.iloc[-(c+1)]
                po = previous_candle_1['Open']
                pc = previous_candle_1['Close']
                ph = previous_candle_1['High']
                pl = previous_candle_1['Low']

                previous_candle_2 = df.iloc[-(c+2)]
                po2 = previous_candle_2['Open']
                pc2 = previous_candle_2['Close']
                ph2 = previous_candle_2['High']
                pl2 = previous_candle_2['Low']
            # ------------------------------------------------------------------------------------------------------

                if(is_15_min_signal_found and (now.minute == 15 or now.minute == 45)):
                    is_15_min_signal_found = False
                    if(candle == 'Right Hammer' and candle_Typ == 'Bearish candle'):
                        ch = lh
                        cl = ll
                        sleep_until_next_15min()
                        df = get_15min_candles()
                        lc = last_close(df)
                        lh = last_high(df)
                        lo = last_open(df)
                        ll = last_low(df)
                        if((lc>=ch) and (lh-lc)>0.02 and is_30_min_allow_buy()):
                            buy_price = lh+0.05
                            # stop limit buy
                            print("All buy signals done. We are going to place buy order!")
                            status, order_time = place_stop_market_buy_order(buy_price)
                            if status:
                                if(status == 'FILLED'):
                                    stoploss = cl
                                    stoploss_set = True
                                    stoploss_orderId = place_stoploss_sell_order(stoploss, 1)
                                    if stoploss_orderId:
                                        stoploss_buy_price = buy_price
                                        stoploss_low_price = stoploss
                                    is_15_min_buy_done = True
                                    # print('Buy Signal')
                                    # print(buy_price)
                                else:
                                    is_buy_waiting_active = True
                                    wh = buy_price
                                    wl = ll
                                    wc = lc
                                    wo = lo
                                    print(f"Buy waiting activated!\nwh:{wh}\nwl:{wl}")
                                    is_combination_of_15_and_30_min = True
                                if(is_15min_wait_completed(order_time)):
                                    is_15min_done = True
                        elif(lc>lo and (lh-lc)>0.02 and is_30_min_allow_buy()):
                            is_one_candle_wait_activated = True
                            is_combination_of_15_and_30_min = True
                            print("One candle wait activated!")
                        # else:
                        #     is_15min_done = True
                            # print('--------------------------------------')
                            # continue
                    elif(candle == 'Inverted hammer' and candle_Typ == 'Bearish candle'):
                        ch = lh
                        cl = ll
                        sleep_until_next_15min()
                        df = get_15min_candles()
                        lc = last_close(df)
                        lh = last_high(df)
                        lo = last_open(df)
                        ll = last_low(df)
                        if((lc>=ch) and (lh-lc)>0.02 and is_30_min_allow_buy()):
                            buy_price = lh+0.05
                            # stop limit buy
                            print("All buy signals done. We are going to place buy order!")
                            status, order_time = place_stop_market_buy_order(buy_price)
                            if status:
                                if(status == 'FILLED'):
                                    stoploss = cl
                                    stoploss_set = True
                                    stoploss_orderId = place_stoploss_sell_order(stoploss, 1)
                                    if stoploss_orderId:
                                        stoploss_buy_price = buy_price
                                        stoploss_low_price = stoploss
                                    is_15_min_buy_done = True
                                    # print('Buy Signal')
                                    # print(buy_price)
                                else:
                                    is_buy_waiting_active = True
                                    wh = buy_price
                                    wl = ll
                                    wc = lc
                                    wo = lo
                                    print(f"Buy waiting activated!\nwh:{wh}\nwl:{wl}")
                                    is_combination_of_15_and_30_min = True
                                if(is_15min_wait_completed(order_time)):
                                    is_15min_done = True
                        elif(lc>lo and (lh-lc)>0.02 and is_30_min_allow_buy()):
                            is_one_candle_wait_activated = True
                            is_combination_of_15_and_30_min = True
                            print("One candle wait activated!")
                        # else:
                        #     is_15min_done = True
                            # print('--------------------------------------')
                            # continue
                    elif(candle == 'Spinning Top' and (candle_Typ == 'Bullish candle' or candle_Typ == 'Bearish candle')):
                        ch = lh
                        cl = ll
                        sleep_until_next_15min()
                        df = get_15min_candles()
                        lc = last_close(df)
                        lh = last_high(df)
                        lo = last_open(df)
                        ll = last_low(df)
                        if((lc>=ch) and (lh-lc)>0.02 and is_30_min_allow_buy()):
                            buy_price = lh+0.05
                            # stop limit buy
                            print("All buy signals done. We are going to place buy order!")
                            status, order_time = place_stop_market_buy_order(buy_price)
                            if status:
                                if(status == 'FILLED'):
                                    stoploss = cl
                                    stoploss_set = True
                                    stoploss_orderId = place_stoploss_sell_order(stoploss, 1)
                                    if stoploss_orderId:
                                        stoploss_buy_price = buy_price
                                        stoploss_low_price = stoploss
                                    is_15_min_buy_done = True
                                    # print('Buy Signal')
                                    # print(buy_price)
                                else:
                                    is_buy_waiting_active = True
                                    wh = buy_price
                                    wl = ll
                                    wc = lc
                                    wo = lo
                                    print(f"Buy waiting activated!\nwh:{wh}\nwl:{wl}")
                                    is_combination_of_15_and_30_min = True
                                if(is_15min_wait_completed(order_time)):
                                    is_15min_done = True
                        elif(lc>lo and (lh-lc)>0.02 and is_30_min_allow_buy()):
                            is_one_candle_wait_activated = True
                            is_combination_of_15_and_30_min = True
                            print("One candle wait activated!")
                        # else:
                        #     is_15min_done = True
                    elif(candle == 'Dragonfly doji' and (candle_Typ == 'Bullish candle' or candle_Typ == 'Bearish candle' or candle_Typ == 'Doji') and ll<=pl):
                        ch = lh
                        cl = ll
                        sleep_until_next_15min()
                        df = get_15min_candles()
                        lc = last_close(df)
                        lh = last_high(df)
                        lo = last_open(df)
                        ll = last_low(df)
                        if((lc>=ch) and (lh-lc)>0.02 and is_30_min_allow_buy()):
                            buy_price = lh+0.05
                            # stop limit buy
                            print("All buy signals done. We are going to place buy order!")
                            status, order_time = place_stop_market_buy_order(buy_price)
                            if status:
                                if(status == 'FILLED'):
                                    stoploss = cl
                                    stoploss_set = True
                                    stoploss_orderId = place_stoploss_sell_order(stoploss, 1)
                                    if stoploss_orderId:
                                        stoploss_buy_price = buy_price
                                        stoploss_low_price = stoploss
                                    is_15_min_buy_done = True
                                    # print('Buy Signal')
                                    # print(buy_price)
                                else:
                                    is_buy_waiting_active = True
                                    wh = buy_price
                                    wl = ll
                                    wc = lc
                                    wo = lo
                                    print(f"Buy waiting activated!\nwh:{wh}\nwl:{wl}")
                                    is_combination_of_15_and_30_min = True
                                if(is_15min_wait_completed(order_time)):
                                    is_15min_done = True
                        elif(lc>lo and (lh-lc)>0.02 and is_30_min_allow_buy()):
                            is_one_candle_wait_activated = True
                            is_combination_of_15_and_30_min = True
                            print("One candle wait activated!")
                        # else:
                        #     is_15min_done = True
                            # print('--------------------------------------')
                            # continue
                    elif(candle == 'Gravestone Doji' and ll<=pl and (candle_Typ == 'Bullish candle' or candle_Typ == 'Bearish candle' or candle_Typ == 'Doji')):
                        ch = lh
                        cl = ll
                        sleep_until_next_15min()
                        df = get_15min_candles()
                        lc = last_close(df)
                        lh = last_high(df)
                        lo = last_open(df)
                        ll = last_low(df)
                        if((lc>=ch) and (lh-lc)>0.02 and is_30_min_allow_buy()):
                            buy_price = lh+0.05
                            # stop limit buy
                            print("All buy signals done. We are going to place buy order!")
                            status, order_time = place_stop_market_buy_order(buy_price)
                            if status:
                                if(status == 'FILLED'):
                                    stoploss = cl
                                    stoploss_set = True
                                    stoploss_orderId = place_stoploss_sell_order(stoploss, 1)
                                    if stoploss_orderId:
                                        stoploss_buy_price = buy_price
                                        stoploss_low_price = stoploss
                                    is_15_min_buy_done = True
                                    # print('Buy Signal')
                                    # print(buy_price)
                                else:
                                    is_buy_waiting_active = True
                                    wh = buy_price
                                    wl = ll
                                    wc = lc
                                    wo = lo
                                    print(f"Buy waiting activated!\nwh:{wh}\nwl:{wl}")
                                    is_combination_of_15_and_30_min = True
                                if(is_15min_wait_completed(order_time)):
                                    is_15min_done = True
                        elif(lc>lo and (lh-lc)>0.02 and is_30_min_allow_buy()):
                            is_one_candle_wait_activated = True
                            is_combination_of_15_and_30_min = True
                            print("One candle wait activated!")
                        # else:
                        #     is_15min_done = True
                            # print('--------------------------------------')
                            # continue
                    elif(candle == 'Simple Doji' and ll<=pl and (candle_Typ == 'Bullish candle' or candle_Typ == 'Bearish candle' or candle_Typ == 'Doji')):
                        ch = lh
                        cl = ll
                        sleep_until_next_15min()
                        df = get_15min_candles()
                        lc = last_close(df)
                        lh = last_high(df)
                        lo = last_open(df)
                        ll = last_low(df)
                        if((lc>=ch) and (lh-lc)>0.02 and is_30_min_allow_buy()):
                            buy_price = lh+0.05
                            # stop limit buy
                            print("All buy signals done. We are going to place buy order!")
                            status, order_time = place_stop_market_buy_order(buy_price)
                            if status:
                                if(status == 'FILLED'):
                                    stoploss = cl
                                    stoploss_set = True
                                    stoploss_orderId = place_stoploss_sell_order(stoploss, 1)
                                    if stoploss_orderId:
                                        stoploss_buy_price = buy_price
                                        stoploss_low_price = stoploss
                                    is_15_min_buy_done = True
                                    # print('Buy Signal')
                                    # print(buy_price)
                                else:
                                    is_buy_waiting_active = True
                                    wh = buy_price
                                    wl = ll
                                    wc = lc
                                    wo = lo
                                    print(f"Buy waiting activated!\nwh:{wh}\nwl:{wl}")
                                    is_combination_of_15_and_30_min = True
                                if(is_15min_wait_completed(order_time)):
                                    is_15min_done = True
                        elif(lc>lo and (lh-lc)>0.02 and is_30_min_allow_buy()):
                            is_one_candle_wait_activated = True
                            is_combination_of_15_and_30_min = True
                            print("One candle wait activated!")
                        # else:
                        #     is_15min_done = True
                            # print('--------------------------------------')
                            # continue
                    elif(candle == 'Bullish Engulfing' and candle_Typ == 'Bullish candle'):
                        if(lh>ph):
                            buy_price = (lh+0.05)
                            # Stop market buy
                            signal_high = buy_price
                            signal_low = ll
                            signal_open = lo
                            signal_close = lc
                        else:
                            buy_price = (ph+0.05)
                            # Stop market buy
                            signal_high = buy_price
                            signal_low = ll
                            signal_open = lo
                            signal_close = lc
                        is_buy_signal_found_between_30_min = True
                        signal_candle = candle
                        print("Signal found between 30 minutes")
                    elif(candle == 'Right Hammer' and candle_Typ == 'Bullish candle'):
                        if((lh-lc)<0.02):
                            buy_price = lh+(lc-lo)/3
                            # stop limit buy
                            signal_high = buy_price
                            signal_low = ll
                            signal_open = lo
                            signal_close = lc
                        else:
                            buy_price = (lh+0.05)
                            # Stop limit order
                            signal_high = buy_price
                            signal_low = ll
                            signal_open = lo
                            signal_close = lc
                        is_buy_signal_found_between_30_min = True
                        signal_candle = candle
                        print("Signal found between 30 minutes")
                    elif(candle == 'Inverted hammer' and candle_Typ == 'Bullish candle'):
                        buy_price = (lh+0.05)
                        signal_high = buy_price
                        signal_low = ll
                        signal_open = lo
                        signal_close = lc
                        is_buy_signal_found_between_30_min = True
                        signal_candle = candle
                        print("Signal found between 30 minutes")
                    elif(candle == 'Reversal' and candle_Typ == 'Bullish candle'):
                        buy_price = (lh+0.05)
                        signal_high = buy_price
                        signal_low = ll
                        signal_open = lo
                        signal_close = lc
                        is_buy_signal_found_between_30_min = True
                        signal_candle = candle
                        print("Signal found between 30 minutes")
                    elif(candle == 'Reversal' and candle_Typ == 'Bearish candle'):
                        buy_price = (lo+lc)/2
                        signal_high = buy_price
                        signal_low = ll
                        signal_open = lo
                        signal_close = lc
                        is_buy_signal_found_between_30_min = True
                        signal_candle = candle
                        print("Signal found between 30 minutes")
                    elif(candle == 'Bullish Marubuzu' and candle_Typ == 'Bullish candle'):
                        if(lh>ph):
                            buy_price = (lh+0.05)
                            # Stop market buy
                            signal_high = buy_price
                            signal_low = ll
                            signal_open = lo
                            signal_close = lc
                        else:
                            buy_price = (ph+0.05)
                            # Stop market buy
                            signal_high = buy_price
                            signal_low = ll
                            signal_open = lo
                            signal_close = lc
                        is_buy_signal_found_between_30_min = True
                        signal_candle = candle
                        print("Signal found between 30 minutes")
                # ---------------------------------------------------------------------------------------------------

                elif(is_15_min_signal_found and (now.minute == 0 or now.minute == 30)):
                    is_15_min_signal_found = False
                    if(candle == 'Bullish Engulfing' and candle_Typ == 'Bullish candle' and is_30_min_allow_buy()):
                        if(lh>ph):
                            buy_price = (lh+0.05)
                            # Stop market buy
                            print("All buy signals done. We are going to place buy order!")
                            status, order_time = place_stop_market_buy_order(buy_price)
                            if status:
                                if(status == 'FILLED'):
                                    if(pl<ll):
                                        stoploss = pl
                                        stoploss_set = True
                                    else:
                                        stoploss = ll
                                        stoploss_set = True
                                    # print('Buy Signal')
                                    # print(buy_price)
                                    stoploss_orderId = place_stoploss_sell_order(stoploss, 1)
                                    if stoploss_orderId:
                                        stoploss_buy_price = buy_price
                                        stoploss_low_price = stoploss
                                    is_15_min_buy_done = True
                                else:
                                    is_buy_waiting_active = True
                                    wh = buy_price
                                    wl = ll
                                    wc = lc
                                    wo = lo
                                    print(f"Buy waiting activated!\nwh:{wh}\nwl:{wl}")
                                    is_combination_of_15_and_30_min = True
                                if(is_15min_wait_completed(order_time)):
                                    is_15min_done = True
                        else:
                            buy_price = (ph+0.05)
                            # Stop market buy
                            print("All buy signals done. We are going to place buy order!")
                            status, order_time = place_stop_market_buy_order(buy_price)
                            if status:
                                if(status == 'FILLED'):
                                    if(pl<ll):
                                        stoploss = pl
                                        stoploss_set = True
                                    else:
                                        stoploss = ll
                                        stoploss_set = True
                                    # print('Buy Signal')
                                    # print(buy_price)
                                    stoploss_orderId = place_stoploss_sell_order(stoploss, 1)
                                    if stoploss_orderId:
                                        stoploss_buy_price = buy_price
                                        stoploss_low_price = stoploss
                                    is_15_min_buy_done = True
                                else:
                                    is_buy_waiting_active = True
                                    wh = buy_price
                                    wl = ll
                                    wc = lc
                                    wo = lo
                                    print(f"Buy waiting activated!\nwh:{wh}\nwl:{wl}")
                                    is_combination_of_15_and_30_min = True
                                if(is_15min_wait_completed(order_time)):
                                    is_15min_done = True
                    elif(candle == 'Right Hammer' and candle_Typ == 'Bullish candle' and is_30_min_allow_buy()):
                        if((lh-lc)<0.02):
                            buy_price = lh+(lc-lo)/3
                            # stop limit buy
                            print("All buy signals done. We are going to place buy order!")
                            status, order_time = place_stop_market_buy_order(buy_price)
                            if status:
                                if(status == 'FILLED'):
                                    stoploss = ll
                                    stoploss_set = True
                                    stoploss_orderId = place_stoploss_sell_order(stoploss, 1)
                                    if stoploss_orderId:
                                        stoploss_buy_price = buy_price
                                        stoploss_low_price = stoploss
                                    is_15_min_buy_done = True
                                    # print('Buy Signal')
                                    # print(buy_price)
                                else:
                                    is_buy_waiting_active = True
                                    wh = buy_price
                                    wl = ll
                                    wc = lc
                                    wo = lo
                                    print(f"Buy waiting activated!\nwh:{wh}\nwl:{wl}")
                                    is_combination_of_15_and_30_min = True
                                if(is_15min_wait_completed(order_time)):
                                    is_15min_done = True
                        else:
                            buy_price = (lh+0.05)
                            # Stop limit order
                            print("All buy signals done. We are going to place buy order!")
                            status, order_time = place_stop_market_buy_order(buy_price)
                            if status:
                                if(status == 'FILLED'):
                                    stoploss = ll
                                    stoploss_set = True
                                    stoploss_orderId = place_stoploss_sell_order(stoploss, 1)
                                    if stoploss_orderId:
                                        stoploss_buy_price = buy_price
                                        stoploss_low_price = stoploss
                                    is_15_min_buy_done = True
                                    # print('Buy Signal')
                                    # print(buy_price)
                                else:
                                    is_buy_waiting_active = True
                                    wh = buy_price
                                    wl = ll
                                    wc = lc
                                    wo = lo
                                    print(f"Buy waiting activated!\nwh:{wh}\nwl:{wl}")
                                    is_combination_of_15_and_30_min = True
                                if(is_15min_wait_completed(order_time)):
                                    is_15min_done = True
                    elif(candle == 'Inverted hammer' and candle_Typ == 'Bullish candle' and is_30_min_allow_buy()):
                        buy_price = (lh+0.05)
                        # Stop limit buy
                        print("All buy signals done. We are going to place buy order!")
                        status, order_time = place_stop_market_buy_order(buy_price)
                        if status:
                            if(status == 'FILLED'):
                                stoploss = ll
                                stoploss_set = True
                                stoploss_orderId = place_stoploss_sell_order(stoploss, 1)
                                if stoploss_orderId:
                                    stoploss_buy_price = buy_price
                                    stoploss_low_price = stoploss
                                is_15_min_buy_done = True
                                # print('Buy Signal')
                                # print(buy_price)
                            else:
                                is_buy_waiting_active = True
                                wh = buy_price
                                wl = ll
                                wc = lc
                                wo = lo
                                print(f"Buy waiting activated!\nwh:{wh}\nwl:{wl}")
                                is_combination_of_15_and_30_min = True
                            if(is_15min_wait_completed(order_time)):
                                is_15min_done = True
                    elif(candle == 'Reversal' and candle_Typ == 'Bullish candle' and is_30_min_allow_buy()):
                        buy_price = (lh+0.05)
                        # Stop limit buy
                        print("All buy signals done. We are going to place buy order!")
                        status, order_time = place_stop_market_buy_order(buy_price)
                        if status:
                            if(status == 'FILLED'):
                                stoploss = ll
                                stoploss_set = True
                                stoploss_orderId = place_stoploss_sell_order(stoploss, 1)
                                if stoploss_orderId:
                                    stoploss_buy_price = buy_price
                                    stoploss_low_price = stoploss
                                is_15_min_buy_done = True
                                # print('Buy Signal')
                                # print(buy_price)
                            # else:
                            #     is_buy_waiting_active = True
                            #     wh = buy_price
                            #     wl = ll
                                # print(f"Buy waiting activated!\nwh:{wh}\nwl:{wl}")
                            if(is_15min_wait_completed(order_time)):
                                is_15min_done = True
                    elif(candle == 'Reversal' and candle_Typ == 'Bearish candle' and is_30_min_allow_buy()):
                        buy_price = (lo+lc)/2
                        # Stop limit buy
                        print("All buy signals done. We are going to place buy order!")
                        status, order_time = place_stop_market_buy_order(buy_price)
                        if status:
                            if(status == 'FILLED'):
                                stoploss = ll
                                stoploss_set = True
                                stoploss_orderId = place_stoploss_sell_order(stoploss, 1)
                                if stoploss_orderId:
                                    stoploss_buy_price = buy_price
                                    stoploss_low_price = stoploss
                                is_15_min_buy_done = True
                                # print('Buy Signal')
                                # print(buy_price)
                            # else:
                            #     is_buy_waiting_active = True
                            #     wh = lh
                            #     wl = ll
                            #     print(f"Buy waiting activated!\nwh:{wh}\nwl:{wl}")
                            if(is_15min_wait_completed(order_time)):
                                is_15min_done = True
                    elif(candle == 'Bullish Marubuzu' and candle_Typ == 'Bullish candle' and is_30_min_allow_buy()):
                        if(lh>ph):
                            buy_price = (lh+0.05)
                            # Stop market buy
                            print("All buy signals done. We are going to place buy order!")
                            status, order_time = place_stop_market_buy_order(buy_price)
                            if status:
                                if(status == 'FILLED'):
                                    if(pl<ll):
                                        stoploss = pl
                                        stoploss_set = True
                                    else:
                                        stoploss = ll
                                        stoploss_set = True
                                    # print('Buy Signal')
                                    # print(buy_price)
                                    stoploss_orderId = place_stoploss_sell_order(stoploss, 1)
                                    if stoploss_orderId:
                                        stoploss_buy_price = buy_price
                                        stoploss_low_price = stoploss
                                    is_15_min_buy_done = True
                                else:
                                    is_buy_waiting_active = True
                                    wh = buy_price
                                    wl = ll
                                    wc = lc
                                    wo = lo
                                    print(f"Buy waiting activated!\nwh:{wh}\nwl:{wl}")
                                    is_combination_of_15_and_30_min = True
                                if(is_15min_wait_completed(order_time)):
                                    is_15min_done = True
                        else:
                            buy_price = (ph+0.05)
                            # Stop market buy
                            print("All buy signals done. We are going to place buy order!")
                            status, order_time = place_stop_market_buy_order(buy_price)
                            if status:
                                if(status == 'FILLED'):
                                    if(pl<ll):
                                        stoploss = pl
                                        stoploss_set = True
                                    else:
                                        stoploss = ll
                                        stoploss_set = True
                                    # print('Buy Signal')
                                    # print(buy_price)
                                    stoploss_orderId = place_stoploss_sell_order(stoploss, 1)
                                    if stoploss_orderId:
                                        stoploss_buy_price = buy_price
                                        stoploss_low_price = stoploss
                                    is_15_min_buy_done = True
                                else:
                                    is_buy_waiting_active = True
                                    wh = buy_price
                                    wl = ll
                                    wc = lc
                                    wo = lo
                                    print(f"Buy waiting activated!\nwh:{wh}\nwl:{wl}")
                                    is_combination_of_15_and_30_min = True
                                if(is_15min_wait_completed(order_time)):
                                    is_15min_done = True
                    elif(candle == 'Right Hammer' and candle_Typ == 'Bearish candle'):
                        # In between one hour check
                        if(now.minute == 0):
                            oneHour_orderId, oneHour_buy_price, is_oneHour_trade_done = check_one_hour_trade()
                            is_pre_order_done = True
                            
                        ch = lh
                        cl = ll
                        sleep_until_next_15min()
                        df = get_15min_candles()
                        lc = last_close(df)
                        lh = last_high(df)
                        lo = last_open(df)
                        ll = last_low(df)
                        if((lc>=ch) and (lh-lc)>0.02):
                            buy_price = lh+0.05
                            signal_high = buy_price
                            signal_low = ll
                            signal_open = lo
                            signal_close = lc
                            is_buy_signal_found_between_30_min = True
                            signal_candle = candle
                            print("Signal found between 30 minutes")
                        elif(lc>lo and (lh-lc)>0.02):
                            s_high = None
                            if(ch>=lh):
                                s_high = ch
                            elif(lh>ch):
                                s_high = lh
                            buy_price = s_high
                            signal_high = buy_price
                            signal_low = ll
                            signal_open = lo
                            signal_close = lc
                            is_buy_signal_found_between_30_min = True
                            print("Signal found between 30 minutes")
                    elif(candle == 'Inverted hammer' and candle_Typ == 'Bearish candle'):
                        # In between one hour check
                        if(now.minute == 0):
                            oneHour_orderId, oneHour_buy_price, is_oneHour_trade_done = check_one_hour_trade()
                            is_pre_order_done = True
                        
                        ch = lh
                        cl = ll
                        sleep_until_next_15min()
                        df = get_15min_candles()
                        lc = last_close(df)
                        lh = last_high(df)
                        lo = last_open(df)
                        ll = last_low(df)
                        if((lc>=ch) and (lh-lc)>0.02):
                            buy_price = lh+0.05
                            signal_high = buy_price
                            signal_low = ll
                            signal_open = lo
                            signal_close = lc
                            is_buy_signal_found_between_30_min = True
                            signal_candle = candle
                            print("Signal found between 30 minutes")
                        elif(lc>lo and (lh-lc)>0.02):
                            s_high = None
                            if(ch>=lh):
                                s_high = ch
                            elif(lh>ch):
                                s_high = lh
                            buy_price = s_high
                            signal_high = buy_price
                            signal_low = ll
                            signal_open = lo
                            signal_close = lc
                            is_buy_signal_found_between_30_min = True
                            print("Signal found between 30 minutes")
                    elif(candle == 'Spinning Top' and (candle_Typ == 'Bullish candle' or candle_Typ == 'Bearish candle')):
                        # In between one hour check
                        if(now.minute == 0):
                            oneHour_orderId, oneHour_buy_price, is_oneHour_trade_done = check_one_hour_trade()
                            is_pre_order_done = True
                        
                        ch = lh
                        cl = ll
                        sleep_until_next_15min()
                        df = get_15min_candles()
                        lc = last_close(df)
                        lh = last_high(df)
                        lo = last_open(df)
                        ll = last_low(df)
                        if((lc>=ch) and (lh-lc)>0.02):
                            buy_price = lh+0.05
                            signal_high = buy_price
                            signal_low = ll
                            signal_open = lo
                            signal_close = lc
                            is_buy_signal_found_between_30_min = True
                            signal_candle = candle
                            print("Signal found between 30 minutes")
                        elif(lc>lo and (lh-lc)>0.02):
                            s_high = None
                            if(ch>=lh):
                                s_high = ch
                            elif(lh>ch):
                                s_high = lh
                            buy_price = s_high
                            signal_high = buy_price
                            signal_low = ll
                            signal_open = lo
                            signal_close = lc
                            is_buy_signal_found_between_30_min = True
                            print("Signal found between 30 minutes")
                    elif(candle == 'Dragonfly doji' and (candle_Typ == 'Bullish candle' or candle_Typ == 'Bearish candle' or candle_Typ == 'Doji') and ll<=pl):
                        # In between one hour check
                        if(now.minute == 0):
                            oneHour_orderId, oneHour_buy_price, is_oneHour_trade_done = check_one_hour_trade()
                            is_pre_order_done = True
                        
                        ch = lh
                        cl = ll
                        sleep_until_next_15min()
                        df = get_15min_candles()
                        lc = last_close(df)
                        lh = last_high(df)
                        lo = last_open(df)
                        ll = last_low(df)
                        if((lc>=ch) and (lh-lc)>0.02):
                            buy_price = lh+0.05
                            signal_high = buy_price
                            signal_low = ll
                            signal_open = lo
                            signal_close = lc
                            is_buy_signal_found_between_30_min = True
                            signal_candle = candle
                            print("Signal found between 30 minutes")
                        elif(lc>lo and (lh-lc)>0.02):
                            s_high = None
                            if(ch>=lh):
                                s_high = ch
                            elif(lh>ch):
                                s_high = lh
                            buy_price = s_high
                            signal_high = buy_price
                            signal_low = ll
                            signal_open = lo
                            signal_close = lc
                            is_buy_signal_found_between_30_min = True
                            print("Signal found between 30 minutes")
                    elif(candle == 'Gravestone Doji' and ll<=pl and (candle_Typ == 'Bullish candle' or candle_Typ == 'Bearish candle' or candle_Typ == 'Doji')):
                        # In between one hour check
                        if(now.minute == 0):
                            oneHour_orderId, oneHour_buy_price, is_oneHour_trade_done = check_one_hour_trade()
                            is_pre_order_done = True
                        
                        ch = lh
                        cl = ll
                        sleep_until_next_15min()
                        df = get_15min_candles()
                        lc = last_close(df)
                        lh = last_high(df)
                        lo = last_open(df)
                        ll = last_low(df)
                        if((lc>=ch) and (lh-lc)>0.02):
                            buy_price = lh+0.05
                            signal_high = buy_price
                            signal_low = ll
                            signal_open = lo
                            signal_close = lc
                            is_buy_signal_found_between_30_min = True
                            signal_candle = candle
                            print("Signal found between 30 minutes")
                        elif(lc>lo and (lh-lc)>0.02):
                            s_high = None
                            if(ch>=lh):
                                s_high = ch
                            elif(lh>ch):
                                s_high = lh
                            buy_price = s_high
                            signal_high = buy_price
                            signal_low = ll
                            signal_open = lo
                            signal_close = lc
                            is_buy_signal_found_between_30_min = True
                            print("Signal found between 30 minutes")
                    elif(candle == 'Simple Doji' and ll<=pl and (candle_Typ == 'Bullish candle' or candle_Typ == 'Bearish candle' or candle_Typ == 'Doji')):
                        # In between one hour check
                        if(now.minute == 0):
                            oneHour_orderId, oneHour_buy_price, is_oneHour_trade_done = check_one_hour_trade()
                            is_pre_order_done = True
                        
                        ch = lh
                        cl = ll
                        sleep_until_next_15min()
                        df = get_15min_candles()
                        lc = last_close(df)
                        lh = last_high(df)
                        lo = last_open(df)
                        ll = last_low(df)
                        if((lc>=ch) and (lh-lc)>0.02):
                            buy_price = lh+0.05
                            signal_high = buy_price
                            signal_low = ll
                            signal_open = lo
                            signal_close = lc
                            is_buy_signal_found_between_30_min = True
                            signal_candle = candle
                            print("Signal found between 30 minutes")
                        elif(lc>lo and (lh-lc)>0.02):
                            s_high = None
                            if(ch>=lh):
                                s_high = ch
                            elif(lh>ch):
                                s_high = lh
                            buy_price = s_high
                            signal_high = buy_price
                            signal_low = ll
                            signal_open = lo
                            signal_close = lc
                            is_buy_signal_found_between_30_min = True
                            print("Signal found between 30 minutes")

                else:
                    print("No signal Found!")
                print('          ------------------')

# -------------------------------------------------------------------------------------------------------------------
        # Setup for 1 hour candle
        now = datetime.now()
        if ((now.minute == 0 or now.minute == 15 or now.minute == 30) and is_oneHour_done == False):
            is_oneHour_done = True
            if(is_15_min_buy_done):
                hours_after_15_min_buy = hours_after_15_min_buy + 1
            if(is_oneHour_trade_done and is_pre_order_done == False):
                status = get_order_status(oneHour_orderId)
                if(status == 'FILLED' or status == 'CANCELED'):
                    is_oneHour_trade_done = False
                    is_shift_towards_30_min = False
                elif(status != 'FILLED'):
                    cancel_order(oneHour_orderId)
                    is_oneHour_trade_done = False
                # oneHour_trade_time = None
            if(is_one_hour_signal_found):
                is_one_hour_signal_found = False
                one_h = None
            print('             1 hour setup')
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
            # emaBuy_status = emaBuy_buy_status(df2)
            # down_percentage = down_percentage_check(df2)
            signal = None
            # stoploss_set = False
            # is_15min_done = False

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
            # -------------------------------------------------------------------------------------------------------
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
                if (signal == 'Buy' and can_one_hour_buy):
                    if(lh>ph):
                        buy_price = (lh+0.08)
                        # Stop market buy
                        oneHour_orderId = place_one_hour_stop_limit_buy_order(buy_price)
                        if oneHour_orderId:
                            oneHour_buy_price = buy_price
                            is_oneHour_trade_done = True
                            if(stoploss<ll):
                                stoploss = ll
                        elif(is_15_min_buy_done):
                            is_one_hour_signal_found = True
                            one_h = buy_price
                        # print('Buy Signal')
                        # print(buy_price)
                    else:
                        buy_price = (ph+0.08)
                        # Stop market buy
                        oneHour_orderId = place_one_hour_stop_limit_buy_order(buy_price)
                        if oneHour_orderId:
                            oneHour_buy_price = buy_price
                            is_oneHour_trade_done = True
                            if(stoploss<ll):
                                stoploss = ll
                        elif(is_15_min_buy_done):
                            is_one_hour_signal_found = True
                            one_h = buy_price
                        # print('Buy Signal')
                        # print(buy_price)

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
                if (signal == 'Buy' and can_one_hour_buy):
                    if((lh-lc)<0.02):
                        buy_price = lh+(lc-lo)/3
                        # stop limit buy
                        oneHour_orderId = place_one_hour_stop_limit_buy_order(buy_price)
                        if oneHour_orderId:
                            oneHour_buy_price = buy_price
                            is_oneHour_trade_done = True
                            if(stoploss<ll):
                                stoploss = ll
                        elif(is_15_min_buy_done):
                            is_one_hour_signal_found = True
                            one_h = buy_price
                        # print('Buy Signal')
                        # print(buy_price)
                    else:
                        buy_price = (lh+0.08)
                        # Stop limit order
                        oneHour_orderId = place_one_hour_stop_limit_buy_order(buy_price)
                        if oneHour_orderId:
                            oneHour_buy_price = buy_price
                            is_oneHour_trade_done = True
                            if(stoploss<ll):
                                stoploss = ll
                        elif(is_15_min_buy_done):
                            is_one_hour_signal_found = True
                            one_h = buy_price
                        # print('Buy Signal')
                        # print(buy_price)

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
                    buy_price = (lh+0.08)
                    # Stop limit buy
                    oneHour_orderId = place_one_hour_stop_limit_buy_order(buy_price)
                    if oneHour_orderId:
                        oneHour_buy_price = buy_price
                        is_oneHour_trade_done = True
                        if(stoploss<ll):
                            stoploss = ll
                    elif(is_15_min_buy_done):
                        is_one_hour_signal_found = True
                        one_h = buy_price
                    # print('Buy Signal')
                    # print(buy_price)

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
                    buy_price = (lh+0.08)
                    # Stop limit buy
                    oneHour_orderId = place_one_hour_stop_limit_buy_order(buy_price)
                    if oneHour_orderId:
                        oneHour_buy_price = buy_price
                        is_oneHour_trade_done = True
                        if(stoploss<ll):
                            stoploss = ll
                    elif(is_15_min_buy_done):
                        is_one_hour_signal_found = True
                        one_h = buy_price
                    # print('Buy Signal')
                    # print(buy_price)

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
                    buy_price = (lh+0.08)
                    # Stop limit buy
                    oneHour_orderId = place_one_hour_stop_limit_buy_order(buy_price)
                    if oneHour_orderId:
                        oneHour_buy_price = buy_price
                        is_oneHour_trade_done = True
                        if(stoploss<ll):
                            stoploss = ll
                    elif(is_15_min_buy_done):
                        is_one_hour_signal_found = True
                        one_h = buy_price
                    # print('Buy Signal')
                    # print(buy_price)

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
                        buy_price = (lh+0.08)
                        # Stop market buy
                        oneHour_orderId = place_one_hour_stop_limit_buy_order(buy_price)
                        if oneHour_orderId:
                            oneHour_buy_price = buy_price
                            is_oneHour_trade_done = True
                            if(stoploss<ll):
                                stoploss = ll
                        elif(is_15_min_buy_done):
                            is_one_hour_signal_found = True
                            one_h = buy_price
                        # print('Buy Signal')
                        # print(buy_price)
                    else:
                        buy_price = (ph+0.08)
                        # Stop market buy
                        oneHour_orderId = place_one_hour_stop_limit_buy_order(buy_price)
                        if oneHour_orderId:
                            oneHour_buy_price = buy_price
                            is_oneHour_trade_done = True
                            if(stoploss<ll):
                                stoploss = ll
                        elif(is_15_min_buy_done):
                            is_one_hour_signal_found = True
                            one_h = buy_price
                        # print('Buy Signal')
                        # print(buy_price)
                    
            # Second Condition
            if(ema_100<ema and trend == 'Down_trend' and ema_100 < ema_buy and 
                ((ema_100<=lh and ema_100>=ll) or (ll<=((ema+ema_100)/2 -((ema-ema_100)/6)))) and (lc<(ema+ema_100)/2 or lo<(ema+ema_100)/2) and trade_status == 'ok' and can_one_hour_buy):

                if(candle == 'Bullish Engulfing' and candle_Typ == 'Bullish candle'):
                    if(lh>ph):
                        buy_price = (lh+0.08)
                        # Stop market buy
                        oneHour_orderId = place_one_hour_stop_limit_buy_order(buy_price)
                        if oneHour_orderId:
                            oneHour_buy_price = buy_price
                            is_oneHour_trade_done = True
                            if(stoploss<ll):
                                stoploss = ll
                        elif(is_15_min_buy_done):
                            is_one_hour_signal_found = True
                            one_h = buy_price
                        # print('Buy Signal')
                        # print(buy_price)
                    else:
                        buy_price = (ph+0.08)
                        # Stop market buy
                        oneHour_orderId = place_one_hour_stop_limit_buy_order(buy_price)
                        if oneHour_orderId:
                            oneHour_buy_price = buy_price
                            is_oneHour_trade_done = True
                            if(stoploss<ll):
                                stoploss = ll
                        elif(is_15_min_buy_done):
                            is_one_hour_signal_found = True
                            one_h = buy_price
                        # print('Buy Signal')
                        # print(buy_price)
                elif(candle == 'Right Hammer' and candle_Typ == 'Bullish candle'):
                    if((lh-lc)<0.02):
                        buy_price = lh+(lc-lo)/3
                        # stop limit buy
                        oneHour_orderId = place_one_hour_stop_limit_buy_order(buy_price)
                        if oneHour_orderId:
                            oneHour_buy_price = buy_price
                            is_oneHour_trade_done = True
                            if(stoploss<ll):
                                stoploss = ll
                        elif(is_15_min_buy_done):
                            is_one_hour_signal_found = True
                            one_h = buy_price
                        # print('Buy Signal')
                        # print(buy_price)
                    else:
                        buy_price = (lh+0.08)
                        # Stop limit order
                        oneHour_orderId = place_one_hour_stop_limit_buy_order(buy_price)
                        if oneHour_orderId:
                            oneHour_buy_price = buy_price
                            is_oneHour_trade_done = True
                            if(stoploss<ll):
                                stoploss = ll
                        elif(is_15_min_buy_done):
                            is_one_hour_signal_found = True
                            one_h = buy_price
                        # print('Buy Signal')
                        # print(buy_price)
                elif(candle == 'Inverted hammer' and candle_Typ == 'Bullish candle'):
                    buy_price = lh + 0.08
                    # Stop limit buy
                    oneHour_orderId = place_one_hour_stop_limit_buy_order(buy_price)
                    if oneHour_orderId:
                        oneHour_buy_price = buy_price
                        is_oneHour_trade_done = True
                        if(stoploss<ll):
                            stoploss = ll
                    elif(is_15_min_buy_done):
                        is_one_hour_signal_found = True
                        one_h = buy_price
                    # print('Buy Signal')
                    # print(buy_price)
                elif(candle == 'Spinning Top' and candle_Typ == 'Bullish candle'):
                    buy_price = (lh+0.08)
                    # Stop limit buy
                    oneHour_orderId = place_one_hour_stop_limit_buy_order(buy_price)
                    if oneHour_orderId:
                        oneHour_buy_price = buy_price
                        is_oneHour_trade_done = True
                        if(stoploss<ll):
                            stoploss = ll
                    elif(is_15_min_buy_done):
                        is_one_hour_signal_found = True
                        one_h = buy_price
                    # print('Buy Signal')
                    # print(buy_price)
                elif(candle == 'Reversal' and candle_Typ == 'Bullish candle'):
                    buy_price = (lh+0.08)
                    # Stop limit buy
                    oneHour_orderId = place_one_hour_stop_limit_buy_order(buy_price)
                    if oneHour_orderId:
                        oneHour_buy_price = buy_price
                        is_oneHour_trade_done = True
                        if(stoploss<ll):
                            stoploss = ll
                    elif(is_15_min_buy_done):
                        is_one_hour_signal_found = True
                        one_h = buy_price
                    # print('Buy Signal')
                    # print(buy_price)
                elif(candle == 'Bullish Marubuzu' and candle_Typ == 'Bullish candle'):
                    if(lh>ph):
                        buy_price = (lh+0.08)
                        # Stop market buy
                        oneHour_orderId = place_one_hour_stop_limit_buy_order(buy_price)
                        if oneHour_orderId:
                            oneHour_buy_price = buy_price
                            is_oneHour_trade_done = True
                            if(stoploss<ll):
                                stoploss = ll
                        elif(is_15_min_buy_done):
                            is_one_hour_signal_found = True
                            one_h = buy_price
                        # print('Buy Signal')
                        # print(buy_price)
                    else:
                        buy_price = (ph+0.08)
                        # Stop market buy
                        oneHour_orderId = place_one_hour_stop_limit_buy_order(buy_price)
                        if oneHour_orderId:
                            oneHour_buy_price = buy_price
                            is_oneHour_trade_done = True
                            if(stoploss<ll):
                                stoploss = ll
                        elif(is_15_min_buy_done):
                            is_one_hour_signal_found = True
                            one_h = buy_price
                        # print('Buy Signal')
                        # print(buy_price)

            if(lc>lo and pc<po and pc2<po2 and lc>po and lc>po2 and lh>ph and lh>ph2 and (pl2>pl or pl2>ll)):
                print("Double Bullish Engulfing")
                buy_price = (lh+0.08)
                # Stop limit buy
                oneHour_orderId = place_one_hour_stop_limit_buy_order(buy_price)
                if oneHour_orderId:
                    oneHour_buy_price = buy_price
                    is_oneHour_trade_done = True
                    if(stoploss<ll):
                        stoploss = ll
                elif(is_15_min_buy_done):
                    is_one_hour_signal_found = True
                    one_h = buy_price
            # ------------------------------------------------------------------------------------------------------
            if(candle_Typ == 'Bullish candle' and trend == 'Down_trend'):
                if(candle == 'Bullish Engulfing' or candle == 'Right Hammer' or candle == 'Inverted hammer' or candle == 'Spinning Top' or candle == 'Reversal' or candle == 'Bullish Marubuzu'):
                    is_trade_shift_one_hour_signal_found = True

            if is_15_min_buy_done and is_30_min_signal_found and is_trade_shift_one_hour_signal_found:
                cancel_limit_sell_order()
                stoploss_orderId = place_stoploss_sell_order(stoploss,1)
                print("Trade is shifted from oco to 30 min trade")
                is_shift_towards_30_min = True
                is_30_min_signal_found = False
                is_trade_shift_one_hour_signal_found = False

            elif is_trade_shift_one_hour_signal_found and is_looking_for_one_hour_signal:
                print("Trade is shifted from 15 min hold to 30 min trade")
                is_shift_towards_30_min = True
                is_trade_shift_one_hour_signal_found = False
                is_looking_for_one_hour_signal = False
            # -------------------------------------------------------------------------------------------------------
            if(is_one_hour_signal_found):
                print("One hour buy signal found")
            if(hours_after_15_min_buy == 2):
                is_15_min_buy_done = False
                hours_after_15_min_buy = 0
                is_trade_shift_one_hour_signal_found = False
                is_looking_for_one_hour_signal = False

            # ------------------------------------------------------------------------------------------------------
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
                        # print('Sell Signal')
                        # print(sell_price)
                    else:
                        sell_price = pl-0.05
                        # Stop limit sell
                        oneHour_orderId = place_one_hour_stop_limit_sell_order(sell_price)
                        if(oneHour_orderId):
                            is_oneHour_trade_done = True
                        # print('Sell Signal')
                        # print(sell_price)

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
                    # print('Sell Signal')
                    # print(sell_price)

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
                        # print('Sell Signal')
                        # print(sell_price)
                    else:
                        sell_price = (ll-0.05)
                        # Stop limit sell
                        oneHour_orderId = place_one_hour_stop_limit_sell_order(sell_price)
                        if(oneHour_orderId):
                            is_oneHour_trade_done = True
                        # print('Sell Signal')
                        # print(sell_price)

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
                    # print('Sell Signal')
                    # print(sell_price)

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
                    # print('Sell Signal')
                    # print(sell_price)

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
                        # print('Sell Signal')
                        # print(sell_price)
                    else:
                        sell_price = pl-0.05
                        # Stop limit sell
                        oneHour_orderId = place_one_hour_stop_limit_sell_order(sell_price)
                        if(oneHour_orderId):
                            is_oneHour_trade_done = True
                        # print('Sell Signal')
                        # print(sell_price)

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
                        # print('Sell Signal')
                        # print(sell_price)
                    else:
                        sell_price = pl-0.05
                        # Stop limit sell
                        oneHour_orderId = place_one_hour_stop_limit_sell_order(sell_price)
                        if(oneHour_orderId):
                            is_oneHour_trade_done = True
                        # print('Sell Signal')
                        # print(sell_price)
                elif(candle == 'Right Hammer' and candle_Typ == 'Bearish candle'):
                    sell_price = (ll-0.05)
                    # Stop limit sell
                    oneHour_orderId = place_one_hour_stop_limit_sell_order(sell_price)
                    if(oneHour_orderId):
                        is_oneHour_trade_done = True
                    # print('Sell Signal')
                    # print(sell_price)
                elif(candle == 'Inverted hammer' and candle_Typ == 'Bearish candle'):
                    if((lc-ll)<0.02):
                        sell_price = ll-(lo-lc)/3
                        # Stop limit sell
                        oneHour_orderId = place_one_hour_stop_limit_sell_order(sell_price)
                        if(oneHour_orderId):
                            is_oneHour_trade_done = True
                        # print('Sell Signal')
                        # print(sell_price)
                    else:
                        sell_price = (ll-0.05)
                        # Stop limit sell
                        oneHour_orderId = place_one_hour_stop_limit_sell_order(sell_price)
                        if(oneHour_orderId):
                            is_oneHour_trade_done = True
                        # print('Sell Signal')
                        # print(sell_price)
                elif(candle == 'Spinning Top' and candle_Typ == 'Bearish candle'):
                    sell_price = (ll-0.05)
                    # Stop limit sell
                    oneHour_orderId = place_one_hour_stop_limit_sell_order(sell_price)
                    if(oneHour_orderId):
                        is_oneHour_trade_done = True
                    # print('Sell Signal')
                    # print(sell_price)
                elif(candle == 'Reversal' and candle_Typ == 'Bearish candle'):
                    sell_price = (ll-0.05)
                    # Stop limit sell
                    oneHour_orderId = place_one_hour_stop_limit_sell_order(sell_price)
                    if(oneHour_orderId):
                        is_oneHour_trade_done = True
                    # print('Sell Signal')
                    # print(sell_price)
                elif(candle == 'Bearish Marubuzu' and candle_Typ == 'Bearish candle'):
                    if(ll<pl):
                        sell_price = ll-0.05
                        # Stop limit sell
                        oneHour_orderId = place_one_hour_stop_limit_sell_order(sell_price)
                        if(oneHour_orderId):
                            is_oneHour_trade_done = True
                        # print('Sell Signal')
                        # print(sell_price)
                    else:
                        sell_price = pl-0.05
                        # Stop limit sell
                        oneHour_orderId = place_one_hour_stop_limit_sell_order(sell_price)
                        if(oneHour_orderId):
                            is_oneHour_trade_done = True
                        # print('Sell Signal')
                        # print(sell_price)

            print('          ------------------')
# -------------------------------------------------------------------------------------------------------------------
        # candle remember
        now = datetime.now()
        if((now.minute == 15 or now.minute == 16) and is_15_min_signal_found):
            if(candles_wait == None):
                candle_number = 2
                candles_wait = 1
        elif((now.minute == 30 or now.minute == 31) and is_15_min_signal_found):
            if(candles_wait == None):
                candle_number = 2
                candles_wait = 1
            elif(candles_wait == 1):
                candle_number = 3
                candles_wait = 2
        elif((now.minute == 45 or now.minute == 46) and is_15_min_signal_found):
            if(candles_wait == None):
                candle_number = 2
                candles_wait = 1
            elif(candles_wait == 1):
                candle_number = 3
                candles_wait = 2
            elif(candles_wait == 2):
                candle_number = 4
                candles_wait = 3
        elif((now.minute == 0 or now.minute == 1) and is_15_min_signal_found):
            if(candles_wait == None):
                candle_number = 2
                candles_wait = 1
            elif(candles_wait == 1):
                candle_number = 3
                candles_wait = 2
            elif(candles_wait == 2):
                candle_number = 4
                candles_wait = 3
            elif(candles_wait == 3):
                candle_number = 5
                candles_wait = 4

        if((now.minute == 0 and candles_wait != None) or (now.minute==15 and candles_wait !=1 and candles_wait != None)):
            candles_wait = None
            candle_number = None
            is_15_min_signal_found = False
            is_30_min_signal_found = False
            is_buy_signal_found_between_30_min = False
            print("Candle signals below ema's deactivated!")

# -------------------------------------------------------------------------------------------------------------------
        wdf = get_15min_candles()
        c = 2
        last_candle = wdf.iloc[-c]
        flo = last_candle['Open']
        flc = last_candle['Close']
        flh = last_candle['High']
        fll = last_candle['Low']

        previous_candle_1 = wdf.iloc[-(c+1)]
        fpo = previous_candle_1['Open']
        fpc = previous_candle_1['Close']
        fph = previous_candle_1['High']
        fpl = previous_candle_1['Low']

        previous_candle_2 = wdf.iloc[-(c+2)]
        fpo2 = previous_candle_2['Open']
        fpc2 = previous_candle_2['Close']
        fph2 = previous_candle_2['High']
        fpl2 = previous_candle_2['Low']
# -------------------------------------------------------------------------------------------------------------------
        # Stoploss
        print("          Stpoloss Setting...")
        if(stoploss_set == False):
            if(is_shift_towards_30_min == False):
                if(fpc2<fpo2 and fpc<fpo and flc<flo):
                    if(flc==fll and flh==flo):
                        sell_price = fll - (flo-flc)/4
                    else:
                        sell_price = fll - 0.05
                    # Stop limit sell
                    # if(is_sol_available()):
                    status, order_time = place_stop_market_sell_order(sell_price)
                    if(status == 'FILLED'):
                        stoploss = 0
                        is_shift_towards_30_min = False
                        print(f'Stop loss sell:{sell_price}')
                    else:
                        stoploss = sell_price
                    if(is_15min_wait_completed(order_time)):
                        is_15min_done = True
                elif(flc<stoploss):
                    sell_price = flc
                    # market sell
                    # if(is_sol_available()):
                    market_sell_order(sell_price)
                    stoploss = 0
                    print(f'Stop loss sell:{sell_price}')
                elif(fpc2<fpo2  and (fpc<fpo and (fpo-fpc)>0.08) and flc>flo):
                    if(fpl>stoploss):
                        stoploss = fpl
            # ----------------------------------------------------------------
            elif(is_shift_towards_30_min):
                if(flc3<stoploss):
                    sell_price = flc
                    # market sell
                    # if(is_sol_available()):
                    market_sell_order(sell_price)
                    stoploss = 0
                    is_shift_towards_30_min = False
                    print(f'Stop loss sell:{sell_price}')
                elif(fpc2<fpo2 and fpc<fpo and flc<flo):
                    if(fpl<fll):
                        if(fpl>stoploss):
                            stoploss = fpl
                    else:
                        if(fll>stoploss):
                            stoploss = fll
                elif(fpc2<fpo2  and (fpc<fpo and (fpo-fpc)>0.08) and flc>flo):
                    if(fpl>stoploss):
                        stoploss = fpl

        # elif(lh>r4 and ll<r4 and lc>r4 and lc>lo):
        #     stoploss = r4
        #     # implement stop limit sell
        # elif(lh>r4 and ll<r4 and lc<r4 and lc<lo):
        #     stoploss = lc
        # ---------------------------------------------------------------------
        # Afterbuy Stoploss

        print(f"Stoploss:{stoploss}")
        print(f'Available USDT:{check_usdt()}')
        print(f'Available SOL:{check_SOL()}')

# -------------------------------------------------------------------------------------------------------------------
        # Waiting for buy trade
        if(is_buy_waiting_active):
        #     if(wh>=lh and wl<=ll):
        #         is_buy_waiting_active = True
            if(fll<wl or (flh>wh and flc<wh) or (flc<flo and (flo-flc)>(wc-wo)/2)):
                is_buy_waiting_active = False
                wh = None
                wl = None
                wc = None
                wo = None
                print("Buy waitng deactivated!")
                is_combination_of_15_and_30_min = False
            elif(flh>wh and flc>wh):
                if market_buy_order(flc):
                    stoploss = wl
                    is_15_min_buy_done = True
                    if(is_combination_of_15_and_30_min):
                        stoploss_orderId = place_stoploss_sell_order(stoploss, 1)
                        if stoploss_orderId:
                            stoploss_buy_price = flc
                            stoploss_low_price = stoploss
                    else:
                        stoploss_orderId = set_profit_1(df,flc,stoploss)
                        if stoploss_orderId:
                            stoploss_buy_price = flc
                            stoploss_low_price = stoploss
                    is_buy_waiting_active = False
                    is_combination_of_15_and_30_min = False
                    wh = None
                    wl = None
                    print("Buy waitng filled!")

# -------------------------------------------------------------------------------------------------------------------
        if(is_30_min_signal_found):
            if(is_15_min_buy_done):
                cancel_limit_sell_order()
                stoploss_orderId = place_stoploss_sell_order(stoploss,1)
                print("Trade shift from oco to 15 min hold")
                is_30_min_signal_found = False
            else:
                is_30_min_signal_found = False
# -------------------------------------------------------------------------------------------------------------------
        # Stoploss change setting
        if(stoploss_orderId):
            one_per = stoploss_buy_price + (stoploss_buy_price/100)
            one_and_half_percent  = stoploss_buy_price + (1.5*(stoploss_buy_price/100))
            if(is_shift_towards_30_min):
                if(flc>one_and_half_percent):
                    stoploss_orderId = place_stoploss_sell_order(stoploss_buy_price)
                    stoploss_buy_price = None
                    stoploss_low_price = None
                    stoploss_orderId = None
                elif(flc>one_per):
                    stoploss_orderId = place_stoploss_sell_order(stoploss_low_price)
            else:
                if(flc>one_per):
                    stoploss_orderId = place_stoploss_sell_order(stoploss_buy_price)
                    stoploss_buy_price = None
                    stoploss_low_price = None
                    stoploss_orderId = None
                elif(flh>one_per):
                    stoploss_orderId = place_stoploss_sell_order(stoploss_low_price)

        if(stoploss_orderId == None):
            stoploss_buy_price = None
            stoploss_low_price = None
# -------------------------------------------------------------------------------------------------------------------
        print('--------------------------------------')
        if(now.minute >= 30):
            is_oneHour_done = False
        # ---------------------------------
        if(is_15min_done == False):
            sleep_until_next_15min()
    except Exception as e:
                print("Error occurred:", e)
                time.sleep(30)
