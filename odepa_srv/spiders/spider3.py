#!/usr/bin/env python
# -*- coding: utf-8 -*-

from scrapy.item import Field
from scrapy.item import Item
from scrapy.spiders import Spider
from scrapy.selector import Selector
from scrapy.contrib.loader import ItemLoader
from FrutasyVerduras.items import *

#Página : http://www.verduras-y-frutas.cl


class VerdurasyFrutas(Spider):
    name="verduras y frutas"
    start_urls = ["http://www.verduras-y-frutas.cl/filesweb/verduras-y-frutas.cl/carro.php"]
    
    def parse(self, response):
    	sel = Selector(response)
        #problema al entregar los tr desde el id de la tabla, 
        #se genera busqueda temporal por caracteristicas de tr
    	verdurasfrutas = sel.xpath('//tr[@align ="center"]')
        for sel in verdurasfrutas:
            item = Atributos()
            #falta precio
            item['Precio'] = sel.xpath('td[4]/text()').extract()
            item['Producto'] = sel.xpath('td[2]/a/b/text()').extract()
            item['Observaciones'] = sel.xpath('td[3]/center/text()').extract()
            item['Fuente'] = "www.verduras-y-frutas.cl"
            yield item
    	


