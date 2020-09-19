import numpy
import talib
from numpy import genfromtxt

close = numpy.random.random(100)
# print(close)

#talib uses numpy arrays, this is becasue they are tuples and are more efficient in terms of time and space complexity

#moving average:
# moving_average =  talib.SMA(close, timeperiod=10)
# print(moving_average)

#RSI
# rsi = talib.RSI(close)
# print(rsi)

#Generate numpy data from csv file
my_data = genfromtxt('2012-2020.csv', delimiter=',')

#find closing prices
close = my_data[:,4]
rsi = talib.RSI(close)
print(rsi[-100:-1])