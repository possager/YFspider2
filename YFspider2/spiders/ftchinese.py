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



class tfchinese(CrawlSpider):
    name = 'tfchinese'
    # start_urls=['http://www.sherig.org/tb/page/{}/'.format(str(i)) for i in range(1,10)]
    start_urls=['http://www.tfchinese.org/tb/']

    rules = (
        # Extract links matching 'category.php' (but not matching 'subsection.php')
        # and follow links from them (since no callback means follow=True by default).
        # Rule(LinkExtractor(allow=r'http\:\/\/www\.sherig\.org\/tb\/\d{4}\/\d{1,2}\/.*?\/$',),callback='parse_content',follow=True),
        #http\:\/\/www\.sherig\.org\/tb\/\d{4}\/\d{1,2}\/[^\\\/\']*?\/\B
        Rule(LinkExtractor(allow=r'http\:\/\/www\.tfchinese\.org\/tb\/\d{4}\/\d{1,2}\/[^\\\/\']*?\/\B', ), callback='parse_content',
             follow=True),

        # Extract links matching 'item.php' and parse them with the spider's method parse_item
        Rule(LinkExtractor(allow='http://www.tfchinese.org/tb/page/\d{1,5}/'), follow=True),
    )

    def parse_content(self, response):
        print response.url
