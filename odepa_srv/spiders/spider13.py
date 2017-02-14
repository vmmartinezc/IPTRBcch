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
    start_urls = ["https://www.luki.cl/shop/category/frutos-secos-175",
                "https://www.luki.cl/shop/category/frutos-secos-175/page/2?ppg=False"]
    allow_domains = ['luki.cl']

    def parse(self, response):
        sel = Selector(response)
        for sel in sel.xpath('//section[@id="product-name"]'):
            item = Atributos()
            item['Producto'] = sel.xpath('div[1]/center/h6/a/text()').extract()
            item['Precio'] = sel.xpath('div[2]/b/span[2]/text()').extract()
            item['Fuente']="http://www.luki.cl/"
            
            #Opcional convertir a string y manipular datos
            p = (item['Producto'][0]).encode('utf-8')#.split('-')
            datos_precio = (item['Precio'][0]).encode('utf-8').strip("$")
            row = {'Producto': p, 'Precio': datos_precio,'Fuente': item['Fuente'], 'Observaciones':""}
            print (row)
