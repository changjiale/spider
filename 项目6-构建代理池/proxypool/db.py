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

    def decrease(self, proxy):
        '''
        代理值减一，小于最小值删除
        :param proxy: 代理
        :return: 修改后的分数
        '''
        score = self.db.zscore(REDIS_KEY, proxy)
        if score and score > MIN_SCORE:
            print('代理', proxy, '当前分数', score, '减一')
            #将redis_key对应的值+(-1)
            return self.db.zincrby(REDIS_KEY, proxy, -1)
        else:
            print("代理",proxy,'当前分数',score,'移除')
            # 删除
            return self.db.zrem(REDIS_KEY, proxy)

    def exits(self, proxy):
        '''
        判断是否存在
        :param proxy:
        :return:
        '''
        return not self.db.zscore(REDIS_KEY, proxy) == None

    def max(self, proxy):
        '''
        将代理设置为MAX_SCORE
        :param proxy:
        :return:
        '''
        print('代理', proxy, '可用, 设置为',MAX_SCORE)
        return self.db.zadd(REDIS_KEY, MAX_SCORE, proxy)

    def count(self):
        '''
        获取数量
        :return:
        '''
        return self.db.zcard(REDIS_KEY)

    def all(self):
        '''
        获取全部代理
        :return:
        '''
        return self.db.zrangebyscore(REDIS_KEY, MIN_SCORE, MAX_SCORE)

    def batch(self, start, stop):
        '''
        批量获取
        :param start:开始索引
        :param stop:结束索引
        :return:代理列表
        '''
        return self.db.zrevrange(REDIS_KEY, start, stop-1)


class PoolEmptyError(Exception):

    def __init__(self):
        Exception.__init__(self)

    def __str__(self):
        return repr('代理池已经枯竭')

#测试
if __name__ == '__main__':
    conn = RedisClient()
    result = conn.batch(0,100)