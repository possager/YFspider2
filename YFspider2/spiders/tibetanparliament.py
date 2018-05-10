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


def deal_links_to_fallow(link_raw):
    links=link_raw.replace('http://','')
    linksplited= links.strip('/').split('/')
    if len(linksplited)==2:
        print '跟进链接:',link_raw
        return link_raw



class middleway(RedisCrawlSpider):
    name = 'tibetanparliament'
    start_urls=['http://tibetanparliament.org/']
    headers={
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36',
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    }


    rules =  (
        Rule(LinkExtractor(allow=r'http:\/\/tibetanparliament\.org\/.*?\/$',process_value=deal_links_to_fallow),callback='parse_content',follow=True),
        Rule(LinkExtractor(allow=r'http:\/\/tibetanparliament\.org\/.*?',),follow=True)
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



        loader1=ItemLoader(item=YfspiderspeakItem(),response=response)
        loader1.add_value('url',response.url)
        loader1.add_value('spider_time',time.time())
        loader1.add_xpath('title','//article//h2[@class="entry-title"]/text()',lambda x:''.join([y for y in x]))
        loader1.add_xpath('content','//article//div[@class="entry-content"]/p//text()',lambda x:[i.strip() for i in x],Join())
        loader1.add_value('id',response.url.strip('/').split('/')[-1])
        loader1.add_xpath('img_urls','//article//div[@class="entry-content"]//img/@src')
        loader1.add_xpath('publish_time','//article//time[@class="published"]/@datetime',deal_publish_time)
        loader1.add_xpath('publish_user','//article//time[@class="published"]/a[@class="fn"]/text()')



        item=loader1.load_item()
        print (item)
        return item