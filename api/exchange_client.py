from binance.client import Client

LIVE_MODE = True

if LIVE_MODE:
    # api_key = "API_key"
    # api_secret = "Secret_key"
    api_key = "api_key"
    api_secret = "api_secret"
    client = Client(api_key, api_secret)
else:
    api_key = "testnet_api_key"
    api_secret = "testnet_secret_key"
    client = Client(api_key, api_secret)
    client.API_URL = 'https://testnet.binance.vision/api'

    # For getting correct data about candles
    market_data_client = Client() 