#!/usr/bin/env python
# -*- coding: utf-8 -*-

from scrapy.spiders import Spider
from scrapy.selector import Selector
from odepa_srv.items import *
#Página : http://www.foods.cl/
class Foods(Spider):
    name="Foods "
    start_urls = ["http://www.foods.cl/categoria-producto/verduras/"]
    allows_domains = ['foods.cl']
    def parse(self, response):
        sel = Selector(response)
        #Filtrar unidades de medida, se encuentra dentro del string nombre
        for sel in sel.xpath('//main[@id="main"]/div/ul/li'):
            if (sel.xpath('a/h3/text()').extract() and sel.xpath('a/span/span/text()').extract()):
                item  = OdepaSrvItem()
                aux = sel.xpath('a/h3/text()').extract()[0].title().split("(")
                item['producto'] = aux[0]
                item['precio'] = sel.xpath('a/span/span/text()').extract()[0].strip("$").strip("\xa0")
                item['fuente'] ="http://www.foods.cl/"
                item['unidad'] = aux[1].strip(")")
                print (item)