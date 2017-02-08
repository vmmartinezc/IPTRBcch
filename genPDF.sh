#!/bin/bash

PATH=$PATH:/usr/local/bin
export PATH

shopt -s nullglob

echo "Iniciando procesamiento de archivos Tex ..."
echo "... removiendo versiones anteriores de .tex"
rm -rf /home/ruben/proc/tex/
echo "... moviendo archivos .tex nuevos"
mv /home/ruben/Dropbox/IPTR/proc/amb_prueba/od_bdfv_d_v0.20/tex/ /home/ruben/proc/tex/

FILES=/home/ruben/proc/tex/*.tex
cd /home/ruben/proc/tex/

echo "... iniciando batch para archivos nuevos"
for f in $FILES
do
	echo "Generando pdf para $f ..."
	nomCom=${f##*/}
	nomTri=${nomCom%%.*}
	pdflatex -shell-escape -interaction=batchmode $nomTri".tex"
	mv $nomTri".pdf" "/home/ruben/Dropbox/IPTR/proc/amb_prueba/od_bdfv_d_v0.20/pdf/${nomTri}.pdf"
	echo "... archivo generado, procesado y movido a destino final"
done

echo "... limpiando directorios de archivos innecesarios"
rm -rf /home/ruben/proc/tex/
rm -rf /home/ruben/Dropbox/IPTR/proc/amb_prueba/od_bdfv_d_v0.20/tex/
rm -rf /home/ruben/Dropbox/IPTR/proc/amb_prueba/od_bdfv_d_v0.20/eps/
echo "... regenerando estructura de directorios"
mkdir /home/ruben/proc/tex/
mkdir /home/ruben/Dropbox/IPTR/proc/amb_prueba/od_bdfv_d_v0.20/tex/
mkdir /home/ruben/Dropbox/IPTR/proc/amb_prueba/od_bdfv_d_v0.20/eps/

echo "Proceso finalizado con éxito."