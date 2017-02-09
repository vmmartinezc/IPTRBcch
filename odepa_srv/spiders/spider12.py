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
    #//*[@id="mainZone"]/div[1]/div/div[5]/div/p[2]/ins
    #//*[@id="mainZone"]/div[1]/div/div[6]/h3/a
    def parse(self, response):
    	url = "http://www.jumbo.cl/FO/CategoryDisplay?cab=4006&int=11&ter=-1"
        sel = Selector(response)
        #Se trabajará con el browser Chrome
        driver = webdriver.Chrome()
        driver.get(url)
		#Se obtiene la fuente  de la pegina obtenida
        html = driver.page_source 
		#-Se transforma la url a html con Beautifulsoup
        html2 = BeautifulSoup(html, "html.parser")
        regiones = html2.find(id='tabla_productos')
        regiones = html.find_elements_by_xpath("//div[@id='tabla_productos']")
        #regiones=BeautifulSoup(regiones, "html.parser")
        driver.quit()
        print regiones
        #verdurasfrutas = sel.css('#div_productos')
        #verdurasfrutas = regiones.xpath('//tbody')
        #html2 = BeautifulSoup(urlopen(url))
        print verdurasfrutas
        print len(verdurasfrutas)
        #No obtiene los datos
        '''for sel in verdurasfrutas:
            item = Atributos()
            item['Producto'] = sel.xpath('h3/a/text()').extract()
            item['Precio'] = sel.xpath('div/p[2]/ins/text()').extract()
            yield item'''