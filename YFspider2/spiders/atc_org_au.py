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


class atc_org_au(RedisCrawlSpider):
    name = 'atc_org_au'
    # start_urls=['http://www.sherig.org/tb/page/{}/'.format(str(i)) for i in range(1,10)]
    start_urls = ['https://www.atc.org.au/']
    # redis_key = 'atc_org_au:url'

    rules = (
        # Extract links matching 'category.php' (but not matching 'subsection.php')
        # and follow links from them (since no callback means follow=True by default).

        # Rule(LinkExtractor(allow=r'www\.atc\.org\.au\/.*', ),follow=True),
        # Rule(LinkExtractor(allow=r'www\.atc\.org\.au\/((?!item).)*$'),follow=True),
        Rule(LinkExtractor(allow='www\.atc\.org\.au\/[^\/]*?\/[^\/]*?\?.*'), follow=True),

    # Extract links matching 'item.php' and parse them with the spider's method parse_item
        Rule(LinkExtractor(allow='www\.atc\.org\.au\/\S*\/\S*\/item\/.*'), follow=True,callback='parse_content'),
        Rule(LinkExtractor(allow='www\.atc\.org\.au\/[^\/]*?\/[^\/]*?$'),follow=True)
    )

    def parse_content(self,response):
        def deal_publish_time(publish_time_raw):
            if isinstance(publish_time_raw,type([])):
                publish_time_str=publish_time_raw[0]
            else:
                publish_time_str=publish_time_raw

            publish_DMY=publish_time_str.split(',')[1].strip()
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
            publish_time_splited=publish_DMY.split(' ')

            day_str=publish_time_splited[0]
            mounth_str_raw=publish_time_splited[1]
            year=publish_time_splited[2]

            mounth_str_num = mouth_transform[str(mounth_str_raw)]

            return year+'-'+mounth_str_num+'-'+day_str+' 00:00:00'

        def deal_id(id_raw):
            return hashlib.md5(id_raw).hexdigest()

        def deal_img(img_urls_raw):
            img_urls_end=[]
            if not isinstance(img_urls_raw,type([])):
                img_urls_raw=[img_urls_raw]

            for img_url_raw in img_urls_raw:
                if 'http' or 'www' in img_url:
                    # 'https://www.atc.org.au/images/Campaigns/Rudrani%20Tooth.jpg'
                    img_url=urljoin('https://www.atc.org.au/',img_url_raw)
                    img_urls_end.append(img_url)
            return img_urls_end


        # print response.url
        content_loader=itemloader_ll(response=response,item=YfspiderspeakItem())
        content_loader.add_value('url',response.url)
        content_loader.add_value('spider_time',time.time())

        content_loader.add_xpath('title','//div[@class="ItemViewMain"]/div[@class="itemHeader"]/h2[@class="itemTitle"]/text()',lambda x:x[0].strip() if x else None)
        content_loader.add_xpath('content','//div[@class="ItemViewMain"]/div[@class="itemBody"]//p/text()')
        content_loader.add_xpath('publish_time','//div[@class="itemHeader"]/div[@class="infoline"]/span[@class="itemDateCreated"]/text()',deal_publish_time)
        content_loader.add_value('id',response.url.strip('/').split('/')[-1],deal_id)
        content_loader.add_xpath('img_urls','//div[@class="ItemViewMain"]/div[@class="itemBody"]//img/@src',deal_img)

        item1=content_loader.load_item()
        return item1