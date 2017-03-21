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
done<-readRDS('Rbases/done.rds')
bm<-readRDS('Rbases/bm1.rds')

# Ordeno la base madre por: producto, tienda, fecha
bmine<-subset.data.frame(bm,bm$productosINE!=0) 
bmine<-bmine[order(bmine$producto,bmine$productosINE,bmine$tienda,bmine$url),] 



