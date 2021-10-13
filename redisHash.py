from logging import Formatter
import json
from redisUtil import RedisAccess


class RedisHash:

    def __init__(self, key, r=None, callback=None):
        self.redis = RedisAccess.connection(r)
        self.callback = callback
        self.key = key

    @property
    def get_key(self):
        return self.key

    def _getAll(self, key):
        return self.redis.hgetall(key)

    def getAll(self):
        return self._getAll(self.key)

    def _add(self, key, symbol, jsondata):
        data = json.dumps(jsondata)
        self.redis.hset(key, symbol, data)
        if (self.callback != None):
            self.callback(symbol, jsondata)

    def add(self, symbol, jsondata):
        return self._add(self.key, symbol, jsondata)

    def delete(self, symbol):
        self.redis.hdel(self.key, symbol)

    def _value(self, key, symbol):
        data = self.redis.hget(key, symbol)
        if data == None:
            return None
        return json.loads(data)

    def value(self, symbol):
        return self._value(self.key, symbol)

    def isSymbolExist(self, symbol):
        return self.redis.hexists(self.key, symbol)

    def deleteAll(self):
        self.redis.delete(self.key)  # delete all data
