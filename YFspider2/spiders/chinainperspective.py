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
from string import strip
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
    )


    # def start_requests(self):
    #     for url in self.start_urls:
    #         yield scrapy.Request(url=url,headers=self.headers)



    def parse_content(self,response):
        print 'in parseMore'


        def deal_publish_time(publish_time_list=[]):
            if publish_time_list:
                year=str(publish_time_list[2]).strip()
                day=str(publish_time_list[1]).strip()
                mounth=str(publish_time_list[0]).strip()

                mouth_eng_to_num={
                    'January':'01',
                    'February':'02',
                    'March':'03',
                    'April ':'04',
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

                publish_time=year+'-'+moun_num+'-'+day+' 00:00:00'
                return publish_time
            else:
                return None
        def deal_publish_user(publish_user_raw):
            if publish_user_raw:
                publish_user_raw_str=publish_user_raw.pop()
                publish_user_raw_str.replace(u'作者',u'')

                publish_user_list=publish_user_raw_str.split(' ')
                publish_user_list_dealed=[]
                for one_publish_user in publish_user_list:
                    publish_user_list_dealed.append(one_publish_user.strip())
                return publish_user_list_dealed


            else:
                return None



        loader1=ItemLoader(item=YfspiderspeakItem(),response=response)
        loader1.add_value('url',response.url)
        loader1.add_value('spider_time',time.time())
        loader1.add_xpath('title','//span[@id="labArticle_Name"]/text()',TakeFirst(),lambda x:x.strip())
        loader1.add_xpath('content','//div[@id="divContent"]/div/p/text()',lambda x:[i.strip() for i in x],Join())
        loader1.add_value('id',response.url.split('=')[1])
        loader1.add_value('img_urls',response.selector.xpath('//div[@id="divContent"]/div/p//img').re(r'src="(.*?)"'))
        loader1.add_value('publish_time',response.xpath('//span[@id="labResource"]/br').re(ur'\, (\w*) (\d{1,2}).*(\d{4})'),deal_publish_time)
        loader1.add_xpath('publish_user','//span[@id="labAuthor"]/text()',deal_publish_user)
        # loader1.add_value('reply_count',response.selector.xpath('//*[@id="comments"]/h4/text()').re(ur'(\d{1,2}).*条评论'),lambda x:x[0] if x else 0)
        # loader1.add_value('reply_nodes',response.selector.re(ur'var items \= (\[.*?\])\;'),)



        item=loader1.load_item()
        print item
        return item