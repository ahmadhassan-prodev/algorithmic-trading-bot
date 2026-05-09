import pandas as pd

def get_rsi_7(df, candle = 2):

    df['Close'] = pd.to_numeric(df['Close'], errors='coerce')
    df = df.dropna(subset=['Close'])

    close = df['Close']

    # Price change
    delta = close.diff()

    # Gains and losses
    gain = delta.where(delta > 0, 0.0)
    loss = -delta.where(delta < 0, 0.0)

    period = 7

    # Wilder smoothing
    avg_gain = gain.ewm(alpha=1/period, min_periods=period, adjust=False).mean()
    avg_loss = loss.ewm(alpha=1/period, min_periods=period, adjust=False).mean()

    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))

    # Return RSI of last closed candle
    rsi_value = round(rsi.iloc[-candle], 2)

    return rsi_value
