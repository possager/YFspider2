#_*_coding:utf-8_*_
from hashlib import md5
import chardet
import re
import requests
from scrapy.selector import Selector
import json



Re_find_time=re.compile(r'.*?(\d{1,4}).*?(\d{1,2}).*?(\d{1,2})')
# data='২০১৫০৩০৬'
# data='ཕྱི་ལོ། ২০১৪ ཟླ། ১১ ཚེས། ১৭ ཉིན་གནས་ཚུལ་སྤེལ། : གསལ་བསྒྲགས།'
# aa=bytes(data)
data='afsdfadsfsadsf'


# data=unicode(u'ཕྱི་ལོ། ২০১৪ ཟླ། ১১ ཚེས། ১৭ ཉིན་གནས་ཚུལ་སྤེལ།:གསར་འཕྲིན།')
# aaa=bytes(b'\x0e\xa7\xae').decode('utf-8')


headers1={
    'user-agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36',
    'accept-encoding':'gzip, deflate, br',
    'accept':'*/*',
    'x-client-data':'CJK2yQEIprbJAQjBtskBCKmdygEIqKPKAQ=='
}
response1=requests.get(url='http://tibetanwomen.org/bo/?p=530',headers=headers1)
text_contain_date=Selector(text=response1.text).xpath('//div[@class="entry"]//aside[@class="entry-meta"]//text()').extract()
data=''.join(text_contain_date)

zangwen2han={
    bytes(b'\xe0\xa7\xa6'):'0',
    '১':'1',
    '২':'2',
    '৩':'3',
    '৪':'4',
    '৫':'5',
    '৬':'6',
    '৭':'7',
    bytes(b'\xe0\xa7\xae'):'8',
    bytes(b'\xe0\xa7\xb0'):'9'
}
zangwen2hanUnicode={
    u"০": "0",
    u"১": "1",
    u"ৰ": "9",
    u"৮": "8",
    u"৬": "6",
    u"৭": "7",
    u"৪": "4",
    u"৫": "5",
    u"২": "2",
    u"৩": "3"
}
with open('zangwen.json','w+') as fl:
    json.dump(zangwen2han,fl)
print len(data)


for ii in zangwen2hanUnicode.keys():
    # print ii
    if ii in data:
        print ii
        print 'ii in data'
        data= data.replace(ii,zangwen2hanUnicode[ii])
    # data.replace(ii,zangwen2han[ii])
    # print data
print data

print Re_find_time.findall(data)

