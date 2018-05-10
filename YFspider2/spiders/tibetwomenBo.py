#_*_coding:utf-8_*_
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



class tibetwomenBo(RedisCrawlSpider):
    name = 'tibetwomenBo'
    headers={
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36',
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    }


    rules =  (
        Rule(LinkExtractor(allow='http\:\/\/tibetanwomen\.org\/bo/\?p=\d*',),callback='parse_content',follow=True),
        Rule(LinkExtractor(allow='http\:\/\/tibetanwomen\.org\/bo\/\?attachment\_id\=\d*'),callback='parse_content',follow=True),
        Rule(LinkExtractor(allow='http\:\/\/tibetanwomen\.org\/bo.*'),follow=True),
    )



    def parse_content(self,response):
        print ('in parseMore')


        def deal_publish_time(publish_time_raw):
            if type(publish_time_raw)==type([]):
                publish_time_raw_str=''.join(publish_time_raw)
            else:
                publish_time_raw_str=publish_time_raw

            Re_find_time = re.compile(r'.*?(\d{1,4}).*?(\d{1,2}).*?(\d{1,2})')
            zangwen2hanUnicode = {
                u"০": "0",
                u"১": "1",
                u"ৰ": "9",
                u"৮": "8",
                u"৬": "6",
                u"৭": "7",
                u"৪": "4",
                u"৫": "5",
                u"২": "2",
                u"৩": "3"
            }

            for ii in zangwen2hanUnicode.keys():
                if ii in publish_time_raw_str:
                    publish_time_raw_str = publish_time_raw_str.replace(ii, zangwen2hanUnicode[ii])

            publishtime= Re_find_time.findall(publish_time_raw_str)
            if not publishtime:
                return '2018-02-01 00:00:00'
            else:
                try:#[(2018,01,02)]
                    year=str(publishtime[0][0])
                    mounth=str(publishtime[0][1])
                    days=str(publishtime[0][2])

                    return year+'-'+mounth+'-'+days+' 00:00:00'
                except Exception as e:
                    print e
                    return '2018-02-01 00:00:00'


        def deal_read_count(read_count_raw):
            if read_count_raw:#这里边一定是list对象。
                read_count_str=read_count_raw.pop()
                read_count=str(read_count_str).strip()
                return read_count
            else:
                return 0


        loader1=itemloader_ll(response=response,item=YfspiderspeakItem())
        loader1.add_value('url',response.url)
        loader1.add_value('id',response.url.split('/')[-1])
        loader1.add_value('spider_time',time.time())
        loader1.add_xpath('title','//div[@class="entry"]//h1[@class="entry-title"]/text()',lambda x:x[0].strip())
        loader1.add_xpath('content','//div[@class="entry"]//div[@class="entry-content"]//p//text()',lambda x:''.join([oneP.strip() for oneP in x]))
        loader1.add_xpath('publish_time','//div[@class="entry"]//aside[@class="entry-meta"]//text()',deal_publish_time)
        # loader1.add_xpath('publish_user','//div[@id="main"]//span[@class="author"]/text()',deal_publish_user)
        loader1.add_value('read_count',response.xpath('//div[@class="entry"]//div[@class="entry-content"]//p[contains(@style,"font-style")]').re('.* (\d*) .*'),deal_read_count)
        loader1.add_xpath('img_urls','//div[@class="entry"]//div[@class="entry-content"]//img/@src')

        item1=loader1.load_item()
        return item1


