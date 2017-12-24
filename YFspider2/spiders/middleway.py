from scrapy.spiders import CrawlSpider,Rule
from scrapy.linkextractor import LinkExtractor
import scrapy




class middleway(CrawlSpider):
    name = 'middleway'
    start_urls=['http://woeser.middle-way.net/']
    headers={
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36',
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    }


    rules =  (
        Rule(LinkExtractor(allow='http\:\/\/woeser\.middle\-way\.net\/\d{4}\/\d{1,2}\/[\S|\s]{1,12}\.html',),callback='parse_more',follow=True),
    )


    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url,headers=self.headers)



    def parse_more(self,response):
        print 'in parseMore'
        print response.xpath('#Blog1 > div.blog-posts.hfeed > div > div > div > div.post.hentry > h3').extract