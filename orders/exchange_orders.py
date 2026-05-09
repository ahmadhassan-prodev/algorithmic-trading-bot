from api.exchange_client import client
from binance.exceptions import BinanceAPIException
from assets.exchange_assets import *
from utils.exchange_helpers import *
from urllib.parse import urlencode
import hmac
import requests
import hashlib
import time
import math
from datetime import datetime

# check order status
def get_order_status(order_id):
    symbol = 'SOLUSDT'
    try:
        order = client.get_order(
            symbol=symbol,
            orderId=order_id
        )
        return order['status']
    except Exception as e:
        print(f"Failed to fetch order status: {e}")
        return None

# cancel OCO order
def cancel_oco_order(symbol, orderListId):
    API_KEY = "API_key"
    API_SECRET = "secret_key"
    BASE_URL = "https://api.binance.com"
    try:
        timestamp = int(time.time() * 1000)
        params = {
            "symbol": symbol,
            "orderListId": orderListId,
            "timestamp": timestamp
        }
        query_string = urlencode(params)
        signature = hmac.new(API_SECRET.encode(), query_string.encode(), hashlib.sha256).hexdigest()
        headers = {"X-MBX-APIKEY": API_KEY}

        url = f"{BASE_URL}/api/v3/orderList?{query_string}&signature={signature}"
        response = requests.delete(url, headers=headers)
        return response.json()
    except Exception as e:
        print(f"Error canceling OCO order: {e}")
        return None
    
# cancel limit sell order
def cancel_limit_sell_order():
    symbol = 'SOLUSDT'

    # === Cancel existing STOP_MARKET sell orders ===
    try:
        open_orders = client.get_open_orders(symbol=symbol)
        for order in open_orders:
            if order['side'] == 'SELL':
                if order.get("orderListId", -1) != -1:
                    cancel_oco_order(symbol=symbol, orderListId=order["orderListId"])
                    print(f"Canceled previous OCO sell order (orderListId={order['orderListId']})")
                else:
                    client.cancel_order(symbol=symbol, orderId=order['orderId'])
                    print(f"Canceled previous {order['type']} sell order (orderId={order['orderId']})")
    except Exception as e:
        print(f"Error while canceling existing sell orders: {e}")
        return None
    
# cancel any order
def cancel_order(order_id):
    symbol = 'SOLUSDT'
    try:
        result = client.cancel_order(
            symbol=symbol,
            orderId=order_id
        )
        print(f"Order not filled after one hour. canceled successfully.")
        return result
    except Exception as e:
        print(f"Failed to cancel order {order_id}: {e}")
        return None
    
# helper function to place OCO order
def place_manual_oco_order(quantity, tp_price, stop_price, stop_limit_price):
    BASE_URL = "https://api.binance.com"
    api_key = "API_key"
    api_secret = "secret_key"
    path = "/api/v3/order/oco"
    
    url = BASE_URL + path
    timestamp = int(time.time() * 1000)

    params = {
        "symbol": "SOLUSDT",
        "side": "SELL",
        "quantity": quantity,
        "price": tp_price,
        "stopPrice": stop_price,
        "stopLimitPrice": stop_limit_price,
        "stopLimitTimeInForce": "GTC",
        "timestamp": timestamp
    }

    # Sign request
    query_string = "&".join([f"{k}={v}" for k, v in params.items()])
    signature = hmac.new(api_secret.encode(), query_string.encode(), hashlib.sha256).hexdigest()
    params["signature"] = signature

    headers = {"X-MBX-APIKEY": api_key}

    try:
        response = requests.post(url, headers=headers, params=params, timeout=10)
        data = response.json()

        if "orderReports" in data and len(data["orderReports"]) > 0:
            return data["orderReports"][0]["orderId"]
        else:
            print("Binance OCO error:", data)
            return None

    except Exception as e:
        print("Exception while placing OCO order:", str(e))
        return None
    

# place OCO order
def place_oco_sell_order(gprice_take_profit,stoploss):
    symbol = 'SOLUSDT'
    side = 'SELL'
    previous_order = None
    cp = current_SOL()
    one_percent = cp/100
    stoploss = stoploss - one_percent
    gprice_stop_trigger = stoploss
    gprice_stop_limit = stoploss - 0.01

    try:
        # 1. Cancel existing SELL orders and store previous for restore
        try:
            open_orders = client.get_open_orders(symbol=symbol)
            for order in open_orders:
                if order['side'] == 'SELL':
                    previous_order = {
                        'side': order['side'],
                        'quantity': float(order['origQty']),
                        'price': float(order.get('price', 0)),
                        'stop_price': float(order.get('stopPrice', 0))
                    }
                    client.cancel_order(symbol=symbol, orderId=order['orderId'])
                    print(f"Canceled previous sell order: {order['orderId']}")
        except Exception as e:
            print(f"Error canceling existing sell orders: {e}")
            return None

        # 2. Get available quantity
        available_sol = float(check_SOL())
        quantity = adjust_quantity(symbol, available_sol * 0.99)

        if quantity < 0.01:
            print(f"Available quantity too low ({quantity}) to place OCO order.")
            return None
        
        tp_price = float(adjust_price(symbol, gprice_take_profit, direction='up'))
        stop_price = float(adjust_price(symbol, gprice_stop_trigger, direction='down'))
        stop_limit_price = float(adjust_price(symbol, gprice_stop_limit, direction='down'))
        
        order_id = place_manual_oco_order(
            quantity=quantity,
            tp_price=tp_price,
            stop_price=stop_price,
            stop_limit_price=stop_limit_price
        )

        if order_id:
            print("OCO Order placed, ID:", order_id)
            return order_id
        else:
            print("OCO order failed.")
    
        # 3. Place OCO order
        # print(f"Placing OCO sell order: TP={gprice_take_profit}, Stop={gprice_stop_trigger}")
        # order = client.create_oco_order(
        #     symbol=symbol,
        #     side=side,
        #     quantity=float(quantity),
        #     price=float(adjust_price(symbol, gprice_take_profit, direction='up')),
        #     stopPrice=float(adjust_price(symbol, gprice_stop_trigger, direction='down')),
        #     stopLimitPrice=float(adjust_price(symbol, gprice_stop_limit, direction='down')),
        #     stopLimitTimeInForce='GTC'
        # )
        # print("OCO order placed successfully:", order)
        # return order['orderReports'][1]['orderId']

    except Exception as e:
        print("Error placing OCO sell order:", e)

        # 4. Restore previous order if OCO fails
        if previous_order:
            try:
                print("Restoring previous order...")
                if previous_order['stop_price'] == 0:
                    client.create_order(
                        symbol=symbol,
                        side='SELL',
                        type='LIMIT',
                        quantity=str(previous_order['quantity']),
                        price=str(previous_order['price']),
                        timeInForce='GTC'
                    )
                else:
                    client.create_order(
                        symbol=symbol,
                        side='SELL',
                        type='STOP_LOSS_LIMIT',
                        quantity=str(previous_order['quantity']),
                        price=str(previous_order['price']),
                        stopPrice=str(previous_order['stop_price']),
                        timeInForce='GTC'
                    )
                print("Previous order restored.")
                return None
            except Exception as re:
                print("Failed to restore previous order:", re)
        else:
            print("No previous order to restore.")

        return None
    
    
