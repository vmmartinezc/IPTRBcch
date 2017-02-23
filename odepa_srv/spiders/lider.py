#!/usr/bin/env python
# -*- coding: utf-8 -*-
from scrapy.spiders import Spider
from scrapy.selector import Selector
from odepa_srv.items import *
#from bs4 import BeautifulSoup
#from selenium import webdriver

#Página : https://www.lider.cl/
class Lider(Spider):
    name="lider"
    #Estructuras html iguales
    start_urls = ["https://www.lider.cl/walmart/catalog/category.jsp?id=cat640020&pId=CF_Nivel1_000004&navAction=jump&navCount=0#categoryCategory=cat640020"]
                    #"https://www.lider.cl/walmart/catalog/category.jsp?id=cat640020&pId=CF_Nivel1_000004&navAction=jump&navCount=0#categoryCategory=cat640020&pageSizeCategory=20&currentPageCategory=2&currentGroupCategory=1&lowerLimitCategory=0&upperLimitCategory=0&&849",
                    #"https://www.lider.cl/walmart/catalog/category.jsp?id=cat640020&pId=CF_Nivel1_000004&navAction=jump&navCount=0#categoryCategory=cat640020&pageSizeCategory=20&currentPageCategory=3&currentGroupCategory=1&lowerLimitCategory=0&upperLimitCategory=0&&252"]
   
    allow_domains = ['lider.cl']
    def parse(self, response):
        driver = webdriver.Chrome()
        driver.get(self.start_urls[0])
        #Se obtiene la fuente  de la pegina obtenida
        html = driver.page_source 
        s = BeautifulSoup(html,'lxml')
        datos = s.find_all(id ='cajaResultado')
        precios = s.find_all('span','sale-price')
        nombres = s.find_all('div','nombre')
        
        print (precios)
    
