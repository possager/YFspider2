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




class boxunE(RedisCrawlSpider):
    name = 'boxunE'
    start_urls=['https://boxun.com/']
    headers={
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36',
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    }


    rules =  (
        Rule(LinkExtractor(allow=r'http\:\/\/en\.boxun\.com\/\d*\/\d*\/\d*\/.*\/',),callback='parse_content',follow=True),
        Rule(LinkExtractor(allow=r'http\:\/\/en\.boxun\.com\/.*',),follow=True)
    )




    def parse_content(self,response):
        print ('in parseMore')


        def deal_publish_time(publish_time_list=[]):
            try:
                year=publish_time_list[0]
                mounth=publish_time_list[1]
                days=publish_time_list[2]

                return str(year)+'-'+str(mounth)+'-'+str(days)+' 00:00:00'

            except Exception as e:
                return '2018-02-01 00:00:00'



        loader1=ItemLoader(item=YfspiderspeakItem(),response=response)
        loader1.add_value('url',response.url)
        loader1.add_value('spider_time',time.time())
        loader1.add_xpath('title','//div[@id="container"]//div[@id="main"]//h1[@class="entry_title"]//text()',lambda x:''.join([y for y in x]).strip())
        loader1.add_xpath('content','//div[@id="container"]//div[@id="main"]//p/text()',lambda x:[i.strip() for i in x],Join())
        loader1.add_value('id',response.url.strip('/').split('/')[-1].split('.')[0])
        loader1.add_xpath('img_urls','//div[@id="container"]//div[@id="main"]//p//img/@src')
        loader1.add_xpath('video_urls','//div[@id="container"]//div[@id="main"]//p//iframe/@src')
        loader1.add_value('publish_time',response.xpath('//div[@id="container"]//div[@id="main"]//div[@class="singlepostmeta"]//text()').re('(\d{4})\/(\d{2})\/(\d{2})'),deal_publish_time)
        # loader1.add_xpath('read_count','//div[@align="center"]//td[@align="right"]//font[@color="red"]/text()')
        loader1.add_xpath('publish_user','//div[@id="container"]//div[@id="main"]//a[@rel="author"]//text()',lambda x:''.join([y for y in x]))



        item=loader1.load_item()
        print (item)
        return item