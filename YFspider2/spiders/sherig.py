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



class sherig(CrawlSpider):
    name = 'sherig'
    # start_urls=['http://www.sherig.org/tb/page/{}/'.format(str(i)) for i in range(1,10)]
    start_urls=['http://www.sherig.org/tb/']

    rules = (
        # Extract links matching 'category.php' (but not matching 'subsection.php')
        # and follow links from them (since no callback means follow=True by default).
        # Rule(LinkExtractor(allow=r'http\:\/\/www\.sherig\.org\/tb\/\d{4}\/\d{1,2}\/.*?\/$',),callback='parse_content',follow=True),
        #http\:\/\/www\.sherig\.org\/tb\/\d{4}\/\d{1,2}\/[^\\\/\']*?\/\B
        Rule(LinkExtractor(allow=r'http\:\/\/www\.sherig\.org\/tb\/\d{4}\/\d{1,2}\/[^\\\/\']*?\/\B', ), callback='parse_content',
             follow=True),

        # Extract links matching 'item.php' and parse them with the spider's method parse_item
        Rule(LinkExtractor(allow='http://www.sherig.org/tb/page/\d{1,5}/'), follow=True),
    )

    def parse_content(self, response):
        def deal_publish_time(publish_time_list):
            year=publish_time_list[0]
            mounth=publish_time_list[1]
            day=publish_time_list[2]

            if len(mounth)<2:
                mounth='0'+mounth
            if len(day)<2:
                day='0'+day
            publish_time=year+'-'+mounth+'-'+day+' 00:00:00'
            return publish_time

        loaders1=itemloader_ll(response=response,item=YfspiderspeakItem())
        loaders1.add_value('url',response.url)
        loaders1.add_value('spider_time',time.time())
        loaders1.add_xpath('title','//h1[@class="entry-title"]/text()')
        loaders1.add_value('publish_time',response.xpath('//span[@class="entry-date"]').re(r'(\d{4}).*?(\d).*?(\d)'),deal_publish_time)
        loaders1.add_xpath('content','//div[contains(@id,"post")]/div[@class="entry-content"]//text()',Join())
        loaders1.add_value('img_urls',response.xpath('//div[contains(@id,"post")]/div[@class="entry-content"]').re(r'href="([\S]*?\.jpg)"'))
        loaders1.add_xpath('id','//div[@id="content"]/div[contains(@id,"post")]/@id')


        item1=loaders1.load_item()
        print item1
        return item1