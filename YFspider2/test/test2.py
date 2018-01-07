#_*_coding:utf-8_*_
import requests
import time
from bs4 import BeautifulSoup
import re




headers={
    'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36',
    'Upgrade-Insecure-Requests':'1',
    'Host':'tchrd.org',
    'Connection':'keep-alive',
    'Cache-Control':'max-age=0',
    'Accept-Language':'zh-CN,zh;q=0.9',
    'Accept-Encoding':'gzip, deflate',
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
}


url_tchrd='http://tchrd.org/chinese/%E8%A5%BF%E8%97%8F%E4%B8%80%E5%83%A7%E4%BA%BA%E8%A2%AB%E5%85%B3%E6%8A%BC10%E5%B9%B4%E5%90%8E%E5%87%BA%E7%8B%B1/'
# response1=requests.get(url='http://tchrd.org/chinese/%E8%A5%BF%E8%97%8F%E4%B8%80%E5%83%A7%E4%BA%BA%E8%A2%AB%E5%85%B3%E6%8A%BC10%E5%B9%B4%E5%90%8E%E5%87%BA%E7%8B%B1/',headers=headers)
response2=requests.get(url=url_tchrd,headers=headers)
response_text= response2.text
datasoup=BeautifulSoup(response_text,'lxml')
# print datasoup.select('')