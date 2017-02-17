#!/usr/bin/env python
# -*- coding: utf-8 -*-

from scrapy.spiders import Spider
from scrapy.selector import Selector
from odepa_srv.items import *
#Página : https://www.fullmercado.cl/

class FullMercado(Spider):
    name="fullmercado "
    start_urls = ["https://www.fullmercado.cl/tienda/"]
    allow_domains = ['fullmercado.cl']
    
    def parse(self, response):
        #Falta crawl horizontal para obtener la unidad
        sel = Selector(response)
        verduras = sel.xpath('//div[@class="et_pb_module et_pb_shop  et_pb_shop_1"]/div/ul/li')
        for sel in verduras:
            if(sel.xpath('a/h3/text()').extract() and sel.xpath('a/span[2]/span/text()').extract()):
                item  = OdepaSrvItem()
                item['producto'] = sel.xpath('a/h3/text()').extract()[0].title()
                item['precio'] = sel.xpath('a/span[2]/span/text()').extract()[0].strip("\xa0").strip()
                item['fuente'] = "www.fullmercado.cl"
                print (item) 

        frutas = sel.xpath('//div[@class="et_pb_module et_pb_shop  et_pb_shop_2"]/div/ul/li') 
        for sel in frutas:
            if (sel.xpath('a/h3/text()').extract() and sel.xpath('a/span[2]/span/text()').extract()):
                item  = OdepaSrvItem()
                item['producto'] = sel.xpath('a/h3/text()').extract()[0].title()
                item['precio'] = sel.xpath('a/span[2]/span/text()').extract()[0].strip("\xa0").strip()
                item['fuente'] = "www.fullmercado.cl"
                print (item)

