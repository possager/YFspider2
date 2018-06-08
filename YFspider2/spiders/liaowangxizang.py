#_*_coding:utf-8_*_
# from scrapy.spiders import CrawlSpider,Rule
from scrapy.spiders import Rule
from scrapy_redis.spiders import RedisCrawlSpider
from scrapy.linkextractors import LinkExtractor
from YFspider2.items import YfspiderspeakItem
from scrapy.loader import ItemLoader
from scrapy.loader.processors import Join,TakeFirst,MapCompose

import scrapy
import time
import datetime





class liaowangxizang(RedisCrawlSpider):
    name = 'liaowangxizang'
    start_urls=['https://liaowangxizang.net/']
    headers={
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36',
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    }


    rules =  (
        Rule(LinkExtractor(allow=r'https\:\/\/liaowangxizang\.net\/\d*/\d*/\d*/.*/',),callback='parse_content',follow=True),
        Rule(LinkExtractor(allow=r'https\:\/\/liaowangxizang\.net\/.*',),follow=True)
    )




    def parse_content(self,response):
        print ('in parseMore')


        def deal_publish_time(publish_time_url=[]):
            if publish_time_url:
                try:
                    publish_time_raw=publish_time_url.strip('/').split('/')
                    days=publish_time_raw[-2]
                    mounth=publish_time_raw[-3]
                    year=publish_time_raw[-4]
                    return year+'-'+mounth+'-'+days+' 00:00:00'
                except:
                    return '2018-02-01 00:00:00'
            else:
                return '2018-02-01 00:00:00'




        loader1=ItemLoader(item=YfspiderspeakItem(),response=response)
        loader1.add_value('url',response.url)
        loader1.add_value('spider_time',time.time())
        loader1.add_xpath('title','//main[@class="content"]//h1[@class="entry-title"]/text()',lambda x:''.join([y for y in x]))
        loader1.add_xpath('content','//main[@class="content"]//div[@class="entry-content"]/p/text()',lambda x:[i.strip() for i in x],Join())
        loader1.add_value('id',response.url.strip('/').split('/')[-1])
        loader1.add_xpath('img_urls','//main[@class="content"]//div[@class="entry-content"]/p/img/@src')
        loader1.add_value('publish_time',response.url,deal_publish_time)
        loader1.add_xpath('publish_user','//article//time[@class="published"]/a[@class="fn"]/text()')



        item=loader1.load_item()
        print (item)
        return item