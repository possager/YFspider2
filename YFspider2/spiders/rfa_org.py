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



def deal_links_to_fallow(link_raw):
    if link_raw.endswith('form'):
        return None
    else:
        return link_raw



class middleway(RedisCrawlSpider):
    name = 'rfa_org'
    start_urls=['https://www.rfa.org/mandarin/']
    headers={
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36',
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    }


    rules =  (
        Rule(LinkExtractor(allow=r'https\:\/\/www\.rfa\.org\/mandarin\/\S*\/\S*\/.*\.html',process_value=deal_links_to_fallow),callback='parse_content',follow=True),
        Rule(LinkExtractor(allow=r'https\:\/\/www\.rfa\.org\/mandarin\/.*',),follow=True)
    )




    def parse_content(self,response):
        print ('in parseMore')


        def deal_publish_time(publish_time_list=[]):
            if publish_time_list:
                publish_time_str=''.join(publish_time_list).strip()
            else:
                return '2018-02-01 00:00:00'
            try:
                return publish_time_str+' 00:00:00'
            except:
                return '2018-02-01 00:00:00'



        loader1=ItemLoader(item=YfspiderspeakItem(),response=response)
        loader1.add_value('url',response.url)
        loader1.add_value('spider_time',time.time())
        loader1.add_xpath('title','//div[@id="abovefold"]//div[@id="storypagemaincol"]//h1/text()',lambda x:''.join([y for y in x]))
        loader1.add_xpath('content','//div[@id="abovefold"]//div[@id="storypagemaincol"]//div[@id="storytext"]//text()',lambda x:[i.strip() for i in x],Join())
        loader1.add_value('id',response.url.strip('/').split('/')[-1])
        loader1.add_xpath('img_urls','//div[@id="abovefold"]//div[@id="storypagemaincol"]//div[@id="storytext"]//img/@src',lambda x:[y for y in x if 'icon-' not in y])
        loader1.add_xpath('publish_time','//div[@id="abovefold"]//div[@id="storypagemaincol"]//div[@id="storytop"]//span[@id="story_date"]//text()',deal_publish_time)
        # loader1.add_xpath('publish_user','//article//time[@class="published"]/a[@class="fn"]/text()')



        item=loader1.load_item()
        print (item)
        return item