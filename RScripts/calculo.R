## Utilizo la base mdre construida en los procesos anteriores
# Scrip para hacer el índice de precios:
# 0. Arranco ordenando archivos de la carpeta
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
} else if (path.expand('~/')=='/home/spot/'){
  print('Servidor')
  pathGit<-'~/iptr-local/IPTRBcch/RScripts'
  pathDrpx <- '~/Dropbox/iptr-sharedJP/bbddbranch/frutas_verdurasJP'
} else {
  print('Juan Pablo')
  pathGit<-'~/iptr-local/prod/IPTRBcch/RScripts'
  pathDrpx <- '~/Dropbox/iptr-sharedJP/bbddbranch/frutas_verdurasJP'
}

setwd(pathDrpx)
bm<-readRDS('Rbases/bm1.rds')

# Ordeno la base madre por: producto, tienda, fecha
bmine<-subset.data.frame(bm,bm$productosINE!=0) 
bmine<-bmine[order(bmine$productosINE,bmine$tienda,as.POSIXct(bmine$fecha)),] 

## 1. Ordeno las variedades y las tiendas:

# a. Creo un ID por tienda:
bmine$idtienda<-with(bmine, ave(rep(1, nrow(bmine)), bmine$tienda, FUN = seq_along))

# Ordeno la categoía de variedad para completarla. Hay que considerar que en ODEPA existe una categoría, 
# en algunas bases hay NA y en otras simplemente está vacío.
bmine$variedad<-ifelse(bmine$variedad==''|is.na(bmine$variedad),0,bmine[,c('variedad')])

## Vamos a completar los 0 con las variedades que encontremos para cada alimento:

## HORTALIZAS FRESCAS
##=======================================

#Acelga
bmine$variedad <-
  
bmine$producto2<-str_extract(bmine[,c('producto')],'^[a-z].*[a-z]+ ')
                          
test<-as.data.frame(bmine[,c('fecha','producto','producto2','tienda','productosINE')])



print('Fin del calculo')



