import websocket, json, numpy, csv
from binance.client import Client
from binance.enums import *
import config
import math
import btalib
import pandas as pd
import datetime
import concurrent.futures

#Websocket client
# SOCKET = "wss://stream.binance.com:9443/ws/<symbol>@kline_<interval>"

def getSocket(TOKEN):
    print(f'Retreiving {TOKEN} socket from: wss://stream.binance.com:9443/ws/{TOKEN.lower()}gbp@kline_1d')
    return f"wss://stream.binance.com:9443/ws/{TOKEN.lower()}usdt@kline_1d"

# #params= ['fast', 'slow', ORDER_PERCENTAGE]
# params = [12, 26, 0.95]

def order(side, quantity, symbol, order_type=ORDER_TYPE_MARKET):
    try:
        client = Client(config.API_KEY, config.API_SECRET)
        order = client.create_order(symbol=symbol, side = side, type=order_type, quantity=quantity)
        print(order)
        return True
    except Exception as e:
        print(e)
        print("ERROR ORDERING")
        return False
    return True

#Create websocket client
def on_open(ws):
    print("Opened Connection")

def on_close(ws):
    print("Closed Connection")

def sellAmount(TOKEN):
    for balance in balances:
        if balance['asset'] == TOKEN:
            return balance['free']

def on_message(ws, message):

    client = Client(config.API_KEY, config.API_SECRET)
    info = client.get_account()
    exchange_info = client.get_exchange_info()
    balances = (info['balances'])
    symbols = exchange_info['symbols']

    try:
        inPosition = inPosition
    except:
        inPosition = False
    cash = 12
    json_message = json.loads(message)
    TRADE_SYMBOL = json_message['s']
    TOKEN = TRADE_SYMBOL.replace('USDT', '')
    candle = json_message['k']
    t = datetime.datetime.fromtimestamp(candle['t']/1000)
    day = t.strftime('%Y-%m-%d')
    candle['t'] = day
    formatted_message = (candle['t'], candle['o'], candle['h'], candle['l'], candle['c'], candle['v'], 0.00)
    
    if candle['x']: #If the candle is closed, we append to the csv
        f = open(f"data/all_time_daily_{TOKEN.lower()}.csv", 'a')
        writer = csv.writer(f)
        writer.writerow(formatted_message)
        f.close()
        print("Today's data added to CSV!")
        
    df = pd.read_csv(f'data/all_time_daily_{TOKEN.lower()}.csv', parse_dates=True)

    stochastic = btalib.stochastic(df.High, df.Low, df.Close)
    todays_stochastic = stochastic.df.iloc[[-1],[-1]]

    fast_moving_average = btalib.sma(
        df,
        period=12,
    )
    
    slow_moving_average = btalib.sma(
        df,
        period=26,
    )
    
    #Execute buy and sell orders based off of conditions:
    if not inPosition:
        if (fast_moving_average.df.iloc[[-1],[-1]] >= slow_moving_average.df.iloc[[-1],[-1]]).bool() and (todays_stochastic > 50).bool():
            amount_to_invest = (0.95 * cash)
            TRADE_QUANTITY = round((amount_to_invest/ df.Close.iloc[-1]), 5)
            print(f"Buying {TRADE_QUANTITY} of {TRADE_SYMBOL} at {df.Close[0]}")

            order_succeeded = order(SIDE_BUY, TRADE_QUANTITY, TRADE_SYMBOL)
            if order_succeeded:
                print(f"Bought {TRADE_QUANTITY} of {TRADE_SYMBOL} Successfully")
                inPosition = True
    
    if inPosition:
        if (fast_moving_average.df.iloc[[-1],[-1]] <= slow_moving_average.df.iloc[[-1],[-1]]).bool() and (todays_stochastic < 50).bool():
            TRADE_QUANTITY = sellAmount(TOKEN)
            print(f"Selling {TRADE_QUANTITY} shares of {TRADE_SYMBOL} at ${df.Close[0]}")

            order_succeeded = order(SIDE_SELL, TRADE_QUANTITY, TRADE_SYMBOL)

            if order_succeeded:
                print(f"Sold {TRADE_QUANTITY} of {TRADE_SYMBOL} Successfully")
                inPosition = False

#fully functioning without threading

# def run_websocket(TOKEN):
#     ws = websocket.WebSocketApp(getSocket(TOKEN), on_open = on_open, on_close = on_close, on_message = on_message)
#     print(f"{TOKEN} websocket running")
#     ws.run_forever()
    
# with concurrent.futures.ThreadPoolExecutor() as executor:
#     TOKENS = ['ETH', 'LINK'] #'BTC', 
#     results = executor.map(run_websocket, TOKENS)

ws = websocket.WebSocketApp(getSocket('ETH'), on_open = on_open, on_close = on_close, on_message = on_message)
ws.run_forever()