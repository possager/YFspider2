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


class dhokhamchushigangdrug(RedisCrawlSpider):
    name = 'chushigangdrug'
    # start_urls=['http://www.sherig.org/tb/page/{}/'.format(str(i)) for i in range(1,10)]
    start_urls=['http://www.chushigangdrug.ch/aktuelles/',
                'http://www.chushigangdrug.ch/geschichte/geschichte_hintergrund.php',
                'http://www.chushigangdrug.ch/']
    # redis_key = 'chushigangdrug:url'

    headers={
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36',
        'Upgrade-Insecure-Requests':'1',
        'Host':'ww.chushigangdrug.ch',
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Referer':'http://www.chushigangdrug.ch/'
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
        Rule(LinkExtractor(allow=r'www\.chushigangdrug\.ch\/.*?', ), callback='parse_content',
             follow=True),

        # Extract links matching 'item.php' and parse them with the spider's method parse_item
        # Rule(LinkExtractor(allow='http://www.sherig.org/tb/page/\d{1,5}/'), follow=True),
    )

    def parse_content(self, response):
        def deal_img_urls(img_urls_raw):
            img_urls_list=[]
            for one_img_url_raw in img_urls_raw:
                if 'mages/up' or 'arrow_big_up' in one_img_url_raw:
                    continue
                img_url=urljoin('http://www.chushigangdrug.ch/',one_img_url_raw.lstrip('.'))
                img_urls_list.append(img_url)

            return img_urls_list



        print (response.url)
        if response.xpath('//table//table[@class="titel"]//tr/td'):
            content_loader=itemloader_ll(response=response,item=YfspiderspeakItem())
            content_loader.add_value('url',response.url)
            content_loader.add_value('spider_time',time.time())
            content_loader.add_value('id',response.url.strip('/').split('/')[-1].replace('.','_'))

            content_loader.add_xpath('title','//table//table[@class="titel"]//tr/td/text()',lambda x:x[0].strip())
            content_loader.add_xpath('content','//td[@class="inhalt"]//text()|//table[@class="inhalt"]//text()',Join())
            content_loader.add_value('publish_time','1111-11-11 11:11:11')
            content_loader.add_xpath('img_urls','//td[@class="inhalt"]//img/@src|//table[@class="inhalt"]//img/@src',deal_img_urls)

            item1=content_loader.load_item()
            return item1
        else:
            print ('unknown page')