# douban_top250_movies

[![Build Status](https://travis-ci.org/DIZhang1109/douban_top250_movies.svg?branch=master)](https://travis-ci.org/DIZhang1109/douban_top250_movies) [![Coverage Status](https://coveralls.io/repos/github/DIZhang1109/douban_top250_movies/badge.svg?branch=master)](https://coveralls.io/github/DIZhang1109/douban_top250_movies?branch=master)

Scrapy Web Crawler Framework --- Douban top250 movie pages

# Notes
1.  Mainly solve the issue of crawling multiple pages and writing results into mongoDB (250 results including movie names and scores)
2.  Implement simple data analysis using matplotlib

# How to kick off
1.  Install python 2.7
2.  Install pip
3.  Install scrapy
4.  Install mongodb
5.  Run 'scrapy crawl douban_top250_movies_spider'
6.  Check the database
7.  Run 'python data_analysis.py'
