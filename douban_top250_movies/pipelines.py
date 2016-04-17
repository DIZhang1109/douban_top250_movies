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
        self.name = 'name'
        self.category = 'category'
        self.country = 'country'

    # Open mongoDB
    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_url, self.mongo_port)
        self.db = self.client[self.db_name]
        self.con_name = self.db[self.name]
        self.con_category = self.db[self.category]
        self.con_country = self.db[self.country]

    # Close mongoDB
    def close_spider(self, spider):
        self.client.close()

    # Process the items to insert three items into mongoDB
    def process_item(self, item, spider):
        for i in range(len(item['movie_name'])):
            self.con_name.insert_one(
                {
                    'movie_name': str(item['movie_name'][i].replace('', '')),
                    'movie_score': item['movie_score'][i]
                }
            )

        for i in item['movie_category']:
            if self.con_category.find_one({"movie_category": unicode(i)}):
                add_one = self.con_category.find_one({'movie_category': str(i)})
                count = int(add_one['count'])
                count = count + 1
                add_one['count'] = count
                self.con_category.save(add_one)
            else:
                self.con_category.insert_one({'movie_category': i, "count": 1})

        for j in item['movie_country']:
            if self.con_country.find_one({"movie_country": unicode(j)}):
                add_one = self.con_country.find_one({'movie_country': str(j)})
                count = int(add_one['count'])
                count = count + 1
                add_one['count'] = count
                self.con_country.save(add_one)
            else:
                self.con_country.insert_one({'movie_country': j, "count": 1})