# place stop limit buy order for one hour
def place_one_hour_stop_limit_buy_order(gprice):
    symbol = 'SOLUSDT'
    side = "BUY"
    stop_price = round(gprice, 2)
    limit_price = round((gprice+0.01), 2)

    previous_order = None

    # 1. Cancel previous STOP_LOSS_LIMIT orders
    try:
        open_orders = client.get_open_orders(symbol=symbol)
        for order in open_orders:
            if order['type'] == 'STOP_LOSS_LIMIT' and order['side'] == 'BUY':
                previous_order = {
                    'side': order['side'],
                    'quantity': float(order['origQty']),
                    'stop_price': float(order['stopPrice']),
                    'price': float(order['price'])
                }
                client.cancel_order(symbol=symbol, orderId=order['orderId'])
                print(f"Canceled previous STOP_LOSS_LIMIT buy order")
    except Exception as e:
        print(f"Error while canceling existing stop orders: {e}")
        return None
    
    available_usdt = check_usdt()
    available_usdt = available_usdt * 0.98
    if available_usdt < 10:
        print("Not enough USDT to place market buy order.")
        return None
    
    quantity = round(available_usdt / gprice, 3)

    # 2. Place new STOP_LOSS_LIMIT order
    try:
        print(f"Placing new STOP_LOSS_LIMIT order for one hour: {stop_price}")
        new_order = client.create_order(
            symbol=symbol,
            side=side,
            type="STOP_LOSS_LIMIT",
            quantity=str(quantity),
            price=str(limit_price),        
            stopPrice=str(stop_price),    
            timeInForce='GTC'
        )
        print("New STOP_LOSS_LIMIT buy order placed. Monitoring...")
        return new_order['orderId']

    except BinanceAPIException as e:
        print("Error placing new STOP_LOSS_LIMIT order:", e)

        if e.code == -2010 and "trigger immediately" in str(e.message).lower():
            print("STOP_LOSS_LIMIT rejected due to trigger price. Placing MARKET order instead...")
            try:
                market_order = client.create_order(
                    symbol=symbol,
                    side=side,
                    type="MARKET",
                    quantity=str(quantity)
                )
                print("Market order placed successfully.")
                return market_order['orderId']
            except Exception as me:
                print("Failed to place market order:", me)

        # 5. Restore previous order if placing failed
        if previous_order:
            try:
                print("Attempting to restore previous STOP_LOSS_LIMIT buy order...")
                restored_order = client.create_order(
                    symbol=symbol,
                    side='BUY',
                    type="STOP_LOSS_LIMIT",
                    quantity=str(previous_order['quantity']),
                    price=str(previous_order['price']),
                    stopPrice=str(previous_order['stop_price']),
                    timeInForce='GTC'
                )
                print("Previous order re-placed successfully.")
            except Exception as re:
                print("Failed to restore previous order:", re)
        else:
            print("No previous order to restore.")

        return None
    

