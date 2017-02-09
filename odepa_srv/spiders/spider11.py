#!/usr/bin/env python
# -*- coding: utf-8 -*-

from scrapy.item import Field
from scrapy.item import Item
from scrapy.spiders import Spider
from scrapy.selector import Selector
from scrapy.contrib.loader import ItemLoader
from FrutasyVerduras.items import *

#Página : http://www.elverdulero.cl
class Verdulero(Spider):
    name="El verdulero "
    start_urls = ["http://www.elverdulero.cl/verduras/"]

    def parse(self, response):
        sel = Selector(response)
        verdurasfrutas = sel.xpath('//div[@id="mainZone"]/div/div/div')
        for sel in verdurasfrutas:
            item = Atributos()
            item['Producto'] = sel.xpath('h3/a/text()').extract()
            item['Precio'] = sel.xpath('div/p[2]/ins/text()').extract()
            item['Fuente'] = "http://www.elverdulero.cl"
            yield item

