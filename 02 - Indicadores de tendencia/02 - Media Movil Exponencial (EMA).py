# Import libraries
from cProfile import label

import pandas as pd
import yfinance as yf
import mplfinance as mpf
import matplotlib.pyplot as plt
from matplotlib.pyplot import title


# Function to calculate Exponential Moving Average (EMA)

def Media_Movil_Exponencial(df: pd.DataFrame, longitud: int = 26, columna: str = "Close") -> pd.Series:
    """
    La Media Móvil Exponencial (ema) es un indicador técnico que rastrea el precio de un activo
    (como una acción o una mercancía) a lo largo del tiempo. La ema es un tipo de media móvil ponderada (WMA)
    que otorga mayor peso a los datos de precios más recientes.
    ----------
    Parámetros:
    ----------
    df : pd.DataFrame
        Datos históricos del activo.

    longitud : int, opcional (por defecto=26)
        Ventana de tiempo utilizada para calcular la ema.

    columna : str, opcional (por defecto='Close')
        Columna del DataFrame sobre la cual se calculará la ema.

    ----------
    Retorna:
    ----------
    pd.Series
        Serie con los valores de la Media Móvil Exponencial (ema).
    """

    df = df[columna]
    EMA = df.ewm(span=longitud, min_periods=longitud, adjust=False).mean()
    EMA.name = "EMA"

    return EMA

# Descargar los datos

df = yf.download("MSFT", start="2023-01-01", end="2024-01-01", interval="1d", multi_level_index=False)


# Calcular Indicador

ema_12 = Media_Movil_Exponencial(df, longitud=12, columna="Close")
ema_26 = Media_Movil_Exponencial(df, longitud=26, columna="Close")

# Graficar

ema_plots = [
    mpf.make_addplot(ema_12, label="EMA 12 Días", color="green", type="line"),
    mpf.make_addplot(ema_26, label="EMA 26 Días", color="blue", type="line")
]

mpf.plot(df, type="candle", style="yahoo", volume=True, figsize=(22,10), addplot=ema_plots, figscale=3.0,
         title="Medias Móviles Exponenciales")
plt.show()


# Recordatorio

# - La Media Móvil Exponencial (EMA) da más peso a los precios recientes, lo que la hace más sensible a los cambios recientes en el precio.
# - Las EMAS comunes son las de 12 y 26 días. La EMA se utiliza para identificar la tendencia y generar señales de compra o venta.
# - La EMA se puede operar de manara similar a la SMA, pero es más reactiva a los cambios recientes en el precio.
# - Para evitar malas interpretaciones, es útil usar la EMA en combinacion con otra EMA de diferente longitud.