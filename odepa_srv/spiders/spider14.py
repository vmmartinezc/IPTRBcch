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
    #paginación maximo de 100
    start_urls = ["http://www.lachacra.cl/13-verdur?n=100&id_category=13",
    				"http://www.lachacra.cl/14-frut?n=100&id_category=14"]
    allow_domains = ['lachacra.cl']
    def parse(self, response):
        sel = Selector(response)
        for sel in sel.xpath('//ul[@id="product_list"]/li'):
            item = Atributos()
            item['Producto'] = sel.xpath('div[1]/h3/a/text()').extract()
            item['Precio'] = sel.xpath('div[2]/span[1]/text()').extract()
            item['Observaciones']= sel.xpath('div[1]/p/a/text()').extract()
            item['Fuente'] = "www.lachacra.cl"

            #Opcional convertir a string y manipular datos
            p = (item['Producto'][0]).encode('utf-8')#.split('-')
            datos_precio = (item['Precio'][0]).encode('utf-8').strip("$")
            row = {'Producto': p, 'Precio': datos_precio,'Fuente': item['Fuente'], 'Observaciones':item['Observaciones']}

            yield row