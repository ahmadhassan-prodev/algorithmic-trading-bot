from data.data_fetcher import get_1hour_candles
import ta

def trend_check(df, hour = 1):
    c = 2
    last_candle = df.iloc[-c]
    lo = last_candle['Open']
    lc = last_candle['Close']
    lh = last_candle['High']
    ll = last_candle['Low']

    # Second Last candle
    previous_candle_1 = df.iloc[-(c+1)]
    po1 = previous_candle_1['Open']
    pc1 = previous_candle_1['Close']
    ph1 = previous_candle_1['High']
    pl1 = previous_candle_1['Low']

    
    # 3rd Last candle
    previous_candle_2 = df.iloc[-(c+2)]
    po2 = previous_candle_2['Open']
    pc2 = previous_candle_2['Close']
    ph2 = previous_candle_2['High']
    pl2 = previous_candle_2['Low']

    # 4th Last candle
    previous_candle_3 = df.iloc[-(c+3)]
    po3 = previous_candle_3['Open']
    pc3 = previous_candle_3['Close']
    ph3 = previous_candle_3['High']
    pl3 = previous_candle_3['Low']
    
    # 5th Last candle
    previous_candle_4 = df.iloc[-(c+4)]
    po4 = previous_candle_4['Open']
    pc4 = previous_candle_4['Close']
    ph4 = previous_candle_4['High']
    pl4 = previous_candle_4['Low']
    
    # 6th Last candle
    previous_candle_5 = df.iloc[-(c+5)]
    po5 = previous_candle_5['Open']
    pc5 = previous_candle_5['Close']
    ph5 = previous_candle_5['High']
    pl5 = previous_candle_5['Low']

    # 7th Last candle
    previous_candle_6 = df.iloc[-(c+6)]
    po6 = previous_candle_6['Open']
    pc6 = previous_candle_6['Close']
    ph6 = previous_candle_6['High']
    pl6 = previous_candle_6['Low']

    # 8th Last candle
    previous_candle_7 = df.iloc[-(c+7)]
    po7 = previous_candle_7['Open']
    pc7 = previous_candle_7['Close']
    ph7 = previous_candle_7['High']
    pl7 = previous_candle_7['Low']

    ch = 0
    cc = 0
    cl = 0
    index = 0
    rcount = 0

    for i in range(8,2,-1):
        open = df.iloc[-(i)]['Open']
        close = df.iloc[-(i)]['Close']
        high = df.iloc[-(i)]['High']
        low = df.iloc[-(i)]['Low']
        if(close<open):
            ch = high
            cc = close
            cl = low
            index = i
            rcount = rcount + 1
            # print(f'Bearish candle found in 6 canldes\nOpen:{open}\nClose:{close}')
            break
    
    # if (pc6<po6):
    #     rcount = rcount + 1
    if (7<index and pc5<=po5 and (ch>ph5 or pc5<cc or pl5<cl)):
        rcount = rcount + 1
        ch = ph5 
        cc = pc5
        cl = pl5
    if (6<index and pc4<=po4 and (ch>ph4 or pc4<cc or pl4<cl)):
        rcount = rcount + 1
        ch = ph4 
        cc = pc4
        cl = pl4
    if (5<index and pc3<=po3 and (ch>ph3 or pc3<cc or pl3<cl)):
        rcount = rcount + 1
        ch = ph3 
        cc = pc3
        cl = pl3
    if (4<index and pc2<=po2 and (ch>ph2 or pc2<cc or pl2<cl)):
        rcount = rcount + 1
        ch = ph2 
        cc = pc2
        cl = pl2
    if (3<index and pc1<=po1 and (ch>ph1 or pc1<cc or pl1<cl)):
        rcount = rcount + 1
        ch = ph1 
        cc = pc1
        cl = pl1

    gcl = 0
    gcc = 0
    gch = 0
    gindex = 0
    gcount = 0

    for i in range(8,2,-1):
        open = df.iloc[-(i)]['Open']
        close = df.iloc[-(i)]['Close']
        low = df.iloc[-(i)]['Low']
        high = df.iloc[-(i)]['High']
        
        if(close>open):
            gcl = low
            gcc = close
            gch = high
            gindex = i
            gcount = gcount + 1
            # print(f'Bullish candle found in 6 canldes\nOpen:{open}\nClose:{close}')
            break
    
    # if (pc6>po6):
    #     gcount = gcount + 1
    if (pc5>=po5 and gindex>7 and (gcl<pl5 or pc5>gcc or ph5>gch)):
        gcount = gcount + 1
        gcl = pl5
        gcc = pc5
        gch = ph5
    if (pc4>=po4 and gindex>6 and (gcl<pl4 or pc4>gcc or ph4>gch)):
        gcount = gcount + 1
        gcl = pl4
        gcc = pc4
        gch = ph4
    if (pc3>=po3 and gindex>5 and (gcl<pl3 or pc3>gcc or ph3>gch)):
        gcount = gcount + 1
        gcl = pl3
        gcc = pc3
        gch = ph3
    if (pc2>=po2 and gindex>4 and (gcl<pl2 or pc2>gcc or ph2>gch)):
        gcount = gcount + 1
        gcl = pl2
        gcc = pc2
        gch = ph2
    if (pc1>=po1 and gindex>3 and (gcl<pl1 or pc1>gcc or ph1>gch)):
        gcount = gcount + 1
        gcl = pl1
        gcc = pc1
        gch = ph1

    ch5 = 0
    cc5 = 0
    cl5 = 0
    index5 = 0
    rcount5 = 0

    for i in range(7,2,-1):
        open = df.iloc[-(i)]['Open']
        close = df.iloc[-(i)]['Close']
        high = df.iloc[-(i)]['High']
        low = df.iloc[-(i)]['Low']
        
        if(close<open):
            ch5 = high
            cc5 = close
            cl5 = low
            index5 = i
            rcount5 = rcount5 + 1
            # print(f'Bearish candle found in 5 canldes\nOpen:{open}\nClose:{close}')
            break
    
    # if (pc5<po5):
    #     rcount5 = rcount5 + 1
    if (6<index5 and pc4<=po4 and (ch5>ph4 or pc4<cc5 or pl4<cl5)):
        rcount5 = rcount5 + 1
        ch5 = ph4 
        cc5 = pc4
        cl5 = pl4
    if (5<index5 and pc3<=po3 and (ch5>ph3 or pc3<cc5 or pl3<cl5)):
        rcount5 = rcount5 + 1
        ch5 = ph3 
        cc5 = pc3
        cl5 = pl3
    if (4<index5 and pc2<=po2 and (ch5>ph2 or pc2<cc5 or pl2<cl5)):
        rcount5 = rcount5 + 1
        ch5 = ph2 
        cc5 = pc2
        cl5 = pl2
    if (3<index5 and pc1<=po1 and (ch5>ph1 or pc1<cc5 or pl1<cl5)):
        rcount5 = rcount5 + 1
        ch5 = ph1 
        cc5 = pc1
        cl5 = pl1

    gcl5 = 0
    gcc5 = 0
    gch5 = 0
    gindex5 = 0
    gcount5 = 0

    for i in range(7,2,-1):
        open = df.iloc[-(i)]['Open']
        close = df.iloc[-(i)]['Close']
        low = df.iloc[-(i)]['Low']
        high = df.iloc[-(i)]['High']
        
        if(close>open):
            gcl5 = low
            gcc5 = close
            gch5 = high
            gindex5 = i
            gcount5 = gcount5 + 1
            # print(f'Bullish candle found in 5 canldes\nOpen:{open}\nClose:{close}')
            break

    # if (pc5>po5):
    #     gcount5 = gcount5 + 1
    if (pc4>=po4 and gindex5>6 and (gcl5<pl4 or pc4>gcc5 or ph4>gch5)):
        gcount5 = gcount5 + 1
        gcl5 = pl4
        gcc5 = pc4
        gch5 = ph4
    if (pc3>=po3 and gindex5>5 and (gcl5<pl3 or pc3>gcc5 or ph3>gch5)):
        gcount5 = gcount5 + 1
        gcl5 = pl3
        gcc5 = pc3
        gch5 = ph3
    if (pc2>=po2 and gindex5>4 and (gcl5<pl2 or pc2>gcc5 or ph2>gch5)):
        gcount5 = gcount5 + 1
        gcl5 = pl2
        gcc5 = pc2
        gch5 = ph2
    if (pc1>=po1 and gindex5>3 and (gcl5<pl1 or pc1>gcc5 or ph1>gch5)):
        gcount5 = gcount5 + 1
        gcl5 = pl1
        gcc5 = pc1
        gch5 = ph1

    ch4 = 0
    cc4 = 0
    cl4 = 0
    index4 = 0
    rcount4 = 0

    for i in range(6,2,-1):
        open = df.iloc[-(i)]['Open']
        close = df.iloc[-(i)]['Close']
        high = df.iloc[-(i)]['High']
        low = df.iloc[-(i)]['Low']
        
        if(close<open):
            ch4 = high
            cc4 = close
            cl4 = low
            index4 = i
            rcount4 = rcount4 + 1
            # print(f'Bearish candle found in 5 canldes\nOpen:{open}\nClose:{close}')
            break
    
    if (5<index4 and pc3<=po3 and (ch4>ph3 or pc3<cc4 or pl3<cl4)):
        rcount4 = rcount4 + 1
        ch4 = ph3 
        cc4 = pc3
        cl4 = pl3
    if (4<index4 and pc2<=po2 and (ch4>ph2 or pc2<cc4 or pl2<cl4)):
        rcount4 = rcount4 + 1
        ch4 = ph2 
        cc4 = pc2
        cl4 = pl2
    if (3<index4 and pc1<=po1 and (ch4>ph1 or pc1<cc4 or pl1<cl4)):
        rcount4 = rcount4 + 1
        ch4 = ph1 
        cc4 = pc1
        cl4 = pl1

    gcl4 = 0
    gcc4 = 0
    gch4 = 0
    gindex4 = 0
    gcount4 = 0

    for i in range(6,2,-1):
        open = df.iloc[-(i)]['Open']
        close = df.iloc[-(i)]['Close']
        low = df.iloc[-(i)]['Low']
        high = df.iloc[-(i)]['High']
        
        if(close>open):
            gcl4 = low
            gcc4 = close
            gch4 = high
            gindex4 = i
            gcount4 = gcount4 + 1
            # print(f'Bullish candle found in 5 canldes\nOpen:{open}\nClose:{close}')
            break

    if (pc3>=po3 and gindex4>5 and (gcl4<pl3 or pc3>gcc4 or ph3>gch4)):
        gcount4 = gcount4 + 1
        gcl4 = pl3
        gcc4 = pc3
        gch4 = ph3
    if (pc2>=po2 and gindex4>4 and (gcl4<pl2 or pc2>gcc4 or ph2>gch4)):
        gcount4 = gcount4 + 1
        gcl4 = pl2
        gcc4 = pc2
        gch4 = ph2
    if (pc1>=po1 and gindex4>3 and (gcl4<pl1 or pc1>gcc4 or ph1>gch4)):
        gcount4 = gcount4 + 1
        gcl4 = pl1
        gcc4 = pc1
        gch4 = ph1

    lcount7 = 0
    if(pl6<=pl7):
        lcount7 = lcount7 + 1
    if(pl5<=pl6):
        lcount7 = lcount7 + 1
    if(pl4<=pl5):
        lcount7 = lcount7 + 1
    if(pl3<=pl4):
        lcount7 = lcount7 + 1
    if(pl2<=pl3):
        lcount7 = lcount7 + 1
    if(pl1<=pl2):
        lcount7 = lcount7 + 1
    if(ll<=pl1):
        lcount7 = lcount7 + 1

    hcount7 = 0
    if(ph6>=ph7):
        hcount7 = hcount7 + 1
    if(ph5>=ph6):
        hcount7 = hcount7 + 1
    if(ph4>=ph5):
        hcount7 = hcount7 + 1
    if(ph3>=ph4):
        hcount7 = hcount7 + 1
    if(ph2>=ph3):
        hcount7 = hcount7 + 1
    if(ph1>=ph2):
        hcount7 = hcount7 + 1
    if(lh>=ph1):
        hcount7 = hcount7 + 1

    lcount6 = 0
    if(pl5<=pl6):
        lcount6 = lcount6 + 1
    if(pl4<=pl5):
        lcount6 = lcount6 + 1
    if(pl3<=pl4):
        lcount6 = lcount6 + 1
    if(pl2<=pl3):
        lcount6 = lcount6 + 1
    if(pl1<=pl2):
        lcount6 = lcount6 + 1
    if(ll<=pl1):
        lcount6 = lcount6 + 1

    hcount6 = 0
    if(ph5>=ph6):
        hcount6 = hcount6 + 1
    if(ph4>=ph5):
        hcount6 = hcount6 + 1
    if(ph3>=ph4):
        hcount6 = hcount6 + 1
    if(ph2>=ph3):
        hcount6 = hcount6 + 1
    if(ph1>=ph2):
        hcount6 = hcount6 + 1
    if(lh>=ph1):
        hcount6 = hcount6 + 1

    lcount5 = 0
    if(pl4<=pl5):
        lcount5 = lcount5 + 1
    if(pl3<=pl4):
        lcount5 = lcount5 + 1
    if(pl2<=pl3):
        lcount5 = lcount5 + 1
    if(pl1<=pl2):
        lcount5 = lcount5 + 1
    if(ll<=pl1):
        lcount5 = lcount5 + 1

    hcount5 = 0
    if(ph4>=ph5):
        hcount5 = hcount5 + 1
    if(ph3>=ph4):
        hcount5 = hcount5 + 1
    if(ph2>=ph3):
        hcount5 = hcount5 + 1
    if(ph1>=ph2):
        hcount5 = hcount5 + 1
    if(lh>=ph1):
        hcount5 = hcount5 + 1

    lcount4 = 0
    if(pl3<=pl4):
        lcount4 = lcount4 + 1
    if(pl2<=pl3):
        lcount4 = lcount4 + 1
    if(pl1<=pl2):
        lcount4 = lcount4 + 1
    if(ll<=pl1):
        lcount4 = lcount4 + 1

    hcount4 = 0
    if(ph3>=ph4):
        hcount4 = hcount4 + 1
    if(ph2>=ph3):
        hcount4 = hcount4 + 1
    if(ph1>=ph2):
        hcount4 = hcount4 + 1
    if(lh>=ph1):
        hcount4 = hcount4 + 1

    if(hour==1):
        if((rcount>=4) and (lcount7>=4)) or((rcount >=3) and (lcount6>=4) and ((pc6<po6 and pc5<po5) or (pc5<po5 and pc4<po4) or (pc4<po4 and pc3<po3) or (pc3<po3 and pc2<po2) or (pc2<po2 and pc1<po1))) or(rcount5>=4 and lcount5>=3) or (rcount4>=3 and lcount4>=2):
            # # (pc2<po2 and pc1<po1) or 
            if(lc>lo and ((pl1<pl2 and pl1<pl3) or (ll<pl1 and ll<pl2))):
            #     #  and pl1<pl2 and ll<pc1
                return 'Down_trend'
            elif(lc<lo and ((ll<pl1 and ll<pl2) or (pl1<pl2 and pl2<pl3 and pl3<pl4) or (pl1<pl2 and pl1<pl3))):
                return 'Down_trend'
            elif(lc==lo and ll<pl1 and ll<pl2):
                return 'Down_trend'
            elif(pl1>=pl2 and ph1<=ph2 and ll>=pl2 and lh<=ph2):
                return 'Down_trend'
            # return 'Down_trend'
            
        elif((gcount>=4) and (hcount7>=4)) or((gcount>=3) and (hcount6>=4) and ((pc6>po6 and pc5>po5) or (pc5>po5 and pc4>po4) or (pc4>po4 and pc3>po3) or (pc3>po3 and pc2>po2) or (pc2>po2 and pc1>po1))) or (gcount5>=4 and hcount5>=3) or (gcount4>=3 and hcount4>=2):
            # # (pc2>po2 and pc1>po1) or 
            if(lc>lo and ((lh>ph1 and lh>ph2) or (ph1>ph2 and ph2>ph3 and ph3>ph4) or (ph1>ph2 and ph1>ph3))):
                return 'Up_trend'
            elif(lc==lo and lh>ph1 and lh>ph2):
                return 'Up_trend'
            elif(lc<lo and ((ph1>ph2 and ph1>ph3) or (lh>ph1 and lh>ph2))): 
            #     #  and ph1>ph2
                return 'Up_trend'
            elif(ph1<=ph2 and pl1>=pl2 and lh<=ph2 and ll>=pl2):
                return 'Up_trend'
            # return 'Up_trend'
            
        else:
            return 'No_trend'
    else:
        if((rcount>=4) and (lcount7>=4)) or((rcount >=3) and (lcount6>=4) and ((pc6<po6 and pc5<po5) or (pc5<po5 and pc4<po4) or (pc4<po4 and pc3<po3) or (pc3<po3 and pc2<po2) or (pc2<po2 and pc1<po1))) or(rcount5>=4 and lcount5>=3) or (rcount4>=3 and lcount4>=3):
            # # (pc2<po2 and pc1<po1) or 
            if(lc>lo and ((pl1<pl2 and pl1<pl3) or (ll<pl1 and ll<pl2))):
            #     #  and pl1<pl2 and ll<pc1
                return 'Down_trend'
            elif(lc<lo and ((ll<pl1 and ll<pl2) or (pl1<pl2 and pl2<pl3 and pl3<pl4) or (pl1<pl2 and pl1<pl3))):
                return 'Down_trend'
            elif(lc==lo and ll<pl1 and ll<pl2):
                return 'Down_trend'
            elif(pl1>=pl2 and ph1<=ph2 and ll>=pl2 and lh<=ph2):
                return 'Down_trend'
            # return 'Down_trend'
            
        elif((gcount>=4) and (hcount7>=4)) or((gcount>=3) and (hcount6>=4) and ((pc6>po6 and pc5>po5) or (pc5>po5 and pc4>po4) or (pc4>po4 and pc3>po3) or (pc3>po3 and pc2>po2) or (pc2>po2 and pc1>po1))) or (gcount5>=4 and hcount5>=3) or (gcount4>=3 and hcount4>=3):
            # # (pc2>po2 and pc1>po1) or 
            if(lc>lo and ((lh>ph1 and lh>ph2) or (ph1>ph2 and ph2>ph3 and ph3>ph4) or (ph1>ph2 and ph1>ph3))):
                return 'Up_trend'
            elif(lc==lo and lh>ph1 and lh>ph2):
                return 'Up_trend'
            elif(lc<lo and ((ph1>ph2 and ph1>ph3) or (lh>ph1 and lh>ph2))): 
            #     #  and ph1>ph2
                return 'Up_trend'
            elif(ph1<=ph2 and pl1>=pl2 and lh<=ph2 and ll>=pl2):
                return 'Up_trend'
            # return 'Up_trend'
            
        else:
            return 'No_trend'


