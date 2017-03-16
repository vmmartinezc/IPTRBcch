# -*- coding: utf-8 -*-
from scrapy.item import Item
from scrapy.spiders import Spider
from scrapy_splash import SplashRequest
from odepa_srv.items import *
import re
#from scrapy.spiders import CrawlSpider, Rule
#from scrapy.linkextractors import LinkExtractor


class Lider(Spider):
    name = "lider"
    #Tiempo de  transicion de descarga entre dos paginas
    download_delay = 5
    start_urls = [
    #Verduras paginadas hasta 200 productos
    "https://electrohogar.lider.cl/supermercado/category/Pan-Vegetales/Verduras/Verduras/_/N-1rnk03k?N=&No=0&Nrpp=200",
    "https://electrohogar.lider.cl/supermercado/category/Pan-Vegetales/Verduras/Verduras-Congeladas/_/N-jyg8vi?N=&No=0&Nrpp=200",
    #Frutas 
    "https://electrohogar.lider.cl/supermercado/category/Pan-Vegetales/Frutas/Frutas-Frescas/_/N-c48hfq",
    "https://electrohogar.lider.cl/supermercado/category/Pan-Vegetales/Frutas/Frutas-Congeladas/_/N-172n2h5"
    ]
    #allow_domains = ['superdespacho.cl']
    #rules = (
     #       Rule(LinkExtractor(allow=('(/frutas*|/verduras*)')), callback='parse_items'),
     #   )

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
                    'wait':1,
                },
                dont_filter=True

            )

    def parse_link(self, response):
        for sel in response.xpath('//*[@id="content-prod-boxes"]/div'):
            item = OdepaSrvItem.inicializar(OdepaSrvItem())
            item['producto'] = sel.xpath('div[2]/div[1]/a/span[2]/text()').extract()[0]
            item['precio'] = sel.xpath('div[2]/div[1]/div/span[2]/b/text()').extract()[0].replace("\t","").replace("\n","").replace(".","").replace("$","")
            item['fuente'] = "www.lider.cl"
            if sel.xpath('div[2]/div[1]/div/span[1]/text()').extract():
                unidad_tmp = sel.xpath('div[2]/div[1]/div/span[1]/text()').extract()[0]
                unidad_norm = Normalization.lider(unidad_tmp)
                item['unidad'] = unidad_norm['unidad']
                item['cantidad'] = unidad_norm['cantidad']
            else :
                item['unidad']=""

            yield(item)
