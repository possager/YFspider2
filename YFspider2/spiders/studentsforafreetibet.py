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

class studentsforafreetibet(RedisCrawlSpider):
    name = 'studentsforafreetibet'
    # start_urls = ['https://www.studentsforafreetibet.org/media-center/']

    rules = {
        Rule(LinkExtractor(allow=r'(https://www.studentsforafreetibet.org/media-center/\S*/\S*/)',deny=r'https://www.studentsforafreetibet.org/media-center/page/',restrict_xpaths='//div[@class="container"]/div[@class="nine columns"]',),callback="parse_content",follow=True),
        Rule(LinkExtractor(allow=r'(https://www.studentsforafreetibet.org/media-center/page/\d{1,2}/)',restrict_xpaths='//div[@class="container"]/div[@class="nine columns"]',),follow=True),

    }

    def parse_content(self,response):

        def deal_publish_time(publish_time_url):
            print ('in deal_publish_time',publish_time_url)
            try:
                publish_time_url=publish_time_url[0]
            except:
                return None
            publish_time_date_str=publish_time_url.split('org/')[1].strip('/').replace('/','-')
            publish_time=publish_time_date_str+' 00:00:00'
            return publish_time

        def deal_id(id):
            id_hash=hashlib.md5(id).hexdigest()
            return id_hash



        print (response.url)
        content_loader=ItemLoader(item=YfspiderspeakItem(),response=response)


        content_loader.add_value('url', response.url)
        content_loader.add_value('spider_time',time.time())

        content_loader.add_xpath('title','//article[@id]/div[@class="gdlr-standard-style"]/div[@class="blog-content-wrapper"]/header/h1/text()')
        content_loader.add_xpath('content','//article[@id]/div[@class="gdlr-standard-style"]/div[@class="blog-content-wrapper"]/div[@class="gdlr-blog-content"]/p/text()',Join())
        content_loader.add_xpath('publish_time','//article[@id]/div[@class="gdlr-standard-style"]/div[@class="blog-content-wrapper"]/header[@class="post-header"]/div[@class="gdlr-blog-info gdlr-info"]/div[@class="blog-info blog-date"]/a[@href]//@href',deal_publish_time)
        content_loader.add_value('img_urls',response.xpath('//div[@class="blog-content-wrapper"]//img').re('src="(.*?)"'))
        content_loader.add_value('id',response.url.strip('/').split('/')[-1],deal_id)
        item=content_loader.load_item()
        print (item)
        return item