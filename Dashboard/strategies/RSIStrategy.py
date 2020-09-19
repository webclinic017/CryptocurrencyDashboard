import math
import backtrader as bt
import talib

OVERSOLD_CONITION = 30
OVERBOUGHT_CONDITION = 70

class RSIStrategy(bt.Strategy):
    def __init__(self):
        self.rsi = bt.talib.RSI(self.data, period=14)
    
    def next(self):
        if self.rsi < OVERSOLD_CONITION and not self.position:
            self.buy(size=1)
        if self.rsi > OVERBOUGHT_CONITION and self.position:
            self.close()