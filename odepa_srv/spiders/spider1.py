# -*- coding: utf-8 -*-
from scrapy.spiders import Spider
from scrapy.selector import Selector
from odepa_srv.items import *


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
            if sel.xpath('.//p[@class="nombre"]/text()').extract() and sel.xpath('.//p[@class="precio"]/text()').extract():
                item = OdepaSrvItem.inicializar(OdepaSrvItem())
                #Cantidad de productos descargados por pagina.
                item['producto'] = sel.xpath('.//p[@class="nombre"]/text()').extract()[0].title()
                item['precio'] = (sel.xpath('.//p[@class="precio"]/text()').extract()[0]).strip("$").replace(".","").split("-")[0] # ej. precio =  $2.300
                item['fuente']= 'www.lavegadelivery.cl'
                #Se obtiene la unidad temporal
                unidad_tmp =  (sel.xpath('.//p[@class="precio"]/text()').extract()[0]).strip("$").replace(".","").split("-")[1]
                unidad_norm = Normalization.general(unidad_tmp)
                item['cantidad'] = unidad_norm['cantidad']
                item['unidad'] = unidad_norm['unidad']
                #Descomentar para comprobar normalizacion visualmente
                ''' 
                print (unidad_tmp)
                print (item['unidad'])
                print (item['cantidad'])
                print ("*************")
                '''
                yield item



    