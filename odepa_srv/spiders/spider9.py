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
    def parse(self, response):
        sel = Selector(response)
        verdurasfrutas = sel.xpath('//main[@id="main"]/div/ul/li')
        #Filtrar unidades de medida, se encuentra dentro del string nombre
        for sel in verdurasfrutas:
            item = Atributos()
            item['Producto'] = sel.xpath('a/h3/text()').extract()
            item['Precio'] = sel.xpath('a/span/span/text()').extract()
            item['Fuente']="http://www.foods.cl/"
            yield item