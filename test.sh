#!/bin/bash
#PATH=$PATH:/usr/local/bin
#export PATH
#Primero volver a la carpeta inicial en Spot
cd
# Primer paso activar el espacio victual. Para eso:
source test_virtual/bin/activate

# Setup de folder
cd ~/iptr-local/IPTRBcch/odepa_srv

echo "Iniciando scrpit de scrapy"
bash bash_od_bdfv_d.sh



