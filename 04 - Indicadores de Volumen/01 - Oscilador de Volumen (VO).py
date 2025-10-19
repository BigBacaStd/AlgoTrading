# Importar Librerias
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
from copy import deepcopy


# Indicador: Oscilador de Volumen

def Oscilador_Volumen(df: pd.DataFrame, longitud_rapida: int = 12, longitud_lenta: int = 26, senal: int = 9) -> pd.DataFrame:
    """
    El Oscilador de Volumen (VO) es un indicador tecnico que se basa en la premisa de que no es el nivel real del volumen, sino
    el cambio en el volumen en relacion con el pasado reciente, lo que tiene más importancia tecnica. Muestra la diferencia
    entre dos medias moviles del volumen de un activo expresada como un porcentaje.

    Como Operarlo:

    La diferencia entre dos medias moviles del volumen se puede usar para determinar si la tendencia general del volumen está
    aumentando o disminuyendo. Cuando el VO sube por encima de cero, indica que la media movil del volumen a corto plazo ha subido
    por encima de la media movil de volumen a largo plazo, y por lo tanto, que la tendencia de volumen a corto plazo es mayor que la dentencia
    de volumen a largo plazo.

    El VO se puede utilizar para confirmar una ruptura de soporte o resistencia. Una ruptura de soporte o resistencia con volumen creciente
    indica un movimiento más fuerte que una ruptura de soporte con bajo volumen. De manera similar, una ruptura de resistencia con volumen en expansion muestra
    más intensidad de compra.

    Parametros:

    param: pd.DataFrame : df: Datos.

    param: int : Longitud_rapida : Ventana rapida a utilizar en el VO (por defecto, se establece en 12).

    param: int: Longitud_lenta: Ventana lenta a utilizar en el VO (por defecto, se establece en 26).

    param: int: señal : Ventana de la señal a utilizar en el VO (por defecto, se establece en 9).

    Salida:

    return: pd.DataFrame: Cálculo del Oscilador de Volumen.

    :param df:
    :param longitud_rapida:
    :param longitud_lenta:
    :param senal:
    :return:
    """

    # Calcular

    datos = deepcopy(df)

    ma_rapida = datos["Volume"].ewm(span=longitud_rapida, min_periods=longitud_rapida, adjust=False).mean()
    ma_lenta = datos["Volume"].ewm(span=longitud_lenta, min_periods=longitud_lenta, adjust=False).mean()

    # Oscilador de Volumen

    datos["Oscilador_Volumen"] = (ma_rapida - ma_lenta) / ma_lenta * 100
    datos["Senal"] = datos["Oscilador_Volumen"].ewm(span=senal, min_periods=senal, adjust=False).mean()

    return datos[["Oscilador_Volumen", "Senal"]]


# Descargar datos desde yfinance

ticker = "BTC-USD"
df = yf.download(ticker, start="2024-01-01", end="2025-10-18", interval="1d", multi_level_index=False)

# Calcular el Oscilador de Volumen

osc_v_df = Oscilador_Volumen(df, longitud_rapida=12, longitud_lenta=26, senal=9)

# Graficar

plt.figure(figsize=(22,12))
plt.subplot(2, 1, 1)
plt.plot(df.index, df["Volume"], label="Volumen", color="coral")
plt.title("Volumen de: " + ticker)
plt.legend()

plt.subplot(2, 1, 2)
plt.plot(osc_v_df.index, osc_v_df["Oscilador_Volumen"], label="Oscilador de Volumen", color="blue")
plt.plot(osc_v_df.index, osc_v_df["Senal"], label="Senal", color="red", linestyle="--")
plt.axhline(y=0, color="green", linestyle="--", linewidth=1.5)
plt.title("Oscilador de Volumen de:" + ticker)
plt.legend()

plt.tight_layout()
plt.show()


# Recordatorio:
#   - El Oscilador de Volumen se basa en el camnio relativo del volumen, no en el nivel absoluto. Un aumento en el VO puede indicar
#   - una tendencia de volumen más fuerte, mientras que una disminucion puede sugerir una debilidad.
#   - La linea de señal de VO actua como un filtro adicional para confirmar las señales generadas por el propio oscilador.