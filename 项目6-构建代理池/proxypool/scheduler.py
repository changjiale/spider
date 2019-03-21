import time
from multiprocessing import Process
from api import app
from getter import Getter
from check import Check
from db import RedisClient

# 检查周期
TESTER_CYCLE = 20
# 获取周期
GETTER_CYCLE = 300
# API配置
API_HOST = '0.0.0.0'
API_PORT = 5000

# 开关
TESTER_ENABLED = False
GETTER_ENABLED = False
API_ENABLED = True

# 最大批测试量
BATCH_TEST_SIZE = 10

'''
定时任务
'''
class Scheduler():
    def schedule_check(self, cycle=TESTER_CYCLE):
        '''
        定时测试代理
        :param cycle:
        :return:
        '''
        check = Check()
        while True:
            print('测试器开始运行')
            check.run()
            time.sleep(cycle)

    def schedule_getter(self, cycle=GETTER_CYCLE):
        '''
        定时获取代理
        :param cycle:
        :return:
        '''
        getter = Getter()
        while True:
            print('开始抓取代理')
            getter.run()
            time.sleep(cycle)

    def schedule_api(self):
        '''
        开启api
        :return:
        '''
        app.run(API_HOST, API_PORT)

    def run(self):
        print('代理池开始运行')
        if TESTER_ENABLED:
            tester_process = Process(target=self.schedule_check())
            tester_process.start()
        if GETTER_ENABLED:
            getter_process = Process(target=self.schedule_getter())
            getter_process.start()
        if API_ENABLED:
            api_process = Process(target=self.schedule_api())
            api_process.start()

if __name__ == '__main__':
    Scheduler().run()