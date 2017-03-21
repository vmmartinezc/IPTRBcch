#!/usr/bin/env python
# -*- coding: utf-8 -*-

from scrapy.spiders import Spider
from scrapy.selector import Selector
from odepa_srv.items import OdepaSrvItem
#Página : www.todofruta.cl

class TodoFruta(Spider):
    name="todoFruta"
    #Limite de entrega de 150 productos por página.
    start_urls = ["http://www.todofruta.cl/index.php/frutas/view/category/virtuemart_category_id/1/virtuemart_manufacturer_id/1/categorylayout/0/showcategory/1/showproducts/1/productsublayout/0/limit/150",
    "http://www.todofruta.cl/index.php/verduras/view/category/virtuemart_category_id/4/virtuemart_manufacturer_id/1/categorylayout/0/showcategory/1/showproducts/1/productsublayout/0/limit/150"]
    allow_domains = ['todofruta.cl']
    

    def parse(self, response):
        sel = Selector(response)
        
        for sel in sel.xpath('//div[@class="browse-view"]/div[@class="row"]/div'):
            #Se verifica que los valores precio y producto existan
            if (sel.xpath('div/div[2]/div/div/span[2]/text()').extract() and sel.xpath('div/div[2]/h2/a/text()').extract()):
                item = OdepaSrvItem.inicializar(OdepaSrvItem())
                item['precio'] = sel.xpath('div/div[2]/div/div/span[2]/text()').extract()[0].strip("$").replace(",00","") #Ej. precio = $ 2000,00
                item['producto'] = sel.xpath('div/div[2]/h2/a/text()').extract()[0].title()
                item['fuente'] = "www.todofruta.cl"
                #//*[@id="gkComponent"]/div[2]/div[11]/div[3]/div/div[2]/p[1]
                if sel.xpath('div/div[2]/p/text()').extract():
                    item ['unidad'] = sel.xpath('div/div[2]/p/text()').extract()[0].strip("\n").strip("\t").strip(item['producto'])
                else : item ['unidad'] = "Sin información"

                yield (item)


