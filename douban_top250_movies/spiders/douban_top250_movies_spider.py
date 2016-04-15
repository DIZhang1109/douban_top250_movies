from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import Selector

from douban_top250_movies.items import DoubanTop250MoviesItem


class DoubanTop250MoviesSpider(CrawlSpider):
    # Spider's name
    name = 'douban_top250_movies_spider'

    # Allowed domains to crawl
    allowed_domains = ['movie.douban.com']

    # Spider's URL
    start_urls = ['https://movie.douban.com/top250?start=25&filter=']

    # Followed rules to crawl
    rules = (
        Rule(LinkExtractor(allow=('https://movie\.douban\.com/top250\?start=\d+&filter=',)), callback='parse_item'),
    )

    # Spider's function
    def parse_item(self, response):
        sel = Selector(response)

        # Search the item with xpath and return with a list
        movie_names = sel.xpath('//div[@class="pic"]/a/img/@alt').extract()
        movie_scores = sel.xpath('//span[@class="rating_num"]/text()').extract()

        # State a instance of DoubanNewMovieItem and save all items with a loop
        item = DoubanTop250MoviesItem()
        item['movie_name'] = [movie_name.encode('utf-8') for movie_name in movie_names]
        item['movie_score'] = [movie_score for movie_score in movie_scores]

        # Print to the console
        print item

        # Yield item and give it to pipelines
        yield item
