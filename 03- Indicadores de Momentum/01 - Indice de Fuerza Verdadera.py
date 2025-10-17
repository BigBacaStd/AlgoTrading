# Importar librerias

import pandas as pd
import yfinance as yf
import mplfinance as mpf
import matplotlib.pyplot as plt
from matplotlib.pyplot import ylabel


# Indicador: Indicador de Fuerza Verdadera (TSI)

def Indicador_Fuerza_Verdadera(df: pd.DataFrame, longitud_rapida: int = 13, longitud_lenta: int = 25, senal: int = 13,
                               columna: str = "Close") -> pd.DataFrame:
    """
    El indicador de Fuerza Verdadera (TSI) es un oscilador de impulso tecnico utilizado para identificar tendencias y reversiones.
    Es util para determinar condiciones de sobrecompra y sobreventa, indicando cambios de direccion de la tendencias a traves
    de cruces de la linea central o de la linea de señal, advirtiendo sobre la tendencia mediante divergencias.

    Como Operarlo:

    El TSI fluctua entre los positivos y negativos. Territorio positivo significa que los alcistas tienen más control sobre el activo,
    mientras que numeros negativos indican que los bajistas tienen más control. Cuando el indicador diverge con el precio, el TSI
    podria estar señalando que la tendencia del precio se esta debilitando y podria revertirse.

    Se puede aplicar una linea de señal al indicador TSI. Cuando el TSI cruza por encima de la linea de señal, puede ser utilizado como una
    señal de compra; cuando cruza por debajo, como una señal de venta. Los niveles de sobrecompra y sobreventa variaran segun el activo que se esté operando.

    ----------------
    Parámetros:

    -----------------

    param: int: Longitud_rapida: Ventana rapida a usar en el calculo del TSI (por defecto, se establece en 13)

    ------------------

    param: int: Longitud_lenta: Ventana lenta a usar en el calculo del TSI (por defecto, se establece en 25)

    param: int: señal: Ventana de señal a usar en el calculo del TSI (por defecto, se establece en 13)

    param: str: columna: Columna a utilizar para el calculo del TSI (por defecto, se establece en 'Close')

    Salida:
    ----------------
    return: pd.Dataframe: Calculo del Indicador de Fuerza Verdadera.
    """

    # Calcular
    Momento = df[columna].diff(periods=1)
    # EMA de Momento
    EMA_lenta = Momento.ewm(span=longitud_lenta, min_periods=longitud_lenta, adjust=False).mean()
    EMA_rapida = EMA_lenta.ewm(span=longitud_rapida, min_periods=longitud_rapida, adjust=False).mean()
    # EMA del Momentum Abs
    Momento_abs = abs(Momento)
    EMA_lenta_abs = Momento_abs.ewm(span=longitud_lenta, min_periods=longitud_lenta, adjust=False).mean()
    EMA_rapida_abs = EMA_lenta_abs.ewm(span=longitud_rapida, min_periods=longitud_rapida, adjust=False).mean()
    # Calcular TSI
    TSI_df = 100 * (EMA_rapida / EMA_rapida_abs)
    Senal = TSI_df.ewm(span=senal, min_periods=senal, adjust=False).mean()
    TSI = pd.concat([TSI_df, Senal], axis=1)
    TSI.columns = ["TSI", "Senal"]

    # Determinar tendencia alcista o bajista

    TSI["Tendencia"] = TSI["TSI"] > TSI["Senal"]

    return TSI


# Descargar datos

ticker = "BTC-USD"
df = yf.download(ticker, start="2024-01-01", end="2025-10-15", interval="1d",multi_level_index=False)

# Calcular el TSI
tsi_df = Indicador_Fuerza_Verdadera(df)

# Colores de la tendencia

tsi_colores = ["green" if tendencia else "red" for tendencia in tsi_df["Tendencia"]]

# Niveles de sobrecompra y sobreventa

sobrecomprayventa = [
    mpf.make_addplot([25] * len(tsi_df), panel=2, color="black", linestyle="--"),
    mpf.make_addplot([-25] * len(tsi_df), panel=2, color="black", linestyle="--")
]

ap = [
         mpf.make_addplot(tsi_df["TSI"], panel=2, color="blue", ylabel="TSI"),
         mpf.make_addplot(tsi_df["Senal"], panel=2, color="red"),
         mpf.make_addplot(tsi_df["TSI"], panel=2, type="bar", color=tsi_colores, alpha=0.40)
     ] + sobrecomprayventa

mpf.plot(df, type="candle", style="yahoo", volume=True, addplot=ap, title="Indicador Fuerza Verdadera (TSI)",
         ylabel="Precio", ylabel_lower="Volumen",figsize=(22,10), figscale=3.0, warn_too_much_data=df.shape[0])


#Recordatorio
#   - EL TSI es un oscilador de impulso que ayuda a identificar tendencias y posibles reversiones en el mercado.
#   - Los cruces de la linea TSI con la linea de la señal pueden ser utilizados como señales de compra (cruce hacia arriba) o venta (cruce hacia abajo)
#   - El histograma proporciona una representacion visual de la fuerza de tendencia, con barras verdes indicando un impulso alcista y barras
#     rojas señalando un impulso bajista.
#   - Los niveles de sobrecompra y sobreventa, marcados por las lineas negras discontinuas, son puntos criticos donde el mercado puede estar listo
#     para una reversion.