# place stop market buy order
def place_stop_market_buy_order(gprice):
    symbol = 'SOLUSDT'
    side = "BUY"
    stop_price = round(gprice, 2)
    limit_price = round((gprice+0.01), 2)

    previous_order = None

    # 1. Cancel previous STOP_LOSS_LIMIT orders
    try:
        open_orders = client.get_open_orders(symbol=symbol)
        for order in open_orders:
            if order['type'] == 'STOP_LOSS_LIMIT' and order['side'] == 'BUY':
                previous_order = {
                    'side': order['side'],
                    'quantity': float(order['origQty']),
                    'stop_price': float(order['stopPrice']),
                    'price': float(order['price'])
                }
                client.cancel_order(symbol=symbol, orderId=order['orderId'])
                print(f"Canceled previous STOP_LOSS_LIMIT buy order")
    except Exception as e:
        print(f"Error while canceling existing stop orders: {e}")
        return None, None
    
    available_usdt = check_usdt()
    available_usdt = available_usdt * 0.98
    if available_usdt < 10:
        print("Not enough USDT to place market buy order.")
        return None, None
    
    quantity = round(available_usdt / gprice, 3)

    # 2. Place new STOP_LOSS_LIMIT order
    try:
        print(f"Placing new STOP_LOSS_LIMIT order: {stop_price}")
        new_order = client.create_order(
            symbol=symbol,
            side=side,
            type="STOP_LOSS_LIMIT",
            quantity=str(quantity),
            price=str(limit_price),        
            stopPrice=str(stop_price),    
            timeInForce='GTC'
        )
        print("New STOP_LOSS_LIMIT buy order placed. Monitoring...")
        order_placed_time = datetime.now()

        # 3. Monitor for 15 minutes (check every 3 min)
        for _ in range(5):
            time.sleep(3 * 60)
            order_status = client.get_order(symbol=symbol, orderId=new_order['orderId'])
            if order_status['status'] == 'FILLED':
                print("Order filled.")
                print(f'Buy price: {gprice}')
                return order_status['status'], order_placed_time

        # 4. Cancel if not filled after 15 minutes
        order_status = client.get_order(symbol=symbol, orderId=new_order['orderId'])
        if order_status['status'] != 'FILLED':
            client.cancel_order(symbol=symbol, orderId=new_order['orderId'])
            print("Order not filled after 15 minutes. Cancelled.")

        if previous_order:
            try:
                print("Attempting to restore previous STOP_LOSS_LIMIT buy order...")
                restored_order = client.create_order(
                    symbol=symbol,
                    side='BUY',
                    type="STOP_LOSS_LIMIT",
                    quantity=str(previous_order['quantity']),
                    price=str(previous_order['price']),
                    stopPrice=str(previous_order['stop_price']),
                    timeInForce='GTC'
                )
                print("Previous order re-placed successfully.")
            except Exception as re:
                print("Failed to restore previous order:", re)

        return order_status['status'], order_placed_time

    except BinanceAPIException as e:
        print("Error placing new STOP_LOSS_LIMIT order:", e)

        if e.code == -2010 and "trigger immediately" in e.message:
            print("STOP_LOSS_LIMIT rejected due to trigger price. Placing MARKET order instead...")
            try:
                market_order = client.create_order(
                    symbol=symbol,
                    side=side,
                    type="MARKET",
                    quantity=str(quantity)
                )
                print("Market order placed successfully.")
                return market_order['status'], datetime.now()
            except Exception as me:
                print("Failed to place market order:", me)

        # 5. Restore previous order if placing failed
        if previous_order:
            try:
                print("Attempting to restore previous STOP_LOSS_LIMIT buy order...")
                restored_order = client.create_order(
                    symbol=symbol,
                    side='BUY',
                    type="STOP_LOSS_LIMIT",
                    quantity=str(previous_order['quantity']),
                    price=str(previous_order['price']),
                    stopPrice=str(previous_order['stop_price']),
                    timeInForce='GTC'
                )
                print("Previous order re-placed successfully.")
            except Exception as re:
                print("Failed to restore previous order:", re)
        else:
            print("No previous order to restore.")

        return None, None


# place market buy order
def market_buy_order(gprice):
    symbol = 'SOLUSDT'

    # === Cancel previous STOP_MARKET buy order ===
    try:
        open_orders = client.get_open_orders(symbol=symbol)
        for order in open_orders:
            if order['type'] == 'STOP_LOSS_LIMIT' and order['side'] == 'BUY':
                client.cancel_order(symbol=symbol, orderId=order['orderId'])
                print("Canceled previous STOP_LOSS_LIMIT buy order.")
    except Exception as e:
        print(f"Error while canceling existing stop orders: {e}")
        return None
    
    available_usdt = check_usdt()
    available_usdt = available_usdt * 0.98

    # Return if not enough USDT
    if available_usdt < 10:
        print("Not enough USDT to place market buy order.")
        return None

    try:
        # === Get correct step size and precision ===
        symbol_info = client.get_symbol_info(symbol)
        lot_filter = next(f for f in symbol_info['filters'] if f['filterType'] == 'LOT_SIZE')
        step_size = float(lot_filter['stepSize'])
        precision = int(round(-math.log10(step_size)))

        # === Calculate valid quantity ===
        raw_quantity = available_usdt / gprice
        quantity = math.floor(raw_quantity / step_size) * step_size
        quantity = round(quantity, precision)

        if quantity <= 0:
            print("Calculated quantity is too low.")
            return None

        # === Place market buy order ===
        order = client.order_market_buy(symbol=symbol, quantity=quantity)
        print(f"Market BUY order placed. Order ID: {order['orderId']}")
        print(f"Buy quantity: {quantity}, Price at call: {gprice}")

        return order['orderId']

    except Exception as e:
        print(f"ailed to place market buy order: {e}")
        return None


