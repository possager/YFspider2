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




class middleway_visiontimes(RedisCrawlSpider):
    name = 'middleway-visiontimes'
    start_urls=['http://www.visiontimes.com/']
    # redis_key='middleway:urls'
    headers={
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36',
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    }


    rules =  (
        Rule(LinkExtractor(allow='http\:\/\/www\.visiontimes\.com\/\d{4}\/\d{2}\/\d{2}\/.*\.html',),callback='parse_content',follow=True),
        Rule(LinkExtractor(allow='http\:\/\/www\.visiontimes\.com.*'),follow=True)
    )



    def parse_content(self,response):

        def deal_publish_time(publish_time_raw):
            if type(publish_time_raw)==type([]):
                publish_time_str=publish_time_raw[0]
            else:
                publish_time_str=publish_time_raw

            publish_time_list=publish_time_str.split('/')
            year=publish_time_list[1]
            mounth=publish_time_list[2]
            day=publish_time_list[3]

            publish_time=year+'-'+mounth+'-'+day+' 00:00:00'
            return publish_time




        loader1=itemloader_ll(item=YfspiderspeakItem(),response=response)
        loader1.add_value('url',response.url)
        loader1.add_value('spider_time',time.time())
        loader1.add_value('id',response.url.split('/')[-1].split('.')[0])
        loader1.add_xpath('title','//div[@id="main-content"]//h1[@class="article-title"]/text()',lambda x:x[0].strip())
        loader1.add_value('publish_time',response.url,deal_publish_time)
        loader1.add_xpath('content','//div[@id="main-content"]//div[@class="article-content"]/p/text()',lambda x:[prograph.strip() for prograph in x])
        loader1.add_xpath('img_urls','//div[@id="main-content"]//div[@class="article-content"]//img/@src')
        loader1.add_xpath('publish_user','//div[@id="main-content"]//div[@class="article-author"]//div[@class="author-name"]/a/text()'),lambda x:x[0].strip() if x else None

        item1=loader1.load_item()
        return item1