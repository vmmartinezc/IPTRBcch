#!/usr/bin/env python
# -*- coding: utf-8 -*-

from scrapy.item import Field
from scrapy.item import Item
from scrapy.spiders import Spider
from scrapy.selector import Selector
from scrapy.contrib.loader import ItemLoader
from FrutasyVerduras.items import *

#Página : https://www.luki.cl/
class luki(Spider):
    name="Luki "
    start_urls = ["https://www.luki.cl/shop/category/frutos-secos-175"]
    def parse(self, response):

        sel = Selector(response)
        frutossecos = sel.xpath('//div[@id="products_grid"]/div')
        print frutossecos
        for sel in frutossecos:
            item = Atributos()
            item['Producto'] = sel.xpath('a/h3/text()').extract()
            item['Precio'] = sel.xpath('a/span/span/text()').extract()
            item['Fuente']="http://www.luki.cl/"
            yield item