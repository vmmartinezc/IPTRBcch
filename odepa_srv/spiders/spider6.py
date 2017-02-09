#!/usr/bin/env python
# -*- coding: utf-8 -*-

from scrapy.item import Field
from scrapy.item import Item
from scrapy.spiders import Spider
from scrapy.selector import Selector
from scrapy.contrib.loader import ItemLoader
from bs4 import BeautifulSoup

from FrutasyVerduras.items import *

#Página : http://www.vegavirtual.cl

class VegaVirtual(Spider):
    name="Vega virtual "
    start_urls = ["http://www.vegavirtual.cl"]
    def parse(self, response):
        sel = Selector(response)
        verdurasfrutas = sel.xpath('//div[@class="row products-loop products-grid row-count-6"]/div')
        for sel in verdurasfrutas:
            item = Atributos()
            #//*[@id="st-container"]/div[1]/div/div/div/div[3]/div/div/div/div[2]/div[2]/div/div/div/div[1]/div/div[2]/span/span
            item['Producto'] = sel.xpath('div/div[2]/div[1]/a/text()').extract()
            item['Precio'] = sel.xpath('div/div[2]/span/span/text()').extract()
            item['Fuente'] = "http://www.vegavirtual.cl"
            yield item
