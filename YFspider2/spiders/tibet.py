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
    if 'pdf' not in link_raw:
        return link_raw



class tibet(RedisCrawlSpider):
    name = 'tibet'
    start_urls=['http://tibet.net/']
    headers={
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36',
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    }


    rules =  (
        Rule(LinkExtractor(allow=r'http\:\/\/tibet\.net\/\d{4}/\d{2}\/.*\/',process_value=deal_links_to_fallow),callback='parse_content',follow=True),
        Rule(LinkExtractor(allow=r'http\:\/\/tibet\.net\/.*',),follow=True)
    )




    def parse_content(self,response):
        print ('in parseMore')


        def deal_publish_time(publish_time_couple):
            publish_time_list,url=publish_time_couple[0],publish_time_couple[1]
            if publish_time_list:
                publish_time_str=publish_time_list[0]
            else:
                return '2018-02-01 00:00:00'
            try:
                publish_time_str=str(publish_time_str)
                datetime=url.split('tibet.net/')[1]
                datetime_splited=datetime.strip('/').split('/')
                year=datetime_splited[0]
                mounth=datetime_splited[1]
                return str(year)+'-'+str(mounth)+'-'+str(publish_time_str).strip()+' 00:00:00'
            except:
                return '2018-02-01 00:00:00'



        loader1=ItemLoader(item=YfspiderspeakItem(),response=response)
        loader1.add_value('url',response.url)
        loader1.add_value('spider_time',time.time())
        loader1.add_xpath('title','//main//div[@class="page-header"]/h1/text()',lambda x:''.join([y for y in x]))
        loader1.add_xpath('content','//main//div[@class="pf-content"]/p//text()',lambda x:[i.strip() for i in x],Join())
        loader1.add_value('id',response.url.strip('/').split('/')[-1])
        loader1.add_xpath('img_urls','//main//div[@class="pf-content"]//img/@src')
        loader1.add_value('publish_time',(response.xpath('//main//div[@id="single_meta"]//div[contains(@class,"date")]//text()').re('\S* (\d*)\, \d*'),response.url),deal_publish_time)
        # loader1.add_xpath('publish_user','//article//time[@class="published"]/a[@class="fn"]/text()')



        item=loader1.load_item()
        print (item)
        return item