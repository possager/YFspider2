#_*_coding:utf-8_*_
# from scrapy.spiders import CrawlSpider,Rule
from scrapy.spiders import Rule
from scrapy_redis.spiders import RedisCrawlSpider
from scrapy.linkextractors import LinkExtractor
from YFspider2.items import YfspiderspeakItem
# from scrapy.loader import
from YFspider2.othermodule.itemloader_ll import itemloader_ll
from scrapy.loader import ItemLoader
from scrapy.loader.processors import Join,TakeFirst,MapCompose

import scrapy
import time
import datetime




class dalailamaworld(RedisCrawlSpider):
    name = 'dalailamaworld'
    start_urls=['http://www.dalailamaworld.com']
    headers={
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36',
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    }


    rules =  (
        Rule(LinkExtractor(allow=r'http\:\/\/www\.dalailamaworld\.com\/topic\.php\?t\=\d*',),callback='parse_content',follow=True),
        Rule(LinkExtractor(allow=r'http\:\/\/www\.dalailamaworld\.com',),follow=True)
    )




    def parse_content(self,response):
        print ('in parseMore')


        loader1=ItemLoader(item=YfspiderspeakItem(),response=response)
        loader1.add_value('url',response.url)
        loader1.add_value('spider_time',time.time())
        loader1.add_xpath('title','//div[@class="page"]//div[@class="subject_bg1 nav"]//text()',lambda x:''.join([y for y in x]))
        loader1.add_xpath('content','//div[@class="page"]//div[@class="topic_body"]//text()',lambda x:[i.strip() for i in x],Join())
        loader1.add_value('id',response.url.split('t=')[-1].split('&')[0])
        loader1.add_xpath('img_urls','//div[@class="page"]//div[@class="topic_body"]//img/@src')
        loader1.add_value('publish_time','2018-02-01 00:00:00')
        loader1.add_value('publish_user','dalailamaworld')
        loader1.add_xpath('video_urls','//div[@class="page"]//div[@class="topic_body"]//iframe/@src')



        item=loader1.load_item()
        print (item)
        return item