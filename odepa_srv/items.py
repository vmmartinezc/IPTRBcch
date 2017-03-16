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


    def tostani(unidad_tmp):
        item = {'unidad':"",'cantidad':"",'producto':""}
        unidad_tmp = unidad_tmp.lower()
        part0 = re.compile('\d+\s?(kg|grs)')
        gramos_kl = part0.search(unidad_tmp)
        if gramos_kl:
            item['producto'] = unidad_tmp.replace(gramos_kl.group(),"")
            #Se obtiene el valor
            pat1 = re.compile('\d+')
            valor = pat1.search(gramos_kl.group())
            unidad = gramos_kl.group().replace(valor.group(),"").strip()
            if unidad=='kg':
                item['unidad'] = 'Gramos'
                item['cantidad'] = int(valor.group())*1000
                return item           
            else:
                item['unidad'] = 'Gramos'
                item['cantidad'] = valor.group()
                return item
        else:
            item['unidad'] = ''
            item['cantidad'] = unidad_tmp
            return item

    def vegetalesyfrutas(unidad_tmp):
        item = {'unidad':"",'cantidad':"",'producto':""}
        unidad_tmp = unidad_tmp.lower().replace(",",".")
        part0 = re.compile('\d{1,3}\sx\d{1,3}\sun(\.)?')
        particular = part0.search(unidad_tmp)
        
        pat0 = re.compile('\d(\.\d)?\sa\s\d(\.\d)?')
        particular2 = pat0.search(unidad_tmp)

        #Valores relacionados a kilos
        pat= re.compile('(\d{1,3}(\.)){0,1}\d{0,5}\s{0,2}(kilos|kilo|kgs\.|kg\.|kg|k(\s|$))')
        kilos = pat.search(unidad_tmp)
        #Valores relacionados a gramos
        pat1= re.compile('\d{1,5}\s{0,2}(\.)?(grs(\.)?|gr|g)')
        gramos = pat1.search(unidad_tmp)
        #Valors relacionados con unidades
        pat2= re.compile('\d{0,5}\s{0,2}(un(\.)?|mata(s)?(\.)?|cabeza(s)?|atado(\.)?|bandeja|pqte(\.)?$|bdja(\.)?|mitad$)')
        unidades = pat2.search(unidad_tmp)

        if particular:
            item['producto'] = unidad_tmp.replace(particular.group(),"")
            valores = particular.group().replace("un","").split("x")
            item['unidad'] = 'Unidades'
            item['cantidad'] =  str((float(valores[0].strip()) * float(valores[1].strip()))).replace(".0","")
            return item
        elif particular2:
            item['producto'] = unidad_tmp.replace(particular2.group(),"")
            valores = particular2.group().split("a")
            item['unidad'] = 'Gramos'
            item['cantidad'] = str((float(valores[0].strip()) + float(valores[1].strip()))*1000/2).replace(".0","")
            return item
       #Buscamos las expresiones que tengan la palabra kilo ej 2kilo, kilo...
        elif kilos:
            item['producto'] = unidad_tmp.replace(kilos.group(),"")
            pataux= re.compile('(\d{1,3}(\.)){0,1}\d{1,5}')
            numero_antes = pataux.search(kilos.group())
            if numero_antes:
                item['unidad'] = 'Gramos'
                item['cantidad'] = str(float(numero_antes.group().strip())*1000).replace(".0","")
                return item
            else:
                item['unidad'] = 'Gramos'
                item['cantidad'] = '1000'
                return item
        elif gramos:
            item['producto'] = unidad_tmp.replace(gramos.group(),"")
            pataux= re.compile('\d{1,5}')
            numero_antes = pataux.search(gramos.group())
            if numero_antes:
                item['unidad'] = 'Gramos'
                item['cantidad'] = (numero_antes.group().strip())
                return item
            else:
                item['unidad'] = 'Gramos'
                item['cantidad'] = '1'
                return item
        elif unidades:
            item['producto'] = unidad_tmp.replace(unidades.group(),"")
            pataux= re.compile('\d{1,5}')
            numero_antes = pataux.search(unidades.group())
            if numero_antes:
                item['unidad'] = 'Unidades'
                item['cantidad'] = numero_antes.group().strip()
                return item
            else:
                item['unidad'] = 'Unidades'
                item['cantidad'] = '1'
                return item
        else:
            item['producto'] = unidad_tmp
            item['unidad'] = 'SIN INFORMACION'
            item['cantidad'] = "0"




    def verdurasyfrutas(unidad_tmp):
        item = {'unidad':"",'cantidad':""}
        unidad_tmp = unidad_tmp.lower()
        pat= re.compile('(\d[\/]){0,1}\d{0,5}\s{0,2}(x){0,1}(kg|kilo|unid|und|g\.|gr|grs|gramos|g|litro|cc)')
        pat1 = re.compile('(\d[\/]){0,1}\d{1,5}')
        match = pat.search(unidad_tmp)
        tiene_valor = pat1.search(unidad_tmp)

        if match and tiene_valor:
            cantidad= tiene_valor.group()
            unidad =match.group().replace(cantidad,"").strip()
            if unidad =='litro':
                #Verificamos si tiene una fraccion
                pat= re.compile('\d[\/]\d')
                fraccion = pat.search(cantidad)
                if fraccion:
                    #ej. 1/2 .. valor0 =1 ... valor1: =2
                    valores=fraccion.group().split("/")
                    cantidad = float(valores[0].strip())/float(valores[1].strip())
                    item['unidad'] = 'CC'
                    item['cantidad'] = str(float(cantidad*1000)).replace(".0","")
                    return item
                else:
                    item['unidad'] = 'CC'
                    item['cantidad'] = "1000"
                    return item

            elif unidad=='cc':
                 item['unidad'] = 'CC'
                 item['cantidad'] = cantidad
                 return item

            elif unidad=='kilo'  or unidad=='kg':
                #Verificamos si tiene una fraccion
                pat= re.compile('\d[\/]\d')
                fraccion = pat.search(cantidad)
                if fraccion:
                    #ej. 1/2 .. valor0 =1 ... valor1: =2
                    valores=fraccion.group().split("/")
                    cantidad = float(valores[0].strip())/float(valores[1].strip())
                    item['unidad'] = 'Gramos'
                    item['cantidad'] = str(float(cantidad*1000)).replace(".0","")
                    return item
                else:        
                    item['unidad'] = 'Gramos'
                    item['cantidad'] = int(cantidad.strip())*1000
                    return item
            elif unidad=='g' or unidad=='gramos' or unidad=='g.' or unidad=='gr':
                item['unidad'] = 'Gramos'
                item['cantidad'] = cantidad
                return item
            else:
                item['unidad'] = "Unidades"
                item['cantidad'] = cantidad                   
                return item
        else: 
            #Nos aseguramos que la unidad esté
            pat= re.compile('(kg|kilo|unid|und|g\.|gr|grs|gramos|g|paquete)')
            unidad = pat.search(unidad_tmp)
            if unidad:
                if unidad.group()=='kilo'  or unidad.group()=='kg':
                    item['unidad'] = 'Gramos'
                    item['cantidad'] = '1000'
                    return item
                elif unidad.group()=='g' or unidad.group()=='gramos'  or unidad.group()=='grs'  or unidad.group()=='g.':
                    item['unidad'] = 'Gramos'
                    item['cantidad'] = cantidad
                    return item
                else:
                    item['unidad'] = "Unidades"
                    item['cantidad'] = "1"                   
                    return item

            else:

                item['unidad'] = "Unidades"
                item['cantidad'] = "1"                  
                return item



