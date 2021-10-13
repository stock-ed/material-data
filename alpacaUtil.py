from alpaca_trade_api.rest import REST, TimeFrame
from datetime import datetime, timedelta
from enum import Enum
import alpaca_trade_api as tradeapi
import requests

custom_header = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'}
response = requests.get('https://www.dev2qa.com', headers=custom_header)


class TimePeriod(Enum):
    Min1 = "1Min"
    Min5 = "5Min"
    Min10 = "10Min"
    Min15 = "15Min"
    Min30 = "30Min"
    Hour = "Hour"
    Hour4 = "4Hour"
    Day = "Day"
    Week = "Week"


class AlpacaAccess:
    ALPACA_API_KEY = 'AKAV2Z5H0NJNXYF7K24D'
    ALPACA_SECRET_KEY = '262cAEeIRrL1KEZYKSTjZA79tj25XWrMtvz0Bezu'
    ALPACA_URL = 'https://data.alpaca.markets/v2/stocks/%s/bars?start=%s&end=%s&timeframe=%s'
    conn: REST = None

    def __init__(self):
        self.custom_header = {
            'APCA-API-KEY-ID': AlpacaAccess.ALPACA_API_KEY,
            'APCA-API-SECRET-KEY': AlpacaAccess.ALPACA_SECRET_KEY
        }

    def timeframe_start(self, timeframe):
        switcher = {
            TimePeriod.Min1.value: datetime.now() - timedelta(days=7),
            TimePeriod.Min5.value: datetime.now() - timedelta(days=7),
            TimePeriod.Min10.value: datetime.now() - timedelta(days=7),
            TimePeriod.Min30.value: datetime.now() - timedelta(days=14),
            TimePeriod.Hour.value: datetime.now() - timedelta(days=28),
            TimePeriod.Day.value: datetime.now() - timedelta(days=360),
            TimePeriod.Week.value: datetime.now() - timedelta(days=1080),
        }
        dt = switcher.get(timeframe, datetime.now())
        date_string = dt.isoformat('T') + 'Z'
        return date_string
        # return "2021-02-08"

    def timeframe_end(self, timeframe):
        dt = datetime.now()
        date_string = dt.isoformat('T') + 'Z'
        return date_string
        # return "2021-02-10"

    def HistoricalPrices(self, symbol, timeframe):
        start = self.timeframe_start(timeframe)
        end = self.timeframe_end(timeframe)
        url = AlpacaAccess.ALPACA_URL % (symbol, start, end, timeframe)
        bars = requests.get(url, headers=self.custom_header)
        return bars