# place limit sell order for 15 minute
def place_stop_market_sell_order(gprice):
    symbol = 'SOLUSDT'
    side = 'SELL'
    try:
        previous_order = None
        previous_order_type = None

        try:
            oco_orders = client.get_open_oco_orders()
        except Exception as e:
            print(f"Error fetching OCO orders: {e}")
            oco_orders = []

        if oco_orders:
            oco = oco_orders[0]
            stop_leg = None
            limit_leg = None

            try:
                # Loop through each order in the OCO
                for o in oco["orders"]:
                    order_details = client.get_order(symbol=symbol, orderId=o["orderId"])
                    if order_details["type"] == "STOP_LOSS_LIMIT":
                        stop_leg = order_details
                    elif order_details["type"] == "LIMIT_MAKER":
                        limit_leg = order_details
            except Exception as e:
                print(f"Error fetching OCO order details: {e}")

            if stop_leg and limit_leg:
                previous_order = {
                    "type": "OCO",
                    "side": stop_leg["side"],
                    "quantity": float(stop_leg["origQty"]),
                    "price": float(limit_leg.get("price", 0)), 
                    "stop_price": float(stop_leg.get("stopPrice", 0)),
                    "stop_limit_price": float(stop_leg.get("price", 0)),
                    "orderListId": oco["orderListId"]
                }
                previous_order_type = previous_order['type']

            try:
                result = cancel_oco_order(symbol, oco["orderListId"])
                print(f"Cancel result: {result}")
            except Exception as e:
                print(f"Error cancelling OCO order: {e}")
                return None, None

        else:
            # 1. Cancel any existing STOP_LOSS_LIMIT sell orders
            try:
                open_orders = client.get_open_orders(symbol=symbol)
                for order in open_orders:
                    if order['side'] == 'SELL':
                        previous_order_type = order['type']
                        previous_order = {
                            'type': order['type'],
                            'side': order['side'],
                            'quantity': float(order['origQty']),
                            'price': float(order.get('price', 0)),
                            'stop_price': float(order.get('stopPrice', 0)),
                            'orderId': order['orderId']
                        }
                        client.cancel_order(symbol=symbol, orderId=order['orderId'])
                        print("Canceled previous STOP_LOSS_LIMIT sell order.")
            except Exception as e:
                print(f"Error while canceling existing stop orders: {e}")
                return None, None
        
        available_sol = float(check_SOL())
        quantity = adjust_quantity(symbol, available_sol * 0.99)

        if quantity < 0.01:
            print(f"Available quantity too low ({quantity}) to place a sell order.")
            return None, None

        stop_price, limit_price = get_valid_stop_limit_prices(symbol, gprice)

    # 2. Place new STOP_LOSS_LIMIT sell order
        print(f"Placing new STOP_LOSS_LIMIT order: {stop_price}")
        new_order = client.create_order(
            symbol=symbol,
            side=side,
            type="STOP_LOSS_LIMIT",
            quantity=str(quantity),
            price=str(limit_price),        
            stopPrice=str(stop_price),    
            timeInForce='GTC'
        )
        print("New STOP_LOSS_LIMIT sell order placed. Monitoring...")
        order_placed_time = datetime.now()

        # 3. Check status every 3 minutes for 15 minutes
        for _ in range(5):
            time.sleep(3 * 60)
            order_status = client.get_order(symbol=symbol, orderId=new_order['orderId'])
            if order_status['status'] == 'FILLED':
                print("Order filled.")
                print(f"Sell price: {gprice}")
                return order_status['status'], order_placed_time

        # 4. After 15 mins, cancel if not filled
        order_status = client.get_order(symbol=symbol, orderId=new_order['orderId'])
        if order_status['status'] != 'FILLED':
            client.cancel_order(symbol=symbol, orderId=new_order['orderId'])
            print("Order not filled after 15 minutes. Cancelled.")

        # Restore previous order after timeout cancellation
        if previous_order:
            try:
                print(f"Attempting to restore previous {previous_order_type} sell order...")

                if previous_order_type == "LIMIT":              
                    recreate_order = client.create_order(
                        symbol=symbol,
                        side='SELL',
                        type='LIMIT',
                        quantity=str(previous_order['quantity']),
                        price=str(previous_order['price']),
                        timeInForce='GTC'
                    )
                    print("Previous order re-placed successfully.") 
                elif previous_order_type == "STOP_LOSS_LIMIT": 
                    recreate_order = client.create_order(
                        symbol=symbol,
                        side='SELL',
                        type='STOP_LOSS_LIMIT',
                        quantity=str(previous_order['quantity']),
                        price=str(previous_order['price']),
                        stopPrice=str(previous_order['stop_price']),
                        timeInForce='GTC'
                    )
                    print("Previous order re-placed successfully.")
                elif previous_order_type == "OCO":       
                    order_id = place_manual_oco_order(
                        quantity=quantity,
                        tp_price=previous_order['price'],
                        stop_price=previous_order['stop_price'],
                        stop_limit_price=previous_order['stop_limit_price']
                    )
                    if order_id:
                        print("Previous OCO Order placed, ID:", order_id)
            except Exception as re:
                print("Failed to restore previous order after timeout:", re)
        else:
            print("No previous order to restore after timeout.")

        return order_status['status'], order_placed_time

    except Exception as e:
        print("General error occurred:", e)
        if hasattr(e, "code"):
            # 5. Fallback to MARKET SELL if trigger would execute immediately
            if e.code == -2010 and "trigger immediately" in e.message:
                print("STOP_LOSS_LIMIT rejected due to trigger price. Placing MARKET SELL instead...")
                try:
                    market_order = client.create_order(
                        symbol=symbol,
                        side=side,
                        type="MARKET",
                        quantity=quantity
                    )
                    print("Market sell order placed successfully.")
                    return market_order['status'], datetime.now()
                except Exception as me:
                    print("Failed to place market sell order:", me)

        # 5. Restore previous order if needed
        if previous_order:
            try:
                print(f"Attempting to restore previous {previous_order_type} sell order...")

                if previous_order_type == "LIMIT":              
                    recreate_order = client.create_order(
                        symbol=symbol,
                        side='SELL',
                        type='LIMIT',
                        quantity=str(previous_order['quantity']),
                        price=str(previous_order['price']),
                        timeInForce='GTC'
                    )
                    print("Previous order re-placed successfully.") 
                elif previous_order_type == "STOP_LOSS_LIMIT": 
                    recreate_order = client.create_order(
                        symbol=symbol,
                        side='SELL',
                        type='STOP_LOSS_LIMIT',
                        quantity=str(previous_order['quantity']),
                        price=str(previous_order['price']),
                        stopPrice=str(previous_order['stop_price']),
                        timeInForce='GTC'
                    )
                    print("Previous order re-placed successfully.")
                elif previous_order_type == "OCO":       
                    order_id = place_manual_oco_order(
                        quantity=quantity,
                        tp_price=previous_order['price'],
                        stop_price=previous_order['stop_price'],
                        stop_limit_price=previous_order['stop_limit_price']
                    )
                    if order_id:
                        print("Previous OCO Order placed, ID:", order_id)
            except Exception as re:
                print("Failed to restore previous order:", re)
        else:
            print("No previous order to restore.")

        return None, None
    

