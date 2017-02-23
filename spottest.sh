#echo date \'+%s\' -d \'+ 24 hours\' > /sys/class/rtc/rtc0/wakealarm
#!/bin/bash

PATH=$PATH:/usr/local/bin
export PATH

# Setup de folder
cd /home/ruben/Dropbox/IPTR/proc/amb_prueba/od_bdfv_d_v0.20/

# Primer script a correr es el de Scrapy, tiene que ser como root
echo "Iniciando scrpit de scrapy"
sudo -u root bash scrapy.sh
