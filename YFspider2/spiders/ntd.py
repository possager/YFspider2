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


# def deal_links_to_fallow(link_raw):
#     links=link_raw.replace('http://','')
#     linksplited= links.strip('/').split('/')
#     if len(linksplited)==2:
#         print '跟进链接:',link_raw
#         return link_raw



class ntd(RedisCrawlSpider):
    name = 'ntd'
    start_urls=['http://www.ntd.tv/']
    headers={
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36',
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    }


    rules =  (
        Rule(LinkExtractor(allow=r'http\:\/\/www\.ntd\.tv\/\d{4}/\d{2}\/\d{2}\/.*\/',),callback='parse_content',follow=True),
        Rule(LinkExtractor(allow=r'http\:\/\/www\.ntd\.tv\/.*',),follow=True)
    )




    def parse_content(self,response):
        print ('in parseMore')


        def deal_publish_time(publish_time_list=''):
            if publish_time_list:
                publish_time_str=publish_time_list.split('ntd.tv/')[1]
            else:
                return '2018-02-01 00:00:00'

            try:
                time_splited=publish_time_str.split('/')
                year=time_splited[0]
                mounth=time_splited[1]
                days=time_splited[2]

                return str(year)+'-'+str(mounth)+'-'+str(days)+' 00:00:00'
            except:
                return '2018-02-01 00:00:00'



        loader1=ItemLoader(item=YfspiderspeakItem(),response=response)
        loader1.add_value('url',response.url)
        loader1.add_value('spider_time',time.time())
        loader1.add_xpath('title','//main[@id="main"]//h1//text()',lambda x:''.join([y for y in x]).strip())
        loader1.add_xpath('content','//main[@id="main"]//div[@class="left_block"]/div[contains(@class,"content")]//p//text()',lambda x:[i.strip() for i in x],Join())
        loader1.add_value('id',response.url.strip('/').split('/')[-1])
        loader1.add_xpath('img_urls','//main[@id="main"]//div[@class="left_block"]/div[contains(@class,"content")]//img/@src')
        loader1.add_value('publish_time',response.url,deal_publish_time)
        loader1.add_xpath('publish_user','//main[@id="main"]//div[@class="author"]//span[@class="author_name"]/text()')
        loader1.add_xpath('video_urls','//main[@id="main"]//div[@class="left_block"]/div[contains(@class,"content") or contains(@class,"container")]//video/@src')


        item=loader1.load_item()
        print (item)
        return item