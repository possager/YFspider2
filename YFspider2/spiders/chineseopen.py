#_*_coding:utf-8_*_
from scrapy.spiders import Rule
from scrapy_redis.spiders import RedisCrawlSpider
from scrapy.linkextractor import LinkExtractor
from YFspider2.items import YfspiderspeakItem
# from scrapy.loader import
from YFspider2.othermodule.itemloader_ll import itemloader_ll
from scrapy.loader import ItemLoader
from scrapy.loader.processors import Join,TakeFirst,MapCompose
from string import strip
import scrapy
import time
import datetime




class chinesepen(RedisCrawlSpider):
    name = 'chinesepen'
    start_urls=['http://www.chinesepen.org/']
    # redis_key='middleway:urls'
    headers={
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36',
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    }


    rules =  (
        Rule(LinkExtractor(allow='http\:\/\/www\.chinesepen\.org\/blog\/archives\/\d*',),callback='parse_content',follow=True),
    )


    # def start_requests(self):
    #     for url in self.start_urls:
    #         yield scrapy.Request(url=url,headers=self.headers)



    def parse_content(self,response):
        print 'in parseMore'


        def deal_publish_time(publish_time_raw):
            if type(publish_time_raw)==type([]):
                publish_time_raw_str=publish_time_raw.pop()
            else:
                publish_time_raw_str=publish_time_raw
            time_splited=publish_time_raw_str.split(',')
            year=str(time_splited[1]).strip()
            mounth_day=time_splited[0].split(' ')
            day=str(mounth_day[1]).strip()
            mounth=mounth_day[0]

            mounth_dict={
                u'一月':'01',
                u'二月':'02',
                u'三月':'03',
                u'四月':'04',
                u'五月':'05',
                u'六月':'06',
                u'七月':'07',
                u'八月':'08',
                u'九月':'09',
                u'十月':'10',
                u'十一月':'11',
                u'十二月':'12',
            }

            mounth_num_str=mounth_dict[mounth]

            if len(day)<2:
                day='0'+day


            publish_time_dealed=year+'-'+mounth_num_str+'-'+day+' 00:00:00'
            return publish_time_dealed

        def deal_publish_user(publish_user_raw):
            if type(publish_user_raw) ==type([]):
                if publish_user_raw:
                    publish_user_name=publish_user_raw.pop()
                else:
                    publish_user_name=''
            else:
                publish_user_name=publish_user_raw
            return publish_user_name.strip()

        def deal_read_count(read_count_raw):
            if read_count_raw:#这里边一定是list对象。
                read_count_str=read_count_raw.pop()
                read_count=str(read_count_str).replace('阅读次数:','').replace(',','')
                return read_count
            else:
                return 0



        loader1=itemloader_ll(response=response,item=YfspiderspeakItem())
        loader1.add_value('url',response.url)
        loader1.add_value('id',response.url.split('/')[-1])
        loader1.add_value('spider_time',time.time())
        loader1.add_xpath('title','//div[@id="main"]//h1[@class="entry-title"]/text()',lambda x:x[0].strip())
        loader1.add_xpath('content','//meta[@property="og:description"]/@content',Join())
        loader1.add_xpath('publish_time','//div[@id="main"]//span[@class="date"]/text()',deal_publish_time)
        loader1.add_xpath('publish_user','//div[@id="main"]//span[@class="author"]/text()',deal_publish_user)
        loader1.add_value('read_count',response.xpath("//div[@id='content']/article/div/text()").re('阅读次数\:(.*)'),deal_read_count)

        item1=loader1.load_item()
        return item1

