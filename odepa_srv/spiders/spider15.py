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
    start_urls = ["http://www.manolofrutasyverduras.cl/"]

    def parse(self, response):
        item = Atributos()
        sel = Selector(response)
        #verificar path
        verdurasfrutas = sel.xpath('//div[@id="nsp-nsp_152"]/div/div[2]/div/div[1]')
        for sel in verdurasfrutas:
            item['Producto'] = sel.xpath('div/h4/a/text()').extract()
            item['Precio'] = sel.xpath('div[2]/form/span/text()').extract()
            item['Fuente'] = "www.manolofrutasyverduras.cl"
            yield item