# place limit sell order for one hour
def place_one_hour_stop_limit_sell_order(gprice):
    symbol = 'SOLUSDT'
    side = 'SELL'
    try:
        previous_order = None
        previous_order_type = None

        try:
            oco_orders = client.get_open_oco_orders()
        except Exception as e:
            print(f"Error fetching OCO orders: {e}")
            oco_orders = []

        if oco_orders:
            oco = oco_orders[0]
            stop_leg = None
            limit_leg = None

            try:
                # Loop through each order in the OCO
                for o in oco["orders"]:
                    order_details = client.get_order(symbol=symbol, orderId=o["orderId"])
                    if order_details["type"] == "STOP_LOSS_LIMIT":
                        stop_leg = order_details
                    elif order_details["type"] == "LIMIT_MAKER":
                        limit_leg = order_details
            except Exception as e:
                print(f"Error fetching OCO order details: {e}")

            if stop_leg and limit_leg:
                previous_order = {
                    "type": "OCO",
                    "side": stop_leg["side"],
                    "quantity": float(stop_leg["origQty"]),
                    "price": float(limit_leg.get("price", 0)), 
                    "stop_price": float(stop_leg.get("stopPrice", 0)),
                    "stop_limit_price": float(stop_leg.get("price", 0)),
                    "orderListId": oco["orderListId"]
                }
                previous_order_type = previous_order['type']
                last_stoploss_price = previous_order["stop_price"]
                if last_stoploss_price > gprice:
                    print("Previous OCO stoploss is ok, no need to place new one")
                    return stop_leg["orderId"]

            try:
                result = cancel_oco_order(symbol,oco["orderListId"])
                print(f"Cancel result: {result}")
            except Exception as e:
                print(f"Error cancelling OCO order: {e}")
                return None

        else:
            # 1. Cancel any existing STOP_LOSS_LIMIT sell orders
            try:
                open_orders = client.get_open_orders(symbol=symbol)
                for order in open_orders:
                    if order['side'] == 'SELL':
                        previous_order_type = order['type']
                        previous_order = {
                            'type': order['type'],
                            'side': order['side'],
                            'quantity': float(order['origQty']),
                            'price': float(order.get('price', 0)),
                            'stop_price': float(order.get('stopPrice', 0)),
                            'orderId': order['orderId']
                        }
                        if previous_order_type == "STOP_LOSS_LIMIT":
                            last_stoploss_price = previous_order['stop_price']
                            if last_stoploss_price > gprice: 
                                print("Previous stoploss is ok, no need to place new one")
                                return order['orderId']
                        client.cancel_order(symbol=symbol, orderId=order['orderId'])
                        print("Canceled previous STOP_LOSS_LIMIT sell order.")
            except Exception as e:
                print(f"Error while canceling existing stop orders: {e}")
                return None
        
        
        available_sol = float(check_SOL())
        quantity = adjust_quantity(symbol, available_sol * 0.99)

        if quantity < 0.01:
            print(f"Available quantity too low ({quantity}) to place a sell order.")
            return None

        stop_price, limit_price = get_valid_stop_limit_prices(symbol, gprice)

    # 2. Place new STOP_LOSS_LIMIT sell order
        print(f"Placing new STOP_LOSS_LIMIT order: {stop_price}")
        new_order = client.create_order(
            symbol=symbol,
            side=side,
            type="STOP_LOSS_LIMIT",
            quantity=str(quantity),
            price=str(limit_price),        
            stopPrice=str(stop_price),    
            timeInForce='GTC'
        )
        print("New STOP_LOSS_LIMIT sell order placed for one hour.")
        return new_order['orderId']

    except BinanceAPIException as e:
        print("Error placing STOP_LOSS_LIMIT sell order:", e)

        # 5. Fallback to MARKET SELL if trigger would execute immediately
        if e.code == -2010 and "trigger immediately" in str(e.message).lower():
            print("STOP_LOSS_LIMIT rejected due to trigger price. Placing MARKET SELL instead...")
            try:
                market_order = client.create_order(
                    symbol=symbol,
                    side=side,
                    type="MARKET",
                    quantity=str(quantity)
                )
                print("Market sell order placed successfully.")
                return market_order['orderId']
            except Exception as me:
                print("Failed to place market sell order:", me)

        # 5. Restore previous order if needed
        if previous_order:
            try:
                print(f"Attempting to restore previous {previous_order_type} sell order...")

                if previous_order_type == "LIMIT":              
                    recreate_order = client.create_order(
                        symbol=symbol,
                        side='SELL',
                        type='LIMIT',
                        quantity=str(previous_order['quantity']),
                        price=str(previous_order['price']),
                        timeInForce='GTC'
                    )
                    print("Previous order re-placed successfully.") 
                elif previous_order_type == "STOP_LOSS_LIMIT": 
                    recreate_order = client.create_order(
                        symbol=symbol,
                        side='SELL',
                        type='STOP_LOSS_LIMIT',
                        quantity=str(previous_order['quantity']),
                        price=str(previous_order['price']),
                        stopPrice=str(previous_order['stop_price']),
                        timeInForce='GTC'
                    )
                    print("Previous order re-placed successfully.")
                elif previous_order_type == "OCO":       
                    order_id = place_manual_oco_order(
                        quantity=quantity,
                        tp_price=previous_order['price'],
                        stop_price=previous_order['stop_price'],
                        stop_limit_price=previous_order['stop_limit_price']
                    )
                    if order_id:
                        print("Previous OCO Order placed, ID:", order_id)
            except Exception as re:
                print("Failed to restore previous order:", re)
        else:
            print("No previous order to restore.")

        return None


