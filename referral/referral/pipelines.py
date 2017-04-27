# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
from pymongo import MongoClient
from dbhelper import DBhelper
import mailsender

class ReferralPipeline(object):
    def open_spider(self, spider):
        self.dbh = DBhelper()

    
    def process_item(self, item, spider):
        dbItem = {
            'title' : item['title'],
            'url' : item['url'],
            'hashCode' : item['hashCode']
        }
        self.dbh.insert_one(dbItem)
        return item
    
    def close_spider(self, spider):
        today , old = self.dbh.getLatestItems()
        mailsender.send(today = today, old = old) 
	print "Finished"
