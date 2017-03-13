# Víctor Martínez
# Este documento tiene los codigos de expresiones regulares:

## Extraigo los número y las palabras claves
aux$paux <- str_extract(aux[,c('producto')],"[0-9].*|[K][i][l][o].*") 
## las borros de la sección producto
aux$producto <- gsub("[0-9].*|[K][i][l][o].*", "", aux$producto)
#quito parentésis
aux$producto <- gsub("[(]|[)]","",aux$producto)
