#!/usr/bin/env python
# -*- coding: utf-8 -*-
from scrapy.spiders import Spider
from scrapy.selector import Selector
from odepa_srv.items import *
#Página : http://laferiadelivery.cl/
class FeriaDelivery(Spider):
    name="feriaDelivery"
    #Estructura html igual.
    start_urls = ["http://laferiadelivery.cl/categoria-producto/feria/verduras",
    			 "http://laferiadelivery.cl/categoria-producto/feria/frutas"]
    allow_domains = ['laferiadelivery.cl']
    def parse(self, response):
        sel = Selector(response)
        for sel in sel.xpath('//ul[@class="products"]/li'):
            if (sel.xpath('.//span[@class="woocommerce-Price-amount amount"]/text()').extract() and sel.xpath('h3/text()').extract()):
                item = OdepaSrvItem.inicializar(OdepaSrvItem())
                item['precio'] = sel.xpath('.//span[@class="woocommerce-Price-amount amount"]/text()').extract()[0].replace(".","")
                item['fuente'] = "http://laferiadelivery.cl/"
                #La unidad de medida y su cantidad se encuentra en el nombre, por lo tanto es el parámatro de entrada para normalizar
                pat = re.compile('\d{1,3}\s{0,2}(Gramos|Grs.|Grs|kilos|kilo|Kilos|Kilo|Kl|kl|kg|Kg|Unidades|unidades|unidad|Unid.|C/U|G.|g.|gr.|gr|Gr|Gr.|G|g|Un|Ud|uds|ud)')
                nom_fil1= pat.search(sel.xpath('h3/text()').extract()[0])
                pat1 = re.compile('(Gramos|Grs.|Grs|kilos|kilo|Kilos|Kilo|Kl|kl|kg|Kg|Unidades|unidades|unidad|Unid.|C/U|G.|g.|gr.|gr|Gr|Gr.|G|g|Un|Ud|uds|ud)')
                nom_fil2 =pat1.search(sel.xpath('h3/text()').extract()[0])

                if nom_fil1:
                    item['producto']=sel.xpath('h3/text()').extract()[0].replace(nom_fil1.group(),"")
                elif nom_fil2:
                    item['producto']=sel.xpath('h3/text()').extract()[0].replace(nom_fil2.group(),"")
                else : 
                    item['producto'] = sel.xpath('h3/text()').extract()[0]

                unidad_tmp = sel.xpath('h3/text()').extract()[0]
                unidad_norm = Normalization.general(unidad_tmp)
                item['unidad'] = unidad_norm['unidad']
                item['cantidad'] = unidad_norm['cantidad']
               
                #Descomentar para comprobar normalizacion visualmente
                '''
                print (unidad_tmp)
                print (item['unidad'])
                print (item['cantidad'])
                print ("*************")
                '''                
                yield (item)

