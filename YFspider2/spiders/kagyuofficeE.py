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


def deal_links_to_fallow(link_raw):
    links=link_raw.replace('http://','')
    linksplited= links.strip('/').split('/')
    if len(linksplited)==2:
    # if len(linksplited[1])>10:
        print '跟进链接:',link_raw
        return link_raw



class kagyuofficeE(RedisCrawlSpider):
    name = 'kagyuofficeE'
    start_urls=['www.kagyuoffice.org']
    headers={
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36',
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    }


    rules =  (
        Rule(LinkExtractor(allow=r'http\:\/\/kagyuoffice\.org\/\S*\-\S*.*\/',process_value=deal_links_to_fallow),callback='parse_content',follow=True),
        Rule(LinkExtractor(allow=r'http\:\/\/kagyuoffice\.org\/.*',),follow=True)
    )




    def parse_content(self,response):
        print ('in parseMore')


        def deal_publish_time(publish_time_list=[]):
            if publish_time_list:
                publish_time_str=publish_time_list
            else:
                return '2018-02-01 00:00:00'
            try:
                mounth_str=publish_time_list[0]
                day=publish_time_str[1]
                year=publish_time_list[2]

                mouth_transform = {
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
                mounth_num=mouth_transform[str(mounth_str).strip()]
                if len(str(day).strip()) < 2:
                    day='0'+str(day).strip()
                year=str(year)
                return year+'-'+mounth_num+'-'+day+' 00:00:00'

            except:
                return '2018-02-01 00:00:00'

        def deal_publish_user(publish_user_name):
            if publish_user_name:
                try:
                    return publish_user_name.split(',')[0]
                except:
                    return None



        loader1=ItemLoader(item=YfspiderspeakItem(),response=response)
        loader1.add_value('url',response.url)
        loader1.add_value('spider_time',time.time())
        loader1.add_xpath('title','//article//div[@class="entry-title"]//a[@title]/text()',lambda x:''.join([y for y in x]))
        loader1.add_xpath('content','//article//div[@class="entry-content"]//p//text()',lambda x:[i.strip() for i in x],Join())
        loader1.add_value('id',response.url.strip('/').split('/')[-1])
        loader1.add_xpath('img_urls','//article//div[@class="entry-content"]//img/@src')
        loader1.add_xpath('publish_time',response.xpath('//div[@id="content"]//div[@class="entry-content"]//p[1]//text()').re('(\S*) (\d*), (\d{4})'),deal_publish_time)
        loader1.add_xpath('publish_user',response.xpath('//div[@id="content"]//div[@class="entry-content"]/p[1]/text()').extract_first(default=None),deal_publish_user)



        item=loader1.load_item()
        print (item)
        return item