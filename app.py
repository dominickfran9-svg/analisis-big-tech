import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.express as px

st.set_page_config(page_title="Big Tech Analysis", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    .main { background-color: #080a0f; }
    .stMetric { background-color: #111827; padding: 20px; border-radius: 12px; border: 1px solid #1f2937; }
    h1 { color: #ffffff !important; font-family: 'Inter', sans-serif; font-weight: 800; }
    h3, .stSubheader { color: #e5e7eb !important; }
    p { color: #9ca3af; }
    hr { border: 0; height: 2px; background: linear-gradient(to right, #00c3ff, #080a0f); margin-bottom: 2rem; }
    </style>
    """, unsafe_allow_html=True)

st.title("📊 Análisis Estratégico de las Big Tech")
st.markdown("---")

# Usamos un rango de fechas más amplio y seguro
tickers = ['AAPL', 'MSFT', 'GOOGL', 'AMZN']
data = yf.download(tickers, start="2024-01-01")['Adj Close']

if not data.empty and len(data) > 1:
    # Cálculos con protección de datos
    returns = data.pct_change().dropna()
    
    perf_summary = pd.DataFrame({
        'Rendimiento Total': (data.iloc[-1] / data.iloc[0] - 1) * 100,
        'Volatilidad (Std Dev)': returns.std() * 100
    }).reset_index()

    col1, col2, col3, col4 = st.columns(4)
    for i, ticker in enumerate(tickers):
        with [col1, col2, col3, col4][i]:
            val = data[ticker].iloc[-1]
            change = perf_summary.loc[perf_summary['index'] == ticker, 'Rendimiento Total'].values[0]
            st.metric(ticker, f"${val:.2f}", f"{change:.2f}%")

    st.markdown("###")

    col_left, col_right = st.columns([2, 1])
    with col_left:
        st.subheader("Riesgo vs. Retorno")
        fig_scatter = px.scatter(perf_summary, x="Volatilidad (Std Dev)", y="Rendimiento Total", 
                                 text="index", size="Rendimiento Total", color="index", 
                                 template="plotly_dark")
        st.plotly_chart(fig_scatter, use_container_width=True)

    with col_right:
        st.subheader("Interpretación")
        st.info("Este modelo evalúa el desempeño del 2024 a la fecha. Apple y Microsoft suelen mostrar la mayor estabilidad.")

    st.markdown("---")
    st.subheader("Evolución del Mercado")
    st.line_chart(data)
else:
    st.error("Esperando conexión con Yahoo Finance... Intenta recargar en un momento.")
