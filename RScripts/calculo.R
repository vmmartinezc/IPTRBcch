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

    # Cambio a formato Chr para trabajar con esa columna
    try(aux[['producto']]<-as.character(aux$producto))
    aux[['producto']] <- iconv(aux[['producto']],"WINDOWS-1252","UTF-8") # Codifico el icóno para no tener problemas
    try(aux[['producto']]<-tolower(aux$producto))
    
    # Creo una base auxiliar para trabajar: identifico la viabilidad de los datos,
    # Test1-2: Si Precio y Cantidadcontienen sólo números entonces son viables
    # Test 3-4 : Si Unidad y producto sólo tiene letras entronces es víable
    # Test (más adelante) en que no tomo la basi se cantidad está vacía
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
#Cambia el path al Git
    
    #FRUTAS FRESCAS
    ##===========================================
    # MANZANA
    aux1$variedadINE <- ifelse(is.na(str_extract(aux1[,c('producto')],"(manz.*)")),
                               aux1[,c('variedadINE')],
                               'manzana')
    #NARANJA
    aux1$variedadINE <- ifelse(is.na(str_extract(aux1[,c('producto')],"(nara.*)")),
                               aux1[,c('variedadINE')],
                               'naranja')
    #PERA
    aux1$variedadINE <- ifelse(is.na(str_extract(aux1[,c('producto')],"(pera.*)")),
                               aux1[,c('variedadINE')],
                               'pera')
    #PLATANO
    aux1$variedadINE <- ifelse(is.na(str_extract(aux1[,c('producto')],"(platan.*)")),
                               aux1[,c('variedadINE')],
                               'platano')
    
    #FRUTAS DE ESTACIÓN (17)
    ##===========================================
    #CHIRIMOYA
    aux1$variedadINE <- ifelse(is.na(str_extract(aux1[,c('producto')],"(chiri.*)")),
                               aux1[,c('variedadINE')],
                               'festacion')
    #CIRUELAS (TODOS LOS TIPOS)
    aux1$variedadINE <- ifelse(is.na(str_extract(aux1[,c('producto')],"(ciruel.*)")),
                               aux1[,c('variedadINE')],
                               'festacion')
    #DAMASCO 
    aux1$variedadINE <- ifelse(is.na(str_extract(aux1[,c('producto')],"(damasc.*)")),
                               aux1[,c('variedadINE')],
                               'festacion')
    #FRUTILLA
    aux1$variedadINE <- ifelse(is.na(str_extract(aux1[,c('producto')],"(frutill.*)")),
                               aux1[,c('variedadINE')],
                               'festacion')
    #GUINDA
    aux1$variedadINE <- ifelse(is.na(str_extract(aux1[,c('producto')],"(guind.*)")),
                               aux1[,c('variedadINE')],
                               'festacion')
    #CEREZA
    aux1$variedadINE <- ifelse(is.na(str_extract(aux1[,c('producto')],"(cerez.*)")),
                               aux1[,c('variedadINE')],
                               'festacion')
    #KIWI
    aux1$variedadINE <- ifelse(is.na(str_extract(aux1[,c('producto')],"(kiwi.*)")),
                               aux1[,c('variedadINE')],
                               'festacion')
    #MANGO
    aux1$variedadINE <- ifelse(is.na(str_extract(aux1[,c('producto')],"(mango.*)")),
                               aux1[,c('variedadINE')],
                               'festacion')
    #MELÓN
    aux1$variedadINE <- ifelse(is.na(str_extract(aux1[,c('producto')],"(mel.*)")),
                               aux1[,c('variedadINE')],
                               'festacion')
    #NECTARIN
    aux1$variedadINE <- ifelse(is.na(str_extract(aux1[,c('producto')],"(duraz.*)")),
                               aux1[,c('variedadINE')],
                               'festacion')
    #pepino dulce
    aux1$variedadINE <- ifelse(is.na(str_extract(aux1[,c('producto')],"(pepi.*dulc.*)")),
                               aux1[,c('variedadINE')],
                               'festacion')
    #PIÑA
    aux1$variedadINE <- ifelse(is.na(str_extract(aux1[,c('producto')],"(pi.*a)")),
                               aux1[,c('variedadINE')],
                               'festacion')
    #POMELO
    aux1$variedadINE <- ifelse(is.na(str_extract(aux1[,c('producto')],"(pomelo.*)")),
                               aux1[,c('variedadINE')],
                               'festacion')
    #TUNA
    aux1$variedadINE <- ifelse(is.na(str_extract(aux1[,c('producto')],"(tuna.*)")),
                               aux1[,c('variedadINE')],
                               'festacion')    
    #SANDÍA 
    aux1$variedadINE <- ifelse(is.na(str_extract(aux1[,c('producto')],"(sand.*)")),
                               aux1[,c('variedadINE')],
                               'festacion')
    #UVA 
    aux1$variedadINE <- ifelse(is.na(str_extract(aux1[,c('producto')],"(uva.*)")),
                               aux1[,c('variedadINE')],
                               'festacion')
    
    #FRUTOS SECOS
    ##===========================================
    #FRUTOS SECOS 
    aux1$variedadINE <- ifelse(is.na(str_extract(aux1[,c('producto')],"(.*seco.*)")),
                               aux1[,c('variedadINE')],
                               'fsecos')
    
    
    ## HORTALIZAS FRESCAS
    ##=======================================
    
    #Acelga
    aux1$variedadINE <- ifelse(is.na(str_extract(aux1[,c('producto')],"(acel.*)")),
                               aux1[,c('variedadINE')],
                               'acelga&espinaca')
    
    #Espinaca
    aux1$variedadINE <- ifelse(is.na(str_extract(aux1[,c('producto')],"(espina.*)")),
                               aux1[,c('variedadINE')],
                               'acelga&espinaca')
    #Cebolla o Cebollín
    aux1$variedadINE <- ifelse(is.na(str_extract(aux1[,c('producto')],"(cebo.*)")),
                               aux1[,c('variedadINE')],
                               'cebolla&cebollin')
    #Lechuga
    aux1$variedadINE <- ifelse(is.na(str_extract(aux1[,c('producto')],"(lech.*)")),
                               aux1[,c('variedadINE')],
                               'lechuga')    
    #Limón
    aux1$variedadINE <- ifelse(is.na(str_extract(aux1[,c('producto')],"(lim.*)")),
                               aux1[,c('variedadINE')],
                               'limón')    
    #Palta
    aux1$variedadINE <- ifelse(is.na(str_extract(aux1[,c('producto')],"(palta.*)")),
                               aux1[,c('variedadINE')],
                               'palta')    
    #Pimentón
    aux1$variedadINE <- ifelse(is.na(str_extract(aux1[,c('producto')],"(pimen.*)")),
                               aux1[,c('variedadINE')],
                               'pimenton&Pimiento')  
    #Pimiento
    aux1$variedadINE <- ifelse(is.na(str_extract(aux1[,c('producto')],"(pimie.*)")),
                               aux1[,c('variedadINE')],
                               'pimenton&pimiento')  
    #Tomate
    aux1$variedadINE <- ifelse(is.na(str_extract(aux1[,c('producto')],"(tomate.*)")),
                               aux1[,c('variedadINE')],
                               'tomate')
    #Zanahoria
    aux1$variedadINE <- ifelse(is.na(str_extract(aux1[,c('producto')],"(zanaho.*)")),
                               aux1[,c('variedadINE')],
                               'zanahoria')
    #Zapallo
    aux1$variedadINE <- ifelse(is.na(str_extract(aux1[,c('producto')],"(zapall.*)")),
                               aux1[,c('variedadINE')],
                               'zapallo')
    #Zapallo italiano
    aux1$variedadINE <- ifelse(is.na(str_extract(aux1[,c('producto')],"(zap.*ital.*)")),
                               aux1[,c('variedadINE')],
                               'zapallo italiano')
    ## VERDURAS DE ESTACIÓN
    ##=======================================
    #ALCACHOFA
    aux1$variedadINE <- ifelse(is.na(str_extract(aux1[,c('producto')],"(alcach.*)")),
                               aux1[,c('variedadINE')],
                               'vestacion')  
    #ALCACHOFA
    aux1$variedadINE <- ifelse(is.na(str_extract(aux1[,c('producto')],"(betarr.*)")),
                               aux1[,c('variedadINE')],
                               'vestacion') 
  
    #BRÓCOLI
    aux1$variedadINE <- ifelse(is.na(str_extract(aux1[,c('producto')],"(br.*coli.*)")),
                               aux1[,c('variedadINE')],
                               'vestacion') 
    #COLIFLOR
    aux1$variedadINE <- ifelse(is.na(str_extract(aux1[,c('producto')],"(coli.*)")),
                               aux1[,c('variedadINE')],
                               'vestacion') 
    #CHOCLO
    aux1$variedadINE <- ifelse(is.na(str_extract(aux1[,c('producto')],"(choclo.*)")),
                               aux1[,c('variedadINE')],
                               'choclo') 
    #ESPARRAGO
    aux1$variedadINE <- ifelse(is.na(str_extract(aux1[,c('producto')],"(esp.*rr.*)")),
                               aux1[,c('variedadINE')],
                               'vestacion') 
    #PEPINO
    aux1$variedadINE <- ifelse(is.na(str_extract(aux1[,c('producto')],"(pepino.*)")),
                               aux1[,c('variedadINE')],
                               'vestacion') 
    #HABA
    aux1$variedadINE <- ifelse(is.na(str_extract(aux1[,c('producto')],"(haba.*)")),
                               aux1[,c('variedadINE')],
                               'vestacion') 

    ## VERDURAS CONGELADAS
    ##=======================================
    #CONGELADOS
    aux1$variedadINE <- ifelse(is.na(str_extract(aux1[,c('producto')],"(.*congel.*)")),
                               aux1[,c('variedadINE')],
                               'vcongelada') 
    
    ## LEGUNMBRES
    ##=======================================
    #Garbanzo
    aux1$variedadINE <- ifelse(is.na(str_extract(aux1[,c('producto')],"(garb.*)")),
                               aux1[,c('variedadINE')],
                               'legumbre')
    
    #Lenteja
    aux1$variedadINE <- ifelse(is.na(str_extract(aux1[,c('producto')],"(lente.*)")),
                               aux1[,c('variedadINE')],
                               'legumbre')
    #Poroto
    aux1$variedadINE <- ifelse(is.na(str_extract(aux1[,c('producto')],"(poroto)")),
                               aux1[,c('variedadINE')],
                                           'legumbre')
    
    ## CASOS ESPECIALES DE VERDURAS DENTRO DE LEGUMBRES
    #POROTO VERDE
    aux1$variedadINE <- ifelse(is.na(str_extract(aux1[,c('producto')],"(porot.*verde.*)")),
                               aux1[,c('variedadINE')],
                               'vestacion') 
    #POROTO GRANADO
    aux1$variedadINE <- ifelse(is.na(str_extract(aux1[,c('producto')],"(porot.*granad.*)")),
                               aux1[,c('variedadINE')],
                               'vestacion') 
    
    
     #Cochayuyo
    aux1$variedadINE <- ifelse(is.na(str_extract(aux1[,c('producto')],"(cocha.*)")),
                               aux1[,c('variedadINE')],
                               'legumbre')
    ## TUBERCULOS
    ##=======================================
    #Papas fritas
    aux1$variedadINE <- ifelse(is.na(str_extract(aux1[,c('producto')],"(papa.*)")),
                               aux1[,c('variedadINE')],
                               'papas') 
    aux1$variedadINE <- ifelse(is.na(str_extract(aux1[,c('producto')],"(.*papa.*Congel.*)")),
                               aux1[,c('variedadINE')],
                               'papascongeladas')  
    
    aux1$variedadINE <- ifelse(is.na(str_extract(aux1[,c('producto')],"(.*papa.*Frita.*)")),
                               aux1[,c('variedadINE')],
                               'papasfritas')   

  ## Obstengo una muestra que contiene sólo las variedades INE y otra que contiene las variedades NO INE para analizar.
    bdine <- subset.data.frame(aux1,aux1$variedadINE!=0)   
    bdnoine <- subset.data.frame(aux1,aux1$variedadINE==0) 

    
    #}
    # 2. Se comienza el cálculo
      #a. me aseguro que este con formato numérico
      aux1$precio <- as.numeric(as.character(aux1$precio))
      aux1$pln <- log(aux1$precio,exp(1))
  }
}else{
  print('Nada que procesar!!')
}


# 1. Tomar sólo las tiendas y/o productos homologadas 
#source('exreg.R')