# -*- coding: utf-8 -*-
from scrapy.item import Field
from scrapy.item import Item
from scrapy.spiders import Spider
from scrapy.selector import Selector
from scrapy.loader import ItemLoader
from scrapy.selector import HtmlXPathSelector
from FrutasyVerduras.items import *


# Página  : www.lagranjaexpress.cl/

class GranjaExpress(Spider):
    name="La granja express"
    start_urls = ["http://www.lagranjaexpress.cl/reparto-de-frutas-y-verduras-en-san-pedro-de-la-paz.html"]

    def parse(self, response):
    	sel = Selector(response)
        verduras = sel.xpath('//form[@name="formulario"]/table[4]/tr')
        print len(verduras)
        for sel in verduras:
            print 'asda'
            item = Atributos()
            item['Producto'] = sel.xpath('td[3]/text()').extract()
            item['Precio'] = sel.xpath('td[5]/div/text()').extract()
            item['Observaciones'] = sel.xpath('td[4]/div/text()').extract()
            item ['Fuente'] = "www.lagranjaexpress.cl"
            yield item
