# -*- coding: utf-8 -*-
from selenium import webdriver

urls_jumbo = [
    #Frutas
    "http://www.jumbo.cl/FO/CategoryDisplay?cab=4006&int=11&ter=124",
    #Verduras
    "http://www.jumbo.cl/FO/CategoryDisplay?cab=4006&int=11&ter=125",
    #Frutos secos
    "http://www.jumbo.cl/FO/CategoryDisplay?cab=4006&int=11&ter=123"
    ]
driver = webdriver.Chrome()
aux = 0
for x in range(len(urls_jumbo)):
    driver.get(urls_jumbo[x])
    nombres = driver.find_elements_by_xpath('//*[@id="ficha"]/b')
    precios = driver.find_elements_by_xpath('//*[@id="tabla_productos"]/tbody/tr/td/ul/li/div/div[3]/div[1]')
    unidad = driver.find_elements_by_xpath('//*[@id="tabla_productos"]/tbody/tr/td/ul/li/div/div[3]/div[2]')
    for i in range(len(nombres)):
        print('Producto: '+nombres[i].text+'/ Precio: '+precios[i].text + '/ Unidad: '+unidad[i].text)
        aux = aux+1

print('Cantidad de productos de Jumbo '+str(aux))
print('****************************************')

urls_lider = [
    #Verduras paginadas hasta 200 productos
    "https://electrohogar.lider.cl/supermercado/category/Pan-Vegetales/Verduras/Verduras/_/N-1rnk03k?N=&No=0&Nrpp=200",
    "https://electrohogar.lider.cl/supermercado/category/Pan-Vegetales/Verduras/Verduras-Congeladas/_/N-jyg8vi?N=&No=0&Nrpp=200",
    #Frutas 
    "https://electrohogar.lider.cl/supermercado/category/Pan-Vegetales/Frutas/Frutas-Frescas/_/N-c48hfq",
    "https://electrohogar.lider.cl/supermercado/category/Pan-Vegetales/Frutas/Frutas-Congeladas/_/N-172n2h5"
    ]
aux = 0
for x in range(len(urls_lider)):
    driver.get(urls_lider[x])
    nombres = driver.find_elements_by_xpath('//*[@id="productBox[326172]"]/div/div[1]/a/span[2]')
    precios = driver.find_elements_by_xpath('//*[@id="productBox[326172]"]/div/div[1]/div/span[1]')
    unidad = driver.find_elements_by_xpath('//*[@id="productBox[323490]"]/div/div[1]/div/span[2]/b')
    for i in range(len(nombres)):
        print('Producto: '+nombres[i].text+'/ Precio: '+precios[i].text + '/ Unidad: '+unidad[i].text)
        aux = aux+1

print('Cantidad de productos de Lider '+str(aux))
print('****************************************')



driver.close()
driver.quit()




