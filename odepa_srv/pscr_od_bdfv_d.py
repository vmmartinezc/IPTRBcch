print ("Importando time functions...")
from datetime import datetime, date, timedelta
print ("Importando time functions... done")

print ("Importando scrapy functions...")
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
print ("Importando scrapy functions... done")

print ("Setting actual time...")
dt = datetime.now().date()
print ("Setting actual time... done")

print ("Cambiando directorio... ")
import os
print ("Cambiando directorio... done")

print ("Setting process... ")
process = CrawlerProcess(get_project_settings())
print ("Setting process...  Done")

# 'followall' is the name of one of the spiders of the project.
process.crawl('od_bdfv_d', domain="")
process.crawl('lavegadelivery', domain="")
process.crawl('granja_express', domain="")
process.crawl('Super_despacho', domain="")
process.crawl('Vega_virtual', domain="")
process.crawl('Buen_Campo', domain="")
process.crawl('Foods', domain="")
process.crawl('Feria_Delivery', domain="")
process.crawl('El_verdulero',domain="")
process.crawl('Luki',domain="")


process.start() # the script will block here until the crawling is finished
