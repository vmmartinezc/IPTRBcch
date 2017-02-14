#!/usr/bin/env python
# -*- coding: utf-8 -*-

from scrapy.item import Field
from scrapy.item import Item
from scrapy.spiders import Spider
from scrapy.selector import Selector
from scrapy.contrib.loader import ItemLoader
from FrutasyVerduras.items import *

#Página : http://www.manolofrutasyverduras.cl/

class manolofrutasyverduras(Spider):
    name="Manolo frutas y verduras "
    start_urls = ["http://www.manolofrutasyverduras.cl/"]

    def parse(self, response):
        item = Atributos()
        sel = Selector(response)
        #verificar path
        verdurasfrutas = sel.xpath('//div[@class="nsp_art"]')
        for sel in verdurasfrutas:
            item['Producto'] = sel.xpath('div[1]/h4/a/text()').extract()
            item['Precio'] = sel.xpath('div/div[2]/form/span/text()').extract()
            item['Fuente'] = "www.manolofrutasyverduras.cl"

            #Opcional convertir a string y manipular datos
            p = (item['Producto'][0]).encode('utf-8')#.split('-')
            datos_precio = (item['Precio'][0]).encode('utf-8').strip("$")
            row = {'Producto': p, 'Precio': datos_precio,'Fuente': item['Fuente'], 'Observaciones':""}
            yield row
  