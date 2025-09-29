# Importar librerias
from cProfile import label
from turtledemo.penrose import start

import pandas as pd
import yfinance as yf
import mplfinance as mpf
import matplotlib.pyplot as plt



# Indicador: Media Movil Simple (SMA)

def Media_Movil_Simple(df: pd.DataFrame, longitud: int = 21, columna: str = "Close") -> pd.Series:

    """
La media movil simple (SMA o MA) se utiliza comunmente para identificar la direccion de la tendencia de una accion o para
determinar sus niveles de soporte y resistencia. Es un indicador de seguimiento de tendencia -o rezagado- porque se basa en
precios pasados.

Cuanto más largo es el periodo de la media movil, mayor es el rezago. Así que una SMA de 200 dias tendra un mayor grado de rezago que una SMA de 20 dias
porque contiene precios de los ultimos 200 dias.

Como operarlo:

    Dado que la SMA se utiliza como niveles de soporte y resistencia, la operacion basica es comprar cerca del soporte en
    tendencias alcistas y vender cerca de la resistencia en tendencias bajistas.

    Operar con solo una SMA puede llevar a malas interpretaciones, y puede ser peligroso. Por eso, operar con SMAs requerira
    una media movil rapida y una lenta. Si la MA rapida cruza de abajo hacia arriba a la MA lenta, esto indica una oportunidad de compra. Si la MA rapida
    cruza de arriba hacia abajo a la MA lenta, esto indica una oportunidad de venta.

-----------
Parametros
-----------

param : pd.DataFrame : df : Datos Historicos

param : int : longitud: Ventana a utilizar en el calculo de la SMA (por defecto, se establece en 21)

param : str: columna: Columna a utilizar en el calculo de la SMA (por defecto, se establece en 'Close'

Salida:

return: pd.Series : Calculo de la Media Movil Simple.
    """

# Calcular
    df = df[columna]
    MA = df.rolling(window=longitud, min_periods=longitud).mean()
    MA.name = "MA"

    return MA

# Obtener Datos

df = yf.download("NFLX", start="2024-01-01", end="2025-01-31", interval="1d", multi_level_index=False)

#Calcular Indicador

media_mov_9 = Media_Movil_Simple(df, longitud=9, columna="Close")
media_mov_21 = Media_Movil_Simple(df, longitud=21, columna="Close")

# Graficar

media_mov_plots = [
    mpf.make_addplot(media_mov_9, label="Media Movil 9 dias", color="green", type="line"),
    mpf.make_addplot(media_mov_21,label="Media Movil 21 dias", color="blue", type="line")
]

mpf.plot(df, type="candle", style="yahoo", volume=True, figsize=(22, 10), addplot=media_mov_plots, figscale=3.0,
         title=dict(title="Promedios Moviles", size=20))

plt.show()

#Recordatorio:
#   - La Media Movil Simple (SMA) es útil para identificar tendencias y niveles de soporte y resistencia.
#   -Un periodo más largo en la SMA indica un mayor rezago en nuestro indicador
#   -Operar con una SMA sola puede llevar a malas interpretaciones; por lo tanto, se recomienda utilizarla en conjunto
#    con otra SMA para obtener señales de compra o venta más precisas.