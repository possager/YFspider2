#_*_coding:utf-8_*_
import scrapy
# from scrapy.spider import Spider
from scrapy.spider import CrawlSpider
from scrapy_redis.spiders import RedisCrawlSpider
from YFspider2.items import YfspiderspeakItem
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from YFspider2.othermodule.itemloader_ll import itemloader_ll
from scrapy.loader.processors import Join,MapCompose,Compose,TakeFirst
import time
import hashlib



class dhokhamchushigangdrug(RedisCrawlSpider):
    name = 'dhokhamchushigangdrug'
    # start_urls=['http://www.sherig.org/tb/page/{}/'.format(str(i)) for i in range(1,10)]
    start_urls=['http://dhokhamchushigangdrug.com/']
    redis_key = 'dhokhamchushigangdrug:url'

    headers={
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36',
        'Access-Control-Request-Headers':'x-csrf-token',
        'Access-Control-Request-Method':'GET',
        'Accept':'*/*'
    }
    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url,headers=self.headers)


    rules = (
        # Extract links matching 'category.php' (but not matching 'subsection.php')
        # and follow links from them (since no callback means follow=True by default).
        # Rule(LinkExtractor(allow=r'http\:\/\/www\.sherig\.org\/tb\/\d{4}\/\d{1,2}\/.*?\/$',),callback='parse_content',follow=True),
        #http\:\/\/www\.sherig\.org\/tb\/\d{4}\/\d{1,2}\/[^\\\/\']*?\/\B
        Rule(LinkExtractor(allow=r'http://dhokhamchushigangdrug.com/.*?', ), callback='parse_content',
             follow=True),


        # Extract links matching 'item.php' and parse them with the spider's method parse_item
        # Rule(LinkExtractor(allow='http://www.sherig.org/tb/page/\d{1,5}/'), follow=True),
    )

    def parse_content(self, response):
        print (response.url)

        def deal_id(id_raw):
            return hashlib.md5(id_raw).hexdigest()

        if response.xpath('//div[@class="wrap container"]//main/header'):
            print ('has header,maybe is article')
            content_loader=itemloader_ll(response=response,item=YfspiderspeakItem())
            content_loader.add_value('url',response.url)
            content_loader.add_value('spider_time',time.time())

            content_loader.add_xpath('title','//div[@class="wrap container"]//main//header/h1/text()',lambda x:x[0].strip())
            content_loader.add_xpath('content','//div[@class="wrap container"]//main//div[@class="entry-content"]//text()',Join())
            content_loader.add_value('publish_time',response.xpath('//div[@class="wrap container"]//main//header/time[@class="published"]/@datetime').re(r'\d{4}\-\d{2}\-\d{2}T\d{2}\:\d{2}\:\d{2}'),
                                     lambda x:x[0].replace('T',' ') if x else None)
            content_loader.add_xpath('img_urls','//div[@class="wrap container"]//main//img/@src')
            content_loader.add_value('id',response.url.strip('/').split('/')[-1],deal_id)

            item1=content_loader.load_item()
            return item1
        elif response.xpath('//div[@class="wrap container"]//main/div[@class="page-header"]'):
            print ('anther type page')
            content_loader=itemloader_ll(response=response,item=YfspiderspeakItem())
            content_loader.add_value('url',response.url)
            content_loader.add_value('spider_time',time.time())

            content_loader.add_xpath('title','//div[@class="wrap container"]//main/div[@class="page-header"]/h1/text()',lambda x:x[0].strip())
            content_loader.add_xpath('content','//div[@class="wrap container"]//main//text()',Join())
            content_loader.add_value('publish_time','1111-11-11 11:11:11')
            content_loader.add_value('id',response.url.strip('/').split('/')[-1],deal_id)
            content_loader.add_value('img_urls',response.xpath('//div[@class="wrap container"]//main//img/@src').extract())

            item1=content_loader.load_item()
            return item1
        else:
            print ('unkonwn page')