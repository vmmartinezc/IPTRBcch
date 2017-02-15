#!/usr/bin/env python
# -*- coding: utf-8 -*-

from scrapy.item import Field
from scrapy.item import Item
from scrapy.spiders import Spider
from scrapy.selector import Selector
from scrapy.contrib.loader import ItemLoader
from bs4 import BeautifulSoup
from selenium import webdriver

from odepa_srv.items import *
#Página : http://www.superdespacho.cl

class SuperDespacho(Spider):
    name="Super despacho "
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
        	#Opcional
        	#item['Producto'] = td[0].renderContents()
            #item['Precio'] = td[1].get_text()
            #item['Fuente'] = "www.superdespacho.cl/"
            #Decodificar
        	row ={'Producto':str(td[0].renderContents()).lstrip(" ") ,'Precio':td[1].get_text().lstrip(" "), 'Fuente':"www.superdespacho.cl/" }
        	print (row)
