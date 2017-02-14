#!/usr/bin/env python
# -*- coding: utf-8 -*-

from scrapy.item import Field
from scrapy.item import Item
from scrapy.spiders import Spider
from scrapy.selector import Selector
from scrapy.contrib.loader import ItemLoader
from FrutasyVerduras.items import *
from bs4 import BeautifulSoup
from selenium import webdriver



#Página : http://www.jumbo.cl
class Jumbo(Spider):
    name="Jumbo "
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
        item = Atributos()

        for i in xrange(len(nombres)):
            item['Producto'] = nombres[i].find('b').renderContents()
            item['Precio']=  precios[i].renderContents().strip("$")
            item ['Fuente'] = "http://www.jumbo.cl"
            print (item)
        	