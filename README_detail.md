# Data Model for Stock Prices and Technical Indicators (using RedisTimeSeries)

This repository demonstrate a sample code for using RedisTimeSeries to store, aggregate/query stock prices, technical indicators and time-series data sets used by investors. These sets of scripts create various timeseries for prices and indicators. It shows how to create aggregations on top of the raw time series, and demonstrate how easily bulk time series can be ingested and queried using various RedisTimeSeries commands.

The blog that discusses this code in detail and walks through the Redis datamodel and the various Redis TimeSeries commands can be found in the references section below.

## Pre-requisite

There are multiple services that offer stock prices and technical indicator data. The code presented here uses data from https://iexcloud.io/
Get a trial account in iexcloud.

### Clone this Repository

```
git clone https://github.com/redis-developer/redis-datasets
cd redis-datasets/redistimeseries/StockPrice
```

### Install Python3

Ensure that python3 and pip3 is installed in your system.

### Install Prerequisite software

Using pip3 to install redistimeseries, iexfinance & pandas software.

```
pip3 install -r requirements.txt
```

Once you have the Redis TimeSeries container up and running you can connect to the server (make sure you have the right IP address or hostname) using Python script:

## TS.QUERYINDEX - working command

ts.queryindex INDICATOR=max TIMEFRAME=1MIN

## REDIS-TIMESERIES local version

$ redis-server --loadmodule /home/young/Desktop/code/RedisTimeSeries/bin/redistimeseries.so

## Running GRAFANA in a DOCKER Container

sudo systemctl start grafana-server
sudo systemctl status grafana-server
http://localhost:3000
admin
Admin$11

## Scanning the Keys

```
127.0.0.1:6379> scan 0
1) "15"
2)  1) "INTRADAYPRICES15MINSTDP:GS"
    2) "DAILYRSI:CAT"
    3) "DAILYRSI15MINMAX:GS"
    4) "DAILYRSI15MINMIN:GS"
    5) "INTRADAYPRICES15MINRNG:GS"
    6) "INTRADAYPRICES15MINMIN:GS"
    7) "DAILYRSI15MINLAST:GS"
    8) "INTRADAYPRICES:GS"
    9) "DAILYRSI:GS"
   10) "INTRADAYPRICES15MINMAX:GS"
   11) "DAILYRSI15MINFIRST:GS"
   12) "DAILYRSI15MINRNG:GS"
127.0.0.1:6379> type INTRADAYPRICES15MINSTDP:GS
TSDB-TYPE
127.0.0.1:6379
```

## References

1.  study score
2.  candle stick pattern
3.  price-action
4.  multiframe analysis
5.  fibonacci
    https://www.youtube.com/watch?v=xU9j_MkRYfg
    Calculate and plot fibonacci retracement levels for an upward trending using python
6.  divergence
    https://raposa.trade/trade-rsi-divergence-python/
    RSI Divegence in Python
7.  breakout
8.  trend - with
9.  fresh trend
10. key levels
11. vwap
12. ema50
13. news
14. total
15. volume
16. volitility
17. standard deviation

curl --header 'Accept: text/event-stream' https://cloud-sse.iexapis.com/stable/stocksUS\?token\=pk_4c4cea17cf834cafadd2a57e5bd7f2cc
curl --header 'Accept: text/event-stream' https://cloud-sse.iexapis.com/stable/stocksUS?token=pk_4c4cea17cf834cafadd2a57e5bd7f2cc

[
(1603704600, 1.75999999999999),
(1603705500, 0.775000000000006),
(1603706400, 0.730000000000018),
(1603707300, 0.449999999999989),
(1603708200, 0.370000000000005),
(1603709100, 1.01000000000002),
(1603710000, 0.490000000000009),
(1603710900, 0.89500000000001),
(1603711800, 0.629999999999995),
(1603712700, 0.490000000000009),
(1603713600, 0.27000000000001)
]

# TIMESERIES RANGE

ts.range data_close_1MIN:FANG 0 -1
flushall
keys \*
