#_*_coding:utf-8_*_
# from scrapy.spiders import CrawlSpider,Rule
from scrapy.spiders import Rule
from scrapy_redis.spiders import RedisCrawlSpider
from scrapy.linkextractors import LinkExtractor
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



class sputniknews(RedisCrawlSpider):
    name = 'sputniknews'
    start_urls=['http://sputniknews.cn/']
    headers={
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36',
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    }


    rules =  (
        Rule(LinkExtractor(allow=r'http\:\/\/sputniknews\.cn\/photo/\d*/',),callback='parse_content_photo',follow=True),
        Rule(LinkExtractor(allow=r'http\:\/\/sputniknews\.cn\/video/\d*/', ), callback='parse_content_video',
             follow=True),
        Rule(LinkExtractor(allow=r'http\:\/\/sputniknews\.cn\/infographics/\d*/', ), callback='parse_content_infographics',
             follow=True),
        Rule(LinkExtractor(allow=r'http\:\/\/sputniknews\.cn\/\S*/\d*/', ), callback='parse_content', follow=True),
        Rule(LinkExtractor(allow=r'http\:\/\/sputniknews\.cn\/.*',),follow=True)
    )




    def parse_content(self,response):
        print ('in parseMore')


        def deal_publish_time(publish_time_list=[]):
            if publish_time_list:
                publish_time_str=publish_time_list[0]
            else:
                return '2018-02-01 00:00:00'
            try:
                publish_time_str_split=publish_time_str.split('+')[0]
                return publish_time_str_split.replace('T',' ')+':00'
            except:
                return '2018-02-01 00:00:00'



        loader1=ItemLoader(item=YfspiderspeakItem(),response=response)
        loader1.add_value('url',response.url)
        loader1.add_value('spider_time',time.time())
        loader1.add_xpath('title','//div[@class="l-main m-oh"]//div[@class="l-wrap m-oh"]//h1[@itemprop]/text()',lambda x:''.join([y for y in x]))
        loader1.add_xpath('content','//div[@class="l-main m-oh"]//div[@itemprop="articleBody"]//p//text()|//div[@class="l-main m-oh"]//div[@itemprop="description"]//p//text()',lambda x:[i.strip() for i in x],Join())
        loader1.add_value('id',response.url.strip('/').split('/')[-1])
        loader1.add_xpath('img_urls','//div[@class="l-main m-oh"]//div[@itemprop="articleBody"]//img/@src')
        loader1.add_xpath('publish_time','//div[@class="l-main m-oh"]//div[@class="b-article__refs-credits"]//time[@class="b-article__refs-date"]/@datetime',deal_publish_time)
        loader1.add_xpath('like_count','//span[@class="b-counters-icon b-counters-icon_like"]/text()',lambda x:[y.strip() for y in x])
        loader1.add_xpath('dislike_count','//span[@class="b-counters-icon b-counters-icon_dislike"]/text()',lambda x:[y.strip() for y in x])




        item=loader1.load_item()
        print (item)
        return item

    def parse_content_photo(self,response):
        print ('in parseMore_photo')


        def deal_publish_time(publish_time_list=[]):
            if publish_time_list:
                publish_time_str=publish_time_list[0]
            else:
                return '2018-02-01 00:00:00'
            try:
                publish_time_str_split=publish_time_str.split('+')[0]
                return publish_time_str_split.replace('T',' ')+':00'
            except:
                return '2018-02-01 00:00:00'



        loader1=ItemLoader(item=YfspiderspeakItem(),response=response)
        loader1.add_value('url',response.url)
        loader1.add_value('spider_time',time.time())
        loader1.add_xpath('title','//div[@class="l-main m-oh"]//div[@class="l-wrap m-oh"]//h1[@itemprop]/text()',lambda x:''.join([y for y in x]))
        loader1.add_xpath('content','//div[@class="l-main m-oh"]//div[@itemprop="articleBody"]//p//text()|//div[@class="l-main m-oh"]//div[@itemprop="description"]//p//text()',lambda x:[i.strip() for i in x],Join())
        loader1.add_value('id',response.url.strip('/').split('/')[-1])
        loader1.add_xpath('img_urls','//div[@class="l-main m-oh"]//div[@itemprop="articleBody"]//img/@src|//div[@class="l-main m-oh"]//ul[@class="lightSlider lSSlide lsGrab"]//li/@data-src')
        loader1.add_xpath('publish_time','//div[@class="l-main m-oh"]//div[@class="b-article__refs-credits"]//time[@class="b-article__refs-date"]/@datetime',deal_publish_time)
        loader1.add_xpath('like_count','//span[@class="b-counters-icon b-counters-icon_like"]/text()')
        loader1.add_xpath('dislike_count','//span[@class="b-counters-icon b-counters-icon_dislike"]/text()')




        item=loader1.load_item()
        print (item)
        return item

    def parse_content_video(self,response):
        print ('in parseMore')


        def deal_publish_time(publish_time_list=[]):
            if publish_time_list:
                publish_time_str=publish_time_list[0]
            else:
                return '2018-02-01 00:00:00'
            try:
                publish_time_str_split=publish_time_str.split('+')[0]
                return publish_time_str_split.replace('T',' ')+':00'
            except:
                return '2018-02-01 00:00:00'



        loader1=ItemLoader(item=YfspiderspeakItem(),response=response)
        loader1.add_value('url',response.url)
        loader1.add_value('spider_time',time.time())
        loader1.add_xpath('title','//div[@class="l-main m-oh"]//div[@class="l-wrap m-oh"]//h1[@itemprop]/text()',lambda x:''.join([y for y in x]))
        loader1.add_xpath('content','//div[@class="l-main m-oh"]//div[@itemprop="articleBody"]//p//text()|//div[@class="l-main m-oh"]//div[@itemprop="description"]//p//text()',lambda x:[i.strip() for i in x],Join())
        loader1.add_value('id',response.url.strip('/').split('/')[-1])
        loader1.add_xpath('img_urls','//div[@class="l-main m-oh"]//div[@itemprop="articleBody"]//img/@src')
        loader1.add_xpath('publish_time','//div[@class="l-main m-oh"]//div[@class="b-article__refs-credits"]//time[@class="b-article__refs-date"]/@datetime',deal_publish_time)
        loader1.add_xpath('like_count','//span[@class="b-counters-icon b-counters-icon_like"]/text()')
        loader1.add_xpath('dislike_count','//span[@class="b-counters-icon b-counters-icon_dislike"]/text()')
        loader1.add_xpath('video_urls','//div[@class="l-main m-oh"]//div[@class="video-player"]//video/@src')




        item=loader1.load_item()
        print (item)
        return item

    def parse_content_infographics(self,response):
        print ('in parseMore')


        def deal_publish_time(publish_time_list=[]):
            if publish_time_list:
                publish_time_str=publish_time_list[0]
            else:
                return '2018-02-01 00:00:00'
            try:
                publish_time_str_split=publish_time_str.split('+')[0]
                return publish_time_str_split.replace('T',' ')+':00'
            except:
                return '2018-02-01 00:00:00'



        loader1=ItemLoader(item=YfspiderspeakItem(),response=response)
        loader1.add_value('url',response.url)
        loader1.add_value('spider_time',time.time())
        loader1.add_xpath('title','//div[@class="l-main m-oh"]//div[@class="l-wrap m-oh"]//h1[@itemprop]/text()',lambda x:''.join([y for y in x]))
        loader1.add_xpath('content','//div[@class="l-main m-oh"]//div[@itemprop="articleBody"]//p//text()|//div[@class="l-main m-oh"]//div[@itemprop="description"]//p//text()',lambda x:[i.strip() for i in x],Join())
        loader1.add_value('id',response.url.strip('/').split('/')[-1])
        loader1.add_xpath('img_urls','//div[@class="l-main m-oh"]//div[@itemprop="articleBody"]//img/@src|//div[@class="l-main m-oh"]//div[@class="b-article__media-ig"]/img/@src')
        loader1.add_xpath('publish_time','//div[@class="l-main m-oh"]//div[@class="b-article__refs-credits"]//time[@class="b-article__refs-date"]/@datetime',deal_publish_time)
        loader1.add_xpath('like_count','//span[@class="b-counters-icon b-counters-icon_like"]/text()')
        loader1.add_xpath('dislike_count','//span[@class="b-counters-icon b-counters-icon_dislike"]/text()')




        item=loader1.load_item()
        print (item)
        return item