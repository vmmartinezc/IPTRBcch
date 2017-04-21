# -*- coding: utf-8 -*-
from scrapy import *
from scrapy.item import Field
from scrapy.item import Item
from scrapy.loader import ItemLoader, XPathItemLoader
from scrapy.loader.processors import TakeFirst, MapCompose, Join, Compose
import re
import time

# see the docs for the required imports

class OdepaSrvItem(Item):
    mercado = Field()
    producto = Field()
    variedad = Field()
    calidad = Field()
    volumen = Field()
    precioMin = Field()
    precioMax = Field()
    precioProm = Field()
    precio  = Field()
    url = Field()
    fuente  = Field()
    unidad = Field()
    cantidad = Field()
    tipo = Field() #Odepa o web

    
    #Inicializamos los campos como vacíos ya que al usar "yield" exportará el csv  mediante el archivo "WriteToCsv" y 
    #necesita que cada atributo tenga un valor.
    def inicializar(item):
        keys ={'mercado','producto','variedad','calidad','volumen',
            'precioMin','precioMax','precioProm','precio','unidad',
            'url','fuente','cantidad'}

        #Se inicializan variables para que no existan errores de impresion
        for key in keys:
            item[key]= ""

        #Valores que utilizaran por defecto en algunos spider.
        item['url']=time.strftime("%d/%m/%Y")
        item['tipo'] = "WEB"
        return item


class ReviewLoader(XPathItemLoader):
    default_item_class = OdepaSrvItem()
    default_output_processor = TakeFirst()
    # this in case the review field contains multiple values
    review_out = Compose(MapCompose(lambda s: s.strip()), Join())
