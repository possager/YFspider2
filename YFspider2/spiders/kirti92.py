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




class kirti92(RedisCrawlSpider):
    name = 'kirti92'
    start_urls=['http://www.kirti92.org/']
    # redis_key='middleway:urls'
    headers={
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36',
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    }


    rules =  (
        Rule(LinkExtractor(allow='http\:\/\/www\.kirti92\.org\/index\.php\/\d{4}\-\d{1,2}\-\d{1,2}\-\d{1,2}\-\d{1,2}\-\d{1,2}\/\d*\-\d{4}\-\d{1,2}\-\d{1,2}\-\d{1,2}\-\d{1,2}\-\d{1,2}',),callback='parse_content',follow=True),
        Rule(LinkExtractor(allow='http\:\/\/www\.kirti92\.org'),follow=True)
    )


    # def start_requests(self):
    #     for url in self.start_urls:
    #         yield scrapy.Request(url=url,headers=self.headers)



    def parse_content(self,response):
        print ('in parseMore')


        def deal_publish_time(publish_url_raw):
            publish_time=publish_url_raw.split('/')[-1]
            publish_time_split=publish_time.split('-')
            publish_time_dealed=publish_time_split[1]+'-'+publish_time_split[2]+'-'+publish_time_split[3]+' '+publish_time_split[4]+':'+publish_time_split[5]+':'+publish_time_split[6]

            return publish_time_dealed

        def deal_img_urls(img_urls_raw):
            img_urls=[]
            if img_urls_raw:
                for one_img_url in img_urls_raw:
                    if 'www.kirti92.org' not in one_img_url:
                        img_urls.append('http://www.kirti92.org'+one_img_url)
                    else:
                        img_urls.append(one_img_url)
            return img_urls


        loader1=ItemLoader(item=YfspiderspeakItem(),response=response)
        loader1.add_value('url',response.url)
        loader1.add_value('spider_time',time.time())
        loader1.add_xpath('title','//div[@id="wrapper"]//h2/a/text()',TakeFirst(),lambda x:x.strip())
        loader1.add_xpath('content','//div[@id="centercontent_bg"]//div[@class="item-page"]/p//text()',lambda x:[i.strip() for i in x],Join())
        loader1.add_value('id',response.url.strip('/').split('/')[-1].split('.')[0].strip())
        loader1.add_xpath('img_urls','//div[@id="centercontent_bg"]//div[@class="item-page"]//img/@src',deal_img_urls)
        loader1.add_value('publish_time',response.url,deal_publish_time)
        # loader1.add_value('publish_user','degewa')
        # loader1.add_value('reply_count',response.selector.xpath('//*[@id="comments"]/h4/text()').re(ur'(\d{1,2}).*条评论'),lambda x:x[0] if x else 0)
        # loader1.add_value('reply_nodes',response.selector.re(ur'var items \= (\[.*?\])\;'),deal_reply_nodes)



        item=loader1.load_item()
        print (item)
        return item