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






class middleway(RedisCrawlSpider):
    name = 'cn_rfi_fr'
    start_urls=['http://cn.rfi.fr/']
    headers={
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36',
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    }


    rules =  (
        Rule(LinkExtractor(allow=r'http\:\/\/cn\.rfi\.fr\/.*\/\d{8}\-.*',),callback='parse_content',follow=True),
        Rule(LinkExtractor(allow=r'http\:\/\/cn\.rfi\.fr\/.*',),follow=True)
    )




    def parse_content(self,response):
        print ('in parseMore')


        def deal_publish_time(publish_time_list=[]):
            if publish_time_list:
                publish_time_str=publish_time_list[0]
                publish_time_str=publish_time_str[0] if type(publish_time_str) is type(()) else publish_time_str
            else:
                return '2018-02-01 00:00:00'
            if publish_time_str:
                return publish_time_str.replace('T',' ')
            else:
                return '2018-02-01 00:00:00'



        loader1=ItemLoader(item=YfspiderspeakItem(),response=response)
        loader1.add_value('url',response.url)
        loader1.add_value('spider_time',time.time())
        loader1.add_xpath('title','//div[@class="page-container"]//header/h1/text()',lambda x:''.join([y for y in x]))
        loader1.add_xpath('content','//div[@class="page-container"]//div[@itemprop="articleBody"]//text()',lambda x:[i.strip() for i in x],Join())
        loader1.add_value('id',response.url.strip('/').split('/')[-1])
        loader1.add_xpath('img_urls','//div[@class="page-container"]//div[@itemprop="articleBody"]//img/@src')
        loader1.add_value('publish_time',response.xpath('//head/script[@type="application/ld+json"]//text()').re('\"dateCreated\"\:\"(\d{4}\-\d{2}\-\d{2}T\d{2}\:\d{2}\:\d{2})Z"'),deal_publish_time)
        loader1.add_xpath('publish_user','//article//time[@class="published"]/a[@class="fn"]/text()')
        loader1.add_xpath('video_urls','//div[@class="page-container"]//div[@itemprop="articleBody"]//iframe/@src')



        item=loader1.load_item()
        print (item)
        return item