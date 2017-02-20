#!/usr/bin/env python
# -*- coding: utf-8 -*-

from scrapy.spiders import Spider
from scrapy.selector import Selector
from odepa_srv.items import *
#Página : https://www.buencampo.cl/

class Buencampo(Spider):
    name="Buen_Campo"
    start_urls = ["http://buencampo.cl/categoria-producto/frutas-y-verduras"]
    allow_domains =['buencampo.cl']
    def parse(self, response):
        sel = Selector(response)
        for sel in sel.xpath('//div[@class="view-content"]/div'):
            if (sel.xpath('article/h2/a/text()').extract() and sel.xpath('article/div/div[2]/div/div/text()').extract()):
                item = OdepaSrvItem.inicializar(OdepaSrvItem())
                aux = sel.xpath('article/h2/a/text()').extract()[0].split('-')
                item['precio']  = sel.xpath('article/div/div[2]/div/div/text()').extract()[0]
                item['producto']= aux[0].title().replace(",0","")
                #Normalizacion de unidad
                unidad_tmp = aux[1]
                unidad_norm = Normalization.general(unidad_tmp)
                item['unidad'] = unidad_norm['unidad']
                item['cantidad'] = unidad_norm['cantidad']
                item['fuente'] = "https://www.buencampo.cl/"
                #Descomentar para comprobar normalizacion visualmente
                '''print (unidad_tmp)
                print (item['unidad'])
                print (item['cantidad'])
                print ("*************")
                '''
                yield (item)
