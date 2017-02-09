#!/usr/bin/env python
# -*- coding: utf-8 -*-

from scrapy.item import Field
from scrapy.item import Item
from scrapy.spiders import Spider
from scrapy.selector import Selector
from scrapy.contrib.loader import ItemLoader
from FrutasyVerduras.items import *

#Página : https://www.buencampo.cl/

class Buencampo(Spider):
    name="Buen Campo "
    start_urls = ["http://buencampo.cl/categoria-producto/frutas-y-verduras"]
    def parse(self, response):
        sel = Selector(response)
        verdurasfrutas = sel.xpath('//div[@class="view-content"]/div')
        for sel in verdurasfrutas:
            item = Atributos()
            item['Producto'] = sel.xpath('article/h2/a/text()').extract()
            item['Precio'] = sel.xpath('article/div/div[2]/div/div/text()').extract()
            item['Fuente'] = "https://www.buencampo.cl/"
            yield item
