import redis
from random import choice
import re

#定义常量
MAX_SCORE = 100
MIN_SCORE = 0
INITIAL_SCORE = 10
REDIS_HOST = "localhost"
REDIS_PORT = 6379
REDIS_PASSWORD = None
REDIS_KEY = "proxies"

'''
redis存储模块
'''
class RedisClient(object):

    #decode_responses=True:这样写存的数据是字符串格式
    def __init__(self, host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD):
        '''

        :param host: redis地址
        :param port: 端口
        :param password: 密码
        '''
        self.db = redis.StrictRedis(host=host, port=port, password=password, decode_responses=True)

    def add(self, proxy, score=INITIAL_SCORE):
        '''
        添加代理，默认为10分
        :param proxy: 代理
        :param score: 分数
        :return: 结果
        '''
        if not re.match("\d+\.\d+\.\d+\.\d+\:\d+",proxy):
            print("代理不符合规范,",proxy,"丢弃")
            return
        if not self.db.zscore(REDIS_KEY, proxy):
            return self.db.zadd(REDIS_KEY,score,proxy)

    def random(self):
        '''
        随机获取代理，尝试获取分数最高的代理，如果不存在，按排名获取，否则报错
        :return:
        '''
        #根据分数
        result = self.db.zrangebyscore(REDIS_KEY, MAX_SCORE, MAX_SCORE)
        if len(result):
            return choice(result)
        else:
            #根据分数从大到小排序
            result = self.db.zrevrange(REDIS_KEY,0,100)
            if len(result):
                return choice(result)
            else:
                raise PoolEmptyError


class PoolEmptyError(Exception):

    def __init__(self):
        Exception.__init__(self)

    def __str__(self):
        return repr('代理池已经枯竭')