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




class kagyuoffice(RedisCrawlSpider):
    name = 'kagyuoffice'
    start_urls=['https://www.kagyuoffice.org.tw/']
    headers={
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36',
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    }


    rules =  (
        Rule(LinkExtractor(allow='https\:\/\/www\.kagyuoffice\.org\.tw\/news\/\d*',),callback='parse_content',follow=True),
        Rule(LinkExtractor(allow='https\:\/\/www\.kagyuoffice\.org\.tw\/news\?start\=\d*',),follow=True)
    )




    def parse_content(self,response):
        print ('in parseMore')


        def deal_publish_time(publish_time_list):#20180502
            if not publish_time_list:
                return '2018-05-09 00:00:00'
            else:
                publish_time_list=publish_time_list.replace('-','')
                year=publish_time_list[0:4]
                mounth=publish_time_list[4:6]

                day=publish_time_list[6:8]
                return year+'-'+mounth+'-'+day+' 00:00:00'

        def deal_read_count(read_count=None):
            if read_count:
                return int(str(''.join(read_count)))
            else:
                return 0

        def deal_img_urls(img_urls_raw):
            urlList=[]
            for one_img_url in img_urls_raw:
                if 'printButton' in img_urls_raw or 'emailButton' in one_img_url:
                    continue
                if 'https://www.kagyuoffice.org.tw' not in one_img_url:
                    if one_img_url.startswith('/'):
                        one_img_url_dealed='https://www.kagyuoffice.org.tw'+one_img_url
                        urlList.append(one_img_url_dealed)



        loader1=ItemLoader(item=YfspiderspeakItem(),response=response)
        loader1.add_value('url',response.url)
        loader1.add_value('spider_time',time.time())
        loader1.add_xpath('title','//div[@id="gj-main-content"]//div[@class="span9"]//div[@class="item-page"]//h2//a//text()',lambda x:''.join([y for y in x]))
        loader1.add_xpath('content','//div[@id="gj-main-content"]//div[@class="span9"]//div[@class="item-page"]/p//text()',lambda x:[i.strip() for i in x],Join())
        loader1.add_value('id',response.url.split('news/')[-1])
        loader1.add_xpath('img_urls','//div[@id="gj-main-content"]//div[@class="span9"]//div[@class="item-page"]//img/@src',deal_img_urls)
        loader1.add_value('publish_time',response.url.split('news/')[-1],deal_publish_time)
        loader1.add_value('publish_user','kagyuoffice')
        loader1.add_value('read_count',response.xpath('//div[@class="item-page"]//dd[@class="gj-hits"]//text()').re('.*?(\d*)'),deal_read_count)



        item=loader1.load_item()
        print (item)
        return item