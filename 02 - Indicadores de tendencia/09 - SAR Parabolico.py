#import pandas as pd
import numpy as np
import yfinance as yf
import mplfinance as mpf
import matplotlib.pyplot as plt

# Indicador: SAR Parabolico
def Parabolic_SAR(df: pd.DataFrame, incremento: float = 0.02, max_paso: float = 0.20) -> pd.DataFrame:
    """
    El indicador Parabolic SAR (Stop and Reverse) se usa para determinar la direccion de la tendencia y posibles
    reversales en el precio. El SAR Parabolico utiliza un metodo de stop para indentificar puntos adecuados en la entrada
    y salida.

    Como Operarlo:

    El PSAR genera señales de compra y venta cuando la posicion de los puntos se mueve de un lado del precio del activo
    al otro. Por ejemplo, una señal de compra ocurre cuando los puntos se mueven de arriba del precio abajo del precio,
    mientras que una señal de venta ocurre cuando los puntos se mueven de abajo del precio a arriba del precio.

    Los puntos del PSAR se utilizan para establecer ordenes de stop loss en tendencia. Si el precio esta subiendo y el PSAR
    tambien esta subiendo, el PSAR puede usarse como una posible salida si estas en una posicion larga. Si el precio cae por debajo del PSAR
    sal de la operacion larga.

    ------------
    Parametros:
    -----------
    param : pd.DataFrame : df: Datos del activo.
    -----------
    param: float: incremento: Incremento maximo a utilizar en el cálculo del Parabolic SAR (por defecto, se establece en 0.2)
    ----------
    param: float: max_paso : Paso máximo a utilizar en el cálculo del Parabolic SAR (por defecto, se establece en 0.20).
    ---------
    Salida:
    ---------
    return: pd.DataFrame : Cálculo del SAR Parabolico.
    """

    #Calculo

    data = df.copy()
    High, Low, Close = data["High"].values, data["Low"].values, data["Close"].values
    psar_up, psar_down = np.repeat(np.nan, Close.shape[0]), np.repeat.(np.nan, Close.shape[0])

    # Inicializar variables
    up_trend = True
    up_trend_high = High[0]
    down_trend_low = Low[0]
    acc_factor = incremento

    # Iterar sobre los precios para calcular PSAR

    for i in range(2, Close.shape[0]):
        reversal = False
        max_high = High[i]
        min_low = Low[i]

        # Tendencia Alcista
        if up_trend:
            # Calcular el PSAR para tendencia alcista
