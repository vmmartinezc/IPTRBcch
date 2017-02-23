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

# 'followall' is the name of one of the spiders of the project.
process.crawl('od_bdfv_d', domain="")
process.crawl('lavegadelivery', domain="") #spider1
process.crawl('Todo_Fruta', domain="") #spider2
process.crawl('verdurasyfrutas',domain="")#spider3
process.crawl('granja_express', domain="")#spider4
#process.crawl('Super_despacho', domain="")
process.crawl('Vega_virtual', domain="")#spider6
process.crawl('fullmercado',domain="")#spider7
process.crawl('Buen_Campo', domain="")
process.crawl('Foods', domain="")
process.crawl('Feria_Delivery', domain="")#spider10
process.crawl('El_verdulero',domain="")
#process.crawl('jumbo',domain="")
process.crawl('Luki',domain="") #spider13
process.crawl('La_chacra',domain="") #spider14
process.crawl('Manolo',domain="") #spider15
process.crawl('verdulero',domain="") #spider16
process.crawl('Tottus',domain="") #spider18



process.start() # the script will block here until the crawling is finished


