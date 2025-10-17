# Importar Librerias
import pandas as pd
import numpy as np
import yfinance as yf
import mplfinance as mpf
import matplotlib.pyplot as plt

# Indicador: Indice de Fuerza Relativa (RSI)

def Indicador_Fuerza_Relativa(df: pd.DataFrame, longitud: int = 14, columna: str = "Close") -> pd.Series:
    """
    El Indice de Fuerza Relativa (RSI) es un indicador utlizado en el analisis tecnico que mide la magnitud de los
    cambios recientes en los precios para evaluar condiciones de sobrecompra o sobreventa en el precio de una accion
    u otro activo.

    Como Operarlo:
        La interpretacion y uso tradicionales del RSI indican que valores de 70 o más sugieren que un adtivo esta
        sobrecomprado o sobrevalorado y podrian estar listos para una reversion de tendencia o una correccion de precio.
        Una lectura de RSI de 30 o menos indican una condicion de sobreventa o infravalorada.

    Parametros
    :param int: Longitud: Ventana a usar en el calculo del RSI (por defecto, se establece en 14).
    :param str: Columna a utilizar en el calculo del RSI (por defecto, establece en close).
    Salida:

    :return: pd.Series : Calculo del indice de fuerza relativa (RSI).
    """
    # Calcular

    Delta = df[columna].diff(periods=1)
    Ganancia = Delta.where(Delta >= 0, 0)
    Perdida = np.abs(Delta.where(Delta < 0, 0))
    # Valores en la posicion de la longitud
    media_ganancia = Ganancia.ewm(span=longitud, min_periods=longitud, adjust=False).mean()
    media_perdida = Perdida.ewm(span=longitud, min_periods=longitud, adjust=False).mean()
    RS = media_ganancia / media_perdida
    RSI = pd.Series(np.where(RS == 0, 100, 100 - (100 / (1 + RS))), name="RSI", index=df.index)

    return RSI


# Descargar Datos

ticker = "BTC-USD"
df = yf.download(ticker, start="2024-01-01", end="2025-10-15", interval="1d", multi_level_index=False)

# Calcular RSI

rsi = Indicador_Fuerza_Relativa(df)

# Niveles de sobrecompra y sobreventa

sobrecomprayventa = [
    mpf.make_addplot([70] * len(rsi), panel=2, color="gray", linestyle="--"),
    mpf.make_addplot([30] * len(rsi), panel=2, color="gray", linestyle="--")
]

ap = [
    mpf.make_addplot(rsi, panel=2, color="blue", ylabel="RSI",)

] + sobrecomprayventa

mpf.plot(df, type="candle", style="yahoo", volume=True, addplot=ap, title="Indice de Fuerza Relativa (RSI)",
         ylabel="Precio del Activo", ylabel_lower="Volumen", figsize=(22,10), figscale=3.0, warn_too_much_data=df.shape[0])

plt.show()

# Recordatorio:
#   - El RSI es un indicador de impulso que mide la magnitud de los cambios en los precios para evaluar condiciones de sobrecompra o sobreventa.
#   - Valores de RSI de 70 o más sugieren que el activo podria estar sobrecomprado, mientras que los valores de 30 o menos indican sobreventa.
#   - Las lineas discontinuas en gris representan los niveles criticos de sobrecompra y sobreventa. Cuando el RSI cruza estas lineas,
#     puede ser un indicio de una posible reversion en la tendencia.
#   - El RSI se utiliza para identificar posibles puntos de entrada o salida en el mercado basado en estas condiciones extremas.
