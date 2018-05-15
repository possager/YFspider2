#_*_coding:utf-8_*_
import re
import json
import requests
from scrapy.selector import Selector


zangwenDict={
    '༢':'2',
    '༠':'0',
    '༡':'1',
    '༨':'8',
    '༤':'4',
    '༥':'5',
}

zangwendict2={
    b'\xe0\xbc\xa0': '0',
    b'\xe0\xbc\xa1': '1',
    b'\xe0\xbc\xa2': '2',
    b'\xe0\xbc\xa3': '3',
    b'\xe0\xbc\xa4': '4',
    b'\xe0\xbc\xa5': '5',
    b'\xe0\xbc\xa6': '6',
    b'\xe0\xbc\xa7': '7',
    b'\xe0\xbc\xa8': '8',
    b'\xe0\xbc\xa9': '9',
}

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
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36',
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8'
}
response1=requests.get(url='http://www.vot.org/%E0%BD%A2%E0%BE%92%E0%BE%B1%E0%BC%8B%E0%BD%82%E0%BD%A2%E0%BC%8B%E0%BD%82%E0%BE%B1%E0%BD%B2%E0%BC%8B%E0%BD%82%E0%BE%B2%E0%BD%BC%E0%BD%A6%E0%BC%8B%E0%BD%9A%E0%BD%BC%E0%BD%82%E0%BD%A6%E0%BC%8B%E0%BD%82-2/',headers=headers)

selector1=Selector(text=response1.text)
date_str= selector1.xpath('//div[@class="wrap container"]//article//time[@class="published updated"]/text()').extract()[0]



datezangwen='ཕྱི་ལོ། ༢༠༡༨ ཟླ། ༠༥ ཚེས། ༡༤ ཉིན་སྤེལ།'

date_dict={}

for onechar in zangwendict3.keys():
    if onechar in date_str:
        print '-'
        date_z= zangwendict3[onechar]
        date_index= date_str.index(onechar,0,len(date_str))
        date_dict.update({date_index:date_z})
        datezangwen=date_str.replace(onechar,zangwendict3[onechar])
sortdict= sorted(date_dict.items(),key=lambda item:item[0])

lastindex=sortdict[0][0]
thisindex=sortdict[0][0]
nextString=False
date_list=['','','']
date_list_index=0

for onesortdict in sortdict:

    thisindex=onesortdict[0]
    if thisindex-lastindex<2:
        date_list[date_list_index]+=onesortdict[1]
    else:
        date_list_index+=1
        date_list[date_list_index]+=onesortdict[1]
    lastindex=thisindex

print date_list