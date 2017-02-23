#!/usr/bin/env python
# -*- coding: utf-8 -*-

from scrapy.item import Field
from scrapy.item import Item
from scrapy.spiders import Spider
from scrapy.selector import Selector
from scrapy.contrib.loader import ItemLoader
#from bs4 import BeautifulSoup
#from selenium import webdriver
import re
from odepa_srv.items import *
#Página : http://www.superdespacho.cl

class SuperDespacho(Spider):
    name="Super_despacho"
    start_urls = ["http://www.superdespacho.cl/"]
    allow_domains = ['superdespacho.cl']


    def parse(self, response):
        url = "http://www.superdespacho.cl/"
        driver = webdriver.Chrome()
        driver.get(url)
		#Se obtiene la fuente  de la pegina obtenida
        html = driver.page_source 
        s = BeautifulSoup(html,'html.parser')
        precios = s.find_all('tr', 'ng-scope')
        for td in precios:
            td = td.find_all('td')
            item = OdepaSrvItem.inicializar(OdepaSrvItem())
            item['producto'] = str(td[0].renderContents().strip())
            #Formato de ejemplo de precio :  $2.300 por kilo
            precio = td[1].get_text().strip("\n").strip().replace(".","")
            pat = re.compile('\$\d{1,5}')    #ej. $3300
            sub_precio = pat.search(precio)
            if sub_precio:
                item['precio'] = sub_precio.group().strip("$")
                unidad_tmp = precio.replace(sub_precio.group(),"")
                unidad_norm = Normalization.general(unidad_tmp)
                item['unidad'] = unidad_norm['unidad']
                item['cantidad'] = unidad_norm['cantidad']
                
            item['fuente'] = "www.superdespacho.cl/"
            yield (item)
