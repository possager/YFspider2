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




class khabdha(RedisCrawlSpider):
    name = 'khabdha'
    start_urls=['http://www.khabdha.org/']
    # redis_key='middleway:urls'
    headers={
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36',
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    }


    rules =  (
        Rule(LinkExtractor(allow='http\:\/\/www\.khabdha\.org\/\?p\=\d*',),callback='parse_content',follow=True),
        Rule(LinkExtractor(allow='http\:\/\/www\.khabdha\.org'),follow=True)
    )


    # def start_requests(self):
    #     for url in self.start_urls:
    #         yield scrapy.Request(url=url,headers=self.headers)



    def parse_content(self,response):
        print ('in parseMore')

        def deal_publish_time(publish_time_raw_list):
            mouth_eng_to_num = {
                'Jan': '01',
                'Feb': '02',
                'Mar': '03',
                'Apr': '04',
                'May': '05',
                'Jun': '06',
                'Jul': '07',
                'Aug': '08',
                'Sep': '09',
                'Oct': '10',
                'Nov': '11',
                'Dec': '12'
            }


            if publish_time_raw_list:
                publish_year=publish_time_raw_list[0]
                publish_mounth=str(publish_time_raw_list[1])
                publish_day=str(publish_time_raw_list[2])

                if len(publish_day)<2:
                    publish_day='0'+str(publish_day)
                publish_mounth_num=mouth_eng_to_num[publish_mounth]

                publish_time=publish_year+'-'+publish_mounth_num+'-'+publish_day+' 00:00:00'

                return publish_time

        def deal_reply_nodes(reply_nodes_raw_list):

            def deal_publish_time_inside(publish_time_raw):

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

                if publish_time_raw:
                    Mouth_str= str(publish_time_raw[0])
                    day=str(publish_time_raw[1])
                    year=str(publish_time_raw[2])
                    hourse=str(publish_time_raw[3])
                    minute=str(publish_time_raw[4])
                    am_or_pm=str(publish_time_raw[5])

                    if am_or_pm=='pm':
                        hourse=str(12+int(hourse))

                    publish_time_rpy=year+'-'+mouth_eng_to_num[Mouth_str]+'-'+day+' '+hourse+':'+minute+':00'
                    return publish_time_rpy



            reply_nodes_list=[]


            for one_reply_node in reply_nodes_raw_list:
                publish_user=one_reply_node.xpath('.//strong/text()').extract()
                publish_time=one_reply_node.xpath('.//small[@class="commentmetadata"]/a').re('(\S*) (\d{1,2})th, (\d{4})[\s|\S]*(\d{1,2})\:(\d{1,2}) (\S{1,2})')
                content=one_reply_node.xpath('.//p/text()').extract()

                publish_time_dealed=deal_publish_time_inside(publish_time)
                this_reply_node={
                    'publish_user':publish_user[0].strip() if publish_user else '',
                    'publish_time':publish_time_dealed,
                    'content':content[0].strip() if content else '',
                    'parent_id':response.url.split('=')[1],
                    'ancestor_id':response.url.split('=')[1]
                }
                reply_nodes_list.append(this_reply_node)
            return reply_nodes_list





        loader1=ItemLoader(item=YfspiderspeakItem(),response=response)
        loader1.add_value('url',response.url)
        loader1.add_value('spider_time',time.time())
        loader1.add_xpath('title','//div[@id="page"]//div[@class="post"]/h2/a/text()',TakeFirst(),lambda x:x.strip())
        loader1.add_xpath('content','//div[@id="page"]//div[@class="post"]/div[@class="entry"]/p/text()',lambda x:[i.strip() for i in x],Join())
        loader1.add_value('id',response.url.split('=')[1])
        loader1.add_xpath('img_urls','//div[@id="page"]//div[@class="post"]/div[@class="entry"]/img/@src')
        loader1.add_value('publish_time',response.xpath('//div[@id="page"]//div[@class="post"]//p[@class="postmetadata"]/span').re('(\d{4}) (\S*) (\d{1,2})'),deal_publish_time)
        # loader1.add_value('publish_user','degewa')
        loader1.add_xpath('reply_count','//ol[@class="commentlist"]/li[@id]',lambda x:len(x))
        loader1.add_value('reply_nodes',response.xpath('//ol[@class="commentlist"]/li[@id]'),deal_reply_nodes)
        loader1.add_xpath('video_urls','//div[@id="page"]//div[@class="post"]/div[@class="entry"]/p/iframe/@src')




        item=loader1.load_item()
        print (item)
        return item