# Scrapper buscador de precios

Esta aplicacion de Python sirve para buscar precios por codigo de barra en distintos mercados online. 
Es importante destacar que unicamente funciona por codigo de barra exacto por lo que si el codigo de barra esta mal, no encontrara el producto.
Los precios son exactos al momento de la ejecucion y muestra precios de lista y precios con oferta.
A gran escala la aplicacion abre pagina por pagina, busca el producto por codigo y cierra la pagina. Esto hace que demore mas tiempo del deseado pero tambien habilita a poder buscar muchos codigos sin que las paginas detecten que se trata de una automatización.

## Modo de uso

Para usar la aplicacion lo primero que hay que hacer es un excel con todos los codigos de barra y nombre de los productos que necesites buscar precios. Los EAN tienen que estar en la primera columna y los nombres en la segunda columna. 

##
## Para instalar (devs)

```bash
pip install pandas
pip install requests
pip install beautifulsoup4
pip install selenium
```