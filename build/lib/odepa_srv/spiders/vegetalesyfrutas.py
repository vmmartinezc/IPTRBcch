#!/usr/bin/env python
# -*- coding: utf-8 -*-

from scrapy.spiders import Spider
from scrapy.selector import Selector
from odepa_srv.items import  OdepaSrvItem
#Página : http://www.elverdulero.cl
class VegyFru(Spider):
    name="vegetalesyFrutas"
    start_urls = ["http://www.vegetalesyfrutas.cl/productos-3/frutas.html",
                    "http://www.vegetalesyfrutas.cl/productos-2/verduras.html",
                    "http://www.vegetalesyfrutas.cl/productos-20/frutos-secos.html",
                    "http://www.vegetalesyfrutas.cl/productos-5/frutas-y-verduras-congeladas.html"]
    allow_domains = ['vegetalesyfrutas.cl']

    def parse(self, response):
        sel = Selector(response)
        for sel in sel.xpath('//table[@id="productos"]/tbody/tr'):
            if(sel.xpath('td[2]/a/text()').extract() and sel.xpath('td[3]/text()').extract()):
                item = OdepaSrvItem.inicializar(OdepaSrvItem())
                item['producto'] = sel.xpath('td[2]/a/text()').extract()[0].title()
                item['precio'] = sel.xpath('td[3]/text()').extract()[0].strip().strip("$").replace(".","")
                item['fuente'] = "www.vegetalesyfrutas.cl"
                #La unidad de medida y su cantidad se encuentra en el nombre, por lo tanto es el parámatro de entrada para normalizar
                item['unidad'] = item['producto']
                '''unidad_norm = Normalization.vegetalesyfrutas(unidad_tmp)
                item['unidad'] = unidad_norm['unidad']
                item['cantidad'] = unidad_norm['cantidad']
                item['producto'] = unidad_norm['producto']  '''
                yield (item)
                