# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader import ItemLoader, XPathItemLoader
from scrapy.loader.processors import TakeFirst, MapCompose, Join, Compose

# see the docs for the required imports

class OdepaSrvItem(scrapy.Item):
    mercado = scrapy.Field()
    producto = scrapy.Field()
    variedad = scrapy.Field()
    calidad = scrapy.Field()
    volumen = scrapy.Field()
    precioMin = scrapy.Field()
    precioMax = scrapy.Field()
    precioProm = scrapy.Field()
    unidad = scrapy.Field()
    url = scrapy.Field()

class ReviewLoader(XPathItemLoader):
    default_item_class = OdepaSrvItem
    default_output_processor = TakeFirst()
    # this in case the review field contains multiple values
    review_out = Compose(MapCompose(lambda s: s.strip()), Join())