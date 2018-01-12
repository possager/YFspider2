#_*_coding:utf-8_*_
from scrapy.cmdline import execute



#tchrd网站爬虫启动命令
#redis插入网站地址：
#lpush tchrd:url http://tchrd.org/chinese/%E8%A5%BF%E8%97%8F%E4%B8%80%E5%BA%A7%E5%B7%A8%E5%A4%A7%E7%9A%84%E7%9B%91%E7%8B%B1%E8%A5%BF%E8%97%8F%E4%BA%BA%E6%9D%83%E4%B8%8E%E6%B0%91%E4%B8%BB%E4%BF%83%E8%BF%9B%E4%B8%AD%E5%BF%83%E5%8F%91%E5%B8%83/


# execute('scrapy crawl studentsforafreetibet'.split(' '))
execute('scrapy crawl tibetanentrepreneurs'.split(' '))