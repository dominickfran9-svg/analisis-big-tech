import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go
import plotly.express as px
from scipy.optimize import minimize
import numpy as np

# 1. CONFIGURACIÓN DEL SISTEMA GERENCIAL
st.set_page_config(page_title="Terminal Gerencial Big Tech", layout="wide", initial_sidebar_state="collapsed")

# 2. CSS DINÁMICO: ESTÉTICA SOBERIA Y ELEGANTE (MADERA, NEGRO, AZUL)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Inter:wght@300;400;600&display=swap');
    
    .info-panel {
        background: rgba(128, 128, 128, 0.08); 
        border: 1px solid rgba(128, 128, 128, 0.2);
        border-radius: 12px;
        padding: 35px;
        margin-bottom: 25px;
        min-height: 500px;
    }
    
    .panel-header {
        font-family: 'Orbitron', sans-serif;
        color: #58a6ff;
        font-size: 1.25rem;
        border-bottom: 2px solid #58a6ff;
        padding-bottom: 12px;
        margin-bottom: 20px;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .panel-body {
        font-family: 'Inter', sans-serif;
        line-height: 1.9;
        text-align: justify;
        font-size: 1.05rem;
    }

    .formula-box {
        background: rgba(0, 0, 0, 0.1);
        padding: 20px;
        border-radius: 10px;
        font-family: 'Courier New', monospace;
        color: #2ea043;
        margin: 20px 0;
        border-left: 5px solid #58a6ff;
    }

    div[data-testid="stMetric"] {
        background: rgba(128, 128, 128, 0.05) !important;
        border: 1px solid rgba(128, 128, 128, 0.2) !important;
        border-radius: 10px !important;
        padding: 20px !important;
    }
    </style>
    """, unsafe_allow_html=True)

@st.cache_data(ttl=600)
def load_market_data():
    tickers = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'NVDA', 'META', 'TSLA']
    data = yf.download(tickers, period="2y", interval="1d", progress=False)['Close']
    return data

try:
    df = load_market_data()
    returns = df.pct_change().dropna()
    tickers = sorted(df.columns)

    # --- TÍTULO SOLICITADO ---
    st.title("🏛️ ANÁLISIS ESTRATÉGICO DE ACCIONES BIG TECH")
    st.markdown("---")

    # KPIs SUPERIORES
    m_cols = st.columns(len(tickers))
    for i, t in enumerate(tickers):
        actual = df[t].iloc[-1]
        ytd = (actual / df[t].iloc[0] - 1) * 100
        m_cols[i].metric(t, f"${actual:.2f}", f"{ytd:.1f}% YTD")

    tabs = st.tabs(["🌎 Desempeño & Ciclos", "🛡️ Matriz de Riesgo", "📈 Optimización de Markowitz", "💰 Calculadora de Capital"])

    with tabs[0]:
        c1, c2, c3 = st.columns([3, 2, 2])
        with c1:
            norm = (df / df.iloc[0]) * 100
            st.plotly_chart(px.line(norm, height=550), use_container_width=True)
        with c2:
            st.markdown("""<div class='info-panel'><div class='panel-header'>🔬 Metodología de Normalización</div>
