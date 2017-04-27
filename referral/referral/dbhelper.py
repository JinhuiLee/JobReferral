import pymongo
from pymongo import MongoClient
from sets import Set
import datetime
class DBhelper(object):
    def __init__(self):
        self.client = MongoClient("")
        self.repo = Set()

    def insert_one(self,item):
        db = self.client.indeed
        if not self.exists(item,db.repo):
            item['date'] = str(datetime.date.today())
            db.repo.insert_one(item)


    def exists(self,item,collection):
        return collection.find_one({'hashCode' : item['hashCode']}) != None


    def getLatestItems(self):
        db = self.client.indeed
        today = db.repo.find({'date': str(datetime.date.today())}).sort([('date',1)]).limit(40)
        old = db.repo.find({'date': {'$ne' : str(datetime.date.today()) } }).sort([('date',1)]).limit(40)
        return today,old

