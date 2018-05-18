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



class dalailama(RedisCrawlSpider):
    name = 'dalailama'
    start_urls=['https://www.dalailama.com/']
    headers={
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36',
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    }


    rules =  (
        Rule(LinkExtractor(allow=r'https\:\/\/www\.dalailama\.com\/pictures\/.*',deny=('facebook.com','twitter.com'),allow_domains=('dalailama.com',)), callback='parse_content_piicture',
             follow=True),
        Rule(LinkExtractor(allow=r'https\:\/\/www\.dalailama\.com\/news\/\d*\/.*',process_value=deal_links_to_fallow,deny=('facebook.com','twitter.com')),callback='parse_content',follow=True),
        Rule(LinkExtractor(allow=r'https\:\/\/www\.dalailama\.com\/.*',),follow=True,callback='parse_any_page'),
    )




    def parse_content(self,response):
        print ('in parseMore')


        def deal_publish_time(publish_time_list=[]):
            if publish_time_list:
                publish_time_str=publish_time_list
            else:
                return '2018-02-01 00:00:00'
            try:
                mounth_str=publish_time_list[0]
                day=publish_time_str[1]
                year=publish_time_list[2]

                mouth_transform = {
                    'January': '01',
                    'February': '02',
                    'March': '03',
                    'April': '04',
                    'May': '05',
                    'June': '06',
                    'July': '07',
                    'August': '08',
                    'September': '09',
                    'October': '10',
                    'November': '11',
                    'December': '12'
                }
                mounth_num=mouth_transform[str(mounth_str).strip()]
                if len(str(day).strip()) < 2:
                    day='0'+str(day).strip()
                year=str(year)
                return year+'-'+mounth_num+'-'+day+' 00:00:00'

            except:
                return '2018-02-01 00:00:00'



        loader1=ItemLoader(item=YfspiderspeakItem(),response=response)
        loader1.add_value('url',response.url)
        loader1.add_value('spider_time',time.time())
        loader1.add_xpath('title','//div[@class="hideOnNavigation"]//h1//text()',lambda x:''.join([y for y in x]))
        loader1.add_xpath('content','//div[contains(@class,"newsContentArea")]//p//text()',lambda x:[i.strip() for i in x],Join())
        loader1.add_value('id',response.url.strip('/').split('/')[-1])
        loader1.add_xpath('img_urls','//div[contains(@class,"newsContentArea")]//img/@src')
        loader1.add_xpath('publish_time','//div[@class="hideOnNavigation"]//h1/span//text()',deal_publish_time)




        item=loader1.load_item()
        print (item)
        return item

    def parse_content_picture(self,response):
        print('deal picture')

        def deal_publish_time(publish_time_list=[]):
            if publish_time_list:
                publish_time_str=publish_time_list
            else:
                return '2018-02-01 00:00:00'
            try:
                mounth_str=publish_time_list[0]
                day=publish_time_str[1]
                year=publish_time_list[2]

                mouth_transform = {
                    'January': '01',
                    'February': '02',
                    'March': '03',
                    'April': '04',
                    'May': '05',
                    'June': '06',
                    'July': '07',
                    'August': '08',
                    'September': '09',
                    'October': '10',
                    'November': '11',
                    'December': '12'
                }
                mounth_num=mouth_transform[str(mounth_str).strip()]
                if len(str(day).strip()) < 2:
                    day='0'+str(day).strip()
                year=str(year)
                return year+'-'+mounth_num+'-'+day+' 00:00:00'

            except:
                return '2018-02-01 00:00:00'

        loader1 = ItemLoader(item=YfspiderspeakItem(), response=response)
        loader1.add_value('url', response.url)
        loader1.add_value('spider_time', time.time())
        loader1.add_xpath('title', '//div[@class="hideOnNavigation"]//h1//text()', lambda x: ''.join([y for y in x]))
        loader1.add_xpath('content', '//div[@class="owl-stage"]//text()',
                          lambda x: [i.strip() for i in x], Join())
        loader1.add_value('id', response.url.strip('/').split('/')[-1])
        loader1.add_xpath('img_urls', '//div[@class="owl-stage"]//img/@src')
        loader1.add_xpath('publish_time', '//div[@class="hideOnNavigation"]//h1/span//text()', deal_publish_time)


        item=loader1.load_item()
        return item

    def parse_any_page(self,response):
        if not response.xpath('//div[@class]//section[@role="page"]//div[contains(@class,"showCaptions")]'):
            return

        def deal_publish_time(publish_time_list=[]):
            if publish_time_list:
                publish_time_str=publish_time_list
            else:
                return '2018-02-01 00:00:00'
            try:
                mounth_str=publish_time_list[0]
                day=publish_time_str[1]
                year=publish_time_list[2]

                mouth_transform = {
                    'January': '01',
                    'February': '02',
                    'March': '03',
                    'April': '04',
                    'May': '05',
                    'June': '06',
                    'July': '07',
                    'August': '08',
                    'September': '09',
                    'October': '10',
                    'November': '11',
                    'December': '12'
                }
                mounth_num=mouth_transform[str(mounth_str).strip()]
                if len(str(day).strip()) < 2:
                    day='0'+str(day).strip()
                year=str(year)
                return year+'-'+mounth_num+'-'+day+' 00:00:00'

            except:
                return '2018-02-01 00:00:00'

        loader1=ItemLoader(item=YfspiderspeakItem(),response=response)
        loader1.add_value('url',response.url)
        loader1.add_value('spider_time',time.time())
        loader1.add_xpath('title','//div[@class="hideOnNavigation"]//h1//text()',lambda x:''.join([y for y in x]))
        loader1.add_xpath('content','//div[@class]//section[@role="page"]//div[contains(@class,"showCaptions")]//p//text()',lambda x:[i.strip() for i in x],Join())
        loader1.add_value('id',response.url.strip('/').split('/')[-1])
        loader1.add_xpath('img_urls','//div[@class]//section[@role="page"]//div[contains(@class,"showCaptions")]//img/@src',lambda x:['https://www.dalailama.com'+str(y) for y in x])
        loader1.add_xpath('publish_time','//div[@class="hideOnNavigation"]//h1/span//text()',deal_publish_time)
        loader1.add_xpath('video_urls','//div[@class="video active"]/@data-src')#video板块的

        item1=loader1.load_item()
        return item1
