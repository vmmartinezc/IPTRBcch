#!/usr/bin/env python
# -*- coding: utf-8 -*-
from scrapy.spiders import Spider
from scrapy.selector import Selector
from odepa_srv.items import *
#Página : http://laferiadelivery.cl/
class FeriaDelivery(Spider):
    name="La Feria Delivery "
    #Estructura html igual.
    start_urls = ["http://laferiadelivery.cl/categoria-producto/feria/verduras",
    			 "http://laferiadelivery.cl/categoria-producto/feria/frutas"]
    allow_domains = ['laferiadelivery.cl']
    def parse(self, response):
        sel = Selector(response)
        for sel in sel.xpath('//ul[@class="products"]/li'):
            if (sel.xpath('.//span[@class="woocommerce-Price-amount amount"]/text()').extract() and sel.xpath('h3/text()').extract()):
                item  = OdepaSrvItem()
                item['precio'] = sel.xpath('.//span[@class="woocommerce-Price-amount amount"]/text()').extract()
                item['fuente'] = "http://laferiadelivery.cl/"
                #La unidad de medida y su cantidad se encuentra en el nombre, por lo tanto es el parámatro de entrada para normalizar
                unidad_tmp = sel.xpath('h3/text()').extract()[0]
                unidad_norm = Normalization.unidad(unidad_tmp)
                item['unidad'] = unidad_norm['unidad']
                item['cantidad'] = unidad_norm['cantidad']
                item['producto'] = unidad_norm['producto']
                
                #Descomentar para comprobar normalizacion visualmente
                '''
                print (unidad_tmp)
                print (item['unidad'])
                print (item['cantidad'])
                print ("*************")
                '''                
                print (item)

