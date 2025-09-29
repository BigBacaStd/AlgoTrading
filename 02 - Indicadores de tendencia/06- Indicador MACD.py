# Importar librerias
from cProfile import label

import pandas as pd
import numpy as np
import yfinance as yf
import matplotlib.pyplot as plt
from IPython.core.pylabtools import figsize


# Indicador: Convergencia-Divergencia de Promedios Moviles (MACD)

def MACD(df: pd.DataFrame, longitud_rapida: int = 12, longitud_lenta: int = 26, longitud_señal: int = 9,
         columna: str = "Close") -> pd.DataFrame:
    """
    La Convergencia-Divergencia de Promedios Moviles (MACD) es un indicador de seguimiento de tendencias que muestra la relacion entre
    dos promedios moviles del precio de un activo. El MACD se calcula restando el promedio movil exponencial de largo plazo (usualmente 26 periodos)
    del promedio movil exponencial de corto plazo (usualmente de 12 periodos).

    Como Operarlo:

        El resultado del calculo es la linea MACD. Un EMA de n-periodos de la MACD, llamada "Linea de señal", se traza sobre la linea MACD,
        que puede funcionar como un desencadenante para señales de compra y venta. Los traders pueden comprar el activo cuando la MACD cruza por encima de su
        linea de señal y vender en corto plazo cuando la MACD cruza por debajo de la linea de señal.

        -------------
        Parametros:

        ------------
        param : pd.Dataframe: df: Datos del intrumento o activo financiero.
        ------------
        param: int: Longitud:rapida: Ventana rapida a utilizar en el calculo del MACD (por defecto, se establece en 12).
        ------------
        param: int : Longitud_lenta: Ventana lenta a utilizar en el calculo del MACD (por defecto, se establece en 26).
        -----------
        param: int: longitud_señal: Ventana de la señal a utilizar en el calculo del MACD (por defecto, se establece en 9).
        -----------
        param : str: columna : Columna a utilizar en el calculo del MACD (por defecto, se establece en "close").
        -----------
        salida:
        -----------
        return: pd.DataFrame: Calculo de la convergencia-divergencia de Promedios Moviles.

    """

    # Calcular los promedios moviles exponenciales

    MA_Rapida = df[columna].ewm(span=longitud_rapida, min_periods=longitud_rapida, adjust=False).mean()
    MA_Lenta = df[columna].ewm(span=longitud_lenta, min_periods=longitud_lenta, adjust=False).mean()

    #Determinar la linea MACD como la diferencia entre el EMA corto y el EMA largo
    MACD_d = MA_Rapida - MA_Lenta

    #Calcular la linea de señal como el EMA de la linea MACD
    señal = MACD_d.ewm(span=longitud_señal, min_periods=longitud_señal, adjust=False).mean()
    MACD = pd.concat([MACD_d, señal], axis=1)
    MACD.columns = ["MACD", "Señal"]

    return MACD

#Obtener Datos Historicos del activo

df = yf.download("NVDA",start="2020-01-01", interval="1d")

#Calcular el Indicador
macd = MACD (df, longitud_rapida=12, longitud_lenta=26, longitud_señal=9)

# Graficar Indicador

fig, (ax1, ax2) = plt.subplots(nrows=2, ncols=1, figsize=(22,10), sharex=True)

#Grafico del Precio de Cierre

ax1.plot(df["Close"], label="Precio de Cierre", color="blue")
ax1.set_title("Precio de Cierre", size=18, fontweight="bold")
ax1.set_ylabel("Precio")
ax1.legend(loc="upper left")
ax1.grid(True)

#Grafico del MACD


ax2.plot(macd.index, macd["MACD"], label="MACD", color="blue")
ax2.plot(macd.index, macd["Señal"], label="Linea de la Señal", color="red")
ax2.bar(macd.index, macd["MACD"] - macd["Señal"], color=np.where(macd["MACD"] > macd["Señal"], "green", "red"), label="Histograma")
ax2.set_title("Convergencia-Divergencia de Promedios Moviles (MACD)", size=18, fontweight="bold")
ax2.set_xlabel("Fecha")
ax2.set_ylabel("Valor")
ax2.legend(loc="lower left")
ax2.grid(True)

plt.tight_layout()
plt.show()


#Recordatorio
#   -El MACD se utiliza para indentificar posibles señales de compra y venta. Un cruce de la linea mACD por encima de la linea de la señal
#   puede sugerir una oportunidad de compra.
#   -Un cruce por debajo de la linea de la señal puede indicar una señal de venta. El histograma, que muestra la diferencia entre el MACD y
#   la linea de la señal, puede ayudar a visualizar la fuerza de la tendencia.