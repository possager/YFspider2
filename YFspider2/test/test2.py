#_*_coding:utf-8_*_
import requests
from scrapy.selector import Selector


headers21={
    ''
}
response1=requests.get(url='http://xizang-zhiye.org/2018/05/%E8%A5%BF%E8%97%8F%E4%BA%BA%E6%B0%91%E8%AE%AE%E4%BC%9A%E8%AE%AE%E9%95%BF%E8%87%B4%E5%87%BD%E6%84%9F%E8%B0%A2%E7%BE%8E%E5%9B%BD%E5%8F%82%E8%AE%AE%E9%99%A2/')
selecte1=Selector(text=response1.text)
publish_user_list= selecte1.xpath('//div[@class="content row"]//div[@id="single_byline"]//text()').extract()
print response1.status_code
for onepublisher in publish_user_list:
    publish_user_list2=[]
    if u'发布' in onepublisher:
        continue
    else:
        if onepublisher.strip():
            print onepublisher
            publish_user_list2.append(onepublisher)


print publish_user_list2