from flask import Flask
from flask_cors import CORS
import json
from flask import request, jsonify
import os
from redisUtil import TimeSeriesAccess, KeyName
from alpacaUtil import AlpacaAccess
from redisHash import RedisHash
from operator import itemgetter

app = Flask(__name__)
CORS(app)


def getQueryString(request, name):
    try:
        return request.args.get(name)
    except:
        return None


def getQueryBool(request, name):
    try:
        data = request.args.get(name)
        return True if data.lower() == 'true' else False
    except:
        return False


def _getRealtimeStockPrice(request):
    symbol = getQueryString(request, 'symbol')
    period = getQueryString(request, 'period')
    if getQueryBool(request, 'isStock'):
        symbol = TimeSeriesAccess.RealTimeSymbol(symbol)
    result = TimeSeriesAccess.RealTimeStockData(symbol)
    return json.dumps(result)


def _getStockHistorical(request):
    symbol = getQueryString(request, 'symbol')
    timeframe = getQueryString(request, 'timeframe')
    alpaca = AlpacaAccess()
    result = alpaca.HistoricalPrices(symbol, timeframe)
    return result.text


def api_wrapper(func):
    try:
        data = func()
        return {'status': 200, 'data': data}
    except Exception as e:
        return {'status': 500, 'data': str(e)}


def redisHashWithKey(key):
    hash = RedisHash(key)
    dict = hash.getAll()
    result = []
    for key, value in dict.items():
        data = {'symbol': key.decode('utf-8'), 'data': value.decode('utf-8')}
        result.append(data)
    return result


@app.route("/data/stock-realtime", methods=['GET'])
def getRealtimeStockPrice():
    result = api_wrapper(lambda: _getRealtimeStockPrice(request))
    return result


@app.route("/data/stock-historical", methods=['GET'])
def getStockHistorical():
    result = api_wrapper(lambda: _getStockHistorical(request))
    return result


@ app.route("/study/threebar/score", methods=['GET'])
def getDataScore():
    result = api_wrapper(lambda: redisHashWithKey(KeyName.KEY_THREEBARSCORE))
    return result


@ app.route("/study/threebar/stack", methods=['GET'])
def getDataStack():
    result = api_wrapper(lambda: redisHashWithKey(KeyName.KEY_THREEBARSTACK))
    return result


@ app.route("/study/threebar/score/reset", methods=['GET'])
def resetDataScore():
    result = api_wrapper(lambda: RedisHash(
        KeyName.KEY_THREEBARSCORE).deleteAll())
    return result


@ app.route("/study/threebar/stack/reset", methods=['GET'])
def resetDataStack():
    result = api_wrapper(lambda: RedisHash(
        KeyName.KEY_THREEBARSTACK).deleteAll())
    return result


@ app.route("/live/ping", methods=['GET'])
def live():
    return 'OK'


if __name__ == '__main__':
    hostEnv = os.getenv('HOST_URL', '0.0.0.0')
    portEnv = os.getenv('HOST_PORT', 8105)
    app.run(host=hostEnv, port=portEnv, debug=False, threaded=True)
    # app.run(host='0.0.0.0', port=8102, debug=False, threaded=True)