# place limit sell order for 30 min candle
def place_stop_market_sell_order_30min(gprice):
    symbol = 'SOLUSDT'
    side = 'SELL'
    try:
        previous_order = None

        # 1. Cancel any existing STOP_LOSS_LIMIT sell orders
        try:
            open_orders = client.get_open_orders(symbol=symbol)
            for order in open_orders:
                if order['side'] == 'SELL':
                    previous_order = {
                        'side': order['side'],
                        'quantity': float(order['origQty']),
                        'price': float(order.get('price', 0)),
                        'stop_price': float(order.get('stopPrice', 0))
                    }
                    client.cancel_order(symbol=symbol, orderId=order['orderId'])
                    print("Canceled previous STOP_LOSS_LIMIT sell order.")
        except Exception as e:
            print(f"Error while canceling existing stop orders: {e}")
            return None, None
        
        available_sol = float(check_SOL())
        quantity = adjust_quantity(symbol, available_sol * 0.99)

        if quantity < 0.01:
            print(f"Available quantity too low ({quantity}) to place a sell order.")
            return None, None

        stop_price, limit_price = get_valid_stop_limit_prices(symbol, gprice)

        # 2. Place new STOP_LOSS_LIMIT sell order
        print(f"Placing new STOP_LOSS_LIMIT order: {stop_price}")
        new_order = client.create_order(
            symbol=symbol,
            side=side,
            type="STOP_LOSS_LIMIT",
            quantity=str(quantity),
            price=str(limit_price),        
            stopPrice=str(stop_price),    
            timeInForce='GTC'
        )
        print("New STOP_LOSS_LIMIT sell order placed for 30 minutes. Monitoring...")
        order_placed_time = datetime.now()

        # 3. Check status every 3 minutes for 30 minutes
        for _ in range(10):  # 10 checks × 3 mins = 30 mins
            time.sleep(3 * 60)
            order_status = client.get_order(symbol=symbol, orderId=new_order['orderId'])
            if order_status['status'] == 'FILLED':
                print("Order filled.")
                print(f"Sell price: {gprice}")
                return order_status['status'], order_placed_time

        # 4. After 30 mins, cancel if not filled
        order_status = client.get_order(symbol=symbol, orderId=new_order['orderId'])
        if order_status['status'] != 'FILLED':
            client.cancel_order(symbol=symbol, orderId=new_order['orderId'])
            print("Order not filled after 30 minutes. Cancelled.")

        # Restore previous order after timeout cancellation
        if previous_order:
            try:
                print("Restoring previous STOP_LOSS_LIMIT sell order...")
                if previous_order['stop_price'] == 0:
                    client.create_order(
                        symbol=symbol,
                        side='SELL',
                        type='LIMIT',
                        quantity=str(previous_order['quantity']),
                        price=str(previous_order['price']),
                        timeInForce='GTC'
                    )
                else:
                    client.create_order(
                        symbol=symbol,
                        side='SELL',
                        type='STOP_LOSS_LIMIT',
                        quantity=str(previous_order['quantity']),
                        price=str(previous_order['price']),
                        stopPrice=str(previous_order['stop_price']),
                        timeInForce='GTC'
                    )
                print("Previous order re-placed successfully after timeout.")
            except Exception as re:
                print("Failed to restore previous order after timeout:", re)
        else:
            print("No previous order to restore after timeout.")

        return order_status['status'], order_placed_time

    except BinanceAPIException as e:
        print("Error placing STOP_LOSS_LIMIT sell order:", e)

        if e.code == -2010 and "trigger immediately" in e.message:
            print("STOP_LOSS_LIMIT rejected due to trigger price. Placing MARKET SELL instead...")
            try:
                market_order = client.create_order(
                    symbol=symbol,
                    side=side,
                    type="MARKET",
                    quantity=quantity
                )
                print("Market sell order placed successfully.")
                return market_order['status'], datetime.now()
            except Exception as me:
                print("Failed to place market sell order:", me)

        if previous_order:
            try:
                print("Attempting to restore previous STOP_LOSS_LIMIT sell order...")
                if previous_order['stop_price'] == 0:
                    client.create_order(
                        symbol=symbol,
                        side='SELL',
                        type='LIMIT',
                        quantity=str(previous_order['quantity']),
                        price=str(previous_order['price']),
                        timeInForce='GTC'
                    )
                else:
                    client.create_order(
                        symbol=symbol,
                        side='SELL',
                        type='STOP_LOSS_LIMIT',
                        quantity=str(previous_order['quantity']),
                        price=str(previous_order['price']),
                        stopPrice=str(previous_order['stop_price']),
                        timeInForce='GTC'
                    )
                print("Previous order re-placed successfully.")
            except Exception as re:
                print("Failed to restore previous order:", re)
        else:
            print("No previous order to restore.")

        return None, None


