#!/usr/bin/env python
# -*- coding: utf-8 -*-

from scrapy.spiders import Spider
from scrapy.selector import Selector
from odepa_srv.items import *
#Página : http://www.lachacra.cl/

class Chacra(Spider):
    name="laChacra"
    #paginación maximo de 100
    start_urls = ["http://www.lachacra.cl/13-verdur?n=100&id_category=13",
    				"http://www.lachacra.cl/14-frut?n=100&id_category=14"]
    allow_domains = ['lachacra.cl']
    def parse(self, response):
        sel = Selector(response)
        for sel in sel.xpath('//ul[@id="product_list"]/li'):
            if (sel.xpath('div[1]/h3/a/text()').extract() and sel.xpath('div[2]/span[1]/text()').extract()):
                item = OdepaSrvItem.inicializar(OdepaSrvItem())
                item['producto'] = sel.xpath('div[1]/h3/a/text()').extract()[0]
                item['precio'] = sel.xpath('div[2]/span[@class="price"]/text()').extract()[0].strip("$").replace(".","")
                #unidad etiqueta dentro de otra
                #Si existe se manipulara, sino queda como vacio
                if sel.xpath('//p[@class="product_desc"]/a/p/text()').extract():
                    item['unidad']= sel.xpath('//p[@class="product_desc"]/a/p/text()').extract()[0]
                item['fuente'] = "www.lachacra.cl"
                yield (item)

                