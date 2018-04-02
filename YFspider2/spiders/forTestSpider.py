#_*_coding:utf-8_*_


import scrapy
from scrapy.spiders import CrawlSpider,Rule
from scrapy.linkextractor import LinkExtractor
import re


# class testSpider(CrawlSpider):
#     name = 'testspider'
#     start_urls=['http://brucedone.com/archives/883']
#     headers={
#         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36',
#         'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
#     }
#
#     allow_re=re.compile(r'http\:\/\/brucedone\.com\/archives\/\d{1,5}')
#
#
#     rules = (
#         Rule(LinkExtractor(allow=allow_re),callback='parse_item2',follow=True),
#         Rule(LinkExtractor(allow=(r'http\:\/\/brucedone\.com\/archives\/\d{1,5}',)), callback='parse_item2', follow=True),  # True该False
#         Rule(LinkExtractor(allow=(r'brucedone\.com\/archives\/date\/\d{1,5}\/\d{1,2}',)),callback='parse_item3')
#     )
#
#
#     def start_requests(self):
#         for url in self.start_urls:
#             yield scrapy.Request(url=url,headers=self.headers)
#
#
#     # def parse_item(self,response):
#     #     print response.url
#     #     # print response.body
#     #     yield scrapy.Request(url='https://www.cnblogs.com/stGeekpower/p/3310535.html',callback=self.parse_item2,headers=response.headers)
#
#
#     def parse_item2(self,response):
#         print 'item2'
#         print response.url
#
#
#     def parse_item3(self,response):
#         print 'item3'
#         print response.url