#!/bin/bash

PATH=$PATH:/usr/local/bin
export PATH

#cd /home/ruben/Dropbox/IPTR/proc/amb_prueba/od_bdfv_d_v0.20/odepa_srv/
cd /home/spot/iptr-local/IPTRBcch/odepa_srv/
# Run Python Script Odepa Boletin Diario Frutas y Verdurias Diario (pscr_od_bdfv_d)
python pscr_od_bdfv_d.py
#Se eliminan datos en caso de que puedan ocasionar problemas
rm errores.csv
rm output*
#Se eliminan archivos almacenados en caché que pueden provenir de compilaciones anteriores 
find . -name \*.pyc -delete

#Primero se le agrega al archivo de odepa que tiene el nombre de los atributos en la primera fila, definido en python
#cat 'url,producto,variedad,mercado,volumen,calidad,precioMin,precioProm,precioMax,unidad','tipo'> output.csv
echo 'url,producto,variedad,mercado,volumen,calidad,precioMin,precioProm,precioMax,unidad','tipo'>> output.csv
#cat  od_bdfv_dcsv> output.csv
cat  output_* >>output.csv
#Se crea archivos de errores
echo 'Archivos csv generados por script del mismo nombre sin la palabra output_ y extension .csv' >> errores.csv

#Recorremos todos los archivos que empiecen con la palabra output_...
for entry in $(ls output_*)
do
   if [ -s ${entry} ];then
       echo archivo correcto: ${entry}
   else
       echo archivo vacío : ${entry}
       echo  ${entry} >> errores.csv
   fi
done


#mv output.csv "/home/ruben/Dropbox/IPTR/proc/amb_prueba/od_bdfv_d_v0.20/output_files/`date +%Y%m%d_%H`_d.csv"

#/usr/local/stata/./stata -b do /home/ruben/Dropbox/IPTR/proc/amb_prueba/od_bdfv_d_v0.20/stata/do/main.do 

#cd /home/ruben/Dropbox/IPTR/proc/amb_prueba/od_bdfv_d_v0.20/ 
#bash genPDF.sh

#cd /home/ruben/Dropbox/IPTR/proc/amb_prueba/od_bdfv_d_v0.20/odepa_srv/ && sudo -u ruben sh bash_od_bdfv_d.sh
