#_*_coding:utf-8_*_
import requests
import json

console_url='http://192.168.6.230:6800'




response1=requests.get(url=console_url+'/listspiders.json?',params={'project':'default'})
result1=json.loads(response1.text)
# print('爬虫项目状态是-------------',result1['status'],'可用的爬虫数量：-------',len(result1['spiders']))
# print('可用的爬虫列表：')
print result1
print result1['message']