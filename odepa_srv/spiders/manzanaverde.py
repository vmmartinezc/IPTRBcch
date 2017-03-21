# -*- coding: utf-8 -*-
from scrapy.spiders import Spider
from scrapy_splash import SplashRequest
from odepa_srv.items import OdepaSrvItem



class Manzanaverde(Spider):
    name = "manzana"
    start_urls = [ "http://lamanzanaverde.cl/frutas/",
    "http://lamanzanaverde.cl/frutos-secos/",
    "http://lamanzanaverde.cl/verduras/",
    "http://lamanzanaverde.cl/legumbres/",       
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
        for sel in response.xpath('//*[@class="products"]/li'):
            if sel.xpath('div/div[2]/h3/text()').extract() and sel.xpath('div/div[2]/span/span/text()').extract():
                item = OdepaSrvItem.inicializar(OdepaSrvItem())
                item['producto'] = sel.xpath('div/div[2]/h3/text()').extract()[0].replace("\n","").replace("\t","").split('(')[0]      #En el caso de que exista una oferta
                item['precio'] = sel.xpath('div/div[2]/span/span/text()').extract()[0].replace("\n","").replace("\t","").replace("$","").replace(".","")
                item['fuente'] = 'www.lamanzanaverde.cl'
                item ['unidad'] = sel.xpath('div/div[2]/h3/text()').extract()[0].replace("\n","").replace("\t","").split('(')[1].replace(")","")
                yield (item)
