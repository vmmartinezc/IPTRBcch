#!/usr/bin/env python
# -*- coding: utf-8 -*-
from scrapy.selector import Selector
from odepa_srv.items import OdepaSrvItem
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

class fullMercado(CrawlSpider):
    name="fullMercado"    
    start_urls = ["http://www.fullmercado.cl/producto-categoria/verduras/",
                "http://www.fullmercado.cl/producto-categoria/frutas/",
                "http://www.fullmercado.cl/producto-categoria/congelados/",
                "http://www.fullmercado.cl/producto-categoria/especias-semillas-rutos-secos-huevos/",
                "http://www.fullmercado.cl/producto-categoria/procesados/"]

    allow_domains = ['fullmercado.cl']

      #Expresion regular que recorre verticalmente
    rules = (
            Rule(LinkExtractor(allow=('(/producto/.*)')), callback='parse_items'),
        )
    def parse_items(self, response):
        sel = Selector(response)
        item = OdepaSrvItem.inicializar(OdepaSrvItem())  
        item['producto'] = sel.xpath('//*[@id="left-area"]/nav/text()[2]').extract()[0].replace("/","").rstrip('(')        #En el caso de que exista una oferta
        if sel.xpath('//*[@class="price"]/ins//text()'):
            item['precio'] = sel.xpath('//*[@class="price"]/ins//text()')[1].extract().strip("\xa0").strip().replace(".","")
        else:
            item['precio']= sel.xpath('//*[@class="woocommerce-Price-amount amount"]//text()')[1].extract().strip("\xa0").strip().replace(".","")
        if sel.xpath('//*[@id="tab-description"]//text()'):
             item['unidad']  = sel.xpath('//*[@id="tab-description"]//text()')[3].extract()
        elif sel.xpath('//*[@itemprop="description"]/p/span/text()'):
            item['unidad'] = sel.xpath('//*[@itemprop="description"]/p/span/text()').extract()[0]
        else:
            item['unidad'] ='Sin formato'
        item['unidad'] = item['unidad'].replace(",","")
        item['fuente'] = 'www.fullmercado.cl'
        yield(item)
