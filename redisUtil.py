from operator import methodcaller
import time
import threading
import redis
import json
from alpaca_trade_api.stream import Stream
from alpaca_trade_api.common import URL
from redistimeseries.client import Client
import alpaca_trade_api as alpaca


def bar_key(symbol, suffix, timeframe):
    return "data_" + suffix + "_" + timeframe + ":" + symbol


class RedisAccess:

    @staticmethod
    def connection(r=None):
        if (r == None):
            return redis.StrictRedis(
                host='127.0.0.1', port=6379, db=0)
        else:
            return r


class TimeSeriesAccess:
    @staticmethod
    def connection(r=None):
        if (r is None):
            return Client(host='127.0.0.1', port=6379)
        else:
            return r

    @staticmethod
    def connect(r=None):
        if (r is None):
            rds = redis.StrictRedis(
                host='127.0.0.1', port=6379, db=0)
            return redis.TimeSeries(rds, base_key='my_timeseries')
        else:
            return r

    @staticmethod
    def RealTimeSymbols():
        redis = RedisAccess.connection()
        symbols = []
        realTimeSymbols = redis.keys("data_close_0:*")
        for realTimeSymbol in realTimeSymbols:
            symbol = bytes.decode(realTimeSymbol).split(":")[1]
            symbols.append(symbol)
        return symbols

    @staticmethod
    def RealTimeSymbol(symbol):
        return "data_close_0:" + symbol

    @staticmethod
    def RealTimeStockData(symbol, rts: Client = None):
        timeseries: Client = None
        if rts is None:
            timeseries = TimeSeriesAccess.connection()
        else:
            timeseries = rts
        realTimeData = timeseries.range(symbol, 0, '+')
        return realTimeData


class KeyName:
    # step 1: new bar data is sent.  It is appened to the redis pub/sub
    EVENT_BAR2DB = ["RPS_BAR_RTS"]
    # step 2: once it is added to the redis timeseries, it is sent to new bar storage
    EVENT_BAR2CACHE = ["RPS_BAR_CACHE"]
    # step 3: once the data passes the filter, it is sent to the new bar stack
    EVENT_BAR2STACK = ["RPS_ANALYSIS_STACK"]
    # step 4: data is scored, and the result is stored in sorted set, dashboard and score
    EVENT_BAR2STACK_NEW = ["RPS_ANALYSIS_STACK_NEW"]
    EVENT_BAR2SCORE = ["RPS_SAVE_SCORE"]
    EVENT_NEW_CANDIDATES = ["RPS_THREEBARSTACK_NEW"]

    KEY_THREEBARSTACK = "STUDYTHREEBARSTACK"
    KEY_THREEBARSTACK_SUBSCRIBE = "STUDYTHREEBARSTACK_SUBSCRIBE"
    KEY_THREEBARSTACK_UNSUBSCRIBE = "STUDYTHREEBARSTACK_UNSUBSCRIBE"
    KEY_THREEBARSCORE = "STUDYTHREEBARSCORE"

    STUDY_KEY_LEVELS = "STUDY_KEY_LEVELS"

    # Time Series Key for each symbol, data type and timeframe

    @staticmethod
    def KeyBar(symbol, datatype, timeframe):
        return "RTS_BAR_" + datatype.upper() + "_" + timeframe + ":" + symbol.upper()

    # Sorted Set key for Dashboard for quick lookup
    @staticmethod
    def KeyDashboard():
        return "RSS_DAASHBOARD"

    # Hashed key for scores.  Historical data.  24 hours.
    @staticmethod
    def KeyScore(symbol):
        return "RTS_SCORE:" + symbol.upper()
