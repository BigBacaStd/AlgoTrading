# Importar Librerias

import pandas as pd
import numpy as np
import yfinance as yf
import matplotlib.pyplot as plt
from IPython.core.pylabtools import figsize


# Indicador: Indice de Canal de Materias Primas (CCI)

def CCI(df: pd.DataFrame, longitud: int = 20, constante: float = 0.015) -> pd.Series:
    """
    El indice de Canal de materias primas (CCI) es un indicador tecnico utilizado para determinar cuando el precio de un activo esta
    alcanzando niveles de sobrecompra o sobreventa. Evalua la direccion y fuerza de la tendencia de precio, permitiendo traders
    determinar cuando entrar o salir de una operacion.

    Como operarlo:

        El CCI es un oscilador sin limites, lo que signifca que puede subir o bajar indefinidamente. Por esta razon, los nivles de
        sobrecompra y sobreventa se determinan tipicamente para cada activo mirando los niveles extremos historicos del CCI
        donde el precio se revirtio.

    Parametros:
    ------------

    :param : pd.DataFrame: df: Datos historicos del activo financiero.
    :param : int :longitud: Ventana a utilizar en el calculo del CCI (por defecto, se establece en 20).
    :param : float : constante : Constante multiplicadora (por defecto, se establece en 0.0015).
    Salida:
    -------
    :return: pd.Series : Calculo del indice de canal de materias primas.
    """

    # Calcular el Precio Tipico

    precio_tipico = (df["High"] + df["Low"] + df["Close"]) / 3
    tp_rolling = precio_tipico.rolling(window=longitud, min_periods=longitud)
    desviacion_media = tp_rolling.apply(lambda x: np.abs(x - x.mean()).mean(), raw=True)
    CCI_ = (precio_tipico - tp_rolling.mean()) / (constante * desviacion_media)
    CCI_.name = "CCI"

    return CCI_

# Descargar Datos

df = yf.download("AAPL", start="2020-01-01", end="2025-01-01", interval="1d", multi_level_index=False)

# Calcular Indicador

cci = CCI(df, longitud=20, constante=0.015)

# Calcular Indicador

fig, ax = plt.subplots(figsize=(22,10))

ax.plot(cci.index, cci, label="CCI", color="purple")
ax.axhline(100, color="black", linestyle="--", linewidth=1.5)
ax.axhline(-100, color="black", linestyle="--",linewidth=1.5)
ax.fill_between(cci.index,y1=cci, y2=0, where=(cci > 100), color="Lightgreen", alpha=0.5, label="Sobrecompra")
ax.fill_between(cci.index,y1=cci, y2=0, where=(cci < -100), color="salmon", alpha=0.5, label="Sobreventa")
ax.set_title("Indice de Canal de Materias Primas (CCI", size=18, fontweight="bold")
ax.set_xlabel("Fecha")
ax.set_ylabel("Valor del CCI")
ax.legend(loc="upper left")
ax.grid(True)

ax2 = ax.twinx()
ax2.plot(df.index, df["Close"], label="Precio de Cierre", color="black", alpha=1.0, lw=2)
ax2.set_ylabel("Precio de Cierre", color="black")
ax2.legend(loc="upper right")

plt.tight_layout()
plt.show()

# Recordatorio:
#   -El CCI ayuda a indentificar condiciones de sobrecompra y de sobreventa, destacando niveles extremos en el grafico. Las zonas en verde claro
#   indican sobrecompra y las zonas en rojo salmon indican sobreventa.
#   -Utiliza los niveles de 100 y -100 como referencia para las condiciones extremas.