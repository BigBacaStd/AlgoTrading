# Importar librerias
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt


# Indicador: Nube Ichimoku

def Ichimoku_Cloud(df: pd.DataFrame, periodo_tenkan: int = 9, periodo_kijun: int = 26,
                   offset: bool = False) -> pd.DataFrame:
    """
    El Ichimoku Cloud es una coleccion de indicadores tecnicos que muestran niveles de soporte y resistencia, asi como direccion y momento de la tendencia.
    Calcula multiples promedios y traza una "nube" para pronosticar donde el precio puede encontrar soporte o resistencia en el futuro.

    Comom Operarlo:

    La tendencia general es alcista cuando el precio esta por encima de la nube (posiciones Largas), bajista cuando el precio esta por debajo
    de la nube (posiciones cortas) y sin tendencia o en transicion cuando el precio esta en la nube.

    Cuando el Span A (Senkou Span A) esta en aumento por encima del Span B (Senkou Span B), esto ayuda a confirmar la
    tendencia alcista y el espacio entre las lineas se colorea tipicamente verde. Cuando el Span A esta en disminucion
    y por debajo del Span B, esto confirma la tendencia Bajista y el espacio entre las lineas se colorea rojo.

    -------------
    Parametros:
    -------------
    :param: pd.DataFrame: df: Datos activo.
    :param : int: periodo_tenkan: Ventana a utilizar en el calculo de Ichimoku Cloud (por defecto, se establece en 9).
    :param : int: periodo_kijun: Ventana a utilizar en el calculo de  Ichimoku Cloud ( por defecto, se establece en 26).
    :param : bool: Offset: Mostrar datos desplazados (por defecto, se establece False).

    Saluda:
    --------
    :return: pd.DataFrame : Calculo de Ichimoku Cloud.
    """

    # Calcular

    High, Low = df["High"], df["Low"]

    # Tenkan Sen: Linea de Señal a corto plazo
    rolling_min_tenkan = Low.rolling(window=periodo_tenkan, min_periods=periodo_tenkan).min()
    rolling_max_tenkan = High.rolling(window=periodo_tenkan, min_periods=periodo_tenkan).max()
    tenkan_sen = (rolling_max_tenkan + rolling_min_tenkan) / 2

    # Kijun Sen: Linea de señal a largo plazo
    rolling_min_kijun = Low.rolling(window=periodo_kijun, min_periods=periodo_kijun).min()
    rolling_max_kijun = High.rolling(window=periodo_kijun, min_periods=periodo_kijun).max()
    kijun_sen = (rolling_max_kijun + rolling_min_kijun) / 2

    # Senkou Span A - Nube
    senkou_span_a = ((tenkan_sen + kijun_sen) / 2)

    # Senkou Span B - Nube

    rolling_min_senkou = Low.rolling(window=periodo_kijun * 2, min_periods=periodo_kijun * 2).min()
    rolling_max_senkou = High.rolling(window=periodo_kijun * 2, min_periods=periodo_kijun * 2).max()
    senkou_span_b = ((rolling_min_senkou + rolling_max_senkou) / 2)

    # Chikou Span: Linea de confirmacion

    chikou_span = df["Close"].shift(periods=-periodo_kijun)

    # Crear un DataFrame con los resultados

    IC = pd.concat([tenkan_sen, kijun_sen, senkou_span_a, senkou_span_b, chikou_span], axis=1)
    IC.columns = ["tenkan_sen", "kijun_sen", "senkou_span_a", "senkou_span_b", "chinkou_span"]

    # Desplazar los Span para la nube

    if not offset:
        IC["senkou_span_a"] = senkou_span_a.shift(periods=periodo_kijun)
        IC["senkou_span_b"] = senkou_span_b.shift(periods=periodo_kijun)
    else:
        IC["senkou_span_a"] = senkou_span_a
        IC["senkou_span_b"] = senkou_span_b

    return IC


# Descargar los datos historicos

df = yf.download("BTC-USD", start="2022-01-01", end="2025-10-12", interval="1D", multi_level_index=False)

# Calcular Indicador

ichimoku = Ichimoku_Cloud(df, periodo_tenkan=9, periodo_kijun=26)

# Graficar Ichimoku Cloud

fig, ax = plt.subplots(figsize=(22, 10))

ax.plot(df.index, df["Close"], label="Precio de Cierre", color="black", linewidth=1.0)

# Graficar la nube

ax.plot(ichimoku.index, ichimoku["senkou_span_a"], label="Senkou Span A", color="blue")
ax.plot(ichimoku.index, ichimoku["senkou_span_b"], label="Senkou Span B", color="red")
ax.fill_between(ichimoku.index, ichimoku["senkou_span_a"], ichimoku["senkou_span_b"],
                where=ichimoku["senkou_span_a"] > ichimoku["senkou_span_b"],
                color="lightgreen", alpha=0.5, label="Nube Alcista")
ax.fill_between(ichimoku.index, ichimoku["senkou_span_a"], ichimoku["senkou_span_b"],
                where=ichimoku["senkou_span_a"] <= ichimoku["senkou_span_b"],
                color="lightcoral", alpha=0.5, label="Nube Bajista")

ax.plot(ichimoku.index, ichimoku["tenkan_sen"], label="Tenkan Sen", color="purple", linestyle="--", lw=2)
ax.plot(ichimoku.index, ichimoku["kijun_sen"], label="Kijun Sen", color="orange", linestyle="--", lw=2)

ax.legend(fontsize=10)
ax.set_title("Nube Ichimoku con Precio de Cierre", fontsize=16)
ax.set_xlabel("Fecha")
ax.set_ylabel("Precio")
ax.grid(True)

plt.tight_layout()
plt.show()


#Recordatorio:
#   -El Ichimoku Cloud es una herramienta completa para el analisis tecnico que proporciona informacion sobre niveles de soporte y resistencia,
#   así como la direccion y momento de la tendencia. Utiliza varias lineas para trazar una "nube" que ayuda a prever posibles niveles futuros de
#   soporte y resistencia.
#   -La tendencia es considerada alcista cuando el precio esta por encima de la nube, bajista cuando esta por debajo, y neutras o en transicion
#   cuando el precio esta dentro de la nube.
#   -El area entre el Senkou Span A y el Senkou Span B se colorea para indicar las condiciones del mercado: verde claro para condiciones alcistas
#   y rojo coral para condiciones bajistas. La combinacion de estas lineas y la nube ayuda a los traders a vizualizar la fuerza de la tendencia
#   y a tomar decisiones informadas sobre sus operaciones.