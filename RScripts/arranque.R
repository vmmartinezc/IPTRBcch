
## Identifico path para cargar los datos:
if (path.expand('~/')=='/Users/victormartinez/'){
  print('Mac Victor')
  pathR<-'~/iptr-local/prod/IPTRBcch/RScripts'
} else if (path.expand('~/')=='/Users/ruben/'){
  print('MAC Ruben')
  pathR<-'~/iptr-local/prod/IPTRBcch/RScripts'
} else if (path.expand('~/')=='/home/spot/'){
  print('Servidor')
  pathR<-'~/iptr-local/IPTRBcch/RScripts'
} else {
  print('Juan Pablo')
  pathR<-'~/iptr-local/prod/IPTRBcch/RScripts'
}
setwd(pathR) # Direcci??n working

## Con el Path puedo abrir el archivo de paquetes

packvic <- readRDS('inicial.rds') # Paquetes que hay que tener instalados (lectura)
## a. Instalar paquetes SSI es necesario.
newpack <- packvic[!(packvic %in% installed.packages()[,"Package"])] #comparar paquetes en la máquina con los necesarios
if(length(newpack)) install.packages(newpack, ,repos = "http://cran.us.r-project.org")  # Sólo instalar si hay diferencias

## b. Librerias Cargadas
library(grid)
library(tableplot)
library(stringr)
library(ggplot2)
library(gmodels)
library(tools)
library(foreign)
library(readstata13)
library(stringr)
library(plyr); library(dplyr) # Es clave el orden.
library(formattable)
library(RColorBrewer)
library(data.table)



print(newpack)
rm(newpack)
rm(packvic)


