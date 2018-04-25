#_*_coding:utf-8_*_
import scrapy
# from scrapy.spider import Spider
from scrapy.spider import CrawlSpider
from scrapy_redis.spiders import RedisCrawlSpider
from YFspider2.items import YfspiderspeakItem
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from YFspider2.othermodule.itemloader_ll import itemloader_ll
from scrapy.loader.processors import Join,MapCompose,Compose,TakeFirst
import time
import hashlib
from w3lib.url import urljoin


class tibetsociety(RedisCrawlSpider):
    name = 'xiongdeng'

    headers={
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36',
        'Upgrade-Insecure-Requests':'1',
        'Host':'ww.tibetsociety.com',
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Referer':'http://www.xiongdeng.com/'

    }



    rules = (

        Rule(LinkExtractor(allow=r'http\:\/\/www\.xiongdeng\.com\/\?p\=\d{1,4}', ), callback='parse_content',
             follow=True),
        Rule(LinkExtractor(allow=r'http\:\/\/www\.xiongdeng\.com\/.*', ), follow=True),
    )

    def parse_content(self, response):
        print (response.url)

        def deal_img_urls(img_urls_raw):
            img_url_list=[]
            for one_img_url in img_urls_raw:
                if 'paypal_cn' or 'pixel.gif' in one_img_url:
                    continue
                if 'http' and 'www' not in one_img_url:
                    url_img=urljoin('http://www.tibetanyouthcongress.org/',one_img_url)
                    img_url_list.append(url_img)

            return img_url_list

        def deal_next_page_url(response):
            next_page_url_list=response.xpath('//p[@class="pages"]/a')
            if '&page=' in response.url:
                try:
                    page_now_split=int(response.url.split('&page='))
                    page_now_int=str(page_now_split[1])
                    next_page_url=page_now_split[0]+'&page='+str(page_now_int+1)
                except:
                    page_now_int=1
                    next_page_url=response.url.split('&page')[0]+str(page_now_int+1)


            else:
                page_now_int=1
                next_page_url=response.url+'&page='+str(page_now_int+1)

            if next_page_url_list:
                if page_now_int<len(next_page_url_list):
                    return next_page_url
                else:
                    return None
            else:
                return None


        content_loader=itemloader_ll(response=response,item=YfspiderspeakItem())
        content_loader.add_value('url',response.url)
        content_loader.add_value('spider_time',time.time())
        content_loader.add_value('id',response.url.strip('/').split('=')[1])

        content_loader.add_xpath('title','//div[@id="content"]//div[@class="entry_title_box"]//div[@class="entry_title"]//text()')
        content_loader.add_xpath('content','//div[@class="entry"]/div[@id="entry"]//text()',Join())
        content_loader.add_value('publish_time','1111-11-11 11:11:11')
        content_loader.add_value('img_urls','//div[@class="entry"]/div[@id="entry"]//@src',deal_img_urls)

        item1=content_loader.load_item()

        next_page_url=deal_next_page_url(response)
        if next_page_url:
            return item1

