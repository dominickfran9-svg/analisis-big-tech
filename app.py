import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go
import plotly.express as px
from scipy.optimize import minimize
import numpy as np

# 1. CONFIGURACIÓN DEL SISTEMA
st.set_page_config(page_title="Alpha Strategic Intelligence", layout="wide", initial_sidebar_state="collapsed")

# 2. CSS: ARQUITECTURA VISUAL "EXECUTIVE DARK"
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Inter:wght@300;400;600&display=swap');
    .main { background: #010409; }
    
    .executive-brief {
        background: rgba(13, 17, 23, 0.95);
        border: 1px solid #30363d;
        border-top: 4px solid #1f6feb;
        border-radius: 12px;
        padding: 35px;
        margin-bottom: 25px;
        box-shadow: 0 15px 35px rgba(0,0,0,0.6);
    }
    
    .brief-title { font-family: 'Orbitron', sans-serif; color: #58a6ff; font-size: 1.3rem; margin-bottom: 20px; text-transform: uppercase; border-bottom: 1px solid #30363d; padding-bottom: 10px; }
    .brief-text { font-family: 'Inter', sans-serif; color: #c9d1d9; line-height: 1.9; text-align: justify; font-size: 1.05rem; }
    
    div[data-testid="stMetric"] {
        background: rgba(13, 17, 23, 0.9) !important;
        border: 1px solid #30363d !important;
        border-radius: 10px !important;
        padding: 15px !important;
    }
    
    h1, h2, h3 { font-family: 'Orbitron', sans-serif; color: #f0f6fc; }
    b { color: #58a6ff; }
    </style>
    """, unsafe_allow_html=True)

@st.cache_data(ttl=300)
def get_strategic_data():
    tickers = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'NVDA', 'META', 'TSLA']
    # Obtenemos 2 años de datos para cálculos de volatilidad más robustos
    df = yf.download(tickers, period="2y", interval="1d", progress=False)['Close']
    return df

# --- CUERPO PRINCIPAL CON BLINDAJE ---
try:
    df = get_strategic_data()
    returns = df.pct_change().dropna()
    tickers = df.columns

    st.title("🏛️ ALPHA STRATEGIC INTELLIGENCE v12")
    st.markdown("---")

    # 1. MONITOR DE ACTIVOS
    m_cols = st.columns(len(tickers))
    for i, t in enumerate(tickers):
        curr = df[t].iloc[-1]
        ytd = (curr / df[t].iloc[0] - 1) * 100
        m_cols[i].metric(t, f"${curr:.2f}", f"{ytd:.1f}% YTD")

    # 2. SISTEMA DE ANÁLISIS DE ALTO NIVEL
    tab_macro, tab_risk, tab_alpha = st.tabs(["🌎 Macro-Estrategia", "🛡️ Gestión de Riesgo Quant", "🧬 Optimización de Capital"])

    with tab_macro:
        col_m1, col_m2 = st.columns([3, 2])
        with col_m1:
            fig = go.Figure()
            for t in tickers:
                norm = (df[t] / df[t].iloc[0]) * 100
                fig.add_trace(go.Scatter(x=df.index, y=norm, name=t, line=dict(width=3, shape='spline')))
            fig.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=600)
            st.plotly_chart(fig, use_container_width=True)
        
        with col_m2:
            lider = (df.iloc[-1] / df.iloc[0]).idxmax()
            st.
