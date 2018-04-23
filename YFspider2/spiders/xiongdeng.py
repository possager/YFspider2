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
        content_loader.add_xpath('video_urls','//embed/@src')

        item1=content_loader.load_item()

        next_page_url=deal_next_page_url(response)
        if not next_page_url:
            return item1
        else:
            return scrapy.Request(url=next_page_url,meta={'pre_data':item1},headers=self.headers,callback=self.deal_next_page)


    def deal_next_page(self,response):
        datameta=response.meta['pre_data']


        def deal_content_thisPage(contentdata):
            content=''.join(contentdata)
            return content

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


        content_this_page=response.xpath('//div[@class="entry"]/div[@id="entry"]//text()').extract()

        content=deal_content_thisPage(content_this_page)
        datameta['content']+=content


        next_page_url=deal_next_page_url(response)
        if not next_page_url:
            return datameta
        else:
            return scrapy.Request(url=next_page_url,meta={'pre_data':datameta},headers=self.headers,callback=self.deal_next_page)