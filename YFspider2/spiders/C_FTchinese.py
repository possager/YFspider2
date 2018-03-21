#_*_coding:utf-8_*_
# from scrapy.spiders import CrawlSpider,Rule
from scrapy.spiders import Rule
from scrapy_redis.spiders import RedisCrawlSpider
from scrapy.linkextractor import LinkExtractor
from YFspider2.items import YfspiderspeakItem
# from scrapy.loader import
from YFspider2.othermodule.itemloader_ll import itemloader_ll
from scrapy.loader import ItemLoader
from scrapy.loader.processors import Join,TakeFirst,MapCompose
from string import strip
import scrapy
import time
import datetime
from YFspider2.othermodule.deal_url_func import deal_ftchinese_url



class middleway(RedisCrawlSpider):
    name = 'ftchinese'

    start_urls=['http://www.ftchinese.com/']
    # redis_key='middleway:urls'
    headers={
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36',
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    }


    rules =  (
        Rule(LinkExtractor(allow=r'www\.ftchinese\.com\/story\/\d*',process_value=deal_ftchinese_url),callback='parse_content',follow=True,),
        # Rule(LinkExtractor(allow=''))
    )




    def parse_content(self,response):
        print response.url

        def deal_img_urls(img_url_list):
            for one_img_url in img_url_list:
                print one_img_url
            return img_url_list

        def deal_publish_time(publish_time_raw_list):
            year=str(publish_time_raw_list[0])
            mounth=str(publish_time_raw_list[1]) if len(str(publish_time_raw_list[1]))==2 else '0'+str(publish_time_raw_list[1])
            days=str(publish_time_raw_list[2]) if len(str(publish_time_raw_list[2]))==2 else '0'+str(publish_time_raw_list[2])

            hourse=str(publish_time_raw_list[3])
            minite=str(publish_time_raw_list[4])

            publish_time=year+'-'+mounth+'-'+days+' '+hourse+':'+minite+':00'
            return publish_time

        def deal_reply_nodes(response_url):
            # for one_reply_nodes in reply_nodes:
            #     one_reply_nodes.xpath('')
            # 这里边的评论需要重新发起请求，所以这里全部设置成连接，后期的处理中再生成对应的reply_nodes。------mark!
            reply_id=response_url.split('/')[-1].split('?')[0]
            reply_url='http://www.ftchinese.com/index.php/c/newcomment/'+reply_id+'?v=1'
            return reply_url

        def deal_publish_user(publisher_list):
            publish_user_list=[]
            for one_user in publisher_list:
                _=one_user.strip()
                publish_user_list.append(_)
            return publish_user_list






        loader1 = ItemLoader(item=YfspiderspeakItem(), response=response)
        loader1.add_value('url', response.url)
        loader1.add_value('spider_time', time.time())
        loader1.add_xpath('title','//h1[@class="story-headline"]/text()',TakeFirst())
        # loader1.add_xpath('abstract','//div[@class="story-lead"]/text()')#没有abstract这个字段
        loader1.add_value('id',response.url.split('/')[-1].split('?')[0])
        loader1.add_value('img_urls',response.xpath('//div[@class="story-container"]//img/@src').extract(),deal_img_urls)
        loader1.add_xpath('content','//div[@class="story-body"]/p/text()',Join())
        loader1.add_value('publish_time',response.xpath('//span[@class="story-time"]/text()').re('(\d{4}).(\d{1,2}).(\d{1,2}). (\d{1,2})\:(\d{1,2})'),deal_publish_time)
        loader1.add_xpath('publish_user','//span[@class="story-author"]/a/text()',deal_publish_user)
        loader1.add_value('reply_count',response.xpath('//div[@id="allcomments"]/div[@class="commentcontainer"]'),lambda x:len(x))
        loader1.add_value('reply_nodes',response.url,deal_reply_nodes)

        item1=loader1.load_item()
        return item1