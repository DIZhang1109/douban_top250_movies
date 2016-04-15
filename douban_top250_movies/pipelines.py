# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
import sys

reload(sys)
sys.setdefaultencoding('utf-8')


class DoubanTop250MoviesPipeline(object):
    # Define mongoDB properties
    def __init__(self):
        self.mongo_url = 'localhost'
        self.mongo_port = 27017
        self.db_name = 'douban_top250_movies'
        self.connection_name = 'contents'

    # Open mongoDB
    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_url, self.mongo_port)
        self.db = self.client[self.db_name]
        self.con = self.db[self.connection_name]

    # Close mongoDB
    def close_spider(self, spider):
        self.client.close()

    # Process the items to insert three items into mongoDB
    def process_item(self, item, spider):
        for i in range(len(item['movie_name'])):
            self.con.insert_one(
                {
                    'movie_name': str(item['movie_name'][i].replace('', '')),
                    'movie_score': item['movie_score'][i]
                }
            )
