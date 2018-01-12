#_*_coding:utf-8_*_
import scrapy
# from scrapy.spider import Spider
from scrapy.spider import CrawlSpider
from scrapy_redis.spiders import RedisCrawlSpider
from YFspider2.items import YfspiderspeakItem
from scrapy.spiders import Rule
from scrapy.linkextractor import LinkExtractor
from YFspider2.othermodule.itemloader_ll import itemloader_ll
from scrapy.loader.processors import Join,MapCompose,Compose,TakeFirst
import time
import hashlib
from w3lib.url import urljoin


class tibetsociety(RedisCrawlSpider):
    name = 'tibetanentrepreneurs'
    # start_urls=['http://www.sherig.org/tb/page/{}/'.format(str(i)) for i in range(1,10)]
    start_urls=['']
    redis_key = 'tibetanentrepreneurs:url'

    headers={
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36',
        'Upgrade-Insecure-Requests':'1',
        'Host':'ww.tibetsociety.com',
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Referer':'http://www.tibetanentrepreneurs.org/'
        # 'Accept-Encoding':'gzip, deflate'
    }
    # def start_requests(self):
    #     for url in self.start_urls:
    #         yield scrapy.Request(url=url,headers=self.headers,callback=self.parse_content)


    rules = (
        # Extract links matching 'category.php' (but not matching 'subsection.php')
        # and follow links from them (since no callback means follow=True by default).
        # Rule(LinkExtractor(allow=r'http\:\/\/www\.sherig\.org\/tb\/\d{4}\/\d{1,2}\/.*?\/$',),callback='parse_content',follow=True),
        #http\:\/\/www\.sherig\.org\/tb\/\d{4}\/\d{1,2}\/[^\\\/\']*?\/\B
        Rule(LinkExtractor(allow=r'http\:\/\/tibetanentrepreneurs\.org\/\d{1,4}/\d{1,2}/\d{1,2}.*?', allow_domains=r'tibetanentrepreneurs.org'), callback='parse_content',
             follow=True),
        Rule(LinkExtractor(allow=r'http\:\/\/tibetanentrepreneurs\.org\/.*?\/',allow_domains=r'tibetanentrepreneurs.org'),follow=True)

        # Extract links matching 'item.php' and parse them with the spider's method parse_item
        # Rule(LinkExtractor(allow='http://www.sherig.org/tb/page/\d{1,5}/'), follow=True),
    )

    def parse_content(self, response):

        def deal_publish_time(publish_time_raw):
            if publish_time_raw:
                publish_time_DMY=publish_time_raw[0].split(' ')
                Day_str=publish_time_DMY[1].replace('th,','')
                Mounth_str=publish_time_DMY[0]
                Year_str=publish_time_DMY[2]

                mouth_transform = {
                    'January': '01',
                    'February': '02',
                    'March': '03',
                    'April': '04',
                    'May': '05',
                    'June': '06',
                    'July': '07',
                    'August': '08',
                    'September': '09',
                    'October': '10',
                    'November': '11',
                    'December': '12'
                }
                mounth_str_num = mouth_transform[str(Mounth_str)]

                return Year_str+'-'+mounth_str_num+'-'+Day_str+' 00:00:00'
            else:
                return '1111-11-11 11:11:11'


        print response.url
        content_loader=itemloader_ll(response=response,item=YfspiderspeakItem())
        content_loader.add_value('url',response.url)
        content_loader.add_value('spider_time',time.time())
        content_loader.add_value('id',response.url.strip('/').split('/')[-1])

        content_loader.add_xpath('title','//div[@id="content"]//h2[@class="entry-title"]//text()')
        content_loader.add_xpath('content','//div[@id="content"]//div[@class="post-content"]//text()',Join())
        content_loader.add_value('publish_time',response.xpath('//div[@id="content"]//div[@class="fusion-meta-info"]//text()').re(r'\S* \d{1,2}th, \d{1,4}'),deal_publish_time)
        content_loader.add_xpath('img_urls','//div[@id="main"]//div[@id="content"]//img/@src')

        item1=content_loader.load_item()
        return item1