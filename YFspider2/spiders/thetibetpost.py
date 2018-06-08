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






class thetibetpost(RedisCrawlSpider):
    name = 'thetibetpost'
    start_urls=['http://www.thetibetpost.com/en/']
    headers={
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36',
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    }


    rules =  (
        Rule(LinkExtractor(allow=r'http\:\/\/www\.thetibetpost\.com\/\S*/.*/.*/\d*\-.*',),callback='parse_content',follow=True),
        Rule(LinkExtractor(allow=r'http\:\/\/www\.thetibetpost\.com\/.*',),follow=True)
    )




    def parse_content(self,response):
        print ('in parseMore')


        def deal_publish_time(publish_time_list=[]):
            if publish_time_list:
                publish_time_str=publish_time_list[0]
            else:
                return '2018-02-01 00:00:00'
            if '+' in publish_time_str:
                publish_time_str_split=publish_time_str.split('+')[0]
                return publish_time_str_split.replace('T',' ')
            else:
                return '2018-02-01 00:00:00'


        def deal_publish_user(publish_user_raw):
            if publish_user_raw:
                publish_user_str=''.join(publish_user_raw).strip()
                try:
                    return publish_user_str.split(',')[:-1]
                except :
                    return publish_user_raw
            else:
                return publish_user_raw



        loader1=ItemLoader(item=YfspiderspeakItem(),response=response)
        loader1.add_value('url',response.url)
        loader1.add_value('spider_time',time.time())
        loader1.add_xpath('title','//div[@class="main"]//article//header//h1//text()',lambda x:''.join([y for y in x]).strip())
        loader1.add_xpath('content','//div[@class="main"]//article//div[@class="article-content-main"]//p//text()',lambda x:[i.strip() for i in x],Join())
        loader1.add_value('id',response.url.strip('/').split('/')[-1])
        loader1.add_xpath('img_urls','//div[@class="main"]//article//div[@class="article-content-main"]//section/p//img/@src',lambda x:['http://www.thetibetpost.com'+y for y in x if 'www.thetibetpost.com' not in y])
        loader1.add_xpath('publish_time','//div[@class="main"]//article//dd//time[@datetime]/@datetime',deal_publish_time)
        loader1.add_xpath('publish_user','//div[@class="main"]//article//dd[contains(@class,"createdby")]//span/text()',deal_publish_user)


        item=loader1.load_item()
        print (item)
        return item