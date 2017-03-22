#!/bin/bash

PATH=$PATH:/usr/local/bin
export PATH

#cd /home/ruben/Dropbox/IPTR/proc/amb_prueba/od_bdfv_d_v0.20/odepa_srv/
cd /home/spot/iptr-local/IPTRBcch/odepa_srv/

# Run Python Script Odepa Boletin Diario Frutas y Verdurias Diario (pscr_od_bdfv_d)
python pscr_od_bdfv_d.py
	
#Primero se le agrega al archivo de odepa que tiene el nombre de los atributos en la primera fila, definido en python
echo 'url,producto,variedad,mercado,volumen,calidad,precioMin,precioProm,precioMax,precio,cantidad,unidad,fuente,tipo'>> output.csv
#cat  od_bdfv_dcsv> output.csv
cat  output_* >>output.csv
#Se crea archivos de errores
echo 'Archivos csv generados por script del mismo nombre sin la palabra output_ y extension .csv' >> errores.csv

#Se crea una carpeta donde se alamacenaran los archivos csv exportadas por cada pagina
mkdir /home/spot/Dropbox/iptr-sharedJP/bbddbranch/frutas_verdurasJP/archivos_sep/`date +%Y%m%d_%H`_d
#Recorremos todos los archivos que empiecen con la palabra output_...
for entry in $(ls output_*)
do
   if [ -s ${entry} ];then
       echo archivo correcto: ${entry}
       #Se alamacena el archivo independiente
       mv ${entry} /home/spot/Dropbox/iptr-sharedJP/bbddbranch/frutas_verdurasJP/archivos_sep/`date +%Y%m%d_%H`_d/
   else
       echo archivo vacío : ${entry}
       echo  ${entry} >> errores.csv
       rm ${entry}
   fi
done

#Se mueve el archivo output y los errores a las siguientes rutas
mv output.csv /home/spot/Dropbox/iptr-sharedJP/bbddbranch/frutas_verdurasJP/`date +%Y%m%d_%H`_d.csv
mv errores.csv /home/spot/Dropbox/iptr-sharedJP/bbddbranch/frutas_verdurasJP/errores/`date +%Y%m%d_%H`_d.csv

#Reestablecemos ruta, y se ejecuta la sentencia para eliminar los archivos que terminen con .pyc
cd /home/spot/iptr-local
find . -name \*.pyc -delete

#Normalizamos archivo descargado
cd /home/spot/Dropbox/iptr-sharedJP/bbddbranch
python normaliza_por_archivo.py
#/usr/local/stata/./stata -b do /home/ruben/Dropbox/IPTR/proc/amb_prueba/od_bdfv_d_v0.20/stata/do/main.do 

#cd /home/ruben/Dropbox/IPTR/proc/amb_prueba/od_bdfv_d_v0.20/ 
#bash genPDF.sh

#cd /home/ruben/Dropbox/IPTR/proc/amb_prueba/od_bdfv_d_v0.20/odepa_srv/ && sudo -u ruben sh bash_od_bdfv_d.sh
