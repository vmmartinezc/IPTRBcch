#!/usr/bin/env python
# -*- coding: utf-8 -*-

from scrapy.spiders import Spider
from scrapy.selector import Selector
from odepa_srv.items import *
#Página : http://www.foods.cl/
class Foods(Spider):
    name="foods"
    start_urls = ["http://www.foods.cl/categoria-producto/verduras/",
                "http://www.foods.cl/categoria-producto/frutas/",
                "http://www.foods.cl/categoria-producto/legumbres/",]
    allows_domains = ['foods.cl']
    def parse(self, response):
        sel = Selector(response)
        #Filtrar unidades de medida, se encuentra dentro del string nombre
        for sel in sel.xpath('//main[@id="main"]/div/ul/li'):
            if (sel.xpath('a/h3/text()').extract() and sel.xpath('a/span/span/text()').extract()):
                item = OdepaSrvItem.inicializar(OdepaSrvItem())
                aux = sel.xpath('a/h3/text()').extract()[0].title().split("(")
                item['producto'] = aux[0]
                item['precio'] = sel.xpath('a/span/span/text()').extract()[0].strip("$").strip("\xa0").replace(",","")
                item['fuente'] ="www.foods.cl"
                #Se le elimina el ultimo valor ')', es irrelevante.
                unidad_tmp = aux[1].strip(")")
                unidad_norm = Normalization.general(unidad_tmp)
                item['unidad'] = unidad_norm['unidad']
                item['cantidad'] = unidad_norm['cantidad']
                        
                '''
                #Descomentar para comprobar normalizacion visualmente
                print (unidad_tmp)
                print (item['unidad'])
                print (item['cantidad'])
                print ("*************")
                '''
                yield (item)