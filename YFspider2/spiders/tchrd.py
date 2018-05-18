#_*_coding:utf-8_*_
import scrapy
# from scrapy.spider import Spider
from scrapy.spider import CrawlSpider
from scrapy_redis.spiders import RedisCrawlSpider
from YFspider2.items import YfspiderspeakItem
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from YFspider2.othermodule.itemloader_ll import itemloader_ll
from scrapy.loader.processors import Join,MapCompose,Compose,TakeFirst
import time
import hashlib


def deal_links_to_fallow(link_raw):
    links=link_raw.replace('http://','')
    linksplited= links.strip('/').split('/')
    if len(linksplited)==2:
        print '跟进链接:',link_raw
        return link_raw



class tchrd(RedisCrawlSpider):
    name = 'tchrd'
    start_urls=['http://tchrd.org/chinese/']

    rules = (
        Rule(LinkExtractor(allow=r'(http\:\/\/tchrd\.org\/chinese\/[^\/]*?[\/\"|^])',deny=(r'google.com',r'linkedin.com',r'facebook.com'),restrict_xpaths='//*[@id="main-content"]/div[@class="content"]/div[@class="post-navigation"]'),
             callback='parse_content',#中文
             follow=True),
        Rule(LinkExtractor(allow=r'(http\:\/\/www\.tchrd\.org\/tib\/\d{4}\/\d{2}\/.*\/)',deny=(r'google.com',r'linkedin.com',r'facebook.com'),restrict_xpaths='//*[@id="main-content"]/div[@class="content"]/div[@class="post-navigation"]'),
             callback='parse_content',#藏文
             follow=True),
        Rule(LinkExtractor(allow=r'(http\:\/\/www\.tchrd\.org\/.*\-.*\/)',deny=(r'google.com',r'linkedin.com',r'facebook.com'),restrict_xpaths='//*[@id="main-content"]/div[@class="content"]/div[@class="post-navigation"]',process_value=deal_links_to_fallow),
             callback='parse_content',#英文
             follow=True),
        Rule(LinkExtractor(allow=r'http\:\/\/tchrd\.org\/chinese\/$',deny=(r'google.com',r'linkedin.com',r'facebook.com')),follow=True),
    )

    def parse_content(self,response):
        print ('has get one_website',response.url)

        def deal_publish_time(publish_time_raw_list):
            mounth_str=str(publish_time_raw_list[0])
            day_str=str(publish_time_raw_list[1])
            year_str=str(publish_time_raw_list[2])

            mouth_transform={
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

            mounth_str_num=mouth_transform[mounth_str]

            publish_time_str=year_str+'-'+mounth_str_num+'-'+day_str+' 00:00:00'
            return publish_time_str
        def deal_id(id):
            id_hash=hashlib.md5(id).hexdigest()
            return id_hash


        loaders1=itemloader_ll(response=response,item=YfspiderspeakItem())
        loaders1.add_value('url', response.url)
        loaders1.add_value('spider_time', time.time())
        loaders1.add_xpath('title', '//*[@id="the-post"]/div[@class="post-inner"]/h1/span/text()')
        loaders1.add_value('publish_time', response.xpath('//*[@id="the-post"]//span[@class="tie-date"]/text()').re(r'(\S*) (\d{1,2})\, (\d{1,4})'),
                           deal_publish_time)
        loaders1.add_xpath('content', '//div[@class="content"]//div[@class="entry"]//text()', Join())
        loaders1.add_value('img_urls', response.xpath('//*[@id="the-post"]/div/div[@class="entry"]//img').re(r'src="(.*?)"'))
        loaders1.add_value('id', response.url.split('chinese/')[1].strip('\/'),deal_id)

        item1 = loaders1.load_item()
        return item1