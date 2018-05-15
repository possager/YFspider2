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




class middleway(RedisCrawlSpider):
    name = 'dwnews'
    start_urls=['http://news.dwnews.com/']
    headers={
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36',
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    }


    rules =  (
        Rule(LinkExtractor(allow=r'http\:\/\/news\.dwnews\.com\/\S*\/\S*\/\d{4}\-\d{2}\-\d{2}\/\d*\.html',),callback='parse_content',follow=True),
        Rule(LinkExtractor(allow=r'http\:\/\/news\.dwnews\.com\/.*',),follow=True)
    )




    def parse_content(self,response):
        print ('in parseMore')

        def deal_publish_time(publish_time_list=[]):
            if publish_time_list:
                publish_time_str=publish_time_list[0]
            else:
                return '2018-02-01 00:00:00'
            return publish_time_str.strip()

        loader1=ItemLoader(item=YfspiderspeakItem(),response=response)
        loader1.add_value('url',response.url)
        loader1.add_value('spider_time',time.time())
        loader1.add_xpath('title','//div[@class="main"]//div[@class="dia-lead"]//h1/text()',lambda x:''.join([y for y in x]))
        loader1.add_xpath('content','//div[@class="main"]//div[@class="dia-lead-one"]/div[@id]//text()',lambda x:[i.strip() for i in x],Join())
        loader1.add_value('id',response.url.strip('/').split('/')[-1].split('.')[0])
        loader1.add_xpath('img_urls','//div[@class="main"]//div[@class="dia-lead-one"]/div[@id]//img/@src   ')
        loader1.add_xpath('publish_time','//div[@class="main"]//div[@class="dia-lead"]//div[@class="sign1"]/div[@class="r"]/text()',deal_publish_time)




        item=loader1.load_item()
        print (item)
        return item

    # def parse_comments(self,response):
    #     pass