#!/bin/bash

PATH=$PATH:/usr/local/bin
export PATH

# Setup de folder
cd /home/ruben/Dropbox/IPTR/proc/amb_prueba/od_bdfv_d_v0.20/

# Primer script a correr es el de Scrapy, tiene que ser como root
echo "Iniciando scrpit de scrapy"
sudo -u root bash scrapy.sh

echo "Iniciando procesamiento en Stata ... espere por favor"
# Ahora procesamos via Stata y generamos EPS y TEX, tiene que ser como user ruben
/usr/local/stata/./stata -b do /home/ruben/Dropbox/IPTR/proc/amb_prueba/od_bdfv_d_v0.20/stata/do/main.do 

# Y procesamos TEX, generamos PDF y limpiamos los archivos
echo "Iniciando procesamiento de tex"
bash /home/ruben/Dropbox/IPTR/proc/amb_prueba/od_bdfv_d_v0.20/genPDF.sh

