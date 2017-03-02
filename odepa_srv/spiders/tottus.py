#!/usr/bin/env python
# -*- coding: utf-8 -*-

from scrapy.item import Field
from scrapy.item import Item
from scrapy.spiders import Spider
from scrapy.selector import Selector
from odepa_srv.items import *
import re

#Página : http://www.tottus.cl/

class tottus(Spider):
    name="tottus"
    start_urls = ["http://www.tottus.cl/tottus/browse/Frescos-Verduras-Papa-y-Tomates/_/N-1u09wo2",
                 "http://www.tottus.cl/tottus/browse/Frescos-Frutas-Paltas-y-Plátanos/_/N-6ytsug",
                 "http://www.tottus.cl/tottus/browse/Frescos-Verduras-Lechugas-y-Hortalizas/_/N-ki8en",
                 "http://www.tottus.cl/tottus/browse/Frescos-Verduras-Zapallos/_/N-167y1fo",
                 "http://www.tottus.cl/tottus/browse/Frescos-Verduras-Cebollas-y-Zanahorias/_/N-1488kp0",
                 "http://www.tottus.cl/tottus/browse/Frescos-Verduras-Pepino-y-Apios/_/N-1raumw",
                 "http://www.tottus.cl/tottus/browse/Frescos-Verduras-Ensaladas-Listas/_/N-l9uose",
                 "http://www.tottus.cl/tottus/browse/Frescos-Verduras-Otras-Verduras/_/N-g2ddw8",
                 "http://www.tottus.cl/tottus/browse/Frescos-Frutas-Limones-Naranjas-y-C%C3%ADtricos/_/N-1102po5",
                 "http://www.tottus.cl/tottus/product/Frescos-y-Lacteos-Frutas-Manzanas-y-Peras/Brand-FRUTAS/_/R-product-06900092..catalog20001.es.salePricesCL__listPricesCL.tottusCl",
                 "http://www.tottus.cl/tottus/product/Frescos-Frutas-Otras-Frutas/Frescos-Frutas-Pi%C3%B1as-y-Fruta-Tropical/Brand-FRUTAS/_/R-product-05014013..catalog20001.es.salePricesCL__listPricesCL.tottusCl",
                 "http://www.tottus.cl/tottus/browse/Frescos-Frutas-Otras-Frutas/_/N-e0rhub"]
    allow_domains=['tottus.cl']

    def parse(self, response):
        sel = Selector(response)
        for sel in sel.xpath('//div[@class=" item-product-caption"]'):
            if sel.xpath('div[3]/div[1]/a/h5/div/text()') and sel.xpath('div[3]/div[4]/span/span[1]/text()').extract():
                item = OdepaSrvItem.inicializar(OdepaSrvItem())
                item['producto'] = sel.xpath('div[3]/div[1]/a/h5/div/text()').extract()[0].strip().strip("\n")
                #Recordar precio anterior y precio oferta
                item['precio']= sel.xpath('div[3]/div[4]/span/span[1]/text()').extract()[0].strip().strip("\n").strip("$").replace(".","")
                #item['Precio'] = sel.xpath('div[3]/div[5]/text()').extract()   #Precio por unidad
                item['fuente'] = "www.tottus.cl"

                #La unidad de medida y su cantidad se encuentra en el nombre, por lo tanto es el parámatro de entrada para normalizar
                pat = re.compile('\d{1,3}\s{0,2}(Gramos|Grs.|Grs|kilos|kilo|Kilos|Kilo|Kl|kl|kg|Kg|Unidades|unidades|unidad|Unid.|C/U|G.|g.|gr.|gr|Gr|Gr.|G|g|Un|Ud|uds|ud)')
                nom_fil1= pat.search(item['producto'])
                pat1 = re.compile('(Gramos|Grs.|Grs|kilos|kilo|Kilos|Kilo|Kl|kl|kg|Kg|Unidades|unidades|unidad|Unid.|C/U|G.|g.|gr.|gr|Gr|Gr.|G|g|Un|Ud|uds|ud)')
                nom_fil2 =pat1.search(item['producto'])

                if nom_fil1:
                    item['producto']=item['producto'].replace(nom_fil1.group(),"")
                elif nom_fil2:
                    item['producto']=item['producto'].replace(nom_fil2.group(),"")
                else : 
                    item['producto'] = item['producto']
                item['unidad']=sel.xpath('div[3]/div[2]/text()').extract()[0]
                #unidad_tmp = sel.xpath('div[3]/div[1]/a/h5/div/text()').extract()[0].strip().strip("\n")
                #unidad_norm = Normalization.general(unidad_tmp)
                #item['unidad'] = unidad_norm['unidad']
                #item['cantidad'] = unidad_norm['cantidad']
                
                #Descomentar para comprobar normalizacion visualmente
                '''
                print (unidad_tmp)
                print (item['unidad'])
                print (item['cantidad'])
                print ("*************")
                '''                
                yield (item)
    