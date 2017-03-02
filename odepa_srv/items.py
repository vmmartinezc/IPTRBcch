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

#Normalizacion en desarrollo
class Normalization():

    
    #Unidades de medidas : Un, Kg, g
    def lider (unidad_tmp):
        item = {'unidad':"",'cantidad':"",'producto':""}
        pat = re.compile('\d{1,5}\s{1,3}(kg|Kg|Un|un|g)')
        match = pat.search(unidad_tmp)
        if match:
            cant_unid = match.group()
            #Se busca patron de kilos
            pat1 = re.compile('(kg|Kg)')
            #Se busca patron de gramos 
            pat2 = re.compile('g')
            #Se busca patron de unidades
            pat3 = re.compile('(Un|un)')
            k=  pat1.search(cant_unid) 
            g = pat2.search(cant_unid)            
            u = pat3.search(cant_unid)
            #Si en cant_unidad existe valores relacionados con kilo entonces:
            if k:
                cantidad = cant_unid.split(k.group())[0].strip()
                item['unidad'] = 'Gramos'
                item['cantidad'] = str(int(cantidad)*1000)
            #Si en cant_unidad existe valores relacionados con gramos entonces:
            elif g :
                cantidad = cant_unid.split(g.group())[0].strip()
                item['unidad']="Gramos"
                item['cantidad'] = cantidad
            #Si en cant_unidad existe valores relacionados con unidades entonces:  
            elif u:
                cantidad = cant_unid.split(u.group())[0].strip()
                item['unidad']="Unidades"
                item['cantidad'] = cantidad
            #Else que funcionará cuando las unidades no sean los string anteriores, ejemplo : 1 bandeja, 2 trozos


        else :
            item['unidad']= unidad_tmp

        return item


    def general(unidad_tmp):
        item = {'unidad':"",'cantidad':"",'producto':""}
        pat = re.compile('\d{1,3}\s{0,2}(Gramos|Grs.|Grs|kilos|kilo|Kilos|Kilo|Kl|kl|kg|Kg|Unidades|unidades|unidad|Unid.|Un|un|C/U|G.|g.|gr.|gr|Gr|Gr.|G|g|Un|Ud|uds|ud)')
        numero_antes = pat.search(unidad_tmp)
        #pat = re.compile('\d{0}')#\s{0,3}(Gramos|Grs.|Grs|G.|g.|gr.|gr|Gr|Gr.|G|g|kilos|kilo|Kilos|Kilo|Kl|kl|kg|Kg|Unidades|unidades|unidad|Unid.|C/U|Un|Ud|ud)')
        #sin_numero = pat.search(unidad_tmp)
        #print (sin_numero)
        
        #Ejemplos que entrarían al if : 1 Kilo, 1Gr., 300G, 300 G..
        if(numero_antes):
            cant_unid = numero_antes.group()
            #Se busca patron de gramos 
            pat1 = re.compile('(Grs|Gramos|Grs.|G|g.|g|gr.|gr|Gr|Gr.)')
            #Se busca patron de kilos
            pat2 = re.compile('(Kilo|Kl|Kilos|kilo|kl|kg)')
            #Se busca patron de unidades
            pat3 = re.compile('(Unidades|Unidad|Unid.|unidades|unidad|uds|ud|Ud|unid.|C/U|Un|un)')
            g = pat1.search(cant_unid) 
            k=  pat2.search(cant_unid)            
            u = pat3.search(cant_unid)


            #Si en cant_unidad existe valores relacionados con kilo entonces:
            if k:
                cantidad = cant_unid.split(k.group())[0].strip()
                item['unidad'] = 'Gramos'
                item['cantidad'] = str(int(cantidad)*1000)
            #Si en cant_unidad existe valores relacionados con gramos entonces:
            elif g :
                cantidad = cant_unid.split(g.group())[0].strip()
                item['unidad']="Gramos"
                item['cantidad'] = cantidad
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
        else :
            unidad = unidad_tmp.strip()
            #Palabras sin unidades de medida
            pat0 = re.compile('((P|p)ack|(B|b)andeja,(P|p)aqute)')
            #Se busca patron de gramos 
            pat1 = re.compile('(Grs|Gramos|gramos|Grs.|gr.|gr|Gr|Gr.|G|g.)')
            #Se busca patron de kilos
            pat2 = re.compile('(Kilos|Kilo|kilo|Kilo|kl|Kl|kg|K|k)')
            #Se busca patron de unidades
            pat3 = re.compile('(Unidades|Unidad|Unid.|unidades|unidad|uds|ud|Ud|unid.|C/U)')
            o = pat0.search(unidad)
            g = pat1.search(unidad) 
            k=  pat2.search(unidad)            
            u = pat3.search(unidad)

            if o:
                item['unidad']=unidad_tmp.strip()
                item['cantidad'] = "1"                           
            #Si en unidad existe valores relacionados con kilo entonces:
            elif k:
                item['unidad'] = 'Gramos'
                item['cantidad'] = "1000"
            #Si en unidad existe valores relacionados con gramos entonces:
            elif g :
                item['unidad']="Gramos"
                item['cantidad'] = "1"
            #Si en unidad existe valores relacionados con unidades entonces:  
            elif u:
                item['unidad']="Unidades"
                item['cantidad'] = "1"
            #Else que funcionará cuando las unidades no sean los string anteriores
            else:
                item['unidad']=unidad_tmp.strip()
                item['cantidad'] = "1"           
        return item