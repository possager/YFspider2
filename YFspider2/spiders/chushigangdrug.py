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


class dhokhamchushigangdrug(RedisCrawlSpider):
    name = 'chushigangdrug'

    start_urls=['http://www.chushigangdrug.ch/aktuelles/',
                'http://www.chushigangdrug.ch/geschichte/geschichte_hintergrund.php',
                'http://www.chushigangdrug.ch/']

    headers={
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36',
        'Upgrade-Insecure-Requests':'1',
        'Host':'ww.chushigangdrug.ch',
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Referer':'http://www.chushigangdrug.ch/'
    }


    rules = (

        Rule(LinkExtractor(allow=r'www\.chushigangdrug\.ch\/.*', ), callback='parse_content',
             follow=True),
        # Rule(LinkExtractor(allow=))
    )

    def parse_content(self, response):
        def deal_img_urls(img_urls_raw):
            img_urls_list=[]
            for one_img_url_raw in img_urls_raw:
                if 'mages/up' in one_img_url_raw or 'arrow_big_up' in one_img_url_raw:
                    continue
                if 'verein' in response.url:
                    img_url='http://www.chushigangdrug.ch/verein/'+one_img_url_raw.lstrip('.')
                elif 'tanzgruppe' in response.url:
                    img_url='http://www.chushigangdrug.ch/tanzgruppe/'+one_img_url_raw.strip('.')
                elif 'galerie' in response.url:
                    img_url='http://www.chushigangdrug.ch/galerie/'+one_img_url_raw.strip('.')
                else:
                    img_url='http://www.chushigangdrug.ch/'+one_img_url_raw.strip('.')
                img_urls_list.append(img_url)

            return img_urls_list



        print (response.url)
        if response.xpath('//table//table[@class="titel"]//tr/td'):
            content_loader=ItemLoader(response=response,item=YfspiderspeakItem())
            content_loader.add_value('url',response.url)
            content_loader.add_value('spider_time',time.time())
            content_loader.add_value('id',response.url.strip('/').split('/')[-1].replace('.','_'))

            content_loader.add_xpath('title','//table//table[@class="titel"]//tr/td/text()',lambda x:x[0].strip())
            content_loader.add_xpath('content','//td[@valign="top"]//td[@valign and @bgcolor="#FFFFFF"]//text()',Join())
            content_loader.add_value('publish_time','2018-02-01 00:00:00')
            content_loader.add_xpath('img_urls','//td[@valign="top"]//td[@valign and @bgcolor="#FFFFFF"]//img[@width>50]/@src',deal_img_urls)

            item1=content_loader.load_item()
            return item1
        else:
            print ('unknown page')