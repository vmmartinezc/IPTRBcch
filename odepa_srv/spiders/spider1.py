# -*- coding: utf-8 -*-
from scrapy.item import Field
from scrapy.item import Item
from scrapy.spiders import Spider
from scrapy.selector import Selector
from scrapy.loader import ItemLoader
from FrutasyVerduras.items import *


# Página  : http://www.lavegadelivery.cl/

class Lavegadelivery(Spider):
    name="lavegadelivery"
    start_urls = ["http://www.lavegadelivery.cl/categoria.php?cat=1","http://www.lavegadelivery.cl/categoria.php?cat=2"]

    def parse(self, response):
    	sel = Selector(response)
    	verduras = sel.xpath('//section[@id="cuerpo"]/div')
        print len(verduras)
    	for i, elem in enumerate(verduras):
            item = ItemLoader(Atributos(),elem)
            item.add_xpath('Producto', './/p[@class="nombre"]/text()')
            item.add_xpath('Precio', './/p[@class="precio"]/text()')
            item.add_value('Fuente', 'www.lavegadelivery.cl')
            print item.load_item()

    def parse(self, response):
    	sel = Selector(response)
    	verduras = sel.xpath('//section[@id="cuerpo"]/div')
    	for i, elem in enumerate(verduras):
            item = ItemLoader(Atributos(),elem)
            item.add_xpath('Producto', './/p[@class="nombre"]/text()')
            item.add_xpath('Precio', './/p[@class="precio"]/text()')
            item.add_value('Fuente', 'www.lavegadelivery.cl')         
            #h.append(item.load_item())
            print item.load_item()


   