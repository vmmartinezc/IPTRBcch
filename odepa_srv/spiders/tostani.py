#!/usr/bin/env python
# -*- coding: utf-8 -*-
from scrapy.spiders import Spider
from scrapy.selector import Selector
from odepa_srv.items import *
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor


class tostani(CrawlSpider):
    name="tostani"
    #Estructura html igual.
    start_urls = ["http://www.tostani.cl/productos/frutos-secos",
                  "http://www.tostani.cl/productos/"]
    allow_domains = ['laferiadelivery.cl']
    #Expresion regular que recorre verticalmente
    rules = (
            Rule(LinkExtractor(allow=('(frutos-secos/page/\d+|frutos-secos/$)')), callback='parse_items'),
        )
    def parse_items(self, response):
        sel = Selector(response)
        for sel in sel.xpath('//*[@id="content"]/ul/li'):
            if sel.xpath('a[1]/h3/text()').extract() and sel.xpath('a[1]/span/span/text()').extract():
                item = OdepaSrvItem.inicializar(OdepaSrvItem())
                item['producto'] = sel.xpath('a[1]/h3/text()').extract()[0]
                item['precio'] = sel.xpath('a[1]/span/span/text()').extract()[0].replace(".","").strip("$")
                item['fuente'] = "www.tostani.cl"

                unidad_norm = Normalization.tostani(item['producto'])
                item['unidad'] = unidad_norm['unidad']
                item['cantidad'] = unidad_norm['cantidad']
                item['producto'] = unidad_norm['producto']
                yield (item)