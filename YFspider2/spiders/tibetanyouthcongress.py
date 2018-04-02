#_*_coding:utf-8_*_
import scrapy
# from scrapy.spider import Spider
from scrapy.spider import CrawlSpider
from scrapy_redis.spiders import RedisCrawlSpider
from YFspider2.items import YfspiderspeakItem
from scrapy.spiders import Rule
from scrapy.linkextractor import LinkExtractor
from YFspider2.othermodule.itemloader_ll import itemloader_ll
from scrapy.loader.processors import Join,MapCompose,Compose,TakeFirst
import time
import hashlib


class tibetanyouthcongress(RedisCrawlSpider):
    name = 'tibetanyouthcongress'
    # redis_key = 'tibetanyouthcongress:url'
    start_urls = ['https://www.tibetanyouthcongress.org/']

    rules = {
        Rule(LinkExtractor(allow=r'(https:\/\/www\.tibetanyouthcongress\.org\/\d{1,4}\/\d{1,2}\/\S*?\/)',),callback="parse_content",follow=True),
        # Rule(LinkExtractor(allow=r'()',restrict_xpaths='//div[@class="container"]/div[@class="nine columns"]',),follow=True),
    }

    def parse_content(self,response):
        def deal_id(id_raw):
            id_str=id_raw[0]
            return hashlib.md5(id_str).hexdigest()



        print response.url
        content_loader=itemloader_ll(response=response,item=YfspiderspeakItem())
        content_loader.add_value('url',response.url)
        content_loader.add_value('spider_time',time.time())

        content_loader.add_xpath('title','//div[@class="breadcrumb-inner"]/div[@class="subtitle"]/h2/text()')
        content_loader.add_xpath('content','//div[@class="container"]//div[@class="detail_text rich_editor_text"]//p/text()',Join())
        content_loader.add_xpath('publish_time','//div[@class="container"]//ul[@class="post-options"]//time/@datetime',lambda x:x[0]+' 00:00:00')
        content_loader.add_value('id',response.url.strip('/').split('/')[-1],deal_id)
        content_loader.add_xpath('publish_user','//div[@class="container"]//ul[@class="post-options"]//li/i[@class="icon icon-user"]/ancestor::li/a[@href]/text()')
        content_loader.add_xpath('publish_user_id','//div[@class="container"]//ul[@class="post-options"]//li/i[@class="icon icon-user"]/'
                                                   'ancestor::li/a[@href]/@href',lambda x:x[0].strip('/').split('/')[-1])
        content_loader.add_value('img_urls',response.xpath('//div[@id="main"]/div[@class="container"]/div[@class="row"]//img/@src').re(r'http://.*'))
        item1=content_loader.load_item()
        return item1