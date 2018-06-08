#_*_coding:utf-8_*_
import scrapy
# from scrapy.spider import Spider
from scrapy.spider import CrawlSpider
from scrapy_redis.spiders import RedisCrawlSpider
from YFspider2.items import YfspiderspeakItem
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from scrapy.loader.processors import Join,MapCompose,Compose,TakeFirst
import time
import hashlib
from w3lib.url import urljoin


class tibetswiss(RedisCrawlSpider):
    name = 'tibetswiss'
    # redis_key = 'tibetswiss:url'
    start_urls = ['http://www.tibetswiss.ch/index-bo.html']

    rules = {
        Rule(LinkExtractor(allow=r'www\.tibetswiss\.ch\/(europe\-chitue\-bo|europe-chitue-bo|photo-gallary-bo|news-archive-bo|index-bo)\..*',deny=('http://www.tibetswiss.ch/partner-links-bo.html')),follow=True),
        Rule(LinkExtractor(allow=r'www\.tibetswiss\.ch\/latest\-news\-tibetan\/items\/.*\.html',),callback='parse_content_last_news',follow=True),
        Rule(LinkExtractor(allow=r'www\.tibetswiss\.ch\/photogallery\-bo\/items\/.*\.html',),callback='parse_photo',follow=True),
        Rule(LinkExtractor(allow=r'www\.tibetswiss\.ch\/.*',),follow=True)
        # Rule(LinkExtractor(allow=r'()',restrict_xpaths='//div[@class="container"]/div[@class="nine columns"]',),follow=True),
    }

    def parse_content_last_news(self,response):
        def deal_img_urls(img_urls):
            img_result=[]
            for one_img in img_urls:
                img_urls=urljoin('http://www.tibetswiss.ch/',one_img)
                img_result.append(img_urls)
            return img_result


        print (response.url)

        content_loader=ItemLoader(response=response,item=YfspiderspeakItem())
        content_loader.add_value('url',response.url)
        content_loader.add_value('spider_time',time.time())

        content_loader.add_xpath('title','//div[@id="main"]/div[@class="inside"]//h1//text()')
        content_loader.add_xpath('content','//div[@id="main"]/div[@class="inside"]//div[@class="ce_text"]//p/text()',Join())
        content_loader.add_xpath('img_urls','//div[@id="main"]/div[@class="inside"]//div[@class="ce_text"]//img/@src',deal_img_urls)
        content_loader.add_value('publish_time','1111-11-11 11:11:11')
        content_loader.add_value('id',response.url.strip('/').split('/')[-1].split('.html')[0])


        item1=content_loader.load_item()
        return item1

    def parse_photo(self,response):
        def deal_img_urls(img_urls):
            img_result=[]
            for one_img in img_urls:
                img_urls=urljoin('http://www.tibetswiss.ch/',one_img)
                img_result.append(img_urls)
            return img_result


        print (response.url)
        # print 'in photo'
        content_loader = ItemLoader(response=response, item=YfspiderspeakItem())
        content_loader.add_value('url',response.url)
        content_loader.add_value('spider_time',time.time())

        content_loader.add_xpath('title', '//div[@id="main"]//div[@class="inside"]//div[@class="title"]/h1/text()')
        # content_loader.add_xpath('content', '//div[@id="main"]/div[@class="inside"]//div[@class="ce_text"]//p/text()',
        #                          Join())
        content_loader.add_xpath('img_urls', '//div[@id="main"]//div[@class="inside"]//img/@src',deal_img_urls)
        content_loader.add_value('publish_time','1111-11-11 11:11:11')
        content_loader.add_value('id',response.url.strip('/').split('/')[-1].split('.html')[0])
        item1=content_loader.load_item()

        return item1