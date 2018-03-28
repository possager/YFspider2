import requests
import re
from scrapy.selector import Selector


respnse1=requests.get(url='http://www.chinesepen.org/english/china-pen-renews-its-calls-to-release-all-writers-journalists-and-publishers')
selector1=Selector(text=respnse1.text)
print selector1.xpath('//div[@id="container"]//div[@class="entry-meta"]//span[@class="entry-date"]/text()').re('.*(\d{1,2})\/(\d{1,2})\/(\d{4}).*')