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

# Cargo las bases de entrada a actualizar en el proceso:
setwd(pathDrpx)
temp1 <- file.info(list.files(pattern="*d.csv"))
oldfile<-readRDS('Rbases/done.rds')
done<-readRDS('Rbases/done.rds')
bm<-readRDS('Rbases/bm1.rds')

# tomo las bases que aún no se procesan

newfile <- subset(temp1,!(rownames(temp1) %in% oldfile[,1]))
newfile$nom <- rownames(newfile)
newfile$fecha <- str_extract(newfile[,c('nom')],'[0-9]+')
newfile$hora <- str_extract(newfile[,c('nom')],"_[0-9]+")  
newfile$hora <- substring(newfile[,c('hora')],2)

if (nrow(newfile)!=0){
  print('Se encontraron los siguientes archivos no procesados:')
  print(rownames(newfile))

#nrow(newfile)
for (i in 1:nrow(newfile)){ 
  # Cargo archivos en R
  try(assign(newfile[i,c('nom')],read.csv(file=newfile[i,c('nom')], header=TRUE, sep=",")))
  try(aux<-get(newfile[i,c('nom')]))
  # Sólo me quedo con los que determinan correctamente la tienda
  try(aux$tienda <- str_extract(aux[,c('fuente')],'[www].*.cl'))
  
  #Agrego la Fecha
  try(aux[['fecha']] <- str_extract(newfile[i,c('fecha')],"[0-9]+"))
  try(aux[['fecha']]<-as.Date(aux$fecha,format='%Y%m%d'))
  
  # Cambio a formato Chr para trabajar con esa columna
  try(aux[['producto']]<-as.character(aux$producto))
  #aux[['producto']] <- iconv(aux[['producto']],"WINDOWS-1252","UTF-8") # Codifico el icóno para no tener problemas
  aux[['producto']] <- iconv(aux$producto,"UTF-8", "UTF-8",sub='')
  try(aux[['producto']]<-tolower(aux$producto))
  
  
  #Marco las variables con un ID para poder determinar qué procesé y qué no.
  ## Se asignan los productos del INE  
  try(aux[['id']]<-ifelse(aux$tipo=='WEB',
                          paste(aux$fecha,aux$producto,aux$precio,
                                aux$cantidad,aux$unidad,aux$tipo,aux$tienda, sep="_"),
                          paste(aux$fecha,aux$producto,aux$variedad,aux$mercado,aux$volumen,
                                aux$calidad,aux$precioMin,aux$precioMax,aux$precioProm,
                                aux$precio,aux$cantidad,aux$unidad,aux$tipo,aux$tienda, sep="_")))
  
  try(bm[['id']]<-ifelse(bm$tipo=='WEB',paste(bm$fecha,bm$producto,bm$precio,
                                              bm$cantidad,bm$unidad,bm$tipo,bm$tienda, sep="_"),
                         paste(bm$fecha,bm$producto,bm$variedad,bm$mercado,bm$volumen,
                               bm$calidad,bm$precioMin,bm$precioMax,bm$precioProm,
                               bm$precio,bm$cantidad,bm$unidad,bm$tipo,bm$tienda, sep="_")))
  
  

  # 1. Se asignan variedades
  aux$productosINE <- 0
  #Aca debería haber un for
  
  # Guardo en la base madre lo que se procesó
  try(aux1<-subset(aux,!(aux$id %in% bm$id))) # Extraigo los datos nuevos
  
  ## Pongo fecha y hora al archivo para identificar
  # Proceso aux1 SSI hay datos que procesar
  if (nrow(aux1)==0){
    print('Nada nuevo que agregar')
  }else{
  
  #FRUTAS FRESCAS
  ##===========================================
  # MANZANA
  aux1$productosINE <- ifelse(is.na(str_extract(aux1[,c('producto')],"(^manz.*)")),
                             aux1[,c('productosINE')],
                             'manzana')
  #NARANJA
  aux1$productosINE <- ifelse(is.na(str_extract(aux1[,c('producto')],"(^nara.*)")),
                             aux1[,c('productosINE')],
                             'naranja')
  #PERA
  aux1$productosINE <- ifelse(is.na(str_extract(aux1[,c('producto')],"(^pera.*)")),
                             aux1[,c('productosINE')],
                             'pera')
  #PLATANO
  aux1$productosINE <- ifelse(is.na(str_extract(aux1[,c('producto')],"(^platan.*)")),
                             aux1[,c('productosINE')],
                             'platano')
  
  #FRUTAS DE ESTACIÓN (17)
  ##===========================================
  #CHIRIMOYA
  aux1$productosINE <- ifelse(is.na(str_extract(aux1[,c('producto')],"(^chiri.*)")),
                             aux1[,c('productosINE')],
                             'festacion')
  #CIRUELAS (TODOS LOS TIPOS)
  aux1$productosINE <- ifelse(is.na(str_extract(aux1[,c('producto')],"(^ciruel.*)")),
                             aux1[,c('productosINE')],
                             'festacion')
  #DAMASCO 
  aux1$productosINE <- ifelse(is.na(str_extract(aux1[,c('producto')],"(^damasc.*)")),
                             aux1[,c('productosINE')],
                             'festacion')
  #FRUTILLA
  aux1$productosINE <- ifelse(is.na(str_extract(aux1[,c('producto')],"(^frutill.*)")),
                             aux1[,c('productosINE')],
                             'festacion')
  #GUINDA
  aux1$productosINE <- ifelse(is.na(str_extract(aux1[,c('producto')],"(^guind.*)")),
                             aux1[,c('productosINE')],
                             'festacion')
  #CEREZA
  aux1$productosINE <- ifelse(is.na(str_extract(aux1[,c('producto')],"(^cerez.*)")),
                             aux1[,c('productosINE')],
                             'festacion')
  #KIWI
  aux1$productosINE <- ifelse(is.na(str_extract(aux1[,c('producto')],"(^kiwi.*)")),
                             aux1[,c('productosINE')],
                             'festacion')
  #MANGO
  aux1$productosINE <- ifelse(is.na(str_extract(aux1[,c('producto')],"(^mango.*)")),
                             aux1[,c('productosINE')],
                             'festacion')
  #MELÓN
  aux1$productosINE <- ifelse(is.na(str_extract(aux1[,c('producto')],"(^mel.*)")),
                             aux1[,c('productosINE')],
                             'festacion')
  #NECTARIN
  aux1$productosINE <- ifelse(is.na(str_extract(aux1[,c('producto')],"(^duraz.*)")),
                             aux1[,c('productosINE')],
                             'festacion')
  #pepino dulce
  aux1$productosINE <- ifelse(is.na(str_extract(aux1[,c('producto')],"(^pepi.*dulc.*)")),
                             aux1[,c('productosINE')],
                             'festacion')
  #PIÑA
  aux1$productosINE <- ifelse(is.na(str_extract(aux1[,c('producto')],"(^pi.*a)")),
                             aux1[,c('productosINE')],
                             'festacion')
  #POMELO
  aux1$productosINE <- ifelse(is.na(str_extract(aux1[,c('producto')],"(^pomelo.*)")),
                             aux1[,c('productosINE')],
                             'festacion')
  #TUNA
  aux1$productosINE <- ifelse(is.na(str_extract(aux1[,c('producto')],"(^tuna.*)")),
                             aux1[,c('productosINE')],
                             'festacion')    
  #SANDÍA 
  aux1$productosINE <- ifelse(is.na(str_extract(aux1[,c('producto')],"(^sand.*)")),
                             aux1[,c('productosINE')],
                             'festacion')
  #UVA 
  aux1$productosINE <- ifelse(is.na(str_extract(aux1[,c('producto')],"(^uva.*)")),
                             aux1[,c('productosINE')],
                             'festacion')
  
  #FRUTOS SECOS
  ##===========================================
  #FRUTOS SECOS 
  aux1$productosINE <- ifelse(is.na(str_extract(aux1[,c('producto')],"(.*seco.*)")),
                             aux1[,c('productosINE')],
                             'fsecos')
  
  
  ## HORTALIZAS FRESCAS
  ##=======================================
  
  #Acelga
  aux1$productosINE <- ifelse(is.na(str_extract(aux1[,c('producto')],"(^acel.*)")),
                             aux1[,c('productosINE')],
                             'acelga&espinaca')
  
  #Espinaca
  aux1$productosINE <- ifelse(is.na(str_extract(aux1[,c('producto')],"(^espina.*)")),
                             aux1[,c('productosINE')],
                             'acelga&espinaca')
  #Cebolla o Cebollín
  aux1$productosINE <- ifelse(is.na(str_extract(aux1[,c('producto')],"(^cebo.*)")),
                             aux1[,c('productosINE')],
                             'cebolla&cebollin')
  #Lechuga
  aux1$productosINE <- ifelse(is.na(str_extract(aux1[,c('producto')],"(^lech.*)")),
                             aux1[,c('productosINE')],
                             'lechuga')    
  #Limón
  aux1$productosINE <- ifelse(is.na(str_extract(aux1[,c('producto')],"(^lim.*)")),
                             aux1[,c('productosINE')],
                             'limon')    
  #Palta
  aux1$productosINE <- ifelse(is.na(str_extract(aux1[,c('producto')],"(^palta.*)")),
                             aux1[,c('productosINE')],
                             'palta')    
  #Pimentón
  aux1$productosINE <- ifelse(is.na(str_extract(aux1[,c('producto')],"(^pimen.*)")),
                             aux1[,c('productosINE')],
                             'pimenton&Pimiento')  
  #Pimiento
  aux1$productosINE <- ifelse(is.na(str_extract(aux1[,c('producto')],"(^pimie.*)")),
                             aux1[,c('productosINE')],
                             'pimenton&pimiento')  
  #Tomate
  aux1$productosINE <- ifelse(is.na(str_extract(aux1[,c('producto')],"(^tomate.*)")),
                             aux1[,c('productosINE')],
                             'tomate')
  #Zanahoria
  aux1$productosINE <- ifelse(is.na(str_extract(aux1[,c('producto')],"(^zanaho.*)")),
                             aux1[,c('productosINE')],
                             'zanahoria')
  #Zapallo
  aux1$productosINE <- ifelse(is.na(str_extract(aux1[,c('producto')],"(^zapall.*)")),
                             aux1[,c('productosINE')],
                             'zapallo')
  #Zapallo italiano
  aux1$productosINE <- ifelse(is.na(str_extract(aux1[,c('producto')],"(^zap.*ital.*)")),
                             aux1[,c('productosINE')],
                             'zapallo italiano')
  ## VERDURAS DE ESTACIÓN
  ##=======================================
  #ALCACHOFA
  aux1$productosINE <- ifelse(is.na(str_extract(aux1[,c('producto')],"(^alcach.*)")),
                             aux1[,c('productosINE')],
                             'vestacion')  
  #ALCACHOFA
  aux1$productosINE <- ifelse(is.na(str_extract(aux1[,c('producto')],"(^betarr.*)")),
                             aux1[,c('productosINE')],
                             'vestacion') 
  
  #BRÓCOLI
  aux1$productosINE <- ifelse(is.na(str_extract(aux1[,c('producto')],"(^br.*coli.*)")),
                             aux1[,c('productosINE')],
                             'vestacion') 
  #COLIFLOR
  aux1$productosINE <- ifelse(is.na(str_extract(aux1[,c('producto')],"(^coli.*)")),
                             aux1[,c('productosINE')],
                             'vestacion') 
  #CHOCLO
  aux1$productosINE <- ifelse(is.na(str_extract(aux1[,c('producto')],"(^choclo.*)")),
                             aux1[,c('productosINE')],
                             'choclo') 
  #ESPARRAGO
  aux1$productosINE <- ifelse(is.na(str_extract(aux1[,c('producto')],"(^esp.*rr.*)")),
                             aux1[,c('productosINE')],
                             'vestacion') 
  #PEPINO
  aux1$productosINE <- ifelse(is.na(str_extract(aux1[,c('producto')],"(^pepino.*)")),
                             aux1[,c('productosINE')],
                             'vestacion') 
  #HABA
  aux1$productosINE <- ifelse(is.na(str_extract(aux1[,c('producto')],"(^haba.*)")),
                             aux1[,c('productosINE')],
                             'vestacion') 
  
  ## VERDURAS CONGELADAS
  ##=======================================
  #CONGELADOS
  aux1$productosINE <- ifelse(is.na(str_extract(aux1[,c('producto')],"(.*congel.*)")),
                             aux1[,c('productosINE')],
                             'vcongelada') 
  
  ## LEGUNMBRES
  ##=======================================
  #Garbanzo
  aux1$productosINE <- ifelse(is.na(str_extract(aux1[,c('producto')],"(^garb.*)")),
                             aux1[,c('productosINE')],
                             'legumbre')
  
  #Lenteja
  aux1$productosINE <- ifelse(is.na(str_extract(aux1[,c('producto')],"(^lente.*)")),
                             aux1[,c('productosINE')],
                             'legumbre')
  #Poroto
  aux1$productosINE <- ifelse(is.na(str_extract(aux1[,c('producto')],"(^poroto)")),
                             aux1[,c('productosINE')],
                             'legumbre')
  
  ## CASOS ESPECIALES DE VERDURAS DENTRO DE LEGUMBRES
  #POROTO VERDE
  aux1$productosINE <- ifelse(is.na(str_extract(aux1[,c('producto')],"(^porot.*verde.*)")),
                             aux1[,c('productosINE')],
                             'vestacion') 
  #POROTO GRANADO
  aux1$productosINE <- ifelse(is.na(str_extract(aux1[,c('producto')],"(^porot.*granad.*)")),
                             aux1[,c('productosINE')],
                             'vestacion') 
  
  
  #Cochayuyo
  aux1$productosINE <- ifelse(is.na(str_extract(aux1[,c('producto')],"(^cocha.*)")),
                             aux1[,c('productosINE')],
                             'legumbre')
  ## TUBERCULOS
  ##=======================================
  #Papas fritas
  aux1$productosINE <- ifelse(is.na(str_extract(aux1[,c('producto')],"(^papa.*)")),
                             aux1[,c('productosINE')],
                             'papas') 
  aux1$productosINE <- ifelse(is.na(str_extract(aux1[,c('producto')],"(.*papa.*Congel.*)")),
                             aux1[,c('productosINE')],
                             'papascongeladas')  
  
  aux1$productosINE <- ifelse(is.na(str_extract(aux1[,c('producto')],"(.*papa.*Frita.*)")),
                             aux1[,c('productosINE')],
                             'papasfritas')  
  

  try(aux1[['hora']] <- str_extract(newfile[i,c('nom')],"(_.*_)"))
  try(aux1[['hora']] <- str_extract(newfile[i,c('hora')],"[0-9]+"))
  try(bm<-rbind(bm,aux1))                     # Pego a la base madre los nuevos datos procesados
  }
  
  
  try(done[i,c('file')]<-newfile[i,c('nom')])    # Registro el archivo que procesé
  try(done[i,c('Obs_inthe_file')]<-nrow(aux))    # Observaciones descargadas desde scrapy
  try(done[i,c('newObs')]<-nrow(aux1))           # Observaciones nuevas procesadas en el archivo
  try(done[i,c('ratio')]<-round(100*(nrow(aux1)/nrow(aux)),digits = 2)) # Ratio de lo nuevo
}

try(done<-rbind(done,oldfile))
  
}else{
  print('Nada que procesar!!')
}

print('Fin del Proceso!!')

## Incluyo lo procesado en la base madre (BM) y en la base done:
saveRDS(done,file='Rbases/done.rds')
#Guardo la Base Madre
saveRDS(bm,file='Rbases/bm1.rds')

