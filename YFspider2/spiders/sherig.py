import scrapy
from scrapy.spider import Spider
from scrapy.spider import CrawlSpider
from scrapy.spiders import Rule
from scrapy.linkextractor import LinkExtractor



class sherig(CrawlSpider):
    name = 'sherig'
    # start_urls=['http://www.sherig.org/tb/page/{}/'.format(str(i)) for i in range(1,10)]
    start_urls=['http://www.sherig.org/tb/']

    rules = (
        # Extract links matching 'category.php' (but not matching 'subsection.php')
        # and follow links from them (since no callback means follow=True by default).
        Rule(LinkExtractor(allow=('sherig.org',),)),

        # Extract links matching 'item.php' and parse them with the spider's method parse_item
        Rule(LinkExtractor(allow=('sherig.org',)), callback='parse_item'),
    )

    def parse(self, response):
        print response.url