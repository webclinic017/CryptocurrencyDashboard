import os, sys, argparse
import backtrader as bt
import datetime
from strategies.GoldenCross import GoldenCross
from strategies.RSIStrategy import RSIStrategy
from strategies.BuyHold import BuyHold
from strategies.MACD import MACD
from strategies.WeightedStrategy import WeightedStrategy
from strategies.WeightedStrategy2 import WeightedStrategy2
from strategies.WeightedStrategy3 import WeightedStrategy3
from strategies.WeightedStrategy4 import WeightedStrategy4
from strategies.WeightedStrategy5 import WeightedStrategy5
from strategies.WeightedStrategy6 import WeightedStrategy6
from strategies.WeightedStrategy7 import WeightedStrategy7
from strategies.SimpleStrategy import SimpleStrategy


strategies = {
    "golden_cross": GoldenCross,
    "rsi_strategy": RSIStrategy,
    "buy_hold": BuyHold,
    "macd": MACD,
    "weighted_strategy": WeightedStrategy,
    "weighted_strategy2": WeightedStrategy2,
    "weighted_strategy3": WeightedStrategy3,
    "weighted_strategy4": WeightedStrategy4,
    "weighted_strategy5": WeightedStrategy5,
    "weighted_strategy6": WeightedStrategy6,
    "weighted_strategy7": WeightedStrategy7,
    "simple_strategy": SimpleStrategy,
}

parser = argparse.ArgumentParser()
parser.add_argument("strategy", help="Which strategy to run?", type=str)
args=parser.parse_args()

if not args.strategy in strategies:
    print(f"Please enter a valid strategy: {strategies.keys()}")
    sys.exit()

cerebro = bt.Cerebro()

cerebro.broker.setcash(10000)

fromdate = datetime.datetime.strptime('2018-07-01', '%Y-%m-%d')
todate = datetime.datetime.strptime('2020-09-01', '%Y-%m-%d')

data = bt.feeds.GenericCSVData(dataname='data/all_time_daily_usdt.csv', dtformat=2, compression=15, timeframe=bt.TimeFrame.Minutes)
cerebro.adddata(data)
cerebro.addstrategy(strategies[args.strategy])
cerebro.run()
cerebro.plot()