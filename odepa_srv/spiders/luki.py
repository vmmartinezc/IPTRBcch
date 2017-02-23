#!/usr/bin/env python
# -*- coding: utf-8 -*-

from scrapy.spiders import Spider
from scrapy.selector import Selector
from odepa_srv.items import *
#Página : https://www.luki.cl/
class luki(Spider):
    name="luki"
    start_urls = ["https://www.luki.cl/shop/category/frutos-secos-175",
                "https://www.luki.cl/shop/category/frutos-secos-175/page/2?ppg=False"]
    allow_domains = ['luki.cl']

    def parse(self, response):
        sel = Selector(response)
        for sel in sel.xpath('//section[@id="product-name"]'):
            if(sel.xpath('div[1]/center/h6/a/text()').extract() and sel.xpath('div[2]/b/span[2]/text()').extract()):
                item = OdepaSrvItem.inicializar(OdepaSrvItem())
                #Se hace split en producto y almacenamos solo el primer valor de la lista generada, ya que el segundo no da informacion
                pat = re.compile('\d{1,3}\s{0,2}(Gramos|Grs.|Grs|kilos|kilo|Kilos|Kilo|Kl|kl|kg|Kg|Unidades|unidades|unidad|Unid.|C/U|G.|g.|gr.|gr|Gr|Gr.|G|g|Un|Ud|uds|ud)')
                nom_fil1= pat.search(sel.xpath('div[1]/center/h6/a/text()').extract()[0].split("-")[0].title())
                pat1 = re.compile('(Gramos|Grs.|Grs|kilos|kilo|Kilos|Kilo|Kl|kl|kg|Kg|Unidades|unidades|unidad|Unid.|C/U|G.|g.|gr.|gr|Gr|Gr.|G|g|Un|Ud|uds|ud)')
                nom_fil2 =pat1.search(sel.xpath('div[1]/center/h6/a/text()').extract()[0].split("-")[0].title())

                if nom_fil1:
                    item['producto']=sel.xpath('div[1]/center/h6/a/text()').extract()[0].split("-")[0].title().replace(nom_fil1.group(),"")
                elif nom_fil2:
                    item['producto']=sel.xpath('div[1]/center/h6/a/text()').extract()[0].split("-")[0].title().replace(nom_fil2.group(),"")
                else : 
                    item['producto'] = sel.xpath('div[1]/center/h6/a/text()').extract()[0].split("-")[0].title()

                unidad_tmp = sel.xpath('div[1]/center/h6/a/text()').extract()[0].split("-")[0]
                unidad_norm = Normalization.general(unidad_tmp)
                item['unidad'] = unidad_norm['unidad']
                item['cantidad'] = unidad_norm['cantidad']
                item['precio'] = sel.xpath('div[2]/b/span[2]/text()').extract()[0].replace(".0","")
                item['fuente']="http://www.luki.cl/"
                yield (item)
