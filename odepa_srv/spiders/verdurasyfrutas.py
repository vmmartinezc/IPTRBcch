#!/usr/bin/env python
# -*- coding: utf-8 -*-

from scrapy.spiders import Spider
from scrapy.selector import Selector
from odepa_srv.items import *
from scrapy_splash import SplashRequest

#Página : http://www.verduras-y-frutas.cl


class VerdurasyFrutas(Spider):
    name="verdurasyfrutas"
    start_urls = ["http://www.verduras-y-frutas.cl/filesweb/verduras-y-frutas.cl/carro.php"]
    allow_domains = ['verduras-y-frutas.cl']

    def start_requests(self):
        for link in self.start_urls:
            yield SplashRequest(
                link,
                self.parse_link, #Callback 
                endpoint='render.json',
                args={
                    'har': 1,
                    'html': 1,
                    'wait': 10,
                },
                dont_filter=True

            )
    def parse_link(self, response):
        #Los unicos input hidden en la pagina contienen los precios de las verduras
        #precios =  sel.xpath('.//input[@type="hidden"]/@value').extract()
        for sel in response.xpath('.//tr[@align ="center"]'):
            if (sel.xpath('td[2]/a/b/text()').extract()):
                item = OdepaSrvItem.inicializar(OdepaSrvItem())                
                item['precio'] = sel.xpath('.//input[@type="hidden"]/@value').extract()[0].strip("$").replace(",","")
                item['producto'] = sel.xpath('td[2]/a/b/text()').extract()[0].title()
                item['unidad'] = sel.xpath('td[3]/center/text()').extract()[0].strip("\t").strip("\n")
                item['fuente'] = "www.verduras-y-frutas.cl"
                yield (item)
    	
