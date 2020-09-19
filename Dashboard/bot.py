import websocket, json, pprint, talib, numpy
from binance.client import Client
from binance.enums import *
import config

#Websocket client
# SOCKET = "wss://stream.binance.com:9443/ws/<symbol>@kline_<interval>"
SOCKET = "wss://stream.binance.com:9443/ws/ethusdt@kline_1m"
RSI_PERIOD = 14
RSI_OVERBOUGHT = 70
RSI_OVERSOLD = 30
TRADE_SYMBOL = 'ETHUSD'
TRADE_QUANTITY = 0.005

closes = []
inPosition = False

client = Client(config.API_KEY, config.API_SECRET, tld='uk')

def order(side, quantity, symbol, order_type=ORDER_TYPE_MARKET):
    try:
        order = client.create_order(symbol=symbol, side = side, type=order_type, quantity=quantity)
        print(order)
        return True
    except Exception:
        return False
    return True

#Create websocket client
def on_open(ws):
    print("Opened Connection")

def on_close(ws):
    print("Closed Connection")

def on_message(ws, message):
    global closes

    json_message = json.loads(message)
    pprint.pprint(json_message)

    candle = json_message['k']

    candleClosed = candle['x']
    close = candle['c']

    if candleClosed:
        print(f"Candle closed at {close}")
        closes.append(float(close))

    if len(closes) > RSI_PERIOD:
        np_closes = numpy.array(closes)
        rsi = talib.RSI(np_closes, RSI_PERIOD)
        print(rsi)
        last_rsi = rsi[-1]

        if last_rsi > RSI_OVERBOUGHT:
            #Sell
            if inPosition:
                #Sell
                order_succeeded = order(SIDE_SELL, TRADE_QUANTITY, TRADE_SYMBOL)
                if order_succeeded:
                    inPosition = False
            else:
                #Nothing to do
                "...(no sale)"
        if last_rsi < RSI_OVERSOLD:
            #Buy
            if inPosition:
                #We already own
                print("...no buy")
            else:
                #If we have not already bought: buy
                order_succeeded = order(SIDE_BUY, TRADE_QUANTITY, TRADE_SYMBOL)
                if order_succeeded:
                    inPosition = True

ws = websocket.WebSocketApp(SOCKET, on_open = on_open, on_close = on_close, on_message = on_message)
ws.run_forever()