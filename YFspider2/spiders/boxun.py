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
import re



def deal_links_to_fallow(link_raw):
    links_splited=link_raw.split('/')
    link_year=links_splited[-3]
    try:
        yearint=int(link_year)
        if yearint>2008:
            return link_raw
    except:
        return



class middleway(RedisCrawlSpider):
    name = 'boxun'
    start_urls=['https://boxun.com/']
    headers={
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36',
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    }


    rules =  (
        Rule(LinkExtractor(allow=r'https\:\/\/boxun\.com\/\S*\/\S*\/\S*\/\d*\/\d*\/\d*\.shtml',process_value=deal_links_to_fallow),callback='parse_content',follow=True),
        # Rule(LinkExtractor(allow=r'https\:\/\/boxun\.com\/.*?\/news\/gb\_display\/print\_versiOn\.cgi\?art\=/\S*\/\S*\/\d*\/.*link\=\d*\.shtml', ),
        #      callback='parse_content', follow=True),
        Rule(LinkExtractor(allow=r'https\:\/\/boxun\.com\/.*',),follow=True)
    )




    def parse_content(self,response):
        print ('in parseMore')


        def deal_publish_time(publish_time_list=[]):
            try:
                publish_str=publish_time_list.split('/')[-1].split('.')[0]
                year_str=publish_str[0:4]
                mounth_str=publish_str[4:6]
                day_str=publish_str[6:8]
                hours_str=publish_str[8:10]
                minute=publish_str[10:12]
                return str(year_str)+'-'+str(mounth_str)+'-'+str(day_str)+' '+str(hours_str)+':'+str(minute)+':00'

            except Exception as e:
                return '2018-02-01 00:00:00'

        def deal_img_urls(img_urls_raw):
            img_urls_list=[]
            for one_img in img_urls_raw:
                if 'boxun.com' not in one_img and 'http' not in one_img:
                    one_img='https://boxun.com'+one_img
                # if 'boxun.com' in one_img:
                img_urls_list.append(one_img)
            return img_urls_list

        def deal_repace_javascript(response):
            Re_replace_javascript = re.compile('\<script.*?\>[\s|\S]*?\<\/script\>')
            RE_replace_nojavascript=re.compile('\<noscript.*?\>[\s|\S]*?\<\/noscript\>')
            resurltt1 = Re_replace_javascript.sub('', response.text)
            resurltt2=RE_replace_nojavascript.sub('',resurltt1)
            response=response.replace(body=resurltt2,url=response.url,status=response.status,headers=response.headers,
                             request=response.request,flags=response.flags)
            return response

        if response.xpath('//table[@class="content"]//tr[@align="center"]'):
            #boxun的版面在很早之前是不一样的，所以由两个版面。
            loader2=ItemLoader(item=YfspiderspeakItem(),response=response)
            loader2.add_value('url', response.url)
            loader2.add_value('spider_time', time.time())
            loader2.add_value('title',
                              response.xpath('//tr//table[@class="content"]//tr[@align="center"]//center//b//text()').extract_first(
                                  default=''), lambda x: x.strip())
            loader2.add_xpath('content', '//tr//table[@class="content"]//tr[@align="center"]//p//text()',
                              lambda x: [i.strip() for i in x], Join())
            loader2.add_value('id', response.url.strip('/').split('/')[-1].split('.')[0])
            loader2.add_xpath('img_urls', '//tr//table[@class="content"]//tr[@align="center"]//p//img/@src', deal_img_urls)
            loader2.add_xpath('video_urls', '//tr//table[@class="content"]//tr[@align="center"]//iframe/@src')
            loader2.add_value('publish_time', response.url, deal_publish_time)
            # loader2.add_xpath('read_count', '//div[@align="center"]//td[@align="right"]//font[@color="red"]/text()')

            item2=loader2.load_item()
            print (item2)
            return item2
        elif response.xpath('//div[@id="Content"]//table[@align]'):
            response=deal_repace_javascript(response)
            loader1=ItemLoader(item=YfspiderspeakItem(),response=response)
            loader1.add_value('url',response.url)
            loader1.add_value('spider_time',time.time())
            loader1.add_value('title',response.xpath('//div[@id="Content"]//table[@align]//center//text()').extract_first(default=''),lambda x:x.strip())
            loader1.add_xpath('content','//div[@id="Content"]//table[@align]//tr/td//text()',lambda x:[i.strip() for i in x],Join())
            loader1.add_value('id',response.url.strip('/').split('/')[-1].split('.')[0])
            loader1.add_xpath('img_urls','//div[@id="Content"]//table[@align]//tr//img/@src',deal_img_urls)
            loader1.add_xpath('video_urls','//div[@id="Content"]//table[@align]//tr//iframe/@src')
            loader1.add_value('publish_time',response.url,deal_publish_time)
            loader1.add_xpath('read_count','//div[@align="center"]//td[@align="right"]//font[@color="red"]/text()')
            # loader1.add_xpath('publish_user','//article//time[@class="published"]/a[@class="fn"]/text()')



            item=loader1.load_item()
            print (item)
            return item




