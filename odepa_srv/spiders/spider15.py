#!/usr/bin/env python
# -*- coding: utf-8 -*-


from scrapy.spiders import Spider
from scrapy.selector import Selector
from odepa_srv.items import *
#Página : http://www.manolofrutasyverduras.cl/

class manolofrutasyverduras(Spider):
    name="Manolo"
    start_urls = ["http://www.manolofrutasyverduras.cl/"]

    def parse(self, response):
        sel = Selector(response)
        verdurasfrutas = sel.xpath('//div[@class="nsp_art"]')
        for sel in verdurasfrutas:
            if(sel.xpath('div[1]/h4/a/text()').extract() and sel.xpath('div/div[2]/form/span/text()').extract()):
                item  = OdepaSrvItem()
                item['producto'] = sel.xpath('div[1]/h4/a/text()').extract()
                item['precio'] = sel.xpath('div/div[2]/form/span/text()').extract()
                item['fuente'] = "www.manolofrutasyverduras.cl"
                yield (item)
  