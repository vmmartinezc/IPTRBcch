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

# Desactivamos el espacio virtual
deactivate

# Vamos a Correr el main de R, para esto:
## 1. vamos al cd correspondiente
cd ~/iptr-local/IPTRBcch/RScripts
## 2. corremos el Script de R
echo "Inicia construcción de BBDD"
R CMD BATCH mainS.R
## 3. Se genera un output con el run, ese se mueve a otra carpeta.
mv mainS.Rout /home/spot/Dropbox/iptr-sharedJP/bbddbranch/frutas_verdurasJP/Routput/R_`date +%Y%m%d_%H`_d.Rout
