#_*_coding:utf-8_*_



import requests
from scrapy.selector import Selector


headers={
    'user-agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36',
    'accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8'
}
headers2={
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'
}
resposne1=requests.get(url='http://www.bbc.com/zhongwen/simp/world-44178972')

# print resposne1.text

selector1=Selector(text=resposne1.text)
# print selector1.xpath("//div[@id='content']/article/div[contains(@class,'tags')]//text()").extract()#.re('阅读次数\:(.*)')

print selector1.xpath('//div[@role="main"]//div[@class="story-body__inner"]//div//img/@src').extract()
print selector1.xpath('//div[@role="main"]//div[@class="story-body__inner"]//div//@data-src').extract()