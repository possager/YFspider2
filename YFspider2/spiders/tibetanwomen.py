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



class tibetanwomen(CrawlSpider):
    name = 'tibetanwomen'
    start_urls=['http://tibetanwomen.org/']

    rules = (
        Rule(LinkExtractor(allow=r'http\:\/\/tibetanwomen\.org\/[^\.\/]*\/$', restrict_xpaths='//div[@id="content"]'), callback='parse_content',
             follow=True),
        Rule(LinkExtractor(allow='http://tibetanwomen.org/page/\d{1,4}/',restrict_xpaths='//div[@id="content"]'), follow=True),
    )

    def parse_content(self, response):

        def deal_id(id_raw):
            return hashlib.md5(id_raw).hexdigest()


        print response.url
        content_loader=itemloader_ll(response=response,item=YfspiderspeakItem())
        content_loader.add_value('url',response.url)
        content_loader.add_value('spider_time',time.time())

        content_loader.add_xpath('title','//div[@id="content"]/div[@id="content-main"]//div[@class="entry clearfix"]//h1[@class="post-title entry-title"]//text()',
                                 lambda x:x[0].strip() if x else None)
        content_loader.add_xpath('content','//div[@id="content"]/div[@id="content-main"]//div[@class="entry clearfix"]/div[@class="entry-content clearfix"]/p//text()',Join())
        content_loader.add_xpath('publish_time','//div[@id]/div[@class="entry clearfix"]/div[@class="date updated alpha with-year"]/span/@title',lambda x:x[0].replace('T',' ')+':00' if x else None)
        content_loader.add_value('id',response.url.strip('/').split('/')[-1],deal_id)
        content_loader.add_xpath('img_urls','//div[@id="content-main"]//img/@src')
        content_loader.add_xpath('video_urls','//div[@id="content"]//div[@class="hentry-container clear"]//iframe/@src')
        # content_loader.add_xpath('publish_user')

        item1=content_loader.load_item()
        return item1