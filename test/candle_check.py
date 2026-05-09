from data.data_fetcher import *
from indicators.candlestick_details import detect_candlestick_pattern

# df = get_1hour_candles()
df = get_15min_candles()
candle = detect_candlestick_pattern(df,13)
print(candle)