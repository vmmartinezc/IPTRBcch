# -*- coding: utf-8 -*-
from scrapy import *
from scrapy.item import Field
from scrapy.item import Item
from scrapy.loader import ItemLoader, XPathItemLoader
from scrapy.loader.processors import TakeFirst, MapCompose, Join, Compose
import re


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
    #Cantidad de productos descargados por pagina.
    cantidad = Field()

    
    #Inicializamos los campos como vacíos ya que al usar "yield" exportará el csv  mediante el archivo "WriteToCsv" y 
    #necesita que cada atributo tenga un valor.
    def inicializar(item):
        keys ={'mercado','producto','variedad','calidad','volumen',
            'precioMin','precioMax','precioProm','precio','unidad',
            'url','fuente','cantidad'}

        for key in keys:
            item[key]= ""
        return item


class ReviewLoader(XPathItemLoader):
    default_item_class = OdepaSrvItem
    default_output_processor = TakeFirst()
    # this in case the review field contains multiple values
    review_out = Compose(MapCompose(lambda s: s.strip()), Join())

#Normalizacion en desarrollo
class Normalization():

    def general(unidad_tmp):
        item = {'unidad':"",'cantidad':"",'producto':""}
        pat = re.compile('\d{1,3}\s{0,3}(Gramos|Grs.|Grs|G.|g.|gr.|gr|Gr|Gr.|G|g|kilos|kilo|Kilos|Kilo|Kl|kl|kg|Kg|Unidades|unidades|unidad|Unid.|C/U|Un|Ud|ud)')
        numero_antes = pat.search(unidad_tmp)
        pat = re.compile('\d{0}')#\s{0,3}(Gramos|Grs.|Grs|G.|g.|gr.|gr|Gr|Gr.|G|g|kilos|kilo|Kilos|Kilo|Kl|kl|kg|Kg|Unidades|unidades|unidad|Unid.|C/U|Un|Ud|ud)')
        sin_numero = pat.search(unidad_tmp)
        
        #Ejemplos que entrarían al if : 1 Kilo, 1Gr., 300G, 300 G..
        if(numero_antes):
            cant_unid = numero_antes.group()
            #Se busca patron de gramos 
            pat1 = re.compile('(Grs|Gramos|Grs.|G|g.|g|gr.|gr|Gr|Gr.)')
            #Se busca patron de kilos
            pat2 = re.compile('(Kilo|Kl|Kilos|kilo|kl)')
            #Se busca patron de unidades
            pat3 = re.compile('(Unidades|Unidad|Unid.|unidades|unidad|ud|Ud|unid.|C/U)')
            g = pat1.search(cant_unid) 
            k=  pat2.search(cant_unid)            
            u = pat3.search(cant_unid)

            #Si en cant_unidad existe valores relacionados con gramos entonces:
            if g :
                cantidad = cant_unid.split(g.group())[0].strip()
                item['unidad']="Gramos"
                item['cantidad'] = cantidad
            #Si en cant_unidad existe valores relacionados con kilo entonces:
            elif k:
                cantidad = cant_unid.split(k.group())[0].strip()
                item['unidad'] = 'Gramos'
                item['cantidad'] = str(int(cantidad*1000))
            #Si en cant_unidad existe valores relacionados con unidades entonces:  
            elif u:
                cantidad = cant_unid.split(u.group())[0].strip()
                item['unidad']="Unidades"
                item['cantidad'] = cantidad
            #Else que funcionará cuando las unidades no sean los string anteriores, ejemplo : 1 bandeja, 2 trozos
            else:
                pat = re.compile('\d{1,3}')
                o = pat.search(cant_unid)
                if o: 
                    cantidad = cant_unid.split(o.group())[0].strip()
                    unidad = cant_unid.split(o.group())[1].strip()
                    item['unidad']=unidad
                    item['cantidad'] = cantidad                    

        #Busqueda sin precedencia de numero, ej. kilo,unidad, etc.
        elif sin_numero:
            unidad = sin_numero.group()
            #Se busca patron de gramos 
            pat1 = re.compile('(Grs|Gramos|gramos|Grs.|gr.|gr|Gr|Gr.|G|g.|g)')
            #Se busca patron de kilos
            pat2 = re.compile('(Kilos|Kilo|kilo|Kilo|kl|Kl|K|k)')
            #Se busca patron de unidades
            pat3 = re.compile('(Unidades|unidades|unidad|Unidad|Unid.|unid.|ud|Ud|C/U)')
            g = pat1.search(unidad) 
            k=  pat2.search(unidad)            
            u = pat3.search(unidad)

            #Si en unidad existe valores relacionados con gramos entonces:
            if g :
                item['unidad']="Gramos"
                item['cantidad'] = "1"
            #Si en unidad existe valores relacionados con kilo entonces:
            elif k:
                item['unidad'] = 'Gramos'
                item['cantidad'] = "1000"
            #Si en unidad existe valores relacionados con unidades entonces:  
            elif u:
                item['unidad']="Unidades"
                item['cantidad'] = "1"
            #Else que funcionará cuando las unidades no sean los string anteriores, ejemplo : bandeja, trozos
            else:
                item['unidad']=unidad_tmp.strip()
                item['cantidad'] = "1"           
        return item