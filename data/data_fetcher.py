from api.exchange_client import client
from binance.client import Client
import pandas as pd

# get 15 minutes candle data
def get_15min_candles():
    candles = client.get_klines(
      symbol='SOLUSDT',
      interval = Client.KLINE_INTERVAL_15MINUTE,
      limit = 200
      )
    df = pd.DataFrame(candles)[[0,1,2,3,4,5]]
    df.columns = ['Open Time','Open', 'High', 'Low', 'Close', 'Volume']
    df['Open Time'] = pd.to_datetime(df['Open Time'], unit='ms')
    df['Open Time'] = df['Open Time'].dt.tz_localize('UTC').dt.tz_convert('Asia/Karachi')
    df[['Open', 'High', 'Low', 'Close']] = df[['Open', 'High', 'Low', 'Close']].astype(float)
    return df

# get 30 minutes candle data
def get_30min_candles():
    candles = client.get_klines(
        symbol='SOLUSDT',
        interval = Client.KLINE_INTERVAL_30MINUTE,
        limit = 200
        )
    df = pd.DataFrame(candles)[[0,1,2,3,4,5]]
    df.columns = ['Open Time','Open', 'High', 'Low', 'Close', 'Volume']
    df['Open Time'] = pd.to_datetime(df['Open Time'], unit='ms')
    df['Open Time'] = df['Open Time'].dt.tz_localize('UTC').dt.tz_convert('Asia/Karachi')
    df[['Open', 'High', 'Low', 'Close']] = df[['Open', 'High', 'Low', 'Close']].astype(float)
    return df

# get one hour candle data
def get_1hour_candles():
    candles = client.get_klines(
        symbol='SOLUSDT',
        interval = Client.KLINE_INTERVAL_1HOUR,
        limit = 200
        )
    df = pd.DataFrame(candles)[[0,1,2,3,4,5]]
    df.columns = ['Open Time','Open', 'High', 'Low', 'Close', 'Volume']
    df['Open Time'] = pd.to_datetime(df['Open Time'], unit='ms')
    df['Open Time'] = df['Open Time'].dt.tz_localize('UTC').dt.tz_convert('Asia/Karachi')
    df[['Open', 'High', 'Low', 'Close']] = df[['Open', 'High', 'Low', 'Close']].astype(float)
    return df