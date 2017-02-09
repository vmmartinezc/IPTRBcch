#!/usr/bin/env python
# -*- coding: utf-8 -*-

from scrapy.item import Field
from scrapy.item import Item
from scrapy.spiders import Spider
from scrapy.selector import Selector
from scrapy.contrib.loader import ItemLoader
from FrutasyVerduras.items import *

#Página : http://laferiadelivery.cl/
class FeriaDelivery(Spider):
    name="La Feria Delivery "
    start_urls = ["http://laferiadelivery.cl/categoria-producto/feria/verduras"]
    #//*[@id="ajax-content-wrap"]/div[1]/div/div/ul/li[1]/div/div/div[1]/span/span/text()
    #////*[@id="ajax-content-wrap"]/div[1]/div/div/ul/li[8]/div/div/div[1]/span/span
    #//*[@id="ajax-content-wrap"]/div[1]/div/div/ul/li[1]/h3
    def parse(self, response):
        sel = Selector(response)
        verdurasfrutas = sel.xpath('//ul[@class="products"]/li')
        for sel in verdurasfrutas:
            item = Atributos()
            item['Producto'] = sel.xpath('h3/text()').extract()
            #Revisar Precio
            item['Precio'] = sel.xpath('div/div/div[1]/span/text()').extract()
            item['Fuente'] = "http://laferiadelivery.cl/"
            yield item

