
#!/usr/bin/env python
# -*- coding: utf-8 -*-

from scrapy.item import Field
from scrapy.item import Item
from scrapy.spiders import Spider
from scrapy.selector import Selector
from scrapy.contrib.loader import ItemLoader
from odepa_srv.items import *
#from bs4 import BeautifulSoup
#from selenium import webdriver



#Página : http://www.jumbo.cl
class Jumbo(Spider):
    name="jumbo"
    start_urls = ["http://www.jumbo.cl/FO/CategoryDisplay?cab=4006&int=11&ter=-1"]
    allow_domains= ['jumbo.cl']

    def parse(self, response):
    	#Se trabajará con el browser Chrome
        driver = webdriver.Chrome()
        driver.get(self.start_urls[0])
        #Se obtiene la fuente  de la pegina obtenida
        html = driver.page_source 
        s = BeautifulSoup(html,'lxml')
        nombres = s.find_all(id ='ficha')
        precios = s.find_all('div', 'txt_precio_h')
        for i in range(len(nombres)):
            item = OdepaSrvItem.inicializar(OdepaSrvItem())
            item['producto'] = nombres[i].find('b').renderContents()
            item['precio']=  str(precios[i].renderContents()).strip("$")
            item ['fuente'] = "www.jumbo.cl"
            yield (item)
        	

