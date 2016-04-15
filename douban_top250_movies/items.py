# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DoubanTop250MoviesItem(scrapy.Item):
    # Two fields that I want to save to the database
    movie_name = scrapy.Field()
    movie_score = scrapy.Field()
