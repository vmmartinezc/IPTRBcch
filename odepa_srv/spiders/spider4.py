# -*- coding: utf-8 -*-

from scrapy.spiders import Spider
from scrapy.selector import Selector
from odepa_srv.items import *

# Página  : www.lagranjaexpress.cl/

class GranjaExpress(Spider):
    name="La granja express"
    start_urls = ["http://www.lagranjaexpress.cl/reparto-de-frutas-y-verduras-en-san-pedro-de-la-paz.html"]
    allow_domains = ['lagranjaexpress.cl']

    def parse(self, response):
        sel = Selector(response)
        for sel in sel.xpath('//form[@name="formulario"]/table[4]/tr'):
            if(sel.xpath('.//td[3]/text()').extract() and sel.xpath('.//td[5]/div/text()').extract()):
                item  = OdepaSrvItem()
                item['producto'] = sel.xpath('.//td[3]/text()').extract()[0].strip("\xa0").title()
                item['precio'] = sel.xpath('.//td[5]/div/text()').extract()[0].strip("\xa0")
                item['unidad'] = sel.xpath('.//td[4]/div/text()').extract()
                item ['fuente'] = "www.lagranjaexpress.cl"
                print (item)
