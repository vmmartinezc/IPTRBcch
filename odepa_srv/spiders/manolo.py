#!/usr/bin/env python
# -*- coding: utf-8 -*-

from scrapy.selector import Selector
from odepa_srv.items import OdepaSrvItem
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
#Página : http://www.manolofrutasyverduras.cl/

class manolofrutasyverduras(CrawlSpider):
    name="manolo"
    start_urls = ["http://www.manolofrutasyverduras.cl/"]
    allow_domains=['manolofrutasyverduras.cl']
    rules = (
            Rule(LinkExtractor(allow=('/index.php\?option=com_k2&view=item&id')), callback='parse_items'),
        )

    def parse_items(self, response):
        sel = Selector(response)
        item = OdepaSrvItem.inicializar(OdepaSrvItem())

        item['producto'] = sel.xpath('//*[@id="k2Container"]/div[3]/div[2]/p[1]/text()').extract()[0]
        item['precio'] = sel.xpath('//*[@id="k2Container"]/div[3]/div[2]/p[2]/text()').extract()[0].replace("\xa0","").replace(".","").strip("$")
        item['fuente'] = "www.manolofrutasyverduras.cl"
        item['unidad'] = item['precio']
        '''
        unidad_norm = Normalization.manolo(item['precio'])
        item['unidad'] = unidad_norm['unidad']
        item['cantidad'] = unidad_norm['cantidad']
        item['precio'] = unidad_norm['precio']
'''

        yield (item)

