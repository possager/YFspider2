#_*_coding:utf-8_*_
from scrapy.selector import Selector
import requests




headers={
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36',
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8'
}
response1=requests.get(url='http://www.bbc.com/zhongwen/simp/world/2011/03/110310_us-china_cyber.shtml',headers=headers)


selector1=Selector(text=response1.text)

read_count=selector1.xpath('//div[@role="main"]//div[@class="story-body"]//div[contains(@class,"date date")]/@data-seconds').extract()
#//div[@role="main"]//div[@class="story-body"]//div[contains(@class,"date date")]
print read_count