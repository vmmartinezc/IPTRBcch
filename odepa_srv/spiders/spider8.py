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
    allow_domains =['buencampo.cl']
    def parse(self, response):
        sel = Selector(response)
        item = Atributos()
        for sel in sel.xpath('//div[@class="view-content"]/div'):
            item['Producto'] = sel.xpath('article/h2/a/text()').extract()
            item['Precio'] = sel.xpath('article/div/div[2]/div/div/text()').extract()
            item['Fuente'] = "https://www.buencampo.cl/"
            #Opcional convertir a string y manipular datos
            p = (item['Producto'][0]).encode('utf-8').split('-')
            datos_precio = (item['Precio'][0]).encode('utf-8').strip("$")
            row = {'Producto': p[0], 'Precio': datos_precio,'Fuente': item['Fuente'], 'Observaciones':p[1]}
            print (row)
