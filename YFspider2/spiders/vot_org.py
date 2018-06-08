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
        print '跟进链接:',link_raw
        return link_raw



class vot_org(RedisCrawlSpider):
    name = 'vot_org'
    start_urls=['http://www.vot.org/']
    headers={
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36',
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    }


    rules =  (
        Rule(LinkExtractor(allow=r'http\:\/\/www\.vot\.org\/.*\/',process_value=deal_links_to_fallow),callback='parse_content',follow=True),
        Rule(LinkExtractor(allow=r'http\:\/\/www\.vot\.org\/.*',),follow=True)
    )




    def parse_content(self,response):
        print ('in parseMore')

        title=response.xpath('//div[@class="wrap container"]//article//h1[@class="entry-title"]').extract()
        if not title:
            return


        def deal_publish_time(publish_time_list=[]):
            date_dict = {}
            if publish_time_list:
                publish_time_str=''.join(publish_time_list)
            else:
                return '2018-02-01 00:00:00'
            try:
                zangwendict3 = {
                    u"༧": u"7",
                    u"༦": u"6",
                    u"༥": u"5",
                    u"༤": u"4",
                    u"༣": u"3",
                    u"༢": u"2",
                    u"༡": u"1",
                    u"༠": u"0",
                    u"༩": u"9",
                    u"༨": u"8"
                }
                for onechar in zangwendict3.keys():
                    if onechar in publish_time_str:
                        print '-'
                        date_z = zangwendict3[onechar]
                        date_index = publish_time_str.index(onechar, 0, len(publish_time_str))
                        date_dict.update({date_index: date_z})
                        publish_time_str = publish_time_str.replace(onechar, zangwendict3[onechar],1)
                sortdict = sorted(date_dict.items(), key=lambda item: item[0])

                lastindex = sortdict[0][0]
                thisindex = sortdict[0][0]
                date_list = ['', '', '']
                date_list_index = 0

                for onesortdict in sortdict:
                    thisindex = onesortdict[0]
                    if thisindex - lastindex < 2:
                        date_list[date_list_index] += onesortdict[1]
                    else:
                        date_list_index += 1
                        date_list[date_list_index] += onesortdict[1]
                    lastindex = thisindex


                if len(date_list[0])!=4:
                    return '2018-02-01 00:00:00'
                if len(date_list[1])>2:
                    return '2018-02-01 00:00:00'
                if len(date_list[2])>2:
                    return '2018-02-01 00:00:00'
                if len(date_list[1])<2:
                    if len(date_list[1])<1:
                        date_dict[1]='1'
                    date_list[1]='0'+date_list[1]
                if len(date_list[2])<2:
                    if len(date_dict[2])<1:
                        date_dict[2]='1'
                    date_list[2]='0'+date_list[2]

                return date_list[0]+'-'+date_list[1]+'-'+date_list[2]+' 00:00:00'



            except:
                return '2018-02-01 00:00:00'



        loader1=ItemLoader(item=YfspiderspeakItem(),response=response)
        loader1.add_value('url',response.url)
        loader1.add_value('spider_time',time.time())
        loader1.add_xpath('title','//div[@class="wrap container"]//article//h1[@class="entry-title"]/text()',lambda x:''.join([y for y in x]))
        loader1.add_xpath('content','//div[@class="wrap container"]//article//div[@class="entry-content"]//text()',lambda x:[i.strip() for i in x],Join())
        loader1.add_value('id',response.url.strip('/').split('/')[-1])
        loader1.add_xpath('img_urls','//div[@class="wrap container"]//article//div[@class="entry-content"]//img/@src')
        loader1.add_xpath('publish_time','//div[@class="wrap container"]//article//time[@class="published updated"]/text()',deal_publish_time)
        # loader1.add_xpath('publish_user','//article//time[@class="published"]/a[@class="fn"]/text()')



        item=loader1.load_item()
        print (item)
        return item