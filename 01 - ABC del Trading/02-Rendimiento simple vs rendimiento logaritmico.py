import yfinance as yf
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Configuracion de Parametros

ticker = "TSLA"
fecha_inicial = "2023-01-01"
fecha_final = "2024-01-01"

#Descargar Datos
datos = yf.download(ticker, start=fecha_inicial, end=fecha_final, interval="1d")

#Calcular el Rendimiento Simple
datos["Rendimiento_Simple"] = datos ["Close"].pct_change() # datos ["Close"] / datos ["Close"].shift(periods=1) -1

#Calcular el Rendimiento Logaritmico

datos["Rendimiento_Logaritmico"] = np.log(datos["Close"] / datos ["Close"].shift(periods=1))

#Mostrar los primeros registros
print("Datos con Rendimiento Simple y Logaritmico:")
print(datos[["Rendimiento_Simple", "Rendimiento_Logaritmico"]].head())

#Graficas

plt.figure(figsize=(14, 7))

#Grafica de rendimientos simples
plt.subplot(2, 1, 1)
plt.plot(datos.index, datos["Rendimiento_Simple"], label="Rendimiento Simple", color="blue")
plt.xlabel("Fecha")
plt.ylabel("Rendimiento Simple")
plt.title("Rendimiento Simple")
plt.legend()

#Grafica de rendimiento logaritmico

plt.subplot(2, 1, 2)
plt.plot(datos.index, datos["Rendimiento_Logaritmico"], label="Rendimiento Logaritmico", color="green")
plt.xlabel("Fecha")
plt.ylabel("Rendimiento Logaritmico")
plt.title("Rendimiento Logaritmico")
plt.legend()

plt.tight_layout()
plt.show()

#Comparar relevancia de cada rendimiento

rendimiento_simple_promedio_anualizado = datos["Rendimiento_Simple"].mean() * datos.dropna().shape[0]
rendimiento_logatirmico_promedio_anualizado = np.exp(datos["Rendimiento_Logaritmico"].mean() * datos.dropna().shape[0]) - 1
print("Rendimiento Simple Anualizado:", rendimiento_simple_promedio_anualizado)
print("Rendimiento Logaritmico Anualizado:", rendimiento_logatirmico_promedio_anualizado)

print("Rendimiento Real:", datos["Close"].iloc[-1] / datos["Close"].iloc[0] -1)

#Escenario Hipotetico
precios_accion = pd.DataFrame(data=[100, 20, 40,80], index=[0,1,2,3], columns=["Precios"])
rendimiento_simple = precios_accion.pct_change().mean()
rendimiento_logaritmico = np.exp(np.log(precios_accion / precios_accion.shift(periods=1)).mean() * (precios_accion.shape[0] -1)) -1
print("Rendimiento Simple Erroneo:", rendimiento_simple)
print("Rendimiento Logaritmico Correcto:", rendimiento_logaritmico)


#Recordatorio:

# - Rendimiento Simple:
#   *Es la tasa de cambio porcentual en el precio de cierrre de un activo de un dia al siguiente.
#   *Es facil de interpretar y comunmente utlizado en informes financieros.
#   *No es aditivo a lo largo del tiempo, lo que puede complicar el analisis a largo plazo y llevar a conclusiones erroneas.
# - Rendimiento Logaritmico:
#   *Es la diferencia logaritmica entre el precio de cierre de un activo de un dia al siguiente.
#   *Es aditivo a lo largo del tiempo, lo que facilita el analisis de rendimientos acumulados y la modelizacion de series temporales
#   *A menudo es preferido en analisis cuantitativo y financiero debido a sus propiedades matematicas.