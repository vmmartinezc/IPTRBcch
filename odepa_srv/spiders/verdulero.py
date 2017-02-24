#!/usr/bin/env python
# -*- coding: utf-8 -*-

from scrapy.spiders import Spider
from scrapy.selector import Selector
from odepa_srv.items import *
#Página : http://www.elverdulero.cl
class Verdulero(Spider):
    name="verdulero"
    start_urls = ["http://www.elverdulero.cl/verduras/",
                    "http://www.elverdulero.cl/frutas/"]
    allow_domains = ['elverdulero.cl']

    def parse(self, response):
        sel = Selector(response)
        for sel in sel.xpath('//div[@id="mainZone"]/div/div/div'):
            if(sel.xpath('h3/a/text()').extract() and sel.xpath('div/p[2]/ins/text()').extract()):
                item = OdepaSrvItem.inicializar(OdepaSrvItem())
                item['producto'] = sel.xpath('h3/a/text()').extract()[0].title()
                item['precio'] = sel.xpath('div/p[2]/ins/text()').extract()[0].strip("$").replace(",","")
                item['fuente'] = "www.elverdulero.cl"
                #La unidad de medida y su cantidad se encuentra en el nombre, por lo tanto es el parámatro de entrada para normalizar
                unidad_tmp = item['producto']
                unidad_norm = Normalization.general(unidad_tmp)
                item['unidad'] = unidad_norm['unidad']
                item['cantidad'] = unidad_norm['cantidad']
                item['producto'] = unidad_norm['producto']   
                #Problema con la normalizacion de ej. 1/2 kilo, lo toma como 2 kilo.

                yield (item)
                