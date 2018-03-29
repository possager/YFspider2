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
from string import strip
import scrapy
import time
import datetime




class chinaaid(RedisCrawlSpider):
    name = 'chinaaid'
    start_urls=['http://www.chinaaid.net']
    # redis_key='middleway:urls'
    headers={
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36',
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    }


    rules =  (
        Rule(LinkExtractor(allow='http\:\/\/www\.chinaaid\.net\/\d{4}/\d{1,2}/.*?\_\d*\.html',),callback='parse_content',follow=True),
        Rule(LinkExtractor(allow='http\:\/\/www\.chinaaid\.net\/.*?'),follow=True),
        Rule(LinkExtractor(allow='http\:\/\/www\.chinaaid\.org\/\d{4}/\d{1,2}/.*?.html',),callback='parse_content',follow=True),
        Rule(LinkExtractor(allow='http\:\/\/www\.chinaaid\.org\/.*?',),follow=True)
    )


    # def start_requests(self):
    #     for url in self.start_urls:
    #         yield scrapy.Request(url=url,headers=self.headers)



    def parse_content(self,response):
        print 'in parseMore'


        def deal_publish_time(publish_time_list=[]):
            if not publish_time_list:
                print 'time is None'
                return None
            if len(publish_time_list)==3:
                publish_time_list1=[]

                for time_num in publish_time_list:
                    time_num=str(time_num)
                    if len(time_num)<2:
                        time_num1='0'+time_num
                        publish_time_list1.append(time_num1)
                    else:
                        publish_time_list1.append(str(time_num))
                publish_time_str=publish_time_list1[2]+'-'+publish_time_list1[0]+'-'+publish_time_list1[1]
                publish_time_str=publish_time_str.strip('-')
                publish_time_str+=' 00:00:00'
                return publish_time_str
            else:
                print 'publish_time_wrong'
                return None


        loader1=ItemLoader(item=YfspiderspeakItem(),response=response)
        loader1.add_value('url',response.url)
        loader1.add_value('spider_time',time.time())
        loader1.add_value('id',response.url.split('/')[-1].split('.')[0])
        loader1.add_xpath('title','//div[@id="main"]//div[@class="post-outer"]/h2/text()',lambda x:x[0].strip())
        loader1.add_xpath('content','//div[@id="main"]//div[@class="post-entry"]//text()',lambda x:[x1.strip() for x1 in x],Join())
        loader1.add_value('publish_time',response.xpath('//div[@id="main"]//div[@class="date-outer"]//span[@class="heading-date"]').re('(\d{1,2})\/(\d{1,2})\/(\d{4})'),deal_publish_time)
        loader1.add_xpath('img_urls','//div[@id="main"]//div[@class="post-entry"]//img/@src')




        item=loader1.load_item()
        print item
        return item