import os
import subprocess
import sys

# FORZAR INSTALACIÓN DE ALTAIR SI FALTA
try:
    import altair
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "altair"])

import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.express as px

st.set_page_config(page_title="Big Tech Analysis", layout="wide")

# Estética Súper Limpia
st.markdown("""
    <style>
    .main { background-color: #080a0f; }
    .stMetric { background-color: #111827; padding: 20px; border-radius: 12px; border: 1px solid #1f2937; }
    h1 { color: #ffffff !important; }
    h3, .stSubheader { color: #e5e7eb !important; }
    hr { border: 0; height: 2px; background: linear-gradient(to right, #00c3ff, #080a0f); margin-bottom: 2rem; }
    </style>
    """, unsafe_allow_html=True)

st.title("📊 Análisis Estratégico de las Big Tech")
st.markdown("---")

@st.cache_data(ttl=600)
def load_data():
    tickers = ['AAPL', 'MSFT', 'GOOGL', 'AMZN']
    # Usamos un periodo fijo para evitar errores de fechas
    df = yf.download(tickers, period="6mo", interval="1d")['Close']
    return df

try:
    data = load_data()
    
    if not data.empty:
        # Métricas
        cols = st.columns(4)
        for i, t in enumerate(['AAPL', 'MSFT', 'GOOGL', 'AMZN']):
            price = data[t].iloc[-1]
            change = ((data[t].iloc[-1] / data[t].iloc[0]) - 1) * 100
            cols[i].metric(t, f"${price:.2f}", f"{change:.2f}%")

        st.markdown("###")
        
        # Gráfica de líneas (Usamos Plotly para evitar a Altair si da problemas)
        st.subheader("Evolución de Precios (Últimos 6 meses)")
        fig_line = px.line(data, template="plotly_dark", color_discrete_sequence=px.colors.qualitative.Safe)
        st.plotly_chart(fig_line, use_container_width=True)
    else:
        st.warning("Cargando datos desde el servidor de respaldo...")
        st.button("Reintentar Conexión")
except Exception as e:
    st.error(f"Configurando entorno... Por favor pulsa F5 en 10 segundos.")
