#!/usr/bin/env python
# -*- coding: utf-8 -*-

from scrapy.item import Field
from scrapy.item import Item
from scrapy.spiders import Spider
from scrapy.selector import Selector
from scrapy.contrib.loader import ItemLoader
from FrutasyVerduras.items import *

#Página : http://www.elverdulero.cl
class verdulero(Spider):
    name="El verdulero "
    start_urls = ["http://www.elverdulero.cl/verduras/",
                    "http://www.elverdulero.cl/frutas/"]
    allow_domains= ['elverdulero.cl']

    def parse(self, response):
        sel = Selector(response)
        #No obtiene los datos
        for sel in sel.xpath('//div[@id="mainZone"]/div/div/div'):
            item = Atributos()
            item['Producto'] = sel.xpath('h3/a/text()').extract()
            item['Precio'] = sel.xpath('div/p[2]/ins/text()').extract()
            item['Fuente'] = "http://www.elverdulero.cl"
            #Eliminar vacíos
            #Opcional convertir a string y manipular datos
            p = (item['Producto'][0]).encode('utf-8')#.split('-')
            datos_precio = (item['Precio'][0]).encode('utf-8').strip("$")
            row = {'Producto': p, 'Precio': datos_precio,'Fuente': item['Fuente'], 'Observaciones':""}
            yield row 
