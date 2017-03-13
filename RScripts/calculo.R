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
temp1 <- file.info(list.files(pattern="*d.csv"))
#oldfile <- rownames(oldfile)
#saveRDS(oldfile1,file='Rbases/archivosbm.rds')

# cargo archivos no procesados
oldfile <- readRDS('Rbases/archivosbm.rds')
newfile <- subset(temp1,!(rownames(temp1) %in% oldfile[,1]))
## creo la hora desde el nombre
newfile$nom <- row.names(newfile)
newfile$fecha <- str_extract(newfile[,c('nom')],'[0-9]+')
newfile$hora <- str_extract(newfile[,c('nom')],"_[0-9]+")  
newfile$hora <- substring(newfile[,c('hora')],2)


if (nrow((newfile))!=0){
  print('Se encontraron los siguientes archivos no procesados:')
  print(rownames(newfile))
  # nrow(newfile)
  for (i in 1:nrow(newfile)){ 
    # Abro Archivos nuevos:
    try(assign(newfile[i,c('nom')],read.csv(file=newfile[i,c('nom')], header=TRUE, sep=",")))
    try(aux<-get(newfile[i,c('nom')]))
    # Creo una base auxiliar para trabajar
    aux[['test1']] <-  as.numeric(as.character(ifelse(is.na(str_extract(aux[,c('precio')],"[aA-zZ]+")),0,1)))
    aux[['test2']] <- as.numeric(as.character(ifelse(is.na(str_extract(aux[,c('cantidad')],"[aA-zZ]+")),0,1)))
    aux[['test3']] <- as.numeric(as.character(ifelse(is.na(str_extract(aux[,c('unidad')],"[aA-zZ]+")),1,0)))
    aux[['test4']] <- as.numeric(as.character(ifelse(is.na(str_extract(aux[,c('producto')],"[0-9]+")),0,1)))
    aux[['test']] <- as.numeric(as.character(aux[,c('test1')]+aux[,c('test2')]+aux[,c('test3')]+aux[,c('test4')]))
    ## Estadistica de la normalización
    viables <-as.data.frame(aggregate(test~fuente,aux,sum))
    setnames(viables,'test','gtest')
    aux <- merge.data.frame(aux,viables, by='fuente')
    aux1 <- subset.data.frame(aux,aux$gtest==0 & aux$cantidad!="")
    ## Se calculan los índices
    # 1. Se asignan variedades
    aux1$variedadINE <- 0
    #Aca debería haber un for
    #for(k in c('Manzana','Naranja','Pera','Platano')){
    # MANZANA
    aux1$variedadINE <- ifelse(is.na(str_extract(aux1[,c('producto')],"(Manz.*)")),
                               aux1[,c('variedadINE')],
                                     'Manzana')
    #NARANJA
    aux1$variedadINE <- ifelse(is.na(str_extract(aux1[,c('producto')],"(Nara.*)")),
                               aux1[,c('variedadINE')],
                               'Naranja')
    #PERA
    aux1$variedadINE <- ifelse(is.na(str_extract(aux1[,c('producto')],"(Pera.*)")),
                               aux1[,c('variedadINE')],
                               'Pera')
    #PLATANO
    aux1$variedadINE <- ifelse(is.na(str_extract(aux1[,c('producto')],"(Platan.*)")),
                               aux1[,c('variedadINE')],
                               'Platano')
    #}
    # 2. Se comienza el cálculo
      #a. me aseguro que este con formato numérico
      aux1$precio <- as.numeric(as.character(aux1$precio))
      aux1$pln <- log(aux1$precio,exp(1))
  }
}else{
  print('Nada que procesar!!')
}


try(aux[['fuente']]<-gsub('[$].*','www.odepa.cl',aux$fuente))
try(aux$index <- 1)
try(B<-aggregate(index~fuente,aux,sum))
try(A<-merge(A,B,by='fuente', all=TRUE))
hoy<-as.character(newfile[i,c('nom')])
try(setnames(A,c('index'),c(hoy)))
try(assign(newfile[i,c('nom')],aux))
try(pfile <- newfile$nom[1:i])

# 1. Tomar sólo las tiendas y/o productos homologadas 
#source('exreg.R')