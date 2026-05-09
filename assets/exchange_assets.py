from api.exchange_client import client

# Check available USDT
def check_usdt():
    balance = client.get_asset_balance(asset='USDT')
    return float(balance['free'])

# Check Available SOLANA
def check_SOL():
    balance = client.get_asset_balance(asset='SOL')
    return float(balance['free'])

# check current SOLANA  price
def current_SOL():
    sol_price = client.get_symbol_ticker(symbol="SOLUSDT")
    current_sol_price = float(sol_price['price'])
    return current_sol_price

# check tradable USDT
def is_usdt_available():
    avaiable_usdt = check_usdt()
    if(avaiable_usdt>10):
        return True
    else:
        return False

# Check sufficent SOL to sell
def is_sol_available():
    available_sol = check_SOL()
    if(available_sol>0.05):
        return True
    else:
        return False
