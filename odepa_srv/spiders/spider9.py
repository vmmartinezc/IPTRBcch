#!/usr/bin/env python
# -*- coding: utf-8 -*-

from scrapy.item import Field
from scrapy.item import Item
from scrapy.spiders import Spider
from scrapy.selector import Selector
from scrapy.contrib.loader import ItemLoader
from FrutasyVerduras.items import *

#Página : http://www.foods.cl/
class Foods(Spider):
    name="Foods "
    start_urls = ["http://www.foods.cl/categoria-producto/verduras/"]
    allows_domains = ['foods.cl']
    def parse(self, response):
        sel = Selector(response)
        #Filtrar unidades de medida, se encuentra dentro del string nombre
        for sel in sel.xpath('//main[@id="main"]/div/ul/li'):
            item = Atributos()
            item['Producto'] = sel.xpath('a/h3/text()').extract()
            item['Precio'] = sel.xpath('a/span/span/text()').extract()
            item['Fuente']="http://www.foods.cl/"

            #decodificar precio \xc2 \xa0
            #Opcional convertir a string y manipular datos
            #p = (item['Producto'][0]).encode('utf-8')
            #datos_precio = (item['Precio'][0]).encode('utf-8').strip("$")
            #row = {'Producto': p, 'Precio': datos_precio,'Fuente': item['Fuente'], 'Observaciones':p[1]}
            print (item)