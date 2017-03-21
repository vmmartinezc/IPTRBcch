# Author:Víctor Martínez
# Collaborators: 
# Fecha: march 3 2017
# Propósito: Lo que busca este script es identificar las descargas diarias, 
#revisarlas y llamar a python a repetir procesos si es necesario
#=======================================================================================
# 1. Arranco ordenando archivos
setwd(pathDrpx)
temp1 <- file.info(list.files(pattern="*d.csv"))
#oldfile <- rownames(oldfile)
#saveRDS(oldfile1,file='Rbases/archivos_procesados.rds')

# 2. Responder preguntas referidas a inspección exterior de los archivos en la carpeta:
## a. ¿Hay archivos nuevos?
#################################################################
# cargo archivos procesados
oldfile <- readRDS('Rbases/archivos_procesados.rds')
newfile <- subset(temp1,!(rownames(temp1) %in% oldfile[,1]))

if (nrow((newfile))!=0){
print('Se encontraron los siguientes archivos no procesados:')
  print(rownames(newfile))
  
  ## b. ¿El tamaño de los archivos nuevos ha cambiado mucho?
  #################################################################
  # Agrego la media por hora
  ## creo la hora desde el nombre
  newfile$nom <- row.names(newfile)
  newfile$fecha <- str_extract(newfile[,c('nom')],'[0-9]+')
  
  newfile$hora <- str_extract(newfile[,c('nom')],"_[0-9]+")  
  newfile$hora <- substring(newfile[,c('hora')],2)
  
  temp1$nom <- row.names(temp1)
  temp1$fecha <- str_extract(temp1[,c('nom')],'[0-9]+')
  temp1$hora <- str_extract(temp1[,c('nom')],"_[0-9]+")  
  temp1$hora <- substring(temp1[,c('hora')],2)
  
  #Use la mediana porque hay muy pocos datos
  mediassize=do.call(data.frame,aggregate(size~hora,temp1,function(x) c(mean = median(x), sd = sd(x))))
  
  # Construye las cotas y el rango para estar al 99% de probabilidad
  newfile <-merge(newfile,mediassize,by='hora')
  newfile$li <- newfile$size.mean-3*newfile$size.sd
  newfile$ls <- newfile$size.mean+3*newfile$size.sd
  # Determinar si pertenece al intervalo
  #newfile$outlier <- cbind( newfile$size < newfile$li & newfile$size > newfile$ls ) 
  newfile$outlier <- cbind( newfile$size < newfile$li) 
  
  # Crea el Archivo problema si hay un cambio extraño en el tamaño de un archivo.
  ifelse(newfile$outlier=='TRUE',problema<-newfile$nom,problema<-0)
  
  if(length(problema)){
    print('No hay cambios de tamaño en los archivos')
    #Agregar Acciones
  }else{
    print('Estos archivos tienen un cambio fuerte en el tamaño')
    print(problema)
    #Agregar Acciones: Llamar SSH al sistema
  }

## c. ¿Se descargaron todas las páginas?
#################################################################
## Ordeno los archivos nuevo por orden
newfile$fecha <- as.Date(newfile$fecha, "%Y%m%d")
newfile <- newfile[with(newfile, order(as.POSIXct(fecha))), ]

if (nrow(newfile)==0) { # Si no hay nuevos archivos que lo diga
  print('No hay archivos nuevos')
} else { # Si hay nuevos archivos que los procese y los integre a la bamse madre (bm)
  #CARGO ARCHIVOS NUEVOS:  length(newfile)
  A<-read.csv(file='segumiento.csv')
  setnames(A,'fuente2','fuente')
  #nrow(newfile)
  for (i in 1:nrow(newfile)){ 
    # Abro Archivos nuevos:
    try(assign(newfile[i,c('nom')],read.csv(file=newfile[i,c('nom')], header=TRUE, sep=",")))
    # Creo una base auxiliar para trabajar
    try(aux<-get(newfile[i,c('nom')]))
    try(aux[['fuente']]<-gsub('[$].*','www.odepa.cl',aux$fuente))
    try(aux$index <- 1)
    try(B<-aggregate(index~fuente,aux,sum))
    try(A<-merge(A,B,by='fuente', all=TRUE))
    hoy<-as.character(newfile[i,c('nom')])
    try(setnames(A,c('index'),c(hoy)))
    try(assign(newfile[i,c('nom')],aux))
    try(pfile <- newfile$nom[1:i])
  }
  # Ordeno la base de datos y la traspongo
  rownames(A)<-A[,1]
  A$fuente <- NULL
  C<-transpose(A)
  rownames(C) <- colnames(A)
  colnames(C) <- rownames(A)
  # Identifico la hora en que cada una fue descargada
  C$hora  <- str_extract(rownames(C),"_[0-9]+")  
  C$hora <- substring(C[,c('hora')],2)
  try(setnames(C,c(""),c('nada')))
  try(C$nada <- NULL)
  
  #sumpo archivos procesados (pfile) a la base de archivos viejos (oldfile)
  oldfile <- as.data.frame(oldfile)
  colnames(oldfile)<-'oldfile'
  pfile <- as.data.frame(pfile)
  colnames(pfile)<-'oldfile'
  oldfile <- rbind(oldfile,pfile)
  #PArche, como son 22 p�ginas las imputo:
  A<-A[1:22,]
  #Exporto archivo procesaro hoy
  C1 <- readRDS('Rbases/seguimiento.rds')
  #C <- rbind.fill(C1,C)
  C <- rbind(C1,C[,names(C1)])
  #C <- rbind.fill(C1,C)
  
  C$fecha <- as.Date(str_extract(rownames(C),'[0-9]+'),'%Y%m%d')
  C <- C[with(C, order(as.POSIXct(fecha),hora)), ]
  C$fecha <- NULL
  
  saveRDS(C,file='Rbases/seguimiento.rds')
  write.csv(C,'errores/seguimiento.csv')
  ## Guardo archivos procesados
  saveRDS(oldfile,file='Rbases/archivos_procesados.rds')
  print('fin del proceso!')
}
} else{
  print('No hay archivos que procesar!!')
}
