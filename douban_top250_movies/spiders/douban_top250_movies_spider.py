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
        movie_name = sel.xpath('//div[@class="pic"]/a/img/@alt').extract()
        movie_score = sel.xpath('//span[@class="rating_num"]/text()').extract()

        # State a instance of DoubanNewMovieItem and save all items with a loop
        item = DoubanTop250MoviesItem()
        item['movie_name'] = [n.encode('utf-8') for n in movie_name]
        item['movie_score'] = [n for n in movie_score]

        # Print to the console
        print item

        # Yield item and give it to pipelines
        yield item
