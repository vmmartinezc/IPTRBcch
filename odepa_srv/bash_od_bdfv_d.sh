#!/bin/bash

PATH=$PATH:/usr/local/bin
export PATH

cd /home/ruben/Dropbox/IPTR/proc/amb_prueba/od_bdfv_d_v0.20/odepa_srv/
# Run Python Script Odepa Boletin Diario Frutas y Verdurias Diario (pscr_od_bdfv_d)
python pscr_od_bdfv_d.py
#mv output.csv "/home/ruben/Dropbox/IPTR/proc/amb_prueba/od_bdfv_d_v0.20/output_files/`date +%Y%m%d_%H`_d.csv"

#/usr/local/stata/./stata -b do /home/ruben/Dropbox/IPTR/proc/amb_prueba/od_bdfv_d_v0.20/stata/do/main.do 

#cd /home/ruben/Dropbox/IPTR/proc/amb_prueba/od_bdfv_d_v0.20/ 
#bash genPDF.sh

#cd /home/ruben/Dropbox/IPTR/proc/amb_prueba/od_bdfv_d_v0.20/odepa_srv/ && sudo -u ruben sh bash_od_bdfv_d.sh
