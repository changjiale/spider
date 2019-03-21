from scheduler import Scheduler
import sys
import io

#sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


def main():
    try:
        print("定时任务")
        s = Scheduler()
        s.run()
    except:
        print('重新开始')
        main()


if __name__ == '__main__':
    main()