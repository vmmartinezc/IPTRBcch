# Author: Víctor martinez
# Fecha : 1 March 2017
# collaborators: 
# Propósito: Crear Estadísticas de precios
#==========================================
# 0. Perar el sistema para Run: cargar paquetes y librerias iniciales.
rm(list=ls()) 
## Identifico path para cargar los datos:
if (path.expand('~/')=='/Users/victormartinez/'){
  print('Mac Victor')
  pathGit <- '~/iptr-local/prod/IPTRBcch/RScripts'
  pathDrpx <- '~/Dropbox/iptr-sharedJP/bbddbranch/frutas_verdurasJP'
} else if (path.expand('~/')=='/Users/ruben/'){
  print('MAC Ruben')
  pathGit<-'~/iptr-local/prod/IPTRBcch/RScripts'
  pathDrpx <- '~/Dropbox/iptr-sharedJP/bbddbranch/frutas_verdurasJP'
} else if (path.expand('~/')=="/root/"){
  print('Servidor')
  pathGit<-'/home/spot/iptr-local/IPTRBcch/RScripts'
  pathDrpx <- '/home/spot/Dropbox/iptr-sharedJP/bbddbranch/frutas_verdurasJP'
} else {
  print('Juan Pablo')
  pathGit<-'~/iptr-local/prod/IPTRBcch/RScripts'
  pathDrpx <- '~/Dropbox/iptr-sharedJP/bbddbranch/frutas_verdurasJP'
}
#Homogenizo el Locade con el que usa el computador. Como estamos usando muchos sistemas operativos con 
# lenguajes gringos y páginas con caracteres en español, R se confunde.
Sys.setlocale('LC_ALL','C')

## 1. Arranque de Programas
setwd(pathGit) # Direcci??n working
source('arranque.R')

# 2. Revisar lo que nos entrega el proceso en python
source('checkdatos.R')

# 3. Prepara BASE MADRE
setwd(pathGit) #ir al path correcto (Git)
source('preparabbdd.R')


# 4. Cálculo índice
setwd(pathGit) #ir al path correcto (Git)
source('calculo.R')

#FIN

