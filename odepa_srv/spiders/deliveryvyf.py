# -*- coding: utf-8 -*-
from scrapy.spiders import Spider
from scrapy_splash import SplashRequest
from odepa_srv.items import OdepaSrvItem



class Deliveryveryfru(Spider):
    name = "deliveryvyf"
    start_urls = [ "http://deliveryverdurasyfrutas.cl/delivery-de-frutas-a-domicilio?n=48",
    "http://deliveryverdurasyfrutas.cl/delivery-verduras-a-domicilio?n=120",
    "http://deliveryverdurasyfrutas.cl/delivery-de-legumbres-a-domicilio",
    "http://deliveryverdurasyfrutas.cl/frutos-secos-y-huevos?n=48",       
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
        for sel in response.xpath('//*[@id="center_column"]/ul/li'):
            item = OdepaSrvItem.inicializar(OdepaSrvItem())
            if sel.xpath('div[2]/div/div/div[2]/div/div[1]/a/text()').extract():
                item['producto'] = sel.xpath('div[2]/div/div/div[2]/div/div[1]/a/text()').extract()[0].replace("\n","").replace("\t","")        #En el caso de que exista una oferta
                item['precio'] = sel.xpath('div[2]/div/div/div[2]/div/div[3]/span/text()').extract()[0].replace("\n","").replace("\t","").replace("$","").replace(".","")
                item['fuente'] = 'www.deliveryverdurasyfrutas.cl'
                item ['unidad'] = item['producto']
                yield (item)

