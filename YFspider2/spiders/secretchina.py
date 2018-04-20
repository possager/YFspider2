#_*_coding:utf-8_*_
# from scrapy.spiders import CrawlSpider,Rule
from scrapy.spiders import Rule
from scrapy_redis.spiders import RedisCrawlSpider
from scrapy.linkextractor import LinkExtractor
from YFspider2.items import YfspiderspeakItem
# from scrapy.loader import
from YFspider2.othermodule.itemloader_ll import itemloader_ll
from scrapy.loader import ItemLoader
from scrapy.loader.processors import Join,TakeFirst,MapCompose

import scrapy
import time
import datetime




class middleway(RedisCrawlSpider):
    name = 'secretchina'
    start_urls=['https://www.secretchina.com/']
    # redis_key='middleway:urls'
    headers={
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36',
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    }


    rules =  (
        Rule(LinkExtractor(allow='www\.secretchina\.com\/news\/\w{1,2}\/\d{1,4}\/\d{1,2}\/\d{1,2}\/\d*\.html',),callback='parse_content',follow=True),
    )


    # def start_requests(self):
    #     for url in self.start_urls:
    #         yield scrapy.Request(url=url,headers=self.headers)



    def parse_content(self,response):

        def deal_publish_time(publish_time_raw):
            publish_time_str=publish_time_raw.pop().strip()
            if len(publish_time_str)==16:
                publish_time_str1=publish_time_str+':00'
            else:
                publish_time_str1=publish_time_str
            return publish_time_str1

        def deal_content(content_list_raw):
            content_str=''
            for one_content in content_list_raw:
                content_str+=one_content.strip()
            return content_str

        def deal_img_urls(img_urls_raw):
            img_url_list=[]
            for one_img_url in img_urls_raw:
                if 'http' not in one_img_url:
                    one_img_url_str='http:'+one_img_url
                    img_url_list.append(one_img_url_str)
            return img_url_list

        def deal_publish_user(publish_user_raw):
            if publish_user_raw:
                publish_user_raw=publish_user_raw[0].strip()
                publish_user_list=publish_user_raw.split(' ')
                return publish_user_list

        print ('in parseMore')
        loader1=itemloader_ll(item=YfspiderspeakItem(),response=response)
        loader1.add_value('url',response.url)
        loader1.add_value('spider_time',time.time())
        loader1.add_value('id',response.url.split('/')[-1].split('.')[0])
        loader1.add_xpath('title','//div[@class="col-left"]/div/center/h1/text()',lambda x:x[0].strip())
        loader1.add_value('publish_time',response.xpath('//div[@class="col-left"]/div/div[@class="fontsize"]/div/h2').re('(\d{4}\-\d{2}\-\d{2} \d{2}\:\d{2})'),deal_publish_time)
        loader1.add_xpath('content','//div[@class="article"]/div[@class="article_right"]/p/text()',deal_content)
        loader1.add_value('img_urls',response.xpath('//div[@class="article"]//img/@src').extract(),deal_img_urls)
        loader1.add_value('publish_user',response.xpath('//div[@class="col-left"]//div[@class="fontsize"]').re(r'作者：(.*)\n?'),deal_publish_user)

        item1=loader1.load_item()
        return item1