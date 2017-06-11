import pymongo
from pymongo import MongoClient
from sets import Set
import datetime
import dateutil.relativedelta
from datetime import timedelta, date


def daterange(start_date, end_date):
    for n in range(int ((end_date - start_date).days)):
        yield end_date - timedelta(n+1)


class DBhelper(object):
    def __init__(self):
        self.client = MongoClient("")
        self.repo = Set()

    def insert_one(self,item):
        db = self.client.indeed
        if not self.exists(item,db.repo):
            if not u'date' in item:
                item['date'] = str(datetime.date.today())
            db.repo.insert_one(item)


    def exists(self,item,collection):
        return collection.find_one({'hashCode' : item['hashCode']}) != None


    def getLatestItems(self):
        db = self.client.indeed
        todayData = db.repo.find({'date': str(datetime.date.today())}).sort([('date',1)]).limit(40)

        old = []
        today = datetime.date.today()
        start_day = today - dateutil.relativedelta.relativedelta(days=20)
        for single_date in daterange(start_day, today):
            jobData = db.repo.find({'date':  str(single_date)  }).sort([('date',1)]).limit(40)
            count = jobData.count()
            if count == 0:
                continue
            jobPack = {'date' : str(single_date), 'jobData': jobData}
            old.append(jobPack)
        return todayData,old




