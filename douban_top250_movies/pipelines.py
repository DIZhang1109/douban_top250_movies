# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
import sys
import settings

reload(sys)
sys.setdefaultencoding('utf-8')


class DoubanTop250MoviesPipeline(object):
    # Open mongoDB
    def open_spider(self, spider):
        self.client = pymongo.MongoClient(settings.MONGODB_URL, settings.MONGODB_PORT)
        self.db = self.client[settings.MONGODB_DB]
        self.collection_name = self.db[settings.MONGODB_COLLECTION_NAME]
        self.collection_category = self.db[settings.MONGODB_COLLECTION_CATEGORY]
        self.collection_country = self.db[settings.MONGODB_COLLECTION_COUNTRY]

    # Close mongoDB
    def close_spider(self, spider):
        self.client.close()

    # Process the items to insert three items into mongoDB
    def process_item(self, item, spider):
        for i in range(len(item['movie_name'])):
            self.collection_name.insert_one(
                {
                    'movie_name': str(item['movie_name'][i].replace('', '')),
                    'movie_score': item['movie_score'][i]
                }
            )

        for i in item['movie_category']:
            if self.collection_category.find_one({"movie_category": unicode(i)}):
                add_one = self.collection_category.find_one({'movie_category': str(i)})
                count = int(add_one['count'])
                count = count + 1
                add_one['count'] = count
                self.collection_category.save(add_one)
            else:
                self.collection_category.insert_one({'movie_category': i, "count": 1})

        for j in item['movie_country']:
            if self.collection_country.find_one({"movie_country": unicode(j)}):
                add_one = self.collection_country.find_one({'movie_country': str(j)})
                count = int(add_one['count'])
                count = count + 1
                add_one['count'] = count
                self.collection_country.save(add_one)
            else:
                self.collection_country.insert_one({'movie_country': j, "count": 1})
