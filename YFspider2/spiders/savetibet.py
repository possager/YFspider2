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


class savetibet(RedisCrawlSpider):
    name = 'savetibet'
    # start_urls=['http://www.sherig.org/tb/page/{}/'.format(str(i)) for i in range(1,10)]
    start_urls=['http://www.savetibet.org/']
    redis_key = 'savetibet:url'

    rules = (
        # Extract links matching 'category.php' (but not matching 'subsection.php')
        # and follow links from them (since no callback means follow=True by default).
        Rule(LinkExtractor(allow=r'http://www.savetibet.org/.*?', deny=('.*?format\=pdf',)), callback='parse_content',
             follow=True),
        # Extract links matching 'item.php' and parse them with the spider's method parse_item
        # Rule(LinkExtractor(allow='http://www.sherig.org/tb/page/\d{1,5}/'), follow=True),
    )

    def parse_content(self, response):
        print (response.url)

        def deal_img_urls(img_urls_raw):
            img_urls_dealed=[]
            for one_url in img_urls_raw:
                if 'download-pdf' in one_url:
                    continue
                if 'http' not in one_url:
                    one_url_dealed=urljoin('http://www.savetibet.org/',one_url)
                    img_urls_dealed.append(one_url_dealed)

            return img_urls_dealed

        if response.xpath('//div[@id="content"]//div[@id="main"]//h1[@class="title"]'):
            #表明有title这个标签，版式就是统一的

            # print response.xpath('//div[@id="content"]//div[@id="main"]//h1[@class="title"]/text()').extract()
            content_laoder=itemloader_ll(response=response,item=YfspiderspeakItem())
            content_laoder.add_value('url',response.url)
            content_laoder.add_value('spider_time',time.time())

            content_laoder.add_xpath('title','//div[@id="content"]//div[@id="main"]//h1[@class="title"]//text()',lambda x:x[0].strip())
            content_laoder.add_xpath('content','//div[@id="content"]//div[@id="main"]//div[@class="entry"]//text()',Join())
            content_laoder.add_xpath('img_urls','//div[@id="main"]//div[@class="entry"]//img/@src',deal_img_urls)
            content_laoder.add_xpath('video_urls','//div[@class="entry"]//iframe/@src')

            content_laoder.add_value('id',response.url.strip('/').split('/')[-1])
            if response.xpath('//div[@class="post-meta"]'):
                content_laoder.add_value('publish_time',response.xpath('//div[@class="post-meta"]//abbr[@class="date time published"]/@title').re('\d{4}\-\d{2}-\d{2}T\d{2}\:\d{2}:\d{2}'),
                                         lambda x:x[0].replace('T',' ') if x else None)
                content_laoder.add_xpath('publish_user','//div[@class="post-meta"]/span[@class="author vcard"]/span[@class="fn"]/a/text()')
                # content_laoder.add_xpath('')
            else:
                content_laoder.add_value('publish_time','1111-11-11 11:11:11')

            item1=content_laoder.load_item()
            return item1
        else:
            print ('no,it not content page')
