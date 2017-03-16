import json

from scrapy.crawler import Crawler
from scrapy.contrib.loader import ItemLoader
from scrapy.contrib.loader.processor import Join, MapCompose, TakeFirst
from scrapy import log, signals, Spider, Item, Field
from scrapy.settings import Settings
from twisted.internet import reactor
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings



# define an item class
class DmozItem(Item):
    title = Field()
    link = Field()
    desc = Field()

# define a spider
class DmozSpider(Spider):
    name = "dmoz"
    allowed_domains = ["dmoz.org"]
    start_urls = [
        "http://www.dmoz.org/Computers/Programming/Languages/Python/Books/",
        "http://www.dmoz.org/Computers/Programming/Languages/Python/Resources/"
    ]

    def parse(self, response):
        for sel in response.xpath('//ul/li'):
            loader = DmozItemLoader(DmozItem(), selector=sel, response=response)
            loader.add_xpath('title', 'a/text()')
            loader.add_xpath('link', 'a/@href')
            loader.add_xpath('desc', 'text()')
            yield loader.load_item()


# callback fired when the spider is closed
def callback(spider, reason):
    stats = spider.crawler.stats.get_stats()  # collect/log stats?

    # stop the reactor
    reactor.stop()


# instantiate settings and provide a custom configuration
settings = CrawlerProcess(get_project_settings())
# instantiate a crawler passing in settings
crawler = Crawler(settings)

# instantiate a spider
spider = DmozSpider()

# configure signals
crawler.signals.connect(callback, signal=signals.spider_closed)

# configure and start the crawler
crawler.configure()
crawler.crawl(spider)
crawler.start()

# start logging
log.start()

# start the reactor (blocks execution)
reactor.run()