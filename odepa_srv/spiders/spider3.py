#!/usr/bin/env python
# -*- coding: utf-8 -*-

from scrapy.spiders import Spider
from scrapy.selector import Selector
from odepa_srv.items import *
#Página : http://www.verduras-y-frutas.cl


class VerdurasyFrutas(Spider):
    name="verduras y frutas"
    start_urls = ["http://www.verduras-y-frutas.cl/filesweb/verduras-y-frutas.cl/carro.php"]
    allow_domains = ['verduras-y-frutas.cl']
    def parse(self, response):
        sel = Selector(response)
        #Los unicos input hidden en la pagina contienen los precios de las verduras
        precios =  sel.xpath('.//input[@type="hidden"]/@value').extract()
        #print len(sel.xpath('//tr[@align ="center"]'))
        for sel in sel.xpath('//tr[@align ="center"]'):
            if (sel.xpath('td[2]/a/b/text()').extract() ):
                item  = OdepaSrvItem()
                #falta precio
                #item['precio'] = sel.xpath('input[@type="hidden"]/@value').extract()[0].strip("$").replace(",","")
                item['producto'] = sel.xpath('td[2]/a/b/text()').extract()[0].title()
                item['unidad'] = sel.xpath('td[3]/center/text()').extract()[0].strip("\t").strip("\n")
                item['fuente'] = "www.verduras-y-frutas.cl"
                print (item)
    	


