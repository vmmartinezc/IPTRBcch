# -*- coding: utf-8 -*-
from scrapy.spiders import Spider
from scrapy_splash import SplashRequest
from odepa_srv.items import OdepaSrvItem



class Huerta(Spider):
    name = "huerta"

    start_urls = [ "http://www.nuestrahuerta.cl/Venta_de_Frutas-1.aspx",
    "http://www.nuestrahuerta.cl/Venta_de_Verduras-5.aspx",
    "http://www.nuestrahuerta.cl/Venta_de_Frutos_Secos_y_Deshidratados-6.aspx",
    "http://www.nuestrahuerta.cl/Venta_de_CONGELADOS-14.aspx",       
    ]
    
    # http_user = 'splash-user'
    # http_pass = 'splash-password'

    def start_requests(self):
        for link in self.start_urls:
            yield SplashRequest(
                link,
                self.parse_link, #Callback 
                endpoint='render.json',
                args={
                    'har': 1,
                    'html': 1,
                    'wait':0.5,
                }
            )

    def parse_link(self, response):
        for sel in response.xpath('//*[@id="grid"]/ul/li'):
            if sel.xpath('div/div[2]/div/div[1]/a/text()').extract():
                item = OdepaSrvItem.inicializar(OdepaSrvItem())
                item['producto'] = sel.xpath('div/div[2]/div/div[1]/a/text()').extract()[0].replace("\n","").replace("\t","")      #En el caso de que exista una oferta
                #Condicion para cuando hay ofertas
                if sel.xpath('.//span[@class="special-price"]//text()').extract():
                    item['precio'] = sel.xpath('.//span[@class="special-price"]//text()').extract()[0].replace("\n","").replace("\t","").replace("$","").replace(".","")
                else:
                    item['precio'] = sel.xpath('.//span[@id="product-price-1"]//text()[1]').extract()[0].replace("\n","").replace("\t","").replace("$","").replace(".","")
                
                item['fuente'] = 'www.nuestrahuerta.cl'
                item['unidad'] = item['producto']
                yield (item)

