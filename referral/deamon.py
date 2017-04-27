from apscheduler.scheduler import Scheduler
from datetime import datetime, timedelta
import os
sched = None


def crawlData():
    os.system("scrapy crawl referral")
    setTimer()


def setTimer():
    now = datetime.now()
    print now.strftime("%Y-%m-%d %H:%M")
    crawlTime = datetime(now.year, now.month, now.day, 7, 0, 0, 0)
    print crawlTime.strftime("%Y-%m-%d %H:%M")
    if crawlTime < now:
        crawlTime = crawlTime + timedelta(days=1)
    job = sched.add_date_job(crawlData, crawlTime)
    if not sched.running:
        sched.start()


if __name__ == '__main__':
    sched = Scheduler()
    sched.daemonic = False
    crawlData()
