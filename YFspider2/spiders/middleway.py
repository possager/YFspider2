#_*_coding:utf-8_*_
# from scrapy.spiders import CrawlSpider,Rule
from scrapy.spiders import Rule
from scrapy_redis.spiders import RedisCrawlSpider
from scrapy.linkextractor import LinkExtractor
from YFspider2.items import YfspiderspeakItem
# from scrapy.loader import
from YFspider2.othermodule.itemloader_ll import itemloader_ll
from scrapy.loader.processors import Join,TakeFirst,MapCompose
from string import strip
import scrapy
import time
import datetime




class middleway(RedisCrawlSpider):
    name = 'middleway'
    # start_urls=['http://woeser.middle-way.net/']
    redis_key='middleway:urls'
    headers={
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36',
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    }


    rules =  (
        Rule(LinkExtractor(allow='http\:\/\/woeser\.middle\-way\.net\/\d{4}\/\d{1,2}\/[\S|\s]{1,12}\.html',),callback='parse_more',follow=True),
    )


    # def start_requests(self):
    #     for url in self.start_urls:
    #         yield scrapy.Request(url=url,headers=self.headers)



    def parse_more(self,response):
        print 'in parseMore'
        def deal_publish_time(publish_time_list):
            if len(publish_time_list)==3:
                publish_time_str=''
                for time_num in publish_time_list:
                    time_num=str(time_num)
                    if len(time_num)<2:
                        time_num='0'+time_num
                    publish_time_str+=time_num
                publish_time_str+=' 00:00:00'
                return publish_time_str
            else:
                print 'publish_time_wrong'
                return None


        # print response.xpath('#Blog1 > div.blog-posts.hfeed > div > div > div > div.post.hentry > h3').extract
        # print response.url
        loader1=itemloader_ll(item=YfspiderspeakItem(),response=response)
        loader1.add_value('url',response.url)
        loader1.add_value('spider_time',time.time())
        loader1.add_xpath('title','//*[@id="Blog1"]/div/div/div/div/div/h3/text()',TakeFirst(),lambda x:x.strip())
        loader1.add_xpath('content','//div[@class="post-body entry-content"]//text()',lambda x:[i.strip() for i in x],Join())
        loader1.add_value('id',response.url.split('.html')[0].split('.net/')[1].replace('/','-'))
        loader1.add_value('img_urls',response.selector.xpath('//div[@class="post-body entry-content"]//img').re(r'src="(.*?)"'))
        loader1.add_value('publish_time',response.selector.xpath('//h2[@class="date-header"]/span/text()').re(ur'(\d{4})年(\d{1,2})月(\d{1,2})日'),deal_publish_time())

        item=loader1.load_item()
        print item