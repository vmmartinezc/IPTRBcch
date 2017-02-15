#!/usr/bin/env python
# -*- coding: utf-8 -*-

from scrapy.spiders import Spider
from scrapy.selector import Selector
from odepa_srv.items import *
#Página : www.todofruta.cl

class TodoFruta(Spider):
    name="Todo Fruta "
    start_urls = ["http://www.todofruta.cl/index.php/frutas"]
    allow_domains = ['todofruta.cl']
    

    def parse(self, response):
        sel = Selector(response)
        
        for sel in sel.xpath('//div[@class="browse-view"]/div[@class="row"]/div'):
            #Se verifica que los valores precio y producto existan
            if (sel.xpath('div/div[2]/div/div/span[2]/text()').extract() and sel.xpath('div/div[2]/h2/a/text()').extract()):
                item  = OdepaSrvItem()
                item['precio'] = sel.xpath('div/div[2]/div/div/span[2]/text()').extract()[0].strip("$")
                item['producto'] = sel.xpath('div/div[2]/h2/a/text()').extract()[0].title()
                item['fuente'] = "www.todofruta.cl"
                print (item)


