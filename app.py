import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.express as px

# Configuración de página con look profesional
st.set_page_config(page_title="Big Tech Analysis", layout="wide", initial_sidebar_state="collapsed")

# Estética Elite: Títulos blancos y acentos azul eléctrico
st.markdown("""
    <style>
    .main { background-color: #080a0f; }
    .stMetric { background-color: #111827; padding: 20px; border-radius: 12px; border: 1px solid #1f2937; }
    h1 { color: #ffffff !important; font-family: 'Inter', sans-serif; font-weight: 800; }
    h3, .stSubheader { color: #e5e7eb !important; font-family: 'Inter', sans-serif; }
    p { color: #9ca3af; }
    hr { border: 0; height: 2px; background: linear-gradient(to right, #00c3ff, #080a0f); margin-bottom: 2rem; }
    </style>
    """, unsafe_allow_html=True)

st.title("📊 Análisis Estratégico de las Big Tech")
st.markdown("---")

# Obtención automática de datos de la bolsa
tickers = ['AAPL', 'MSFT', 'GOOGL', 'AMZN']
data = yf.download(tickers, start="2024-01-01")['Adj Close']

# Cálculos de rendimiento para las tarjetas
returns = data.pct_change().dropna()
perf_summary = pd.DataFrame({
    'Rendimiento Total': (data.iloc[-1] / data.iloc[0] - 1) * 100,
    'Volatilidad (Std Dev)': returns.std() * 100
}).reset_index()

# Fila de indicadores (Métricas)
col1, col2, col3, col4 = st.columns(4)
col1.metric("Apple", f"${data['AAPL'][-1]:.2f}", f"{perf_summary.iloc[0, 1]:.2f}%")
col2.metric("Microsoft", f"${data['MSFT'][-1]:.2f}", f"{perf_summary.iloc[1, 1]:.2f}%")
col3.metric("Google", f"${data['GOOGL'][-1]:.2f}", f"{perf_summary.iloc[2, 1]:.2f}%")
col4.metric("Amazon", f"${data['AMZN'][-1]:.2f}", f"{perf_summary.iloc[3, 1]:.2f}%")

st.markdown("###")

# Gráfico de Dispersión y Análisis
col_left, col_right = st.columns([2, 1])
with col_left:
    st.subheader("Riesgo vs. Retorno (Dispersión)")
    fig_scatter = px.scatter(perf_summary, x="Volatilidad (Std Dev)", y="Rendimiento Total", 
                             text="Ticker", size="Rendimiento Total", color="Ticker", 
                             template="plotly_dark", color_discrete_sequence=px.colors.qualitative.G10)
    st.plotly_chart(fig_scatter, use_container_width=True)

with col_right:
    st.subheader("Interpretación")
    st.markdown("""
    <div style="background-color: #111827; padding: 20px; border-radius: 12px; border: 1px solid #1f2937;">
        <p>Este gráfico muestra la eficiencia de las acciones. Las que están más <b>arriba</b> rinden más, y las que están más a la <b>izquierda</b> son menos riesgosas.</p>
        <p>• <b>Hallazgo:</b> Idealmente buscamos activos en el cuadrante superior izquierdo.</p>
    </div>
    """, unsafe_allow_html=True)

# Gráfico de líneas final
st.markdown("---")
st.subheader("Evolución Histórica de Precios")
st.line_chart(data)
