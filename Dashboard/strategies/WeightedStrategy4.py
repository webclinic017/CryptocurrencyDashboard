import math
import backtrader as bt
import talib

#MACD line is the FastEMA - SlowEMA
#Signal line is the mean of the 9 day MA of the MACD line
#Sell when both stochastic and RSI are oversold
#If markets trend is downwards - we look for overbought
#If markets trend is upwards - we look for oversold
#We can use the stochastic indicator and RSI as conditions to buy or sell - not necessarily a reason to

class WeightedStrategy4(bt.Strategy):
    #Initialise moving average times
    params = (('fast',12), ('slow', 26), ('order_percentage', 0.95), ('ticker', 'DOT'))
    #fast-12, slow-26

    def __init__(self):
        self.fast_moving_average = bt.indicators.SMA(
            self.data.close,
            period=self.params.fast,
            plotname='12 day moving average',
        )
        #Initialise both short term and long term RSI constants
        self.slow_moving_average = bt.indicators.SMA(
            self.data.close,
            period=self.params.slow,
            plotname='26 day moving average'
        )
        self.macd = self.fast_moving_average - self.slow_moving_average
        self.signal_line = bt.indicators.SMA(self.macd)
        self.crossover = bt.indicators.CrossOver(self.macd, self.signal_line)
        self.crossover2 = bt.indicators.CrossOver(self.fast_moving_average, self.slow_moving_average)
        self.stoc = bt.talib.STOCH(self.data.high, self.data.low, self.data.close, fastk_period=14, slowk_period=3)
        self.rsi = bt.talib.RSI(self.data, period=12)
        
    def next(self):
        #We own 0 tokens
        if self.position.size == 0:
            #If MA cross has happened execute a buy order
            if ((self.crossover > 0) or (self.crossover2 > 0)) and ((self.rsi > 55) or (self.stoc > 55)):
                amount_to_invest = (self.params.order_percentage * self.broker.cash)
                self.size = math.floor(amount_to_invest / self.data.close)
                print(f"Buying {self.size} shares of {self.params.ticker} at {self.data.close[0]}")
                self.buy(size=self.size)

        #If we own the token
        if self.position.size > 0:
            #if the MA cross happens sell
            if ((self.crossover < 0) or (self.crossover2 > 0)) and ((self.rsi < 45) or (self.stoc < 45)):
                print(f"Selling {self.size} shares of {self.params.ticker} at {self.data.close[0]}")
                self.close()