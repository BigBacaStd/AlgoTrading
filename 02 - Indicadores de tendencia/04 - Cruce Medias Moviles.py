from cProfile import label

import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.lines import lineStyles
from scipy.stats import alpha


# Indicador/Estrategia: Cruce de Medias Moviles
def Cruce_Medias_Moviles(df: pd.DataFrame, longitud_rapida: int = 9, longitud_lenta: int = 26, columna: str = "Close") -> pd.DataFrame:

    """
    El cruce de Medias Moviles es un indicador tecnico que utiliza dos medias moviles como estrategia. Es un buen ejemplo de las
    denominadas estrategias tradicionales. Las estrategias tradicionales estan siempre en largo o en corto, lo que significa que
    nunca estan fuera del mercado.

    Como operarlo:

    Operar con el cruce de Medias Moviles es bastante simple. Si la Media Movil Rapida cruza de abajo hacia arriba la Media Movil Lenta,
    esto significa una oportunidad de compra. Si la Media Movil Rapida cruza de arriba hacia abajo a la Media Movil Lenta,
    esto significa una oportunidad de venta. El cruce de Medias Moviles a menudo se utiliza junto con otros indicadores para evitar señales
    falsas en mercados de baja volatilidad.

    Parametros:
    -----------
    param: pd.DataFrame: df: Datos del intrumento financiero.
    -----------
    param: int : Longitud_rapida: Ventana rapida a utilizar en el calculo del CMM (por defecto, se establece en 9).
    -----------
    param: int: Longitud_Lenta: Ventana lenta a utilizar en el cálculo del CMM (por defecto, se establece 26).
    -----------
    param: str: columna : Columna a utilizar en el cálculo del CMM (por defecto, se establece 'Close').
    ----------
    Salida:
    ----------
    return : pd.DataFrame : Cálculo del cruce de Medias Moviles.

    """

    # Calcular

    columna_precio = df[columna]
    SMA_Rapida = columna_precio.rolling(window=longitud_rapida, min_periods=longitud_rapida).mean()
    SMA_Rapida_S = SMA_Rapida.shift(periods=1)
    SMA_Lenta = columna_precio.rolling(window=longitud_lenta, min_periods=longitud_lenta).mean()
    SMA_Lenta_S = SMA_Lenta.shift(periods=1)

    # Cruce
    Cruce = np.where(((SMA_Rapida > SMA_Lenta) & (SMA_Lenta_S > SMA_Rapida_S)), 1,
                     np.where(((SMA_Rapida < SMA_Lenta) & (SMA_Lenta_S < SMA_Rapida_S)), -1, 0))

    MAC = pd.concat([SMA_Rapida, SMA_Lenta, pd.Series(Cruce, index=df.index)], axis=1)
    MAC.columns = ["SMA_Rapida", "SMA_Lenta", "Cruce"]

    return MAC

# Obtener Datos

df = yf.download("TSLA", start="2020-01-01", end="2024-01-01", interval="1d",multi_level_index=False)

# Calcular indicador

mac = Cruce_Medias_Moviles(df, longitud_rapida=9, longitud_lenta=26, columna="Close")

# Graficar Indicador

fig, axes = plt.subplots(nrows=1, ncols=1, figsize=(26,12))

# Graficar las medias moviles

filas = 600
mac["Cruce"] = mac["Cruce"].replace(0, np.nan).ffill()
mac[-filas:][["SMA_Rapida", "SMA_Lenta"]].plot(ax=axes)
df["Close"][-filas:].plot(ax=axes, label="Precios de Cierre", color="black", alpha=0.5, style="--")

# Rellenar el area entre las medias moviles segun la tendencia

axes.fill_between(
    x=mac.index[-filas:],
    y1=mac["SMA_Rapida"][-filas:],
    y2=mac["SMA_Lenta"][-filas:],
    where=mac["SMA_Rapida"][-filas:] > mac["SMA_Lenta"][-filas:],
    color="lightgreen",
    alpha=0.5,
    label="Tendencia Alcista"
)

axes.fill_between(
    x=mac.index[-filas:],
    y1=mac["SMA_Rapida"][-filas:],
    y2=mac["SMA_Lenta"][-filas:],
    where=mac["SMA_Rapida"][-filas:] < mac["SMA_Lenta"][-filas:],
    color="lightcoral",
    alpha=0.5,
    label="Tendencia Bajista"
)

# Añadir triangulos solo en los cruces de las lineas

for i in range(1, filas):
    if mac["Cruce"].iloc[-i] == 1 and mac["Cruce"].iloc[-(i-1)] == -1:
        axes.scatter(mac.index[-1], mac["SMA_Rapida"].iloc[-i], marker="^", color="green", s=120, edgecolor="black",
            linewidth=1.5)

    elif mac["Cruce"].iloc[-i] == -1 and mac["Cruce"].iloc[-(i-1)] == 1:
        axes.scatter(mac.index[-1], mac["SMA_Rapida"].iloc[-i], marker="v", color="green", s=120, edgecolor="black",
            linewidth=1.5)


# Configurar leyendas y etiquetas

axes.legend(fontsize=15, loc="lower left")

plt.title("Indicador de Cruce de Medias Moviles", size=24, fontweight="bold")
plt.suptitle("Señales de compra y venta basadas en el cruce de medias moviles", size=16, style="italic")
plt.grid(visible=True, linestyle="--", linewidth=0.75)
plt.show()

# Recordatorio:

#   - Los Cruces de Promedios Móviles son útiles para identificar la dirección de una tendencia.

#   - El Cruce de Promedios Móviles puede producir señales de compra y de venta, pero en mercados con tendencias laterales o poco definidas,

#     estas señales pueden ser engañosas, generando falsas entradas o salidas.