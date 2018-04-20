#_*_coding:utf-8_*_
# from scrapy.spiders import CrawlSpider,Rule
from scrapy.spiders import Rule
from scrapy_redis.spiders import RedisCrawlSpider
from scrapy.linkextractor import LinkExtractor
from YFspider2.items import YfspiderspeakItem
# from scrapy.loader import
from YFspider2.othermodule.itemloader_ll import itemloader_ll
from scrapy.loader import ItemLoader
from scrapy.loader.processors import Join,TakeFirst,MapCompose

import scrapy
import time
import datetime




class radiosoh(RedisCrawlSpider):
    name = 'radiosoh'
    start_urls=['http://radiosoh.com/category/china/page/3/']
    # redis_key='middleway:urls'
    headers={
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36',
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    }


    rules =  (
        Rule(LinkExtractor(allow='http\:\/\/radiosoh\.com\/category\/china\/page\/\d*\/',),follow=True),
        Rule(LinkExtractor(allow='http\:\/\/radiosoh\.com\/((?!\/).)*',restrict_xpaths=('//div[@id="td-outer-wrap"]/div[@class="td-main-content-wrap"]','//div[@id="td-outer-wrap"]/div[@class="td-category-grid"]')),callback='parse_content',follow=True),
    )


    # def start_requests(self):
    #     for url in self.start_urls:
    #         yield scrapy.Request(url=url,headers=self.headers)



    def parse_content(self,response):
        print ('in parseMore')

        def deal_publish_time(publish_time):
            if publish_time:
                #2017-03-29T11:52:42+00:00
                try:
                    publish_time_str_raw=publish_time[0]
                    publish_time_splited=publish_time_str_raw.split('T')
                    publish_date=publish_time_splited[0]
                    publish_hours=publish_time_splited[1].split('+')[0]

                    return publish_date+' '+publish_hours

                except Exception as e:
                    print (e)
                    return None
            else:
                return None



        loader1=ItemLoader(item=YfspiderspeakItem(),response=response)
        loader1.add_value('url',response.url)
        loader1.add_value('spider_time',time.time())
        loader1.add_xpath('title','//h1[@class="entry-title"]/text()',lambda x:x[0].strip())
        loader1.add_xpath('content','//div[@class="td-post-content"]//p/text()',lambda x:[onegraph.strip() for onegraph in x],Join())
        loader1.add_value('id',response.url.strip('/').split('/')[-1].split('.')[0].strip('/'))
        loader1.add_value('img_urls',response.xpath('//div[@class="td-post-content"]//img/@src').extract())
        loader1.add_xpath('publish_time','//div[@class="td-module-meta-info"]/span/time/@datetime',deal_publish_time)
        loader1.add_xpath('video_urls','//iframe[@gesture="media"]/@src')
        # loader1.add_xpath('')




        item=loader1.load_item()
        print (item)
        return item



