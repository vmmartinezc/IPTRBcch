#!/usr/bin/env python
# -*- coding: utf-8 -*-

from scrapy.spiders import Spider
from scrapy.selector import Selector
from odepa_srv.items import *
#Página : http://www.elverdulero.cl
class verdulero(Spider):
    name="verdulero"
    start_urls = ["http://www.elverdulero.cl/verduras/",
                    "http://www.elverdulero.cl/frutas/"]
    allow_domains= ['elverdulero.cl']

    def parse(self, response):
        sel = Selector(response)
        for sel in sel.xpath('//div[@id="mainZone"]/div/div/div'):
            if sel.xpath('h3/a/text()').extract() and sel.xpath('div/p[2]/ins/text()').extract():
                item  = OdepaSrvItem()
                item['producto'] = sel.xpath('h3/a/text()').extract()
                item['precio'] = sel.xpath('div/p[2]/ins/text()').extract()[0].strip("$")
                item['fuente'] = "http://www.elverdulero.cl"
                print (item) 
