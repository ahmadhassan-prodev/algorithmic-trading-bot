import pandas as pd

def is_volume_filter_pass(df,multiplier=1.1):

    df['Volume'] = pd.to_numeric(df['Volume'], errors='coerce')
    df = df.dropna(subset=['Volume'])
    target_candle = df.iloc[-2]
    avg_volume = df['Volume'].iloc[-22:-2].mean()
    candle_volume = target_candle['Volume']

    volume_condition = candle_volume > avg_volume * multiplier

    print(f"Average volume: {avg_volume}\n"
          f"Candle volume: {candle_volume}\n"
          f"Is volume filter pass: {volume_condition}")

    return volume_condition

def get_candle_volume(df,c):
    df['Volume'] = pd.to_numeric(df['Volume'], errors='coerce')
    df = df.dropna(subset=['Volume'])
    target_candle = df.iloc[-c]
    return target_candle['Volume']
