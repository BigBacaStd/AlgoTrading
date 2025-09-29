import yfinance as yf
from datetime import datetime, timedelta
import os

#Configuracion de parametros

ticker = 'AAPL'
fecha_inicial = '2023-01-01'
fecha_final = '2025-01-01'
intervalo = '1d'

# Desgargar datos historicos de Yahoo Finance
datos = yf.download(ticker, start=fecha_inicial, end=fecha_final, interval=intervalo)

# Mostrar los primeros registros
print('Datos Historicos')
print(datos.head())

#Guardar los datos en un archivo csv

if not os.path.isdir("../datos"):
    os.mkdir("../datos")
datos.to_csv("../datos/datos_historicos.csv")

#Ejemplos de uso de diferentes activos e intervalos de tiempo

#Ejemplo1: Descargar datos con intervalo de 1 minuto (limitado a 7 dias)

intervalo_1m = yf.download(tickers="BTC-USD", interval="1m")
print('Datos de 1 minuto:')
print(intervalo_1m)

#Ejemplo2: Descargar datos con intervalo de 15 minutos (limitado a 60 dias)

fecha_final = datetime.now()
fecha_inicial = fecha_final - timedelta(days=30)
fecha_final = fecha_final.strftime("%Y-%m-%d")
fecha_inicial = fecha_inicial.strftime("%Y-%m-%d")
intervalo_15m = yf.download(tickers="BTC-USD", start=fecha_inicial, end=fecha_final, interval="15m")
print("Datos de 15 minutos")
print(intervalo_15m)

#Ejemplo3: Descargar datos con intervalo de 1 dia (No hay limite establecido)
intervalo_1d = yf.download(tickers="CL=F", start="2010-01-01", end="2024-08-01", interval="1d")
print("Datos de 1 dia:")
print(intervalo_1d)

#Ejemplo 4: Descargar todos los datos historicos para un instrumento
accion = yf.Ticker(ticker=ticker)
accion_hist = accion.history(period="max", end=fecha_final, interval="1d")
print("Total de datos historicos es:")
print(accion_hist)
#Imprimir fechas de dividendos
print(accion_hist["Dividends"][accion_hist["Dividends"]!=0.0])
#Imprimir splits
print(accion_hist["Stock Splits"][accion_hist["Stock Splits"]!=0.0])

#Recordatorio:
# - Yahoo Finance es un proveedor de datos historicos por excelencia (es el más utilizado).
# - Yahoo Finance puede limitar la frecuencia de las consultas si se realizan demasiadas peticiones
#   en un corto periodo de tiempo.