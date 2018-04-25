#_*_coding:utf-8_*_
import scrapy
# from scrapy.spider import Spider
from scrapy.spider import CrawlSpider
from scrapy_redis.spiders import RedisCrawlSpider
from YFspider2.items import YfspiderspeakItem
from scrapy.spiders import Rule
from scrapy.linkextractor import LinkExtractor
from YFspider2.othermodule.itemloader_ll import itemloader_ll
from scrapy.loader.processors import Join,MapCompose,Compose,TakeFirst
import time
import hashlib


class tibetanyouthcongress(RedisCrawlSpider):
    name = 'rtycnynj'
    # redis_key = 'rtycnynj:url'
    # start_urls = ['https://www.tibetanyouthcongress.org/']

    rules = {
        # Rule(LinkExtractor(allow=r'(https:\/\/www\.tibetanyouthcongress\.org\/\d{1,4}\/\d{1,2}\/\S*?\/)',),callback="parse_content",follow=True),
        # Rule(LinkExtractor(allow=r'()',restrict_xpaths='//div[@class="container"]/div[@class="nine columns"]',),follow=True),
    }

    def parse_content(self,response):
        pass