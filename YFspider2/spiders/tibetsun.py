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
import re




# Re_match=re.compile(r'^https\:\/\/www\.tibetsun\.com/.*?/\d{4}/\d[1,2]/\d{1,2}/\S*')




class tibetsun(RedisCrawlSpider):
    name = 'tibetsun'
    start_urls=['https://www.tibetsun.com/']
    headers={
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36',
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    }


    rules =  (
        Rule(LinkExtractor(allow='^https\:\/\/www\.tibetsun\.com\/.*?\/\d{4}\/\d{1,2}\/\d{1,2}\/\S*',),callback='parse_content',follow=True),
        Rule(LinkExtractor(allow='^https\:\/\/www\.tibetsun\.com.*',),follow=True,)
    )




    def parse_content(self,response):
        print ('in parseMore')


        def deal_publish_time(publish_time_str):
            Re_find_publish_date=re.compile('\S*\/(\d{4})\/(\d{2})\/(\d{2})')
            publish_date_list=Re_find_publish_date.findall(publish_time_str)
            if publish_date_list:
                publish_time_str_tuple=publish_date_list[0]
                return publish_time_str_tuple[0]+'-'+publish_time_str_tuple[1]+'-'+publish_time_str_tuple[2]+' 00:00:00'



        def deal_reply_nodes(reply_nodes=None):
            reply_nodes_list=[]

            def deal_publish_time_inside(publishtime_cmt_list):

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


                if publishtime_cmt_list:
                    day_cmt=str(publishtime_cmt_list[0])
                    mounth_str=str(publishtime_cmt_list[1])
                    year=str(publishtime_cmt_list[2])
                    hours=str(publishtime_cmt_list[3])
                    minute=str(publishtime_cmt_list[4])


                    am_or_pm=str(publishtime_cmt_list[5])
                    if am_or_pm=='pm':
                        hours_2=str(12+int(hours))
                    hours_2 = hours_2 if len(hours_2) > 1 else '0' + hours_2


                    mounth_num=mouth_eng_to_num[mounth_str]

                    return year+'-'+mounth_num+'-'+day_cmt+' '+hours_2+':'+minute+':'+'00'

            if reply_nodes:
                for one_comment in reply_nodes:
                    publish_user_cmt=one_comment.xpath('.//div[contians(@id,"comment")]/div[@class="comment-author"]/span/cite[@class="fn"]/text()').extract()
                    publish_date_cmt=one_comment.xpath('.//span[@class="date"]').re('(\d{1,2}) (\S*) (\d{1,4}) at (\d{1,2})\:(\d{1,2}) (\S{2})')
                    content_cmt=one_comment.xpath('.//div[@class="comment-body"]/p//text()').extract()

                    publish_time_cmt_dealed=deal_publish_time_inside(publish_date_cmt)
                    content_cmt_dealed=Join([x.strip() for x in content_cmt])
                    publish_user_cmt=publish_date_cmt[0] if publish_user_cmt else ''

                    onecmt_dict={
                        'publish_user':publish_user_cmt,
                        'content':content_cmt_dealed,
                        'publish_time':publish_time_cmt_dealed,
                        'parent_id':response.url.split('/')[-1].strip(),
                        'ancestor_id':response.url.split('/')[-1].strip()
                    }
                    reply_nodes_list.append(onecmt_dict)

            return reply_nodes_list



        loader1=ItemLoader(item=YfspiderspeakItem(),response=response)
        loader1.add_value('url',response.url)
        loader1.add_value('spider_time',time.time())
        loader1.add_xpath('title','//div[@id="content"]//h1[@class="entry-title"]/text()',TakeFirst(),lambda x:x.strip())
        loader1.add_xpath('content','//div[@id="content"]//div[@id="post-content"]/p//text()',lambda x:[i.strip() for i in x],Join())
        loader1.add_value('id',response.url.split('/')[-1].strip().split('?')[0])
        loader1.add_xpath('img_urls','//div[@id="content"]/div[contains(@id,"post")]//img/@src')
        loader1.add_value('publish_time',response.url,deal_publish_time)

        loader1.add_value('reply_count',response.selector.xpath('//ol[@class="commentlist"]/li[contains(@class,"comment")]'),lambda x:len(x))
        loader1.add_value('reply_nodes',response.selector.xpath('//ol[@class="commentlist"]/li[contains(@class,"comment")]'),deal_reply_nodes)



        item=loader1.load_item()
        print (item)
        return item