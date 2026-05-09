from data.data_fetcher import get_1hour_candles
from indicators.volume import get_candle_volume

df = get_1hour_candles()

vol = get_candle_volume(df,)

print(f"Candle volume: {vol}")