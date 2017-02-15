#!/usr/bin/env python
# -*- coding: utf-8 -*-

from scrapy.spiders import Spider
from scrapy.selector import Selector
from odepa_srv.items import *
#Página : https://www.luki.cl/
class luki(Spider):
    name="Luki "
    start_urls = ["https://www.luki.cl/shop/category/frutos-secos-175",
                "https://www.luki.cl/shop/category/frutos-secos-175/page/2?ppg=False"]
    allow_domains = ['luki.cl']

    def parse(self, response):
        sel = Selector(response)
        for sel in sel.xpath('//section[@id="product-name"]'):
            if(sel.xpath('div[1]/center/h6/a/text()').extract() and sel.xpath('div[2]/b/span[2]/text()').extract()):
                item  = OdepaSrvItem()
                #Se hace split en producto y almacenamos solo el primer valor de la lista generada, ya que el segundo no da informacion
                item['producto'] = sel.xpath('div[1]/center/h6/a/text()').extract()[0].split("-")[0].title()
                item['precio'] = sel.xpath('div[2]/b/span[2]/text()').extract()
                item['fuente']="http://www.luki.cl/"
                print (item)
