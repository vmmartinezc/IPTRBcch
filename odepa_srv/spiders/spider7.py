#!/usr/bin/env python
# -*- coding: utf-8 -*-

from scrapy.item import Field
from scrapy.item import Item
from scrapy.spiders import Spider
from scrapy.selector import Selector
from scrapy.contrib.loader import ItemLoader
from FrutasyVerduras.items import *

#Página : https://www.fullmercado.cl/

class FullMercado(Spider):
    name="Vega virtual "
    start_urls = ["https://www.fullmercado.cl/tienda/"]
    def parse(self, response):
        sel = Selector(response)
        item1 = Atributos()
        item2 = Atributos()
        verduras = sel.xpath('//div[@class="et_pb_module et_pb_shop  et_pb_shop_1"]/div/ul/li')
        for sel in verduras:
            item1['Producto'] = sel.xpath('a/h3/text()').extract()
            item1['Precio'] = sel.xpath('a/span[2]/span/text()').extract()
            print item1

        frutas = sel.xpath('//div[@class="et_pb_module et_pb_shop  et_pb_shop_2"]/div/ul/li') 
        for sel in frutas:
            item2['Producto'] = sel.xpath('a/h3/text()').extract()
            item2['Precio'] = sel.xpath('a/span[2]/span/text()').extract()
            print item2

