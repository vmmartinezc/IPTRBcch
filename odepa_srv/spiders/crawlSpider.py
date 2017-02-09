#!/usr/bin/env python
# -*- coding: utf-8 -*-

from scrapy.item import Field
from scrapy.item import Item
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.contrib.loader import ItemLoader
from scrapy.linkextractors import LinkExtractor
from FrutasyVerduras.items import *


class Walmart(CrawlSpider):
	name =" Walmart"
	#URL de frutas
	start_urls= ["https://www.lider.cl/walmart/catalog/category.jsp?id=cat640020&pId=CF_Nivel1_000004&navAction=jump&navCount=0#categoryCategory=cat640020"]
	#allowed_domains= ["lider.cl"]

	rules = (
			#Se busca expresion regular en la url de las paginacion
			Rule(LinkExtractor(allow=r'pageSizeCategory=', ), callback='parse_item'),
		)

	def parse_item(self, response):
		self.logger.info('Pagina numero %s', response.url)
		#sel = Selector(response)
		#verdurasfrutas = response.xpath('//[@id="cajaResultado"]/div/div[2]/div[1]/div/div[2]/div/a/p')
		#//*[@id="cajaResultado"]/div/div[2]/div[1]/div/div[2]/div/a/p
