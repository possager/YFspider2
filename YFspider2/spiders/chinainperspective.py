#_*_coding:utf-8_*_
# from scrapy.spiders import CrawlSpider,Rule
from scrapy.spiders import Rule
from scrapy_redis.spiders import RedisCrawlSpider
from scrapy.linkextractors import LinkExtractor
from YFspider2.items import YfspiderspeakItem
# from scrapy.loader import
from YFspider2.othermodule.itemloader_ll import itemloader_ll
from scrapy.loader import ItemLoader
from scrapy.loader.processors import Join,TakeFirst,MapCompose

import scrapy
import time
import datetime




class chinainperspective(RedisCrawlSpider):
    name = 'chinainperspective'
    start_urls=['http://woeser.middle-way.net/']
    # redis_key='middleway:urls'
    headers={
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36',
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    }


    rules =  (
        Rule(LinkExtractor(allow='http\:\/\/chinainperspective\.com\/ArtShow\.aspx\?AID\=\d*',),callback='parse_content',follow=True),
        Rule(LinkExtractor(allow='http\:\/\/chinainperspective\.com\/.*',),follow=True)
    )






    def parse_content(self,response):
        print ('in parseMore')


        def deal_publish_time(publish_time_list=[]):
            if publish_time_list:
                year=str(publish_time_list[2]).strip()
                day=str(publish_time_list[1]).strip()
                mounth=str(publish_time_list[0]).strip()

                mouth_eng_to_num={
                    'January':'01',
                    'February':'02',
                    'March':'03',
                    'April':'04',
                    'May':'05',
                    'June':'06',
                    'July':'07',
                    'August':'08',
                    'September':'09',
                    'October':'10',
                    'November':'11',
                    'December':'12'
                }

                moun_num=mouth_eng_to_num[mounth]

                if len(day)<2:
                    day='0'+day

                publish_time=year+'-'+moun_num+'-'+day+' 00:00:00'
                return publish_time
            else:
                return None
        def deal_publish_user(publish_user_raw):
            if publish_user_raw:
                publish_user_raw_str=publish_user_raw.pop()
                publish_user_raw_str=publish_user_raw_str.replace(u'作者：',u'')

                publish_user_list=publish_user_raw_str.split(' ')
                publish_user_list_dealed=[]
                for one_publish_user in publish_user_list:
                    publish_used_deal=one_publish_user.strip()
                    if publish_used_deal:
                        publish_user_list_dealed.append(publish_used_deal)
                return publish_user_list_dealed


            else:
                return None
        def deal_img_urls(img_urls_raw):
            img_urls_dealed=[]
            for oneimg in img_urls_raw:
                if 'chinainperspective' not in oneimg:
                    oneimg='http://chinainperspective.com'+oneimg
                img_urls_dealed.append(oneimg)
            return img_urls_dealed



        loader1=ItemLoader(item=YfspiderspeakItem(),response=response)
        loader1.add_value('url',response.url)
        loader1.add_value('spider_time',time.time())
        loader1.add_xpath('title','//span[@id="labArticle_Name"]/text()',TakeFirst(),lambda x:x.strip())
        loader1.add_xpath('content','//div[@id="divContent"]//text()',lambda x:[i.strip() for i in x],Join())
        loader1.add_value('id',response.url.split('=')[1])
        loader1.add_value('img_urls',response.selector.xpath('//div[@id="divContent"]//img/@src').extract(),deal_img_urls)
        loader1.add_value('publish_time',response.xpath('//span[@id="labResource"]').re(ur'\, (\w*) (\d{1,2}).*(\d{4})'),deal_publish_time)
        loader1.add_xpath('publish_user','//span[@id="labAuthor"]/text()',deal_publish_user)
        loader1.add_xpath('video_urls','//div[@id="divContent"]//iframe/@src')
        # loader1.add_value('reply_count',response.selector.xpath('//*[@id="comments"]/h4/text()').re(ur'(\d{1,2}).*条评论'),lambda x:x[0] if x else 0)
        # loader1.add_value('reply_nodes',response.selector.re(ur'var items \= (\[.*?\])\;'),)



        item=loader1.load_item()
        print (item)
        return item