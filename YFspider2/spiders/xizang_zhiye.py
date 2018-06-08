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




class xizang_zhiye(RedisCrawlSpider):
    name = 'xizang_zhiye'
    start_urls=['http://xizang-zhiye.org/']
    headers={
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36',
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    }


    rules =  (
        Rule(LinkExtractor(allow='http\:\/\/xizang\-zhiye\.org\/\d*/\d*/.*/',),callback='parse_content',follow=True),
        Rule(LinkExtractor(allow='http\:\/\/xizang\-zhiye\.org\/.*',),follow=True)
    )




    def parse_content(self,response):
        print ('in parseMore')

        def deal_publish_user(publish_user):
            for one_str in publish_user:
                if u'发布' in one_str:
                    continue
                else:
                    if one_str.strip():
                        return one_str.strip()

        def deal_publish_time(publish_time_raw):
            if publish_time_raw:
                try:
                    publish_time_str=publish_time_raw[0]
                    publish_time_str_splited=publish_time_str.split(' ')
                    mouth_CN=publish_time_str_splited[0].strip()
                    days=publish_time_str_splited[1].strip(',')
                    year=publish_time_str_splited[3].strip()

                    if len(days)<2:
                        days='0'+str(days)
                    mounth_to_num={
                        u'一月':'01',
                        u'二月':'02',
                        u'三月':'03',
                        u'四月':'04',
                        u'五月':'05',
                        u'六月':'06',
                        u'七月':'07',
                        u'八月':'08',
                        u'九月':'09',
                        u'十月':'10',
                        u'十一月':'11',
                        u'十二月':'12',
                    }

                    mounth_num=mounth_to_num[mouth_CN]

                    return str(year)+'-'+mounth_num+'-'+days+' 00:00:00'
                except Exception as e:
                    return '2018-02-01 00:00:00'

            else:
                return '2018-05-09 00:00:00'




        loader1=ItemLoader(item=YfspiderspeakItem(),response=response)
        loader1.add_value('url',response.url)
        loader1.add_value('spider_time',time.time())
        loader1.add_xpath('title','//div[@class="content row"]//div[@class="page-header"]/h1/text()',lambda x:''.join([y for y in x]))
        loader1.add_xpath('content','//div[@class="content row"]//div[@class="entry-content"]//div[@class="pf-content"]//text()',lambda x:[i.strip() for i in x],Join())
        loader1.add_value('id',response.url.strip('/').split('/')[-1])
        loader1.add_xpath('img_urls','//div[@class="content row"]//div[@class="entry-content"]//img/@src')
        loader1.add_value('publish_time',response.xpath('//div[@class="single_meta_item single_meta_date"]/text()').extract(),deal_publish_time)
        loader1.add_xpath('publish_user','//div[@class="content row"]//div[@id="single_byline"]//text()',deal_publish_user)




        item=loader1.load_item()
        print (item)
        return item