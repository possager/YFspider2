import re
import requests
from scrapy.selector import Selector



headers={
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36',
    # 'Upgrade-Insecure-Requests':'1',
    # 'Host':'kagyuoffice.org',
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8'
}


str1='http://tibet.net/2018/05/chinas-south-east-asia-push-threatened-by-new-malaysia-regime/'

response1=requests.get(url=str1,headers=headers)
selector1=Selector(text=response1.text)
print selector1.xpath('//main//div[@id="single_meta"]//div[contains(@class,"date")]//text()').re('\S* (\d*)\, \d*')