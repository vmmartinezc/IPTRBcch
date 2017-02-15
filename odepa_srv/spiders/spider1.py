# -*- coding: utf-8 -*-
from scrapy.spiders import Spider
from scrapy.selector import Selector
from odepa_srv.items import *


# Página  : http://www.lavegadelivery.cl/

class Lavegadelivery(Spider):
    name="lavegadelivery"
    start_urls = ["http://www.lavegadelivery.cl/categoria.php?cat=1",
                  "http://www.lavegadelivery.cl/categoria.php?cat=2"]

    allow_domains= ['lavegadelivery.cl']

    #Entra a las 2 url, conveniente ya que los codigos son los mismos.
    #Filtrar unidades de medida
    def parse(self, response):
        sel = Selector(response)
        for sel in sel.xpath('//section[@id="cuerpo"]/div[@class="cuadro"]'):
            item  = OdepaSrvItem()
            item['producto'] = sel.xpath('.//p[@class="nombre"]/text()').extract()[0].title()
            aux= (sel.xpath('.//p[@class="precio"]/text()').extract()[0]).strip("$").split("-")
            item['unidad'] = aux[1]
            item['precio'] = aux[0]
            item['fuente']= 'www.lavegadelivery.cl'
            
            print (item)