#2 Unidades 2 Kilos 400 Grs 1 kilo 1 Unidad paquete gde 1 Bandeja 1 Paquete  
    def vegavirtual(unidad_tmp): 
        item = {'unidad':"",'cantidad':"",'producto':""}
        unidad_tmp = unidad_tmp.lower()
        pataux =re.compile('paquete\s{0,2}gde')
        particular = pataux.search(unidad_tmp)
        pat= re.compile('\d{1,5}\s{1,2}(kilo(s)?|unidad(es)?|bandeja(s)?|paquete|grs|gramo(s)?)')
        match = pat.search(unidad_tmp)

        if particular:
            item['producto'] = unidad_tmp.replace(particular.group(),"")
            item['unidad'] = 'Unidades'
            item['cantidad'] = '1'
            return item

        if match:
            #Se elimina la unidad de medida que se encuentra en el nombre del producto
            item['producto'] = unidad_tmp.replace(match.group(),"")
            cant_unid= match.group().split(" ")
            if cant_unid[1]=='kilo' or cant_unid[1]=='kilos':
                item['unidad'] = 'Gramos'
                item['cantidad'] = int(cant_unid[0].strip())*1000
                return item
            elif cant_unid[1]=='grs' or cant_unid[1]=='gramos':
                item['unidad'] = 'Gramos'
                item['cantidad'] = cant_unid[0]
                return item
            else:
                item['unidad'] = "Unidades"
                item['cantidad'] = cant_unid[0] 
                return item
        else: 
            item['unidad'] = ""
            item['cantidad'] =""
            item['producto'] = unidad_tmp
            return item
    
    
