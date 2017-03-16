#!/usr/bin/env python
# -*- coding: utf-8 -*-

from scrapy.spiders import Spider
from scrapy.selector import Selector
from odepa_srv.items import *
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
#Página : http://www.lachacra.cl/

class Chacra(CrawlSpider):
    name="laChacra"
    #paginación maximo de 100
    start_urls = ["http://www.lachacra.cl/13-verdur?n=100&id_category=13",
    				"http://www.lachacra.cl/14-frut?n=100&id_category=14"]
    allow_domains = ['lachacra.cl']

    #Expresion regular que recorre verticalmente
    rules = (
        #Buscamos cualquier url que empiece con 1 a 3 digitos, lo siga un '-' y que despues tenga cualquier texto pero que termine con .html
            Rule(LinkExtractor(allow=('\d{1,3}-.*\.html$')), callback='parse_items'),
        )

    def parse_items(self, response):
        sel = Selector(response)
        if sel.xpath('//*[@id="pb-left-column"]/h2/text()').extract() and sel.xpath('//*[@id="our_price_display"]/text()').extract():
            item = OdepaSrvItem.inicializar(OdepaSrvItem())
            item['producto'] = sel.xpath('//*[@id="pb-left-column"]/h2/text()').extract()[0]
            item['precio'] = sel.xpath('//*[@id="our_price_display"]/text()').extract()[0].strip("$").replace(".","")
            if sel.xpath('//*[@id="product_reference"]/span/text()').extract():
                item['unidad']= sel.xpath('//*[@id="product_reference"]/span/text()').extract()[0]
            item['fuente'] = "www.lachacra.cl"
            yield (item)

                