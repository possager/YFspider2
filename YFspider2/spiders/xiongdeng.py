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
from w3lib.url import urljoin


class tibetsociety(RedisCrawlSpider):
    name = 'xiongdeng'
    # start_urls=['http://www.sherig.org/tb/page/{}/'.format(str(i)) for i in range(1,10)]
    start_urls=['']
    # redis_key = 'xiongdeng:url'

    headers={
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36',
        'Upgrade-Insecure-Requests':'1',
        'Host':'ww.tibetsociety.com',
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Referer':'http://www.xiongdeng.com/'
        # 'Accept-Encoding':'gzip, deflate'
    }
    # def start_requests(self):
    #     for url in self.start_urls:
    #         yield scrapy.Request(url=url,headers=self.headers,callback=self.parse_content)


    rules = (
        # Extract links matching 'category.php' (but not matching 'subsection.php')
        # and follow links from them (since no callback means follow=True by default).
        # Rule(LinkExtractor(allow=r'http\:\/\/www\.sherig\.org\/tb\/\d{4}\/\d{1,2}\/.*?\/$',),callback='parse_content',follow=True),
        #http\:\/\/www\.sherig\.org\/tb\/\d{4}\/\d{1,2}\/[^\\\/\']*?\/\B
        Rule(LinkExtractor(allow=r'http\:\/\/www\.xiongdeng\.com\/\?p\=\d{1,4}', ), callback='parse_content',
             follow=True),

        # Extract links matching 'item.php' and parse them with the spider's method parse_item
        # Rule(LinkExtractor(allow='http://www.sherig.org/tb/page/\d{1,5}/'), follow=True),
    )

    def parse_content(self, response):
        print response.url

        def deal_img_urls(img_urls_raw):
            img_url_list=[]
            for one_img_url in img_urls_raw:
                if 'paypal_cn' or 'pixel.gif' in one_img_url:
                    continue
                if 'http' and 'www' not in one_img_url:
                    url_img=urljoin('http://www.tibetanyouthcongress.org/',one_img_url)
                    img_url_list.append(url_img)

            return img_url_list


        content_loader=itemloader_ll(response=response,item=YfspiderspeakItem())
        content_loader.add_value('url',response.url)
        content_loader.add_value('spider_time',time.time())
        content_loader.add_value('id',response.url.strip('/').split('=')[1])

        content_loader.add_xpath('title','//div[@id="content"]//div[@class="entry_title_box"]//div[@class="entry_title"]//text()')
        content_loader.add_xpath('content','//div[@class="entry"]/div[@id="entry"]//text()',Join())
        content_loader.add_value('publish_time','1111-11-11 11:11:11')
        content_loader.add_value('img_urls','//div[@class="entry"]/div[@id="entry"]//@src',deal_img_urls)

        item1=content_loader.load_item()
        return item1