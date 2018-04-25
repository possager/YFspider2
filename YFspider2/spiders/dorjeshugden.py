#_*_coding:utf-8_*_
# from scrapy.spiders import CrawlSpider,Rule

'''
    @File        dorjeshugden.py
    @Author      LiangLiang
    @Company     silence
    @Target_web_name_CH     多杰雄登
'''








from scrapy.spiders import Rule
from scrapy_redis.spiders import RedisCrawlSpider
from scrapy.linkextractors import LinkExtractor
from YFspider2.items import YfspiderspeakItem
# from scrapy.loader import
from YFspider2.othermodule.itemloader_ll import itemloader_ll
from scrapy.loader import ItemLoader
from scrapy.loader.processors import Join,TakeFirst,MapCompose,Compose

import scrapy
import time
import datetime









class dorjeshugden(RedisCrawlSpider):




    name = 'dorjeshugden'
    start_urls=['http://www.dorjeshugden.com/']
    # redis_key='middleway:urls'
    headers={
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36',
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    }


    rules =  (
        Rule(LinkExtractor(allow='http\:\/\/www\.dorjeshugden\.com\/all\-articles\/.*?\/',),callback='parse_content',follow=True),
        Rule(LinkExtractor(allow='http\:\/\/www\.dorjeshugden\.com\/.*'),follow=True)
    )



    def parse_content(self,response):
        print ('in parseMore')


        def deal_publish_time(publish_time_list=[]):
            mouth_eng_to_num = {
                'January': '01',
                'February': '02',
                'March': '03',
                'April ': '04',
                'May': '05',
                'June': '06',
                'July': '07',
                'August': '08',
                'September': '09',
                'October': '10',
                'November': '11',
                'December': '12'
            }
            if publish_time_list:
                mouth_eng_str = publish_time_list[0]
                day = publish_time_list[1]
                year = publish_time_list[2]

                mouth_num = mouth_eng_to_num[str(mouth_eng_str)]

                if len(day)<2:
                    day='0'+day

                return year + '-' + mouth_num + '-' + day + ' 00:00:00'

            else:
                print ('publish_time_wrong')
                return None
        def deal_reply_nodes(reply_nodes=None):
            reply_nodes_list=[]

            mouth_eng_to_num = {
                'January': '01',
                'February': '02',
                'March': '03',
                'April ': '04',
                'May': '05',
                'June': '06',
                'July': '07',
                'August': '08',
                'September': '09',
                'October': '10',
                'November': '11',
                'December': '12'
            }

            def deal_publishtime_inside(publishtime_list):
                mouth_eng_str=publishtime_list[0]
                day=publishtime_list[1]
                year=publishtime_list[2]

                mouth_num=mouth_eng_to_num[str(mouth_eng_str)]

                return year+'-'+mouth_num+'-'+day+' 00:00:00'


            for one_reply_node in reply_nodes:
                publish_time_raw=one_reply_node.xpath('.//div[contains(@class,"comment")]//div[contains(@class,"comment-meta")]//text()').re('(\S*) (\d{1,2})\, (\d{4})')
                publish_user=one_reply_node.xpath('.//div[contains(@class,"comment")]//div[contains(@class,"comment-meta")]/p[contains(@class,"comment-author")]/text()').extract()
                content=one_reply_node.xpath('.//div[contains(@class,"comment")]//div[contains(@class,"comment-text")]//text()').extract()
                img_urls=one_reply_node.xpath('.//div[contains(@class,"comment")]//div[contains(@class,"comment-text")]//img/@src').extract()
                id=one_reply_node.xpath('./@id').extract()#li[contains(@id,"li-comment")]
                parent_id=response.url.strip('/').split('/')[-1]
                ancestor_id=response.url.strip('/').split('/')[-1]

                one_reply_dict={
                    'publish_time':deal_publishtime_inside(publish_time_raw),
                    'publish_user':publish_user,
                    'content':Compose([one_content.strip() for one_content in content],Join()),
                    'img_urls':img_urls,
                    'id':id,
                    'parent_id':parent_id,
                    'ancestor_id':ancestor_id
                }
                reply_nodes_list.append(one_reply_dict)
            return reply_nodes_list



        loader1=ItemLoader(item=YfspiderspeakItem(),response=response)
        loader1.add_value('url',response.url)
        loader1.add_value('spider_time',time.time())
        loader1.add_xpath('title','//div[@id="content"]//div[@class="hentry-meta"]/h1/text()',TakeFirst(),lambda x:x.strip())
        loader1.add_xpath('content','//div[@id="content"]//div[@class="hentry-content clear"]//text()',lambda x:[i.strip() for i in x],Join())
        loader1.add_value('id',response.url.strip('/').split('/')[-1])
        loader1.add_xpath('img_urls','//div[@id="content"]//div[@class="hentry-content clear"]//img/@src')
        loader1.add_value('publish_time',response.xpath('//div[@id="content"]//p[@class="hentry-meta-data"]/text()').re('(\S*) (\d{1,2})\, (\d{4})'),deal_publish_time)
        # loader1.add_value('publish_user','degewa')
        loader1.add_xpath('reply_count','//div[@id="comments"]//ol[@class="commentlist"]/li[contains(@id,"li-comment")]',lambda x:len(x))
        loader1.add_value('reply_nodes',response.xpath('//div[@id="comments"]//ol[@class="commentlist"]/li[contains(@id,"li-comment")]'),deal_reply_nodes)



        item=loader1.load_item()
        print (item)
        return item