import requests
from scrapy.selector import Selector



headers={
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36',
    'Upgrade-Insecure-Requests':'1',
    'Host':'kagyuoffice.org',
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8'
}
response1=requests.get(url='http://kagyuoffice.org/a-very-special-guru-rinpoche-practice-with-karmapa/',headers=headers)

selector1=Selector(text=response1.text)

print selector1.xpath('//div[@id="content"]//div[@class="entry-content"]/p[1]//text()').extract()
print selector1.xpath('//div[@id="content"]//div[@class="entry-content"]/p[1]/text()').extract()[0]