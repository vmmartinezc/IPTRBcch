#!/usr/bin/env python
# -*- coding: utf-8 -*-

from scrapy.item import Field
from scrapy.item import Item
from scrapy.spiders import Spider
from scrapy.selector import Selector
from scrapy.contrib.loader import ItemLoader
from bs4 import BeautifulSoup

from FrutasyVerduras.items import *

#Página : www.todofruta.cl

class TodoFruta(Spider):
    name="Todo Fruta "
    start_urls = ["http://www.todofruta.cl/index.php/frutas"]
    #gkComponent > div.browse-view > div:nth-child(5) > div:nth-child(1) > div > div.width70.floatright > h2 > a
    def parse(self, response):
        sel = Selector(response)
        verdurasfrutas = sel.xpath('//div[@class="browse-view"]/div[@class="row"]/div')
        for sel in verdurasfrutas:
            item = Atributos()
            item['Precio'] = sel.xpath('div/div[2]/div/div/span[2]/text()').extract()
            item['Producto'] = sel.xpath('div/div[2]/h2/a/text()').extract()
            item['Fuente'] = "www.todofruta.cl"
            yield item
