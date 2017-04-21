
# -*- coding: utf-8 -*-
#Página : http://www.superdespacho.cl
from scrapy.item import Item
from scrapy.spiders import Spider
from scrapy_splash import SplashRequest
from odepa_srv.items import OdepaSrvItem
import re


class SuperDespacho(Spider):
    name="superDesp"
    start_urls = ["http://www.superdespacho.cl/"]
    allow_domains = ['superdespacho.cl']
    # http_user = 'splash-user'
    # http_pass = 'splash-password'

    #El metodo principal debe estar definido como start_requests, ya que no se necesitará el response con el tipico parse.
    def start_requests(self):
        for link in self.start_urls:
            yield SplashRequest(
                link,
                self.parse_link, #Callback 
                endpoint='render.json',
                args={
                    'har': 1,
                    'html': 1,
                }
            )

    def parse_link(self, response):
        for sel in response.xpath('//*[@id="realizar-pedido"]/div'):
            for subsel in sel.xpath('//div/table/tbody/tr'):
                if subsel.xpath('td[1]/text()').extract() and subsel.xpath('td[2]/text()').extract():
                    item = OdepaSrvItem.inicializar(OdepaSrvItem())
                    item['producto'] = subsel.xpath('td[1]/text()').extract()[0].strip().replace("\t","").replace("\n","").replace(".","").strip("$")
                    item['precio'] = subsel.xpath('td[2]/text()').extract()[0].strip().replace("\t","").replace("\n","").replace(".","").strip("$")
                    item['fuente'] = "www.superdespacho.cl"
                    item['unidad'] = item['precio']
                   
                    yield(item)



