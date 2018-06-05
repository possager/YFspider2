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


def deal_links_to_fallow(link_raw):
    '''
    这个函数用来处理crawlspider在遍历抓取时需要对url进一步处理的需求。比如有些网站需要添加?full=yes这样的字段，才能获取全部网页内容，否着会让你请求下一页。
    :param link_raw: link_raw是Rule中满足的对应正则表达式的连接，满足的连接有很多个，但每次只会传入一个，类型是str，多个满足的连接会多次调用这个函数。
    :return: 返回的连接会放入  requests任务请求队列。
    '''
    links=link_raw.replace('http://','')
    linksplited= links.strip('/').split('/')
    if len(linksplited)==2:
        print '跟进链接:',link_raw
        return link_raw



class tibetanparliament(RedisCrawlSpider):
    '''
    rediscrawlspider是scrapy的某一类爬虫，主要特点继承于crawlspider，会根据rules中的方法来对整个网站进行遍历式爬取，满足relues中的连接都会被跟进。rediscrawlspider只是结合了redis中的功能
    将任务队列放在了redis中，去重功能也放在了任务队列中。

    '''
    name = 'tibetanparliament'#爬虫名，全局唯一，用来让scrapy定位识别爬虫
    start_urls=['http://tibetanparliament.org/']#只适用于spider类和crawlspider类，rediscrawlspider中没有此字段，
    headers={
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36',
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    }#只适用于spider类和crawlspider类，rediscrawlspider中没有此字段，


    rules =  (
        # linkextractor类，crawlspider遍历网站的时候，url遍历规则都在这里设置。可以参见帮助文档，里边有详细的介绍说明
        Rule(LinkExtractor(allow=r'http:\/\/tibetanparliament\.org\/.*?\/$',process_value=deal_links_to_fallow),callback='parse_content',follow=True),
        Rule(LinkExtractor(allow=r'http:\/\/tibetanparliament\.org\/.*?',),follow=True)
    )




    def parse_content(self,response):
        '''
        这个函数在rulus中定义好了的一个callback，满足这个rules规则的所有链接的response都会交给这个方法来处理。

        :param response: 是一个标准的scrapy的response对象，详细可以参看官方帮助文档。常用功能，response.xpath(),response.css(),response.xpath().re(),response.css().re().....
        :return: 这是一个回调函数，返回的若是dict或者item（spiders文件夹同级目录中的items文件中定义的class）,则会流经pipeline，若是requests，则会经过调度器调度，交给下载器去下载。
        '''
        print ('in parseMore')


        def deal_publish_time(publish_time_list=[]):
            '''
            所有deal_...()这样的函数，都是为了处理函数名后边的字段的值。这就是这些函数的作用。相似的还有deal_publish_user,deal_img_urls...,使用回调的方式来使用这些函数。

            :param publish_time_list: xpath解析出来的默认都是list，
            :return: 处理好了的时间格式的字段
            '''
            if publish_time_list:
                publish_time_str=publish_time_list[0]
            else:
                return '2018-02-01 00:00:00'
            if '+' in publish_time_str:
                publish_time_str_split=publish_time_str.split('+')[0]
                return publish_time_str_split.replace('T',' ')
            else:
                return '2018-02-01 00:00:00'


        loader1=ItemLoader(item=YfspiderspeakItem(),response=response)
        loader1.add_value('url',response.url)
        loader1.add_value('spider_time',time.time())
        loader1.add_xpath('title','//article//h2[@class="entry-title"]/text()',lambda x:''.join([y for y in x]))
        loader1.add_xpath('content','//article//div[@class="entry-content"]/p//text()',lambda x:[i.strip() for i in x],Join())
        loader1.add_value('id',response.url.strip('/').split('/')[-1])
        loader1.add_xpath('img_urls','//article//div[@class="entry-content"]//img/@src')
        loader1.add_xpath('publish_time','//article//time[@class="published"]/@datetime',deal_publish_time)
        loader1.add_xpath('publish_user','//article//time[@class="published"]/a[@class="fn"]/text()')



        item=loader1.load_item()
        print (item)
        return item