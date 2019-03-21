from db import RedisClient
from crawler import Crawler
import sys

#代理池最大代理数量
POOL_UPPER_THRESHOLD = 50000
'''
调用crawler代理获取模块，自动匹配方法，动态获取代理
'''
class Getter():
    def __init__(self):
        self.redis = RedisClient()
        self.crawler = Crawler()

    def is_over_threshold(self):
        """
        判断是否达到了代理池限制
        """
        if self.redis.count() >= POOL_UPPER_THRESHOLD:
            return True
        else:
            return False

    def run(self):
        '''
        运行
        :return:
        '''
        print('获取器开始执行')
        if not self.is_over_threshold():
            print(self.crawler.__CrawlFuncCount__)
            for callback_label in range(self.crawler.__CrawlFuncCount__):
                callback = self.crawler.__CrawlFunc__[callback_label]
                # 获取代理
                proxies = self.crawler.get_proxies(callback)
                #强制刷新缓冲区
                sys.stdout.flush()
                print('存储代理')
                for proxy in proxies:
                    self.redis.add(proxy)