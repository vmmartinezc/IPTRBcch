# -*- coding: utf-8 -*-
from scrapy.spiders import Spider
from scrapy.selector import Selector
from odepa_srv.items import OdepaSrvItem

# Página  : www.lagranjaexpress.cl/

class GranjaExpress(Spider):
    name="granjaExp"
    start_urls = ["http://www.lagranjaexpress.cl/reparto-de-frutas-y-verduras-en-san-pedro-de-la-paz.html"]
    allow_domains = ['lagranjaexpress.cl']

    def parse(self, response):
        sel = Selector(response)
        for sel in sel.xpath('//form[@name="formulario"]/table'):
            for tr in sel.xpath('tr'):
                #Se verifica que los campos producto y precio existan
                if(sel.xpath('.//td[3]/text()').extract() and sel.xpath('.//td[5]/div/text()').extract()):
                    item = OdepaSrvItem.inicializar(OdepaSrvItem())
                    #Condición necesaria para cuando hay descuento, éste genera una etiqueta span y almacena su valor ahí, no en div
                    if tr.xpath('.//span[@class="rojo"]/text()').extract() :
                        item['precio'] = tr.xpath('.//span[@class="rojo"]/text()').extract()[0].strip("\xa0").strip("$").replace(".","")
                    else :
                        item['precio'] = tr.xpath('.//td[5]/div/text()').extract()[0].strip("\xa0").strip("$").replace(".","")

                    item['producto'] = tr.xpath('.//td[3]/text()').extract()[0].strip("\xa0").title()
                    item ['fuente'] = "www.lagranjaexpress.cl"
                    item['unidad']= tr.xpath('.//td[4]/div/text()').extract()[0].title()
        
                    yield (item) 