# place sell order for adjusting stoploss
def place_stoploss_sell_order(gprice,set_time = None):
    symbol = 'SOLUSDT'
    side = 'SELL'
    if(set_time == 1):
        gprice = gprice - (gprice/100)
    try:
        previous_order = None
        previous_order_type = None

        try:
            oco_orders = client.get_open_oco_orders()
        except Exception as e:
            print(f"Error fetching OCO orders: {e}")
            oco_orders = []

        if oco_orders:
            oco = oco_orders[0]
            stop_leg = None
            limit_leg = None

            try:
                # Loop through each order in the OCO
                for o in oco["orders"]:
                    order_details = client.get_order(symbol=symbol, orderId=o["orderId"])
                    if order_details["type"] == "STOP_LOSS_LIMIT":
                        stop_leg = order_details
                    elif order_details["type"] == "LIMIT_MAKER":
                        limit_leg = order_details
            except Exception as e:
                print(f"Error fetching OCO order details: {e}")

            if stop_leg and limit_leg:
                previous_order = {
                    "type": "OCO",
                    "side": stop_leg["side"],
                    "quantity": float(stop_leg["origQty"]),
                    "price": float(limit_leg.get("price", 0)), 
                    "stop_price": float(stop_leg.get("stopPrice", 0)),
                    "stop_limit_price": float(stop_leg.get("price", 0)),
                    "orderListId": oco["orderListId"]
                }
                previous_order_type = previous_order['type']
                last_stoploss_price = previous_order["stop_price"]
                if last_stoploss_price > gprice:
                    print("Previous OCO stoploss is ok, no need to place new one")
                    return stop_leg["orderId"]

            try:
                result = cancel_oco_order(symbol,oco["orderListId"])
                print(f"Cancel result: {result}")
            except Exception as e:
                print(f"Error cancelling OCO order: {e}")
                return None

        else:
            # 1. Cancel any existing STOP_LOSS_LIMIT sell orders
            try:
                open_orders = client.get_open_orders(symbol=symbol)
                for order in open_orders:
                    if order['side'] == 'SELL':
                        previous_order_type = order['type']
                        previous_order = {
                            'type': order['type'],
                            'side': order['side'],
                            'quantity': float(order['origQty']),
                            'price': float(order.get('price', 0)),
                            'stop_price': float(order.get('stopPrice', 0)),
                            'orderId': order['orderId']
                        }
                        if previous_order_type == "STOP_LOSS_LIMIT":
                            last_stoploss_price = previous_order['stop_price']
                            if last_stoploss_price > gprice: 
                                print("Previous stoploss is ok, no need to place new one")
                                return order['orderId']
                        client.cancel_order(symbol=symbol, orderId=order['orderId'])
                        print("Canceled previous STOP_LOSS_LIMIT sell order.")
            except Exception as e:
                print(f"Error while canceling existing stop orders: {e}")
                return None
        
        available_sol = float(check_SOL())
        quantity = adjust_quantity(symbol, available_sol * 0.99)

        if quantity < 0.01:
            print(f"Available quantity too low ({quantity}) to place a sell order.")
            return None

        stop_price, limit_price = get_valid_stop_limit_prices(symbol, gprice)

    # 2. Place new sell order
        if previous_order_type == "OCO":
            print("Placing new OCO sell order...")
            order_id = place_manual_oco_order(
                quantity=quantity,
                tp_price=previous_order['price'],
                stop_price=stop_price,
                stop_limit_price=limit_price
            )
            if order_id:
                print(f"OCO Order placed, ID: {order_id}, Target price: {previous_order['price']}, Stoploss Limit: {stop_price}")
                return order_id
            else:
                print("OCO order failed.")
        else:
            print(f"Placing new STOP_LOSS_LIMIT order: {stop_price}")
            new_order = client.create_order(
                symbol=symbol,
                side=side,
                type="STOP_LOSS_LIMIT",
                quantity=str(quantity),
                price=str(limit_price),        
                stopPrice=str(stop_price),    
                timeInForce='GTC'
            )
            print("New STOP_LOSS_LIMIT sell order placed.")
            return new_order['orderId']

    except Exception as e:
        print("Error placing STOP_LOSS_LIMIT sell order:", e)

        # 5. Fallback to MARKET SELL if trigger would execute immediately
        if e.code == -2010 and "trigger immediately" in e.message:
            print("STOP_LOSS_LIMIT rejected due to trigger price. Placing MARKET SELL instead...")
            try:
                market_order = client.create_order(
                    symbol=symbol,
                    side=side,
                    type="MARKET",
                    quantity=str(quantity)
                )
                print("Market sell order placed successfully.")
                return market_order['orderId']
            except Exception as me:
                print("Failed to place market sell order:", me)

        # 5. Restore previous order if needed
        if previous_order:
            try:
                recreate_order = None
                print(f"Attempting to restore previous {previous_order_type} sell order...")

                if previous_order_type == "LIMIT":              
                    recreate_order = client.create_order(
                        symbol=symbol,
                        side='SELL',
                        type='LIMIT',
                        quantity=str(previous_order['quantity']),
                        price=str(previous_order['price']),
                        timeInForce='GTC'
                    )
                    print("Previous order re-placed successfully.")  
                    return recreate_order['orderId']
                elif previous_order_type == "STOP_LOSS_LIMIT": 
                    recreate_order = client.create_order(
                        symbol=symbol,
                        side='SELL',
                        type='STOP_LOSS_LIMIT',
                        quantity=str(previous_order['quantity']),
                        price=str(previous_order['price']),
                        stopPrice=str(previous_order['stop_price']),
                        timeInForce='GTC'
                    )
                    print("Previous order re-placed successfully.")  
                    return recreate_order['orderId']
                elif previous_order_type == "OCO":       
                    order_id = place_manual_oco_order(
                        quantity=quantity,
                        tp_price=previous_order['price'],
                        stop_price=previous_order['stop_price'],
                        stop_limit_price=previous_order['stop_limit_price']
                    )
                    if order_id:
                        print("Previous OCO Order placed, ID:", order_id)
                        return order_id
                    else:
                        print("OCO order failed.") 
            except Exception as re:
                print("Failed to restore previous order:", re)
        else:
            print("No previous order to restore.")

        return None


