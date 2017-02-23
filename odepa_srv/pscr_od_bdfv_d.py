#!/usr/bin/env python3
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

#print("Ruta actual:"+os.getcwd())
#os.chdir(os.path.join(os.getcwd(), 'spiders'))
#print("Ruta actual:"+os.getcwd())
print("Ruta actual: "+ os.getcwd())


# 'followall' is the name of one of the spiders of the project.
process.crawl('od_bdfv_d', domain="")
process.crawl('vegaDelivery', domain="") 
process.crawl('todoFruta', domain="") 
process.crawl('verdurasyfrutas',domain="")
process.crawl('granjaExp', domain="")
#process.crawl('superDesp', domain="")
process.crawl('vegaVirtual', domain="")
process.crawl('fullMercado',domain="")
process.crawl('buenCampo', domain="")
process.crawl('foods', domain="")
process.crawl('feriaDelivery', domain="")
process.crawl('verdulero',domain="")
#process.crawl('jumbo',domain="")
process.crawl('luki',domain="") 
process.crawl('laChacra',domain="") 
process.crawl('manolo',domain="") 
process.crawl('verdulero',domain="") 
process.crawl('tottus',domain="") 
#process.crawl('errback_example',domain="") Prueba de errores

process.start() # the script will block here until the crawling is finished


