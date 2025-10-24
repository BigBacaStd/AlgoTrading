#Importar Librerias
import pandas as pd
from datetime import timedelta
import matplotlib.pyplot as plt
import yfinance as yf

# Indicador : Indice Acumulación / Distribución

def Indice_Acumulacion_Distribucion(df: pd.DataFrame) -> pd.Series:

    """
    El índice de Acumulación/Distribución (A/D) es el indicador que utiliza el volumen y porecio para evaluar si un activo esta siendo
    acumulado o distribuido. El Índice A/D busca identificar divergencias entre el precio del activo y el flujo de volumen. Esto proporciona
    una visión de cuan fuerte es una tendencia. Si el precio está subiendo pero el indicador está bajando, esto sugiere que el volumen de compra
    o acumulación puede no ser suficiente para respaldar el aumento del precio y podria esperarse una caida en el precio.

    Como Operarlo:

    La línea del Índice A/D se utiliza para ayudar a evaluar las tendencias de precios y potencialmente detectar reversiones futuras.
    Si el precio de un activo está en una tendencia bajista mientras que la línea A/D está en una tendencia alcista, el indicador
    muestra que puede haber una presion de compra y el precio del activo puede revertirse al alza. Por el contrario, si el precio de un activo
    está en una tendencia alcista mientras que la lines A/D está en una tendencia bajista, el indicador muestra que puede haber una presión
    de venta o mayor distribución. Esto advierte que el precio puede estar proximo a una caída.

    Parámetros:

    :param pd.DataFrame: df Datos históricos del instrumento financiero

    Salida:

    :return: pd.Series: Cálculo del índice de Acumulación/ Distribución

    """

    # Calcular

    High, Low, Close = df["High"], df["Low"], df["Close"]
    MFM = ((Close - Low) - (High - Close)) / (High - Low)
    # Flujo de Dinero de Volumen
    MFV = MFM * df["Volume"]
    MFV.name ="ADI"

    return MFV.cumsum()

# Descargar los datos historicos desde yahoo finance

ticker = "AMD"
df =yf.download(ticker, start="2023-06-01", end="2024-06-01")

# Calcular el índice A/D
ad_index = Indice_Acumulacion_Distribucion(df)

# Crear gráfico con subplots

fig, (ax1, ax2) = plt.subplots(nrows=2, ncols=1, figsize=(22,10), sharex=True)

# Subplot 1: Precio de Cierre

ax1.plot(df.index, df["Close"], color="royalblue", label="Precio de Cierre", linewidth=2)
ax1.set_ylabel("Precio del Activo", fontsize=14, color="orange", weight="bold")
ax1.legend(loc="upper left")
ax1.set_title("Precio de Cierre e Índice de Acumulación/Distribución", fontsize=16, weight="bold")
ax1.grid(True, which="both", linestyle="--", linewidth=1.25)
ax1.set_facecolor("#f5f5f5")

# Subplot 2: Índice de Acumulación / Distribución
ax2.plot(ad_index.index, ad_index, color="royalblue", linestyle="--", linewidth=2, label="Indice de Acumulación/Distribución")
ax2.axhline(y=0, color="blue", linestyle="--", linewidth=3.0)
ax2.set_xlabel("Fecha", fontsize=14)
ax2.set_ylabel("Indice de A/D", fontsize=14, color="orange", weight="bold")
ax2.legend(loc="upper left")
ax2.grid(True, which="both", linestyle="--", linewidth=1.25)
ax2.set_facecolor("#f5f5f5")

# Añadir señales de compra/venta al grafico del indice

buy_signals = ad_index[ad_index > 0]
sell_signals = ad_index[ad_index < 0]

ax2.scatter(buy_signals.index, buy_signals, color="green", marker="^", label="Señal de compra", s=100, edgecolors="black")
ax2.scatter(sell_signals.index, sell_signals, color="red", marker="v", label="Señal de venta", s=100, edgecolors="black")

# Añadir texto explicativo sobre como operar
ax2.text(df.index[-1] + timedelta(days=7), ad_index.max() * 0.8, "Señales de compra\n cuando A/D está en alza", fontsize=12, color="green",
         bbox=dict(facecolor="white", edgecolor="green", boxstyle="round,pad=0.5"))
ax2.text(df.index[-1] + timedelta(days=7), ad_index.min() * 0.8, "Señales de venta\n cuando A/D está en baja", fontsize=12, color="red",
         bbox=dict(facecolor="white", edgecolor="red", boxstyle="round,pad=0.5"))

plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

