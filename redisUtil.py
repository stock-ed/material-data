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
    def RealTimeStockTrade(symbol, rts: Client = None):
        timeseries: Client = None
        if rts is None:
            timeseries = TimeSeriesAccess.connection()
        else:
            timeseries = rts
        realTimeData = timeseries.range(symbol, 0, '+')
        return realTimeData

    @staticmethod
    def firstTimestamp(now: int, ts1: int, mins: int):
        if (ts1 + mins) < now:
            return TimeSeriesAccess.firstTimestamp(now, ts1 + mins, mins)
        else:
            return ts1

    @staticmethod
    def composeStockData(stamps: [], data):
        result = []
        for ts in stamps:
            isFound = False
            value = -1
            for item in data:
                if ts >= item[0]:
                    oneitem = (ts, item[1])
                    result.append(oneitem)
                    value = item[1]
                    isFound = True
                    break
            if not isFound and value >= 0:
                oneitem = (ts, value)
                result.append(oneitem)
        return result

    @staticmethod
    def _bar_adjustBar(data, timeframe='1MIN', ts=time.time()):
        # get timestamp
        switcher = {
            "1MIN": 60,
            "2MIN": 120,
            "5MIN": 300,
        }
        mins = switcher.get(timeframe, 60)
        tstamps = []
        ts1 = TimeSeriesAccess.firstTimestamp(ts, data[0][0], mins)
        tstamps.append(ts1 - mins * 4)
        tstamps.append(ts1 - mins * 3)
        tstamps.append(ts1 - mins * 2)
        tstamps.append(ts1 - mins)
        tstamps.append(ts1)
        result = TimeSeriesAccess.composeStockData(tstamps, data)
        return result

    @staticmethod
    def RealTimeStockBar(symbol: str, suffix: str, period: str, rts: Client = None):
        timeseries: Client = None
        if rts is None:
            timeseries = TimeSeriesAccess.connection()
        else:
            timeseries = rts
        key = bar_key(symbol, suffix, period)
        realTimeData = timeseries.range(key, 0, 999999999999999)
        return TimeSeriesAccess.to_datetime(realTimeData)

    @staticmethod
    def timestamp2datetime(ts):
        # ts = timestamp / 1000
        return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(ts))

    @staticmethod
    def to_datetime(bars):
        data = []
        for bar in bars:
            data.append((TimeSeriesAccess.timestamp2datetime(bar[0]), bar[1]))
        return data


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


if __name__ == '__main__':
    data = [(1000, 5.2), (940, 5.1), (820, 5.0)]
    result = TimeSeriesAccess._bar_adjustBar(data, ts=1001)
    print(result)
