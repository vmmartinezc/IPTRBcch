#!/usr/bin/env python
# -*- coding: utf-8 -*-

from scrapy.item import Field
from scrapy.item import Item
from scrapy.spiders import Spider
from scrapy.selector import Selector
from scrapy.contrib.loader import ItemLoader
from bs4 import BeautifulSoup

from FrutasyVerduras.items import *

#Página : http://www.superdespacho.cl

class SuperDespacho(Spider):
    name="Super despacho "
    start_urls = ["http://www.superdespacho.cl/"]
    def parse(self, response):
        sel = Selector(response)
        verdurasfrutas = sel.xpath('//tr[@class="ng-scope"]')
        print len(verdurasfrutas)
        for sel in verdurasfrutas:
            item = Atributos()
            item['Producto'] = sel.xpath('td[1]/text()').extract()
            item['Precio'] = sel.xpath('td[2]/text()').extract()
            item['Fuente'] = "www.superdespacho.cl/"
            yield item
        