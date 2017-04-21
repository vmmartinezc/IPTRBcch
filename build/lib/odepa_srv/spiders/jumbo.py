# -*- coding: utf-8 -*-
from scrapy.item import Item
from scrapy.spiders import Spider
from scrapy_splash import SplashRequest
from odepa_srv.items import OdepaSrvItem
import re


class Jumbo(Spider):
    name = "jumbo"
    #Tiempo de  transicion de descarga entre dos paginas
    download_delay = 3
    start_urls = [
    #Frutas
    "http://www.jumbo.cl/FO/CategoryDisplay?cab=4006&int=11&ter=124",
    #Verduras
    "http://www.jumbo.cl/FO/CategoryDisplay?cab=4006&int=11&ter=125",
    #Frutos secos
    "http://www.jumbo.cl/FO/CategoryDisplay?cab=4006&int=11&ter=123"
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
        print ( response.xpath('//*[@id="tabla_productos"]/tbody/tr/td/ul/li'))
        for sel in response.xpath('//*[@id="tabla_productos"]/tbody/tr/td/ul/li'):
            item = OdepaSrvItem.inicializar(OdepaSrvItem())
            item['producto'] = sel.xpath('div/div[2]/div[2]/a[@id="ficha"]/b/text()').extract()[0]
            item['precio'] = sel.xpath('div/div[3]/div[1]/text()').extract()[0]
            item['unidad'] = sel.xpath('div/div[3]/div[2]/text()').extract()[0]
            item['fuente'] = 'www.jumbo.cl'
            yield(item)
