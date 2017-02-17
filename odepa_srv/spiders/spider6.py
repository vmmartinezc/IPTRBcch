#!/usr/bin/env python
# -*- coding: utf-8 -*-

from scrapy.spiders import Spider
from scrapy.selector import Selector
from odepa_srv.items import *
import re
#Página : http://www.vegavirtual.cl

class VegaVirtual(Spider):
    name="Vega virtual "
    start_urls = ["http://www.vegavirtual.cl"]
    allow_domains = ['vegavirtual.cl']
    def parse(self, response):
        sel = Selector(response)
        for sel in sel.xpath('//div[@class="row products-loop products-grid row-count-6"]/div'):
            if (sel.xpath('div/div[2]/div[1]/a/text()').extract() and sel.xpath('div/div[2]/span/span/text()').extract()):
                item  = OdepaSrvItem()
                item['precio'] = sel.xpath('div/div[2]/span/span/text()').extract()[0].strip("$")
                item['fuente'] = "http://www.vegavirtual.cl"
                item['producto'] =  sel.xpath('div/div[2]/div[1]/a/text()').extract()[0]
                
                #La unidad de medida junto con su cantidad se encuentra en el nombre del producto
                unidad_tmp = item['producto']
                unidad_norm = Normalization.unidad(unidad_tmp)
                item['unidad'] = unidad_norm['unidad']
                item['cantidad'] = unidad_norm['cantidad']
                #Arreglar normalizacion de nombre
                #item['producto'] = unidad_norm['producto']
               
                #Descomentar para comprobar normalizacion visualmente
                #print (unidad_tmp)
                #print (item['unidad'])
                #print (item['cantidad'])
                #print ("*************")
                print (item) 