#    2000 los 250 gr    1300 el Kg     1200 la Unidad     2350 la Bolsa 350 gr aprox     350 la mata     1500 el Corte
    def superDes(unidad_tmp):
        item = {'unidad':"",'cantidad':"",'precio':""}
        unidad_tmp = unidad_tmp.lower()
        pat1 = re.compile('^\d{1,5}')
        #Obtenemos precio
        match1 = pat1.search(unidad_tmp)
        if match1:      
            item['precio']=match1.group().strip()
            unidad_tmp = unidad_tmp.replace(match1.group(),"")
            #Obtenemos cantidad y unidad de medida
            pat2 = re.compile('(el|los|la)(\s{0,2}\d{1,5}){0,1}\s{0,2}(gr|kg|mata|corte|unidad|bolsa|paquete)')
            #Se busca caso en especifico
            pat3 = re.compile('\d{1,4}\s{0,2}uni$')

            match2 = pat2.search(unidad_tmp)
            particular = pat3.search(unidad_tmp)
            if particular:
                 pataux= re.compile('\d{1,5}')
                 cantidad = pataux.search(particular.group())
                 cant_unid = particular.group().split(cantidad.group().strip())
                 item['unidad'] = "Unidades"
                 item['cantidad'] = cantidad.group().strip()
                 return item
            if match2:
                # Se obtine cantidad de unidad de medida
                pataux= re.compile('\d{1,5}')
                cantidad = pataux.search(match2.group())
                # Si tiene cantida  realizamos lo siguiente
                if cantidad:
                    #Se obtiene el tipo de unidad de medida
                    patuni = re.compile('(gr|kg|mata|corte|unidad|bolsa|paquete)')
                    unidad = patuni.search(match2.group())
                    if unidad.group()=='kg':
                        item['unidad'] = 'Gramos'
                        item['cantidad'] = int(cantidad.group().strip())*1000
                    elif unidad.group()=='gr':
                        item['unidad'] = 'Gramos'
                        item['cantidad'] = cantidad.group()
                    else:
                        item['unidad'] = "Unidades"
                        item['cantidad'] = cantidad.group()                   
                    return item
                #EJEMPLO 1200 el kg
                else:
                    #Se obtiene el tipo de unidad de medida
                    patuni = re.compile('(gr|kg|mata|corte|unidad|bolsa|paquete)')
                    unidad = patuni.search(match2.group())
                    if unidad.group()=='kg':
                        item['unidad'] = 'Gramos'
                        item['cantidad'] = '1000'
                    elif unidad.group()=='gr':
                        item['unidad'] = 'Gramos'
                        item['cantidad'] = '1'
                    else:
                        item['unidad'] = "Unidades"
                        item['cantidad'] = '1'                  
                    return item

        item['unidad'] = "Unidades"
        item['cantidad'] = "Sin informacion" 
        item['precio'] = 'Sin informacion'  
        return item

    def tottus(unidad_tmp):
        item = {'unidad':"",'cantidad':"",'producto':""}
        unidad_tmp = unidad_tmp.lower().replace("unidades","un")
        pat1 = re.compile('\d{1,5}\s{0,2}(un){0,1}\s{0,2}(kgs|x\s{0,2}kg|kg|grs|unidades|unidad|un)')
        match1 = pat1.search(unidad_tmp)
        if match1:
            cant_unid = match1.group()
            pat0 = re.compile('x\s{0,2}(kg|kgs)')
            #Se busca patron de kilos
            pat1 = re.compile('(kg|kgs)')
            #Se busca patron de gramos 
            pat2 = re.compile('grs')
            #Se busca patron de unidades
            pat3 = re.compile('unidades|unidad|un')

            kaux = pat0.search(cant_unid)
            k=  pat1.search(cant_unid) 
            g = pat2.search(cant_unid)
            u = pat3.search(cant_unid)            

            if kaux:
                item['unidad'] = 'Gramos'
                item['cantidad'] = '1000'
                return item

            #Si en cant_unidad existe valores relacionados con kilo entonces:
            elif k:
                pataux = re.compile('\d{1,5}')
                matchaux = pataux.search(cant_unid)
                item['unidad'] = 'Gramos'
                item['cantidad'] = str(int(matchaux.group())*1000)
                return item
            #Si en cant_unidad existe valores relacionados con gramos entonces:
            elif g :
                pataux = re.compile('\d{1,5}')
                matchaux = pataux.search(cant_unid)
                item['unidad'] = 'Gramos'
                item['cantidad'] = matchaux.group()
                return item
            #Si en cant_unidad existe valores relacionados con unidades entonces:  
            elif u:
                pataux = re.compile('\d{1,5}')
                matchaux = pataux.search(cant_unid)
                item['unidad'] = 'Unidades'
                item['cantidad'] = matchaux.group()
                return item
        else:      
            item['unidad']="Unidades"
            item['cantidad'] = "1"
            return item

    def manolo(unidad_tmp):
        item = {'unidad':"",'cantidad':"",'producto':""}
        unidad_tmp = unidad_tmp.lower().strip("$")
        #Se busca un numero con 1 o mas digitos 
        pat0 = re.compile('\d+\s?')
        precio = pat0.search(unidad_tmp)
        if precio:
            item['precio'] = precio.group()
        else:
            item['precio'] = '0'

        pat1 = re.compile('(el|la){0,1}(kilo|mata|bolsa|gr.|pte|c/u|unidad|malla|chico)$')
        match1 = pat1.search(unidad_tmp)

        pat2 = re.compile('\d{1,2}[\/]\d{1,2}')
        fraccion = pat2.search(unidad_tmp)

        if fraccion:
             #ej. 1/2 .. valor0 =1 ... valor1: =2
            valores=fraccion.group().split("/")
            cantidad = float(valores[0].strip())/float(valores[1].strip())
            item['unidad'] = 'Gramos'
            item['cantidad'] = str(float(cantidad*1000)).replace(".0","")
            return item

        elif match1:

            cant_unid = match1.group().replace("el","").replace("la","")
            #Se busca patron de kilos
            pat1 = re.compile('kilo|kl')
            #Se busca patron de gramos
            pat3 = re.compile('gr\.|gramos')
            
            k=  pat1.search(cant_unid) 
            #u = pat2.search(cant_unid)            
            u = pat3.search(cant_unid)
            f = pat0.search(cant_unid)

            #Si en cant_unidad exist valores relacionados con kilo entonces:
            if k:
                cantidad = cant_unid.split(k.group())[0].strip()
                item['unidad'] = 'Gramos'
                item['cantidad'] = '1000'
                return item
            elif u:
                cantidad = cant_unid.split(u.group())[0].strip()
                item['unidad'] = 'Gramos'
                item['cantidad'] = cantidad
                return item
            else:
                item['unidad']="Unidades"
                item['cantidad'] = "1"
                return item
        return item

    def chacra(unidad_tmp):
        unidad_tmp = unidad_tmp.lower()
        item = {'unidad':"",'cantidad':"",'producto':""}
        pat1 = re.compile('^(kg\.|c/u|unid\.?|atado)$')
        pat2 = re.compile('^\d{1,5}\s{0,2}(kg.|unid.|unidades|gr.|atados)')
        pat3 = re.compile('\d(,|\.)\d\s{0,2}(kg|unid.|unidades|gr.|atados)')


        match1 = pat1.search(unidad_tmp)
        match2 = pat2.search(unidad_tmp)
        match3 = pat3.search(unidad_tmp)
        if match3:
            cant_unid = match3.group().replace(",",".")
            #Se obtiene decimal
            aux1 = re.compile('\d(,|\.)\d')
            #Borra decimal y queda solo unidad
            unidad=cant_unid.strip(aux1.search(cant_unid).group()).replace(".","").strip()
            matchaux=aux1.search(cant_unid).group().strip()
            if unidad=='kg':
                item['unidad'] = 'Gramos'
                item['cantidad'] = str(float(matchaux)*1000).replace(".0","")
                return item
            if unidad=='gr':
                item['unidad'] = 'Gramos'
                item['cantidad'] = matchaux
                return item
     
        if match1:
            cant_unid = match1.group()
            if cant_unid=='kg.':
                 item['unidad'] = 'Gramos'
                 item['cantidad'] = '1000'
            else:
                 item['unidad'] = 'Unidades'
                 item['cantidad'] = '1'
            return item

        if match2:
            cant_unid = match2.group()
            #Se busca patron de kilos
            pat1 = re.compile('kg.')
            #Se busca patron de gramos 
            pat2 = re.compile('unid.|unidades|atado')
            #Se busca patron de unidades
            pat3 = re.compile('gr.')
            
            k=  pat1.search(cant_unid) 
            u = pat2.search(cant_unid)            
            g = pat3.search(cant_unid)
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

        return item


    def odepa (unidad_tmp):
        item = {'unidad':"",'cantidad':"",'producto':""}
        unidad_tmp = unidad_tmp.lower().replace("$","").replace("/","")
        pat = re.compile('\d{1,5}\s{1,2}((K|k)ilos|(U|u)nida(d|des)|(g|G)ramos)')
        pat1 = re.compile('docena$|paquete$|unidad$')
        pat2 = re.compile('^docena\s{1,2}de.*')
        pat3 = re.compile('\d(,|\.)\d+\s{1,2}a\s{1,2}\d\s{0,2}(((K|k)(ilos|ilo))|((G|g)(ramos|ramo)))')
        match = pat.search(unidad_tmp)
        match1 = pat1.search(unidad_tmp)
        match2 = pat2.search(unidad_tmp)
        match3 = pat3.search(unidad_tmp)
        #ej. 0.1 a 2 kilos
        if match3:
            cant_unid = match3.group().replace(",",".")
            aux = re.compile('\d')
            aux1 = aux.search(cant_unid.split("a")[1])
            uni = re.compile('((K|k)(ilos|ilo))')
            uni1 =  uni.search(cant_unid.split("a")[1])
            #kilos
            if aux1 and uni1:
                cantidad = float((float(aux1.group().strip()) + float(cant_unid.split("a")[0].strip()))/2)
                item['unidad'] = 'Gramos'
                item['cantidad'] = str(float(cantidad*1000)).replace(".0","")
                return item
            #gramos
            else:
                cantidad = float((float(aux1.group().strip()) + float(cant_unid.split("a")[0].strip()))/2)
                item['unidad'] = 'Gramos'
                item['cantidad'] = cantidad.replace(".0","")
                return item
       
        if match:
            cant_unid = match.group()
            #Se busca patron de kilos
            pat1 = re.compile('(K|k)ilo')
            #Se busca patron de gramos 
            pat2 = re.compile('(U|u)nida(d|des)')
            #Se busca patron de unidades
            pat3 = re.compile('(g|G)ramos')
            
            k=  pat1.search(cant_unid) 
            u = pat2.search(cant_unid)            
            g = pat3.search(cant_unid)
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
            return item
        #ej. docena de matas
        if match2:
            item['unidad']="Unidades"
            item['cantidad'] = "12"
            return item

        #ej. 4 unidades
        pataux = re.compile('(docena\sde)')
        particular = pataux.search(unidad_tmp)
        pataux2 = re.compile('(kilo\s\()')
        part2 =  pataux2.search(unidad_tmp)
        if match1 : 
            cant_unid = match1.group()
            if cant_unid == 'docena':
                item['unidad']="Unidades"
                item['cantidad'] = "12"
            else:
                #cantidad = cant_unid.split(u.group())[0].strip()
                item['unidad']="Unidades"
                item['cantidad'] = "1"
            return item
        elif particular:
             item['unidad']="Unidades"
             item['cantidad'] = "12"
        elif part2:
             item['unidad']="Gramos"
             item['cantidad'] = "1000"

        else :
            item['unidad']= unidad_tmp

        return item



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