# Importar librerías
from cProfile import label

import pandas as pd
from datetime import timedelta
import matplotlib.pyplot as plt
import yfinance as yf
import statsmodels.api as sm

# Parámetros de descarga
ticker = "TSLA"
benchmark_ticker = "^GSPC"
fecha_inicial = "2020-01-01"
fecha_final = "2024-01-01"

# Descargar datos
datos = yf.download(ticker, start=fecha_inicial, end=fecha_final, interval="1d")
benchmark = yf.download(benchmark_ticker, start=fecha_inicial, end=fecha_final, interval="1d")

# Calcular los rendimientos diarios
datos["Rendimiento"] = datos["Close"].pct_change()
benchmark["Rendimiento"] = benchmark["Close"].pct_change()
datos.dropna(inplace=True)
benchmark.dropna(inplace=True)

# ---- Máxima Pérdida (Max Drawdown)
def max_drawdown(rendimientos):
    """
    Calcula la máxima pérdida, el capital acumulado, la serie de drawdown,
    la fecha del pico previo y la fecha del valle (máximo drawdown).
    """
    capital_acumulado = (1 + rendimientos).cumprod()
    maximo_acumulado = capital_acumulado.cummax()
    drawdown = (maximo_acumulado - capital_acumulado) / maximo_acumulado

    # Valor de máxima pérdida
    maxima_perdida_valor = drawdown.max()

    # Fecha del valle (día donde el drawdown es máximo)
    fecha_valle = drawdown.idxmax()

    # Fecha del pico previo (máximo acumulado anterior al valle)
    fecha_pico = capital_acumulado.loc[:fecha_valle].idxmax()

    return maxima_perdida_valor, capital_acumulado, drawdown, fecha_pico, fecha_valle

maxima_perdida_accion, capital_acumulado, drawdown, fecha_maxima, fecha_final_dd = max_drawdown(datos["Rendimiento"])
print(f"Maxima Pérdida de {ticker}: {maxima_perdida_accion:.2%}")

print(f"""
La Máxima Pérdida es la mayor caída desde un punto alto hasta un punto bajo durante el periodo analizado.
Para {ticker}, la Máxima Pérdida es {maxima_perdida_accion:.2%}.
""")

# Asegurar tipos datetime (por si se usan en aritmética con timedelta)
fecha_maxima = pd.to_datetime(fecha_maxima)
fecha_final_dd = pd.to_datetime(fecha_final_dd)

# ---- Gráfica
plt.figure(figsize=(22, 8))

# Curva de capital
plt.plot(datos.index, capital_acumulado, label="Rendimiento Acumulado", color="blue")

# Curva "capital sin drawdown" (capital * (1 - drawdown))
plt.plot(datos.index, capital_acumulado * (1 - drawdown), label="Capital * (1 - Drawdown)", color="red", linestyle="--")

# Rellenar el área del drawdown entre pico y valle
mask = (datos.index >= fecha_maxima) & (datos.index <= fecha_final_dd)
plt.fill_between(
    x=datos.index,
    y1=capital_acumulado,
    y2=capital_acumulado * (1 - drawdown),
    where=mask,
    color="red",
    alpha=0.3,
    label="Área de Máxima Pérdida"
)

# Anotaciones
plt.annotate(
    "Inicio del Drawdown",
    xy=(fecha_maxima, capital_acumulado.loc[fecha_maxima]),
    xytext=(fecha_maxima + timedelta(days=30), capital_acumulado.loc[fecha_maxima] * 1.02),
    arrowprops=dict(facecolor="black", arrowstyle="->", connectionstyle="arc3,rad=0.1", lw=2),
    fontsize=12, color="black"
)

plt.annotate(
    "Fin del Drawdown",
    xy=(fecha_final_dd, capital_acumulado.loc[fecha_final_dd]),
    xytext=(fecha_final_dd + timedelta(days=30), capital_acumulado.loc[fecha_final_dd] * 0.98),
    arrowprops=dict(facecolor="black", arrowstyle="->", connectionstyle="arc3,rad=0.1", lw=2),
    fontsize=12, color="black"
)

plt.xlabel("Fecha", size=14)
plt.ylabel("Valor", size=14)
plt.title("Capital Acumulado y Máxima Pérdida", size=16)
plt.legend()
plt.grid(True)
plt.show()



# Calcular Alpha y Beta

x = sm.add_constant(benchmark["Rendimiento"])
y = datos["Rendimiento"]

# Ajustar el  modelo de regresión
modelo = sm.OLS(y, x).fit()

#Extraer Alpha y beta
alpha = modelo.params["const"] * 252 #Anualizar el Alpha
beta = modelo.params["Rendimiento"]

print(f"Alpha de {ticker}: {alpha:.2%}")
print(f"Beta de {ticker}: {beta:.2%}")


#Comentario explicativo
print(f"""
El Alpha de {ticker} es {alpha:.2%}. Esto indica el rendimiento adicional que la accion ha generado en comparacion con el rendimiento
esperado basado en su riesgo relativo del mercado.
Un Alpha positivo sugiere que la accion ha superado las expectativas datas segun sus caracteristicas de riesgo.

El Beta {ticker} es {beta:.2%}. Esto mide la volatilidad de la accion en relacion con el indice de referencia.
Una Beta mayor a 1 indica que la accion es más volatil que el mercado, mientras que una Beta menor a 1 indica que es menos volatil.

""")

# Graficar los rendimientos acumulados
plt.figure(figsize=(22,8))
plt.plot(datos.index, (1 + datos["Rendimiento"]).cumprod(), label=f"Rendimiento acumulado de {ticker}", color="blue", lw=2)
plt.plot(benchmark.index, (1 + benchmark["Rendimiento"]).cumprod(), label=f"Rendimiento Acumulado {benchmark_ticker}", color="orange", linestyle="--", lw=3)
plt.xlabel("Fecha")
plt.ylabel("Rendimiento Acumulado")
plt.title("Rendimiento Acumulado Comparativo")
plt.legend()
plt.grid(True)
plt.show()


#Recordatorio
#   - Máxima Pérdida (Max Drawdown):
#   *Mide la mayor pérdida desde un punto alto hasta un punto hajo durante un periodo.
#   *Ayuda a evaluar el riesgo y la profundidad de las caidas en el capital.
#   -Alpha:
#   *Representa el rendimiento adicional de una inversion en comparacion con el indica de referencia.
#   *Un Alpha positivo indica un rendimiento superior al esperado segun el riesgo asumido.
#   -Beta:
#   *Mide la volatilidad o el riesgo sistematico de una inversion en relacion con el indice de referencia.
#   *Un Beta mayor a 1 indica que la inversion es más volatil que el indica, mientras que un beta menor a
#   1 indica menor volatilidad.