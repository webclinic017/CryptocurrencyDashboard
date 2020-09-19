from binance.client import Client
import csv, config

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
# candlesticks = client.get_historical_klines("BTCUSDT", Client.KLINE_INTERVAL_1DAY, "10 days ago UTC")
#LINK DOT

for candlestick in candlesticks:
    candlestick[0] = candlestick[0] /1000
    candlestick_writer.writerow(candlestick)

csvfile.close()