def detect_trend_1h(df = get_1hour_candles(), short_ema=20, long_ema=50, adx_threshold=20, ema_gap_threshold=0.002, candle_index=-2):
    # Calculate EMAs
    df['ema_short'] = df['Close'].ewm(span=short_ema, adjust=False).mean()
    df['ema_long'] = df['Close'].ewm(span=long_ema, adjust=False).mean()

    # Create ADX indicator instance
    adx_indicator = ta.trend.ADXIndicator(
        high=df['High'],
        low=df['Low'],
        close=df['Close'],
        window=14
    )

    df['adx'] = adx_indicator.adx()
    df['plus_di'] = adx_indicator.adx_pos()
    df['minus_di'] = adx_indicator.adx_neg()

    # Use given candle index (default -2 to avoid incomplete data)
    ema_s = df['ema_short'].iloc[candle_index]
    ema_l = df['ema_long'].iloc[candle_index]
    current_adx = df['adx'].iloc[candle_index]
    plus = df['plus_di'].iloc[candle_index]
    minus = df['minus_di'].iloc[candle_index]
    ema_gap = abs(ema_s - ema_l) / df['Close'].iloc[candle_index]

    # Sideways market condition
    if current_adx < adx_threshold or ema_gap < ema_gap_threshold:
        return "Sideways"

    # Uptrend condition
    if ema_s > ema_l and plus > minus:
        return "Uptrend"

    # Downtrend condition
    if ema_s < ema_l and minus > plus:
        return "Downtrend"

    # Default fallback
    return "Sideways"