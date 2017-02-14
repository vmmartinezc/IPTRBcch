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
    #Estructura html igual.
    start_urls = ["http://laferiadelivery.cl/categoria-producto/feria/verduras",
    			 "http://laferiadelivery.cl/categoria-producto/feria/frutas"]
    allow_domains = ['laferiadelivery.cl']
    def parse(self, response):
        sel = Selector(response)
        for sel in sel.xpath('//ul[@class="products"]/li'):
            item = Atributos()
            item['Producto'] = sel.xpath('h3/text()').extract()
            item['Precio'] = sel.xpath('.//span[@class="woocommerce-Price-amount amount"]/text()').extract()
            item['Fuente'] = "http://laferiadelivery.cl/"
            print (item)