# Profit based limit sell order
def place_profit_stop_limit_sell_order(gprice=None):
    symbol = 'SOLUSDT'
    side = 'SELL'
    try:
        previous_order = None

        # 1. Cancel any existing STOP_LOSS_LIMIT sell orders
        try:
            open_orders = client.get_open_orders(symbol=symbol)
            for order in open_orders:
                if order['side'] == 'SELL':
                    previous_order = {
                        'side': order['side'],
                        'quantity': float(order['origQty']),
                        'price': float(order.get('price', 0)),
                        'stop_price': float(order.get('stopPrice', 0))
                    }
                    if(gprice == None):
                        gprice = previous_order['price']
                        gprice = gprice + (gprice/100)
                    elif(previous_order['price']>gprice):
                        print('previous profit is higher,Previous order is not cancelling.')
                        return None
                    client.cancel_order(symbol=symbol, orderId=order['orderId'])
                    print("Canceled previous STOP_LOSS_LIMIT sell order.")
        except Exception as e:
            print(f"Error while canceling existing stop orders: {e}")
            return None
        
        available_sol = float(check_SOL())
        quantity = adjust_quantity(symbol, available_sol * 0.99)

        if quantity < 0.01:
            print(f"Available quantity too low ({quantity}) to place a sell order.")
            return None

        limit_price = adjust_price(symbol, gprice, direction='up')

    # 2. Place new STOP_LOSS_LIMIT sell order
        print(f"Placing expected profit limit order: {limit_price}")
        new_order = client.create_order(
            symbol=symbol,
            side=side,
            type="LIMIT",
            quantity=str(quantity),
            price=str(limit_price),
            timeInForce='GTC'
        )
        print("New STOP_LOSS_LIMIT sell order placed.")

    except BinanceAPIException as e:
        print("Error placing STOP_LOSS_LIMIT sell order:", e)

        # 3. Restore previous order if needed
        if previous_order:
            try:
                print("Attempting to restore previous STOP_LOSS_LIMIT sell order...")
                if previous_order['stop_price'] == 0:
                    # Restore as LIMIT order
                    client.create_order(
                        symbol=symbol,
                        side='SELL',
                        type='LIMIT',
                        quantity=str(previous_order['quantity']),
                        price=str(previous_order['price']),
                        timeInForce='GTC'
                    )
                else:
                    # Restore as STOP_LOSS_LIMIT order
                    client.create_order(
                        symbol=symbol,
                        side='SELL',
                        type='STOP_LOSS_LIMIT',
                        quantity=str(previous_order['quantity']),
                        price=str(previous_order['price']),
                        stopPrice=str(previous_order['stop_price']),
                        timeInForce='GTC'
                    )
                print("Previous order re-placed successfully.")
            except Exception as re:
                print("Failed to restore previous order:", re)
        else:
            print("No previous order to restore.")

        return None
    
# Another strategy to place profit based limit sell order
def place_half_amount_profit_stop_limit_sell_order():
    gprice = None
    symbol = 'SOLUSDT'
    side = 'SELL'
    try:
        previous_order = None

        # 1. Cancel any existing STOP_LOSS_LIMIT sell orders
        try:
            open_orders = client.get_open_orders(symbol=symbol)
            for order in open_orders:
                if order['side'] == 'SELL':
                    previous_order = {
                        'side': order['side'],
                        'quantity': float(order['origQty']),
                        'price': float(order.get('price', 0)),
                        'stop_price': float(order.get('stopPrice', 0))
                    }
                    gprice = previous_order['price']
                    client.cancel_order(symbol=symbol, orderId=order['orderId'])
                    print("Canceled previous STOP_LOSS_LIMIT sell order.")
        except Exception as e:
            print(f"Error while canceling existing stop orders: {e}")
            return None
        
        available_sol = float(check_SOL())
        available_sol = available_sol/2
        quantity = adjust_quantity(symbol, available_sol * 0.99)

        if quantity < 0.01:
            print(f"Available quantity too low ({quantity}) to place a sell order.")
            return None

        limit_price = adjust_price(symbol, gprice, direction='up')

    # 2. Place new STOP_LOSS_LIMIT sell order
        print(f"Placing expected profit limit order: {limit_price}")
        new_order = client.create_order(
            symbol=symbol,
            side=side,
            type="LIMIT",
            quantity=str(quantity),
            price=str(limit_price),
            timeInForce='GTC'
        )
        print("New LIMIT sell order placed.")

    except BinanceAPIException as e:
        print("Error placing LIMIT sell order:", e)

        # 3. Restore previous order if needed
        if previous_order:
            try:
                print("Attempting to restore previous STOP_LOSS_LIMIT sell order...")
                restored_order = client.create_order(
                    symbol=symbol,
                    side='SELL',
                    type="LIMIT" if previous_order['stop_price'] == 0 else "STOP_LOSS_LIMIT",
                    quantity=str(previous_order['quantity']),
                    price=str(previous_order['price']),
                    stopPrice=str(previous_order['stop_price']) if previous_order['stop_price'] > 0 else None,
                    timeInForce='GTC'
                )
                print("Previous order re-placed successfully.")
            except Exception as re:
                print("Failed to restore previous order:", re)
        else:
            print("No previous order to restore.")

        return None
    

# place market sell order
def market_sell_order(gprice):
    symbol = 'SOLUSDT'

    # === Cancel existing STOP_MARKET sell orders ===
    try:
        open_orders = client.get_open_orders(symbol=symbol)
        for order in open_orders:
            if order['side'] == 'SELL':
                if order.get("orderListId", -1) != -1:
                    cancel_oco_order(symbol=symbol, orderListId=order["orderListId"])
                    print(f"Canceled previous OCO sell order (orderListId={order['orderListId']})")
                else:
                    client.cancel_order(symbol=symbol, orderId=order['orderId'])
                    print(f"Canceled previous {order['type']} sell order (orderId={order['orderId']})")
    except Exception as e:
        print(f"Error while canceling existing sell orders: {e}")
        return None

    quantity = check_SOL()

    # Return early if quantity is too low
    if quantity < 0.01:
        print("No SOL available to sell.")
        return None

    try:
        # === Get step size & precision from symbol info ===
        symbol_info = client.get_symbol_info(symbol)
        lot_filter = next(f for f in symbol_info['filters'] if f['filterType'] == 'LOT_SIZE')
        step_size = float(lot_filter['stepSize'])
        precision = int(round(-math.log10(step_size)))

        # Round quantity safely
        quantity = math.floor(quantity / step_size) * step_size
        quantity = round(quantity, precision)

        if quantity <= 0:
            print("Calculated quantity is too small to sell.")
            return None
        
        # === Place market sell order ===
        order = client.order_market_sell(symbol=symbol, quantity=quantity)
        print(f"Market SELL order placed. Order ID: {order['orderId']}")
        print(f"Sell quantity: {quantity}, Price at call: {gprice}")
        return order

    except Exception as e:
        print(f"Failed to place market sell order: {e}")
        return None
    