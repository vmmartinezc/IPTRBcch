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
                item['producto'] = sel.xpath('h3/text()').extract()
                item['precio'] = sel.xpath('.//span[@class="woocommerce-Price-amount amount"]/text()').extract()
                item['fuente'] = "http://laferiadelivery.cl/"
                print (item)

