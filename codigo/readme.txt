IMPORTANTE.
El archivo analisis_lluvias_piura-archivo_local.py contiene mejoras de código del archivo analisis_lluvias_piura.py para que pueda ser ejecutado sin la necesidad de un notebook como jupyter o Colab, las modificaciones son las siguientes:
 - Se comenta la sentencia plt.show() (línea 83) para ejecutarla al final de código (línea 101) y se agrega la función de guardar la imagen del gráfico de líneas con tablas. (línea 84)
 - Se comenta la sentencia iplot(figInteract) (línea 99) para reemplazarla por la exportación del gráfico interactivo a un archivo html. (línea 100)
