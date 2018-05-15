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



class aboluowang(RedisCrawlSpider):
    name = 'aboluowang'
    start_urls=['http://www.aboluowang.com/']
    headers={
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36',
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    }


    rules =  (
        Rule(LinkExtractor(allow=r'http\:\/\/www\.aboluowang\.com\/\d{4}\/\d{4}\/\d*\.html',),callback='parse_content',follow=True),
        Rule(LinkExtractor(allow=r'http\:\/\/www\.aboluowang\.com\/.*',),follow=True)
    )




    def parse_content(self,response):
        print ('in parseMore')


        def deal_publish_time(publish_time_str):
            if publish_time_str:
                publish_time_str=publish_time_str.strip()
            else:
                return '2018-02-01 00:00:00'
            try:
                year=publish_time_str.split('/')[-3]
                mounth_days=publish_time_str.split('/')[-2]
                mount=mounth_days[0:2]
                days=mounth_days[2:4]
                return year+'-'+mount+'-'+days+' 00:00:00'
            except Exception as e:
                return '2018-02-01 00:00:00'

        def deal_img_urls(img_urls_raw):
            img_urls_list=[]
            for one_img_url in img_urls_raw:
                if 'empty.gif' in one_img_url:
                    continue
                else:
                    if 'http' not in one_img_url:
                        one_img_url='http:'+one_img_url
                        img_urls_list.append(one_img_url)

            return img_urls_list


        loader1=ItemLoader(item=YfspiderspeakItem(),response=response)
        loader1.add_value('url',response.url)
        loader1.add_value('spider_time',time.time())
        loader1.add_xpath('title','//div[@id="main"]//div[@id="Article"]/h1//text()',lambda x:''.join([y for y in x]))
        loader1.add_xpath('content','//div[@id="main"]//div[@id="Article"]//article[@id="content"]/p//text()',lambda x:[i.strip() for i in x],Join())
        loader1.add_value('id',response.url.strip('/').split('/')[-1])
        loader1.add_xpath('img_urls','//div[@id="main"]//div[@id="Article"]//article[@id="content"]/p//img/@src',deal_img_urls)
        loader1.add_value('publish_time',response.url,deal_publish_time)
        loader1.add_xpath('publish_user','//div[@id="main"]//div[@id="Article"]//p[@id="editor"]//b/text()')


        item=loader1.load_item()
        print (item)
        return item