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
import re




class minghui(RedisCrawlSpider):
    name = 'minghui'
    start_urls=['http://www.minghui.org/']
    # redis_key='middleway:urls'
    headers={
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36',
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    }


    rules =  (
        Rule(LinkExtractor(allow='http\:\/\/www\.minghui\.org\/mh\/articles\/\d{4}/\d{1,2}/\d{1,2}/[^\d]{1,4}.*?.html',),callback='parse_content',follow=True),
        Rule(LinkExtractor(allow='http\:\/\/www\.minghui\.org\/.*?'),follow=True)
    )






    def parse_content(self,response):
        print ('in parseMore')


        def deal_publish_time(publish_time_str):
            if not publish_time_str:
                print ('time is None')
                return None
            Re_find_publish_date=re.compile('articles\/(\d{4})\/(\d{1,2})\/(\d{1,2})')
            publish_date_list=Re_find_publish_date.findall(publish_time_str)
            date_str_list=[]
            for datestr in publish_date_list[0]:#findall找到的是一个包含tuple的list。找到的内容放到tuple中。
                if len(datestr)<2:
                    datestr1='0'+str(datestr)
                    date_str_list.append(datestr1)
                else:
                    date_str_list.append(str(datestr))
            publish_time=date_str_list[0]+'-'+date_str_list[1]+'-'+date_str_list[2]+' 00:00:00'
            return publish_time


        loader1=ItemLoader(item=YfspiderspeakItem(),response=response)
        loader1.add_value('url',response.url)
        loader1.add_value('spider_time',time.time())
        loader1.add_xpath('title','//div[@id="master_container"]//div[@class="ar_articleTitle"]/h1/text()',TakeFirst(),lambda x:x.strip())
        loader1.add_xpath('content','//div[@id="master_container"]//div[@class="ar_articleContent"]//text()',lambda x:[i.strip() for i in x],Join())
        loader1.add_value('id',response.url.split('-')[-1].split('.')[0].strip())
        loader1.add_xpath('img_urls','//div[@id="master_container"]//div[@id="ar_article1"]//img/@src')
        loader1.add_value('publish_time',response.url,deal_publish_time)
        # loader1.add_value('publish_user','degewa')
        # loader1.add_value('reply_count',response.selector.xpath('//*[@id="comments"]/h4/text()').re(ur'(\d{1,2}).*条评论'),lambda x:x[0] if x else 0)
        # loader1.add_value('reply_nodes',response.selector.re(ur'var items \= (\[.*?\])\;'),deal_reply_nodes)



        item=loader1.load_item()
        print (item)
        return item