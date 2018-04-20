#_*_coding:utf-8_*_
from scrapy.spiders import Rule
from scrapy_redis.spiders import RedisCrawlSpider
from scrapy.linkextractor import LinkExtractor
from YFspider2.items import YfspiderspeakItem
# from scrapy.loader import
from YFspider2.othermodule.itemloader_ll import itemloader_ll
from scrapy.loader import ItemLoader
from scrapy.loader.processors import Join,TakeFirst,MapCompose
import scrapy
import time
import datetime




class uyghurcongress(RedisCrawlSpider):
    name = 'uyghurcongress'
    start_urls=['http://www.uyghurcongress.org/']
    # redis_key='middleway:urls'
    headers={
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36',
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    }


    rules =  (
        Rule(LinkExtractor(allow='http\:\/\/www\.uyghurcongress\.org\/en\/\?p\=\d*',),callback='parse_content',follow=True),
        Rule(LinkExtractor(allow='http\:\/\/www\.uyghurcongress\.org\/.*',),follow=True)
    )


    # def start_requests(self):
    #     for url in self.start_urls:
    #         yield scrapy.Request(url=url,headers=self.headers)



    def parse_content(self,response):
        print ('in parseMore')


        def deal_publish_time(publish_time_list=[]):
            if not publish_time_list:
                print ('time is None')
                return None
            mouthstr=publish_time_list[0]

            mouth_eng_to_num = {
                'January': '01',
                'February': '02',
                'March': '03',
                'April ': '04',
                'May': '05',
                'June': '06',
                'July': '07',
                'August': '08',
                'September': '09',
                'October': '10',
                'November': '11',
                'December': '12'
            }

            mouth_num=mouth_eng_to_num[str(mouthstr)]
            day_str_raw=str(publish_time_list[1])
            if len(day_str_raw)<2:
                day_str_raw='0'+day_str_raw

            publish_time=str(publish_time_list[2])+'-'+mouth_num+'-'+day_str_raw+' 00:00:00'
            return publish_time


        def deal_reply_nodes(reply_nodes=None):
            reply_nodes_list=[]

            def deal_publishtime_inside(publishtime):
                publish_time = publishtime.replace('年', '-').replace('月', '-').replace('日', '')
                time_split_2 = publish_time.split(' ')

                data_str = time_split_2[0]
                data_str_list = data_str.split('-')
                mounth = data_str_list[1]
                day = data_str_list[2]
                if len(mounth) < 2:
                    mounth = '0' + mounth
                if len(day) < 2:
                    day = '0' + day
                data_str = data_str_list[0] + '-' + mounth + '-' + day

                time_split_2_part2 = time_split_2[1]
                if '下午' in time_split_2_part2:
                    time_part2_h_m = time_split_2_part2.replace('下午', '').split(':')
                    time_split_2_h = int(time_part2_h_m[0])
                    time_split_2_m = time_part2_h_m[1]
                    time_split_2_h_add = 12 + time_split_2_h

                    time_pm_finally = str(time_split_2_h_add) + ':' + time_split_2_m + ':00'
                    return data_str + ' ' + time_pm_finally
                elif '上午' in time_split_2_part2:
                    time_part2_h_m = time_split_2_part2.replace('上午', '').split(':')
                    time_split_2_h = int(time_part2_h_m[0])
                    time_split_2_m = time_part2_h_m[1]
                    time_split_2_h_add = time_split_2_h

                    if time_split_2_h_add < 10:
                        time_split_2_h_add = '0' + str(time_split_2_h)

                    time_am_finally = str(time_split_2_h_add) + ':' + time_split_2_m + ':00'
                    return data_str + ' ' + time_am_finally

            if reply_nodes:
                reply_nodes_list_eval=eval(reply_nodes[0])
                for one_reply_nodes in reply_nodes_list_eval:
                    content=one_reply_nodes['body']
                    publish_time_raw=one_reply_nodes['displayTime']
                    publish_time=deal_publishtime_inside(publish_time_raw)



                    id=one_reply_nodes['id']
                    publish_user_photo=one_reply_nodes['author']['avatarUrl']
                    publish_user=one_reply_nodes['author']['name']

                    child_reply_node={
                        'content':content,
                        'publish_time':publish_time,
                        'id':id,
                        'publish_user_href':'http:'+publish_user_photo if 'http' not in publish_user_photo else publish_user_photo,
                        'publish_user':publish_user
                    }
                    reply_nodes_list.append(child_reply_node)

                return reply_nodes_list
            else:
                return None


        loader1=ItemLoader(item=YfspiderspeakItem(),response=response)
        loader1.add_value('url',response.url)
        loader1.add_value('spider_time',time.time())
        loader1.add_xpath('title','//div[@class="post-content"]//h3[@class="post-title"]/text()',TakeFirst(),lambda x:x.strip())
        loader1.add_xpath('content','//div[@class="post-content"]//p/text()|//div[@class="post-content"]//h1/text()|//div[@class="post-content"]//h2/text()',lambda x:[i.strip() for i in x],Join())
        loader1.add_value('id',response.url.split('=')[1].split('.')[0].strip())
        loader1.add_xpath('img_urls','//div[@class="post-content"]//img/@src')
        loader1.add_value('publish_time',response.xpath('//div[@class="post-content"]//p[@class="post-meta"]').re('(\S*) (\d{1,2})\, (\d{4})'),deal_publish_time)
        # loader1.add_value('publish_user','degewa')
        # loader1.add_value('reply_count',response.selector.xpath('//*[@id="comments"]/h4/text()').re(ur'(\d{1,2}).*条评论'),lambda x:x[0] if x else 0)
        # loader1.add_value('reply_nodes',response.selector.re(ur'var items \= (\[.*?\])\;'),deal_reply_nodes)



        item=loader1.load_item()
        print (item)
        return item