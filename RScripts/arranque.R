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

print('Las librerías se cargaron con éxito')
print(newpack)
rm(newpack)
rm(packvic)


