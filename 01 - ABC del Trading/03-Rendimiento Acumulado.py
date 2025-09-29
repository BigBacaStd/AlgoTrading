#Importar librerias

import yfinance as yf
import numpy as np
import matplotlib.pyplot as plt

#Definir Acción
ticker = "AMZN"

#Descargar datos

datos = yf.download(ticker, start="2023-01-01", end="2024-01-01", interval="1d")

#Calcular el rendimiento simple
datos["Rendimiento_Simple"] = datos["Close"].pct_change()

#Calcular Rendimiento Logaritmico
datos["Rendimiento_Logaritmico"] = np.log(datos["Close"] /datos["Close"].shift(periods=1))

#Calcular el Rendimiento Simple Acumulado
datos["Rendimiento_Simple_Acumulado"] = (1 + datos["Rendimiento_Simple"]).cumprod() -1

#Calcular el Rendimiento Logaritmico Acumulado
datos["Rendimiento_Logaritmico_Acumulado"] = np.exp(datos["Rendimiento_Logaritmico"].cumsum()) - 1

#Mostrar los primeros registros
print("Datos con Rendimiento Simple y Logaritmico Acumulado:")
print(datos[["Rendimiento_Simple_Acumulado", "Rendimiento_Logaritmico_Acumulado"]].head())

#Graficas
plt.figure(figsize=(14,7))

#Grafica de Rendimiento Simple Acumulado
plt.subplot(2,1,1)
plt.plot(datos.index, datos["Rendimiento_Simple_Acumulado"], label="Rendimiento Simple Acumulado", color="blue")
plt.xlabel("Fecha")
plt.ylabel("Rendimiento Acumulado")
plt.title("Rendimiento Simple Acumulado")
plt.legend()

#Grafica de Rendimiento Logaritmico Acumulado
plt.subplot(2,1,2)
plt.plot(datos.index, datos["Rendimiento_Logaritmico_Acumulado"], label="Rendimiento Logaritmico Acumulado", color="green")
plt.xlabel("Fecha")
plt.ylabel("Rendimiento Acumulado")
plt.title("Rendimiento Logaritmico Acumulado")
plt.legend()

plt.tight_layout()
plt.show()


#Recordatorio:
# - El Rendimiento Acumulado representa el crecimiento total de una inversion a lo largo de un periodo.
#   Calculado a partir del rendimiento diario compuesto, nos permite observar como se ha acumulado el rendimiento total
#   considerando los efectos de la capitalizacion de los rendimientos diarios a lo largo del tiempo.