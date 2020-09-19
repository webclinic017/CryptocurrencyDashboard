from django.shortcuts import render, redirect
from .config import API_KEY, API_SECRET
import csv
from binance.client import Client
from binance.enums import *
from django.core import serializers
from django.urls import reverse
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
import pandas as pd
import datetime

client = Client(API_KEY, API_SECRET)

info = client.get_account()
exchange_info = client.get_exchange_info()
balances = (info['balances'])
symbols = exchange_info['symbols']
total_balance = 0
display_balances = {}

positive_balances = []
for balance in balances:
    if float(balance['free']) > 0:
        positive_balances.append(balance)

for balance in positive_balances:
    balance_symbol = balance['asset'].lower()
    if balance_symbol == 'usdt':
        rate = 1
    else: 
        # df = pd.read_csv(f'Dashboard/data/all_time_daily_{balance_symbol}.csv', parse_dates=True)
        # rate = df.Close.iloc[-1]
        right_now = client.get_historical_klines(f"{balance_symbol.upper()}USDT", Client.KLINE_INTERVAL_1HOUR , "1 day ago UTC")
        rate = right_now[-1][4]
    balance_value = float(balance['free']) * float(rate)
    display_balances[f'{balance_symbol}'] = balance_value
    total_balance += balance_value

#If most recent date in database doesn't equal today:
todays_df = pd.read_csv('Dashboard/data/portfolio_balance.csv', parse_dates=True)
recent_date = todays_df.Date.iloc[-1]
todays_date = datetime.datetime.today().strftime('%Y-%m-%d')
todays_data = (todays_date, round(total_balance))
if recent_date == todays_date:
    print('Portfolio value up to date!')
else:
    f = open("Dashboard/data/portfolio_balance.csv", 'a', newline='')
    writer = csv.writer(f)
    writer.writerow(todays_data)
    f.close()
    print("Today's balance added to CSV!")

# Create your views here.
def index(request):
    return render(request, 'Dashboard/index.html', {
        'values': display_balances.values(),
        'balances': positive_balances, 
        'symbols': symbols,
        'total_balance': round(total_balance, 2),
        })

def buy(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)
    try:
        order = client.create_oco_order(
            symbol=request.form['symbol'],
            side=SIDE_BUY,
            type=ORDER_TYPE_MARKET,
            quantity=request.form['quantity']
        )
    except Exception as e:
        return render(request, 'Dashboard/index.html', {
            'message': e
        })
    
    return redirect('/', status=201)

def sell(request):
    return 'sell'

def settings(request):
    return 'settings'

interval = "Monthly"
timeframe = ""
chosen_symbol = "BTCUSDT"

def update(request):
    global interval
    global timeframe
    global chosen_symbol
    
    intervals = {
        "Monthly": {
            "interval": Client.KLINE_INTERVAL_1MONTH,
            "timeframe": "3 years ago UTC"
        },
        "Weekly": {
            "interval": Client.KLINE_INTERVAL_1WEEK,
            "timeframe": "3 year ago UTC"
        },
        "Daily": {
            "interval": Client.KLINE_INTERVAL_1DAY,
            "timeframe": "1 year ago UTC"
        },
        "Hourly": {
            "interval": Client.KLINE_INTERVAL_1HOUR,
            "timeframe": "1 month ago UTC"
        },
        "Per Minute": {
            "interval": Client.KLINE_INTERVAL_1MINUTE,
            "timeframe": "1 day ago UTC"
        }
    }

    if request.method == "POST":
        #Check if post method if for currency or timeframe
        #check for timeframe post data
        try:
            chosen_interval = request.POST["time-period"]
            interval = intervals[chosen_interval]["interval"]
            timeframe = intervals[chosen_interval]["timeframe"]
            chosen_symbol = request.POST["currency"]
        except:
            return render(request, 'Dashboard/index.html', {
        'message': "Please enter both a Time Period and Cryptocurrency",
        'balances': positive_balances, 
        'symbols': symbols,
        'total_balance': total_balance,
    })
    else:
        if chosen_symbol== "":
            print("Initialising Currency")
            chosen_symbol = "BTCUSDT"
        #If not a post method - either load whatever is in /update, or load default
        if (interval == "") and (timeframe == ""):
            interval = Client.KLINE_INTERVAL_1WEEK 
            timeframe = "1 Jan, 2017"
    candlesticks = client.get_historical_klines(f"{chosen_symbol}", interval, timeframe)
    processed_candlesticks = []
    for data in candlesticks:
        candlestick = {
            'time': data[0] / 1000,
            'open': data[1],
            'high': data[2],
            'low': data[3],
            'close': data[4],
        }
        processed_candlesticks.append(candlestick)
    update.processed_candlesticks = processed_candlesticks
    # return JsonResponse(processed_candlesticks, safe=False)
    return render(request, 'Dashboard/index.html', {
        'chosen_interval': chosen_interval,
        'chosen_symbol': chosen_symbol,
        'balances': positive_balances, 
        'symbols': symbols,
        'total_balance': total_balance,
    })

def history(response):
    """New history route - copy of the JSON data, to be passed into graph"""
    #If we have changed settings then update the /update route
    try:
        return JsonResponse(update.processed_candlesticks, safe=False)
    #Else return default - BTCUSDT - Monthly
    except AttributeError: 
        candlesticks = client.get_historical_klines("BTCUSDT", Client.KLINE_INTERVAL_1WEEK , "1 Jan, 2017")
        processed_candlesticks = []
        for data in candlesticks:
            candlestick = {
                'time': data[0] / 1000,
                'open': data[1],
                'high': data[2],
                'low': data[3],
                'close': data[4],
            }
            processed_candlesticks.append(candlestick)
        return JsonResponse(processed_candlesticks, safe=False)

def balance(request):
    processed_balance = []
    with open('Dashboard/data/portfolio_balance.csv') as f:
        rows = csv.reader(f)
        counter = 0
        for row in rows:
            if counter == 0:
                counter += 1
                pass
            else:
                balance_data = {
                    'time': row[0],
                    'value': row[1]
                }
                processed_balance.append(balance_data)
            

    return JsonResponse(processed_balance, safe=False)