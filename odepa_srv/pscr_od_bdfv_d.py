from datetime import datetime, date, timedelta
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from spiders.od_bdfv_d import *


process = CrawlerProcess(get_project_settings())

# 'followall' is the name of one of the spiders of the project.
process.crawl('OdepaBdfvSpider', domain="")
process.start() # the script will block here until the crawling is finished

