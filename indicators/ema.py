from ta.trend import EMAIndicator

# ema 21
def ema_buy_check(df):
    ema_21 = EMAIndicator(close=df['Close'], window=21).ema_indicator()
    buy_ema = ema_21.dropna().iloc[-2]
    return buy_ema

# ema 50
def ema_check(df):
    ema_50 = EMAIndicator(close=df['Close'], window=50).ema_indicator()
    recent_ema = ema_50.dropna().iloc[-2]
    return recent_ema

# ema 100
def ema_last(df,c=2):
    ema_l = EMAIndicator(close=df['Close'], window=95).ema_indicator()
    ema_la = ema_l.dropna().iloc[-(c)]
    return ema_la