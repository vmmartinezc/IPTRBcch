#!/usr/bin/env python
# -*- coding: utf-8 -*-

from scrapy.item import Field
from scrapy.item import Item
from scrapy.spiders import Spider
from scrapy.selector import Selector
from scrapy.contrib.loader import ItemLoader
from FrutasyVerduras.items import *

#Página : http://www.lachacra.cl/

class Chacra(Spider):
    name="La chacra "
    #paginación maximo de 100
    start_urls = ["http://www.lachacra.cl/13-verdur?n=100&id_category=13"]

    def parse(self, response):
        item = Atributos()
        sel = Selector(response)
        verdurasfrutas = sel.xpath('//ul[@id="product_list"]/li')

        for sel in verdurasfrutas:
            item['Producto'] = sel.xpath('div[1]/h3/a/text()').extract()
            item['Precio'] = sel.xpath('div[2]/span[1]/text()').extract()
            item['Fuente'] = "www.lachacra.cl"
            yield item