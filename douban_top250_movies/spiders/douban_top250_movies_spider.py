import jieba
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
        movie_information = sel.xpath('//div[@class="bd"]/p/text()[preceding-sibling::br]').extract()

        # Remove '' contents
        movie_information = filter(None, movie_information)

        # Create a list to save the category
        movie_category = []
        movie_country = []

        # Loop in movie_information to get movie category
        for i in movie_information:
            # Split with '/'
            i = i.split('/')
            # Choose the last part of the split result
            i = i[len(i) - 1]
            # Remove whitespace characters in the beginning and the end
            i = i.strip()
            # Remove any space between categories
            i = i.replace(' ', '')
            # Return unicode string
            word = unicode(i)

            if word != ' ' and len(word) > 0:
                # Cut the word using jieba
                words = jieba.cut(word, cut_all=False)
                for n in words:
                    movie_category.append(n)

        # Loop in movie_information to get movie country
        for j in movie_information:
            # Split with '/'
            j = j.split('/')
            # Choose the last two part of the split result
            j = j[len(j) - 2]
            # Remove whitespace characters in the beginning and the end
            j = j.strip()
            # Remove any space between categories
            j = j.replace(' ', '')
            # Return unicode string
            word = unicode(j)

            if word != ' ' and len(word) > 0:
                # Cut the word using jieba
                words = jieba.cut(word, cut_all=False)
                for n in words:
                    movie_country.append(n)

        # State a instance of DoubanNewMovieItem and save all items with a loop
        item = DoubanTop250MoviesItem()
        item['movie_name'] = [movie_name.encode('utf-8') for movie_name in movie_names]
        item['movie_score'] = [movie_score for movie_score in movie_scores]
        item['movie_category'] = movie_category
        item['movie_country'] = movie_country

        # Yield item and give it to pipelines
        yield item
