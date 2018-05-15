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
    # links=link_raw.replace('http://','')
    # linksplited= links.strip('/').split('/')
    # if len(linksplited)==2:
    #     print '跟进链接:',link_raw
    #     return link_raw
    if '?&zhongwen=simp' not in link_raw:
        return link_raw+'?&zhongwen=simp'
    else:
        return link_raw



class dw(RedisCrawlSpider):
    name = 'dw'
    start_urls=['http://tibetanparliament.org/']
    headers={
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36',
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    }


    rules =  (
        Rule(LinkExtractor(allow=r'http\:\/\/www\.dw\.com\/zh\/.*/a-\d.',process_value=deal_links_to_fallow),callback='parse_content',follow=True),
        Rule(LinkExtractor(allow=r'http\:\/\/www\.dw\.com\/zh\/.*',),follow=True)
    )




    def parse_content(self,response):
        print ('in parseMore')


        def deal_publish_time(publish_time_list=[]):
            if publish_time_list:
                publish_time_str=publish_time_list
            else:
                return '2018-02-01 00:00:00'
            try:
                publish_time=publish_time_str[0]+'-'+publish_time_str[1]+'-'+publish_time_str[2]+' 00:00:00'
                return publish_time
            except:
                return '2018-02-01 00:00:00'

        # def deal_publish_user(publish_user_list=[]):




        loader1=ItemLoader(item=YfspiderspeakItem(),response=response)
        loader1.add_value('url',response.url)
        loader1.add_value('spider_time',time.time())
        loader1.add_xpath('title','//div[@id="bodyContent"]//h1/text()',lambda x:''.join([y for y in x]))
        loader1.add_xpath('content','//div[@id="bodyContent"]//div[@class="group"]//div/p//text()',lambda x:[i.strip() for i in x],Join())
        loader1.add_value('id',response.url.strip('/').split('/')[-1])
        loader1.add_xpath('img_urls','//div[@id="bodyContent"]//div[@class="group"]//div/p//img/@src')
        loader1.add_value('publish_time',response.xpath('//div[@id="bodyContent"]//div[@class="col3"]//div[@class="group"]/ul/li[1]//text()').re('(\d{2})\.(\d{2})\.(\d{4})'),deal_publish_time)
        loader1.add_value('publish_user',response.xpath('//div[@id="bodyContent"]//div[@class="col3"]//div[@class="group"]/ul/li//strong[contains(text(),"作者")]/../text()').extract(),lambda x:''.join([str(y).strip() for y in x]))



        item=loader1.load_item()
        print (item)
        return item