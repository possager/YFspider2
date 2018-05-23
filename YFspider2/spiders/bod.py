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
import re


def deal_links_to_fallow(link_raw):
    if 'pdf' not in link_raw:
        return link_raw




class bod(RedisCrawlSpider):
    name = 'bod'
    start_urls=['http://bod.asia/']
    headers={
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36',
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    }


    rules =  (
        Rule(LinkExtractor(allow=r'http\:\/\/bod\.asia\/\d{4}\/\d{2}\/.*\/',process_value=deal_links_to_fallow),callback='parse_content',follow=True),
        Rule(LinkExtractor(allow=r'http\:\/\/bod\.asia\/.*',),follow=True)
    )




    def parse_content(self,response):
        print ('in parseMore')


        def deal_publish_time(publish_time_list=[]):
            if publish_time_list:
                publish_time_str=publish_time_list[0]
            else:
                return '2018-02-01 00:00:00'
            try:
                zangwendict3 = {
                    u"༧": u"7",
                    u"༦": u"6",
                    u"༥": u"5",
                    u"༤": u"4",
                    u"༣": u"3",
                    u"༢": u"2",
                    u"༡": u"1",
                    u"༠": u"0",
                    u"༩": u"9",
                    u"༨": u"8"
                }
                for onekey in zangwendict3.keys():
                    if onekey in publish_time_list:
                        publish_time_str = publish_time_str.replace(onekey, zangwendict3[onekey])

                Re_find_time=re.compile(r'(\d{1,2}).*?(\d{1,2}).*?(\d{4})')
                publish_time_1=Re_find_time.findall(publish_time_str)#[(u'5', u'19', u'2018')]
                publish_time_2=publish_time_1[0]
                mounth=str(publish_time_2[0])
                days=str(publish_time_2[1])
                year=str(publish_time_2[2])

                if len(mounth)<2:
                    mounth='0'+mounth
                if len(days)<2:
                    days='0'+days
                return year+'-'+mounth+'-'+days+' 00:00:00'


            except:
                return '2018-02-01 00:00:00'



        loader1=ItemLoader(item=YfspiderspeakItem(),response=response)
        loader1.add_value('url',response.url)
        loader1.add_value('spider_time',time.time())
        loader1.add_xpath('title','//main//div[@class="page-header"]//h1//text()',lambda x:''.join([y for y in x]))
        loader1.add_xpath('content','//main//div[@class="entry-content"]//p//text()',lambda x:[i.strip() for i in x],Join())
        loader1.add_value('id',response.url.strip('/').split('/')[-1])
        loader1.add_xpath('img_urls','//main//div[@class="entry-content"]//p//img/@src')
        loader1.add_xpath('publish_time','//header//div[@class="single_meta_item single_meta_date"]//text()',deal_publish_time)
        loader1.add_xpath('publish_user','//header//div[@id="single_byline"]//text()[2]')



        item=loader1.load_item()
        print (item)
        return item