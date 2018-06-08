#_*_coding:utf-8_*_
# from scrapy.spiders import CrawlSpider,Rule
from scrapy.spiders import Rule
from scrapy_redis.spiders import RedisCrawlSpider
from scrapy.linkextractors import LinkExtractor
from YFspider2.items import YfspiderspeakItem
from scrapy.loader import ItemLoader
from scrapy.loader.processors import Join,TakeFirst,MapCompose

import scrapy
import time
import datetime
import re





class phayul(RedisCrawlSpider):
    name = 'phayul'
    start_urls=['www.phayul.com']
    headers={
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36',
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    }


    rules =  (
        Rule(LinkExtractor(allow=r'http\:\/\/www\.phayul\.com\/news\/article\.aspx\?id\=\d*&article\=.*',),callback='parse_content',follow=True),
        Rule(LinkExtractor(allow=r'http\:\/\/www\.phayul\.com\/.*',),follow=True)
    )




    def parse_content(self,response):
        print ('in parseMore')


        def deal_publish_time(publish_time_raw):
            try:
                Re_find_time = re.compile('\S*\, (\S*?) (\d{2})\, (\d{4}) (\d{2}\:\d{2})')
                publish_time_finded=Re_find_time.findall(publish_time_raw)[0]
                mounth=publish_time_finded[0]
                day=publish_time_finded[1]
                year=publish_time_finded[2]
                hour_and_minute=publish_time_finded[3]

                mouth_eng_to_num = {
                    'January': '01',
                    'February': '02',
                    'March': '03',
                    'April': '04',
                    'May': '05',
                    'June': '06',
                    'July': '07',
                    'August': '08',
                    'September': '09',
                    'October': '10',
                    'November': '11',
                    'December': '12'
                }

                mounth_num=mouth_eng_to_num[str(mounth)]

                return str(year)+'-'+mounth_num+'-'+str(day)+' 00:00:00'
            except:
                return '2018-05-10 00:00:00'


        def deal_img_urls(img_urls_raw):
            img_list=[]
            for one_img in img_urls_raw:
                if 'www.phayul.com' not in one_img:
                    one_img='http://www.phayul.com'+str(one_img)
                    img_list.append(one_img)
                else:
                    img_list.append(one_img)

            return img_list



        loader1=ItemLoader(item=YfspiderspeakItem(),response=response)
        loader1.add_value('url',response.url)
        loader1.add_value('spider_time',time.time())
        loader1.add_xpath('title','//td[@class="bodyTable"]//table[@id="_ctl1_newsTable"]//td/span//text()',lambda x:''.join([y for y in x]))
        loader1.add_xpath('content','//td[@class="bodyTable"]//td[@class="newsStory"]//text()',lambda x:[i.strip() for i in x],Join())
        loader1.add_value('id',response.url.split('id=')[-1].split('&')[0])
        loader1.add_xpath('img_urls','//td[@class="bodyTable"]//td[@class="newsStory"]//img/@src',deal_img_urls)
        loader1.add_xpath('publish_time','//td[@class="bodyTable"]//span[@class="newsDate"]//text()',deal_publish_time)
        # loader1.add_xpath('publish_user','//article//time[@class="published"]/a[@class="fn"]/text()')



        item=loader1.load_item()
        print (item)
        return item