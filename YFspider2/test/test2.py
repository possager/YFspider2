#_*_coding:utf-8_*_
import requests
import re
from scrapy.selector import Selector



zangwendict3={
    u"༧": u"7",
    u"༦": u"6",
    u"༥": u"5",
    u"༤": u"4",
    u"༣": u"3",
    u"༢": u"2",
    u"༡": u"1",
    u"༠": u"0",
    u"༩": u"9",
    u"༨": u"8"
}


headers={
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36',
    'Proxy-Connection':'keep-alive',
    'Host':'bod.asia',
    'Accept-Encoding':'gzip, deflate',
    'Accept-Language':'zh-CN,zh;q=0.9'
}

response1=requests.get(url='http://bod.asia/2018/05/%E0%BD%96%E0%BD%BC%E0%BD%91%E0%BC%8B%E0%BD%80%E0%BE%B1%E0%BD%B2%E0%BC%8B%E0%BD%96%E0%BD%B4%E0%BD%91%E0%BC%8B%E0%BD%98%E0%BD%BA%E0%BD%91%E0%BC%8B%E0%BD%A3%E0%BE%B7%E0%BD%93%E0%BC%8B%E0%BD%9A%E0%BD%BC-3/#',headers=headers)

# print response1.text

selector1=Selector(text=response1.text)
publish_time= selector1.xpath('//header//div[@class="single_meta_item single_meta_date"]//text()').extract()
publish_time_zangwen= publish_time[0]

for onekey in zangwendict3.keys():
    if onekey in publish_time_zangwen:
        publish_time_zangwen=publish_time_zangwen.replace(onekey,zangwendict3[onekey])

print publish_time_zangwen


Re_find_publish_time=re.compile(r'(\d{1,2}).*?(\d{1,2}).*?(\d{4})')

print Re_find_publish_time.findall(publish_time_zangwen)