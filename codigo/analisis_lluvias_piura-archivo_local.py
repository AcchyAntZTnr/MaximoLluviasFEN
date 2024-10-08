# -*- coding: utf-8 -*-
"""ANALISIS LLUVIAS PIURA.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1Ha3Fe6Su4YLWbX3dlZ7Fg6ixrORseZCz
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objs as go
from plotly.offline import iplot
#from google.colab import drive
#drive.mount('/content/drive')

"""Importante: De usar el entorno google colab, se debe crear una carpeta llamada "PERU EXP CON DATOS" y guardar el archivo separado por comas (csv) dentro de esa carpeta y tomar la ruta de ese archivo para usarlo en el metodo pd.read_csv"""

#Importante: De usar el entorno google colab y google drive, se debe crear una carpeta llamada
#  "PERU EXP CON DATOS" y guardar el archivo separado por comas (csv) dentro de esa carpeta
#   y tomar la ruta de ese archivo para usarlo en el metodo pd.read_csv
#De ejecutar el código de manera local, copiar la ruta del archivo y pegarla
#  dentro de las comilas en el metodo pd.read_csv

globalTable = pd.read_csv("DATOS HIDROM ESTACION MIRAFLORES PIURA.csv",encoding="latin-1")
nombreEstacionMeteorologica = "MIRAFLORES - PIURA - PIURA" #COLOCAR EL NOMBRE DE LA ESTACIÓN DE DONDE SE TOMARON LOS DATOS
rainPiuraTable = globalTable.iloc[:,[0,1,2,3]]

#SE OBTIENE EL PERIODO DE TIEMPO, ASEGURAR QUE DICHA COLUMNA NO CONTENGA VALORES NAN ANTES DE LEER EL ARCHIVO CSV
periodoReg = [globalTable["Año"].min(), globalTable["Año"].max()]
#CÓDIGO PARA CAMBIAR LOS VALORES DE -99.9 A NAN
rainPiuraTable = rainPiuraTable.replace({-99.9 : float("NaN")})
#SE USA INTERPOLACIÓN LINEAL PARA RELLENAR ALGUNOS DATOS FALTANTES
rainPiuraTableCopy = rainPiuraTable
rainPiuraTableCopy = rainPiuraTableCopy.interpolate(method = "linear", limit = 3, limit_direction ="forward", axis = 0)
globalTable ##SI SE VA A USAR UN ENTORNO DIFERENTE A GOOGLE COLAB, USAR PRINT PARA IMPRIMIR EL DATAFRAME

#SE CREAN LAS LISTAS PARA ENSAMBLAR LA TABLA DEL EJE X DEL PRIMER GRAFICO
#GRAFICO INTERACTIVO, Y SE CREA EL DATAFRAME "dfLluviasPorMes" DONDE SE GUARDAN
#LOS DATOS A GRAFICAR.
meses = ["ene", "feb", "mar", "abr", "may", "jun", "jul", "ago", "sept", "oct", "nov", "dic"]

lluviasPorMes = []
listaTabla = [["Precipitación promedio (mm)", "PAM (mm/dia)", "SAM (mm/dia)", "TAM (mm/dia)"]]
for i in range(1,13):
  lluvias = rainPiuraTableCopy.loc[rainPiuraTableCopy["Mes"] == i].dropna()
  lluvias = lluvias.sort_values(by = "Precipitación acumulada (mm)", ascending = False)
  descripcion = ["llovió {:.1f} mm<br>el {:02d}/{:02d}/{}".format(lluvias.iloc[0,3], lluvias.iloc[0,2], lluvias.iloc[0,1], lluvias.iloc[0,0]),
                 "llovió {:.1f} mm<br>el {:02d}/{:02d}/{}".format(lluvias.iloc[1,3], lluvias.iloc[1,2], lluvias.iloc[1,1], lluvias.iloc[1,0]),
                 "llovió {:.1f} mm<br>el {:02d}/{:02d}/{}".format(lluvias.iloc[2,3], lluvias.iloc[2,2], lluvias.iloc[2,1], lluvias.iloc[2,0])]
  lluviasPorMes.append({  "N° MES": lluvias.iloc[0,1],
                          "MES" : meses[i-1],
                          "PRECIPITACION PROMEDIO (mm)" : round(lluvias["Precipitación acumulada (mm)"].mean(), 2),
                          "1era PRECIP MÁXIMA REG (mm)" : lluvias.iloc[0,3],
                          "2da PRECIP MÁXIMA REG (mm)" : lluvias.iloc[1,3],
                          "3era PRECIP MÁXIMA REG (mm)" : lluvias.iloc[2,3],
                          "descr 1era PRECIP" : descripcion[0],
                          "descr 2da PRECIP" : descripcion[1],
                          "descr 3era PRECIP" : descripcion[2]})
dfLluviasPorMes = pd.DataFrame(lluviasPorMes)
for j in range(2,6):
  listaTabla.append([dfLluviasPorMes.iloc[k,j] for k in range(0,12)])
dfLluviasPorMes #SI SE VA A USAR UN ENTORNO DIFERENTE A GOOGLE COLAB, USAR PRINT PARA IMPRIMIR EL DATAFRAME

#CODIGO PARA ELABORAR Y MOSTRAR EL GRÁFICO CON TABLA USANDO matplotlib (plt)
#Y ELABORAR Y MOSTRAR EL GRÁFICO INTERACTIVO USANDO plotly.graph_objs (go) y iplot

colores = ["#FFFFFF","#FF0000","#CC3300","#006611"]
plt.figure(figsize = (9,6))
plt.plot(dfLluviasPorMes["N° MES"],dfLluviasPorMes["1era PRECIP MÁXIMA REG (mm)"], color = "#FF0000", linewidth = 1, marker = "o", label = "Primer acumulado máximo (PAM)\n(mm/dia)")

plt.plot(dfLluviasPorMes["N° MES"],dfLluviasPorMes["2da PRECIP MÁXIMA REG (mm)"], color = "#CC3300", linewidth = 1, marker = "o", label = "Segundo acumulado máximo (SAM)\n(mm/dia)")

plt.plot(dfLluviasPorMes["N° MES"],dfLluviasPorMes["3era PRECIP MÁXIMA REG (mm)"],color = "#006611", linewidth = 1, marker = "o", label = "Tercer acumulado máximo (TAM)\n(mm/dia)")

plt.title("PRECIPITACIONES MÁXIMAS REGISTRADAS EN EL PERIODO {} - {}\nEN LA ESTACIÓN METEOROLÓGICA {}.".format(periodoReg[0], periodoReg[1], nombreEstacionMeteorologica))
plt.ylabel(" Precipitación (mm)")
plt.xticks([])
plt.legend( loc = "best")
plt.table(cellText = listaTabla[1:], rowLabels = listaTabla[0],colLabels = meses, loc = "bottom", rowColours = colores)
plt.subplots_adjust(left=0.2, bottom=0.2)
#plt.show()
plt.savefig("LluviaMaxPorMeses - estación {}.jpg".format(nombreEstacionMeteorologica), dpi = 600, bbox_inches = 'tight')
print("\n")

figInterac = go.Figure()
figInterac.add_trace(go.Scatter(x = dfLluviasPorMes["MES"], y = dfLluviasPorMes["1era PRECIP MÁXIMA REG (mm)"],mode = "lines+markers",
                                name = "1era Precip. maxima registrada<br>en un dia del mes",
                                text = dfLluviasPorMes["descr 1era PRECIP"]))
figInterac.add_trace(go.Scatter(x = dfLluviasPorMes["MES"], y = dfLluviasPorMes["2da PRECIP MÁXIMA REG (mm)"],mode = "lines+markers",
                                name = "2da Precip. maxima registrada<br>en un dia del mes",
                                text = dfLluviasPorMes["descr 2da PRECIP"]))
figInterac.add_trace(go.Scatter(x = dfLluviasPorMes["MES"], y = dfLluviasPorMes["3era PRECIP MÁXIMA REG (mm)"],mode = "lines+markers",
                                name = "3era Precip. maxima registrada<br>en un dia del mes",
                                text = dfLluviasPorMes["descr 3era PRECIP"]))
figInterac.update_layout(title = "PRECIPITACIONES MÁXIMAS REGISTRADAS EN EL PERIODO {} - {}<br>EN LA ESTACIÓN METEOROLÓGICA {}.".format(periodoReg[0], periodoReg[1], nombreEstacionMeteorologica),)
figInterac.update_yaxes(title_text = "Precipitación (mm)")
#iplot(figInterac)
figInterac.write_html("LluviaMaxPorMeses - estación {}.html".format(nombreEstacionMeteorologica))
plt.show()
