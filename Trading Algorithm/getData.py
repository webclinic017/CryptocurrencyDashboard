from binance.client import Client
import csv, config
import datetime

client = Client(config.API_KEY, config.API_SECRET)

# prices = client.get_all_tickers()
# for price in prices:
#     print(price)

symbol = "LINKUSDT"

candles = client.get_klines(symbol=symbol, interval = Client.KLINE_INTERVAL_1DAY)

csvfile = open('all_time_daily_link.csv', 'w', newline='')
candlestick_writer = csv.writer(csvfile, delimiter = ',')

# for candlestick in candles:
#     candlestick_writer.writerow(candlestick)

candlesticks = client.get_historical_klines(symbol, Client.KLINE_INTERVAL_1DAY, "1 Jan, 2017")
# candlesticks = client.get_historical_klines(symbol, Client.KLINE_INTERVAL_1MINUTE, "1 day ago UTC")
# candlesticks = client.get_historical_klines("BTCUSDT", Client.KLINE_INTERVAL_1DAY, "10 days ago UTC")
#LINK DOT
csvfile.write('Date,Open,High,Low,Close,Volume,OpenInterest\n')
for candlestick in candlesticks:
    candlestick[0] = candlestick[0] /1000
    t = datetime.datetime.fromtimestamp(candlestick[0])
    day = t.strftime('%Y-%m-%d')
    candlestick[0] = day
    candlestick[6] = 0.0
    candlestick_writer.writerow(candlestick[:7])

csvfile.close()