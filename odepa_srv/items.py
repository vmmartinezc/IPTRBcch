# -*- coding: utf-8 -*-
from scrapy import *
from scrapy.item import Field
from scrapy.item import Item
from scrapy.loader import ItemLoader, XPathItemLoader
from scrapy.loader.processors import TakeFirst, MapCompose, Join, Compose

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
    unidad = Field()
    url = Field()
    fuente  = Field()

class ReviewLoader(XPathItemLoader):
    default_item_class = OdepaSrvItem
    default_output_processor = TakeFirst()
    # this in case the review field contains multiple values
    review_out = Compose(MapCompose(lambda s: s.strip()), Join())