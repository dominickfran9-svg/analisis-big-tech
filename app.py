import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go
from scipy.optimize import minimize
import numpy as np

# Configuración Limpia (Sin Scanner)
st.set_page_config(page_title="Alpha Trading Terminal", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=JetBrains+Mono:wght@300;500&display=swap');
    .main { background: #0d1117; }
    div[data-testid="stMetric"] {
        background: rgba(22, 27, 34, 0.7) !important;
        border: 1px solid #30363d !important;
        border-radius: 12px !important;
        padding: 15px !important;
    }
    h1, h2, h3 { font-family: 'Orbitron', sans-serif; color: #58a6ff; }
    .news-box {
        background: rgba(22, 27, 34, 0.5);
        border-left: 5px solid;
        border-radius: 5px;
        padding: 10px;
        margin-bottom: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

@st.cache_data(ttl=300)
def get_terminal_data():
    tickers = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'NVDA', 'META', 'TSLA']
    df = yf.download(tickers, period="2y", interval="1d", progress=False)['Close']
    return df

try:
    data = get_terminal_data()
    returns = data.pct_change().dropna()
    tickers = data.columns
    
    st.title("💹 ALPHA TRADING TERMINAL v5.1")
    
    # 1. MÉTRICAS SUPERIORES
    m_cols = st.columns(len(tickers))
    for i, tick in enumerate(tickers):
        val = data[tick].iloc[-1]
        delta = (val / data[tick].iloc[-2] - 1) * 100
        m_cols[i].metric(tick, f"${val:.1f}", f"{delta:.2f}%")

    # 2. PANELES DE INTELIGENCIA
    tab_opt, tab_news = st.tabs(["🧬 Optimización de Portafolio", "📰 Inteligencia de Mercado"])

    with tab_opt:
        col1, col2 = st.columns([2, 1])
        with col1:
            cash = st.number_input("Capital a Optimizar (USD)", value=10000)
            
            def min_vol(weights):
                return np.sqrt(np.dot(weights.T, np.dot(returns.cov() * 252, weights)))

            num_t = len(tickers)
            res = minimize(min_vol, num_t*[1./num_t], bounds=tuple((0,1) for _ in range(num_t)), constraints={'type':'eq','fun': lambda x: np.sum(x)-1})
            
            fig = go.Figure(go.Bar(x=tickers, y=res.x, marker_color='#38bdf8'))
            fig.update_layout(template="plotly_dark", title="Distribución de Riesgo Mínimo", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("<br><br>", unsafe_allow_html=True)
            for i, t in enumerate(tickers):
                st.write(f"• **{t}**: ${cash * res.x[i]:,.2f}")

    with tab_news:
        n_col1, n_col2 = st.columns([1, 2])
        with n_col1:
            st.subheader("Análisis de Sentimiento")
            st.write("Estado Global: **ALCISTA**")
            st.progress(75) # Nivel de confianza
        
        with n_col2:
            noticias = [
                ("NVDA", "Demanda de IA impulsa proyecciones.", "ALCISTA"),
                ("TSLA", "Nuevas regulaciones impactan margen neto.", "BAJISTA"),
                ("META", "Lanzamiento de Llama 4 genera optimismo.", "ALCISTA")
            ]
            for stock, txt, sent in noticias: # AQUÍ ESTÁ EL FIX: "in" en lugar de "en"
                color = "#2ea44f" if sent == "ALCISTA" else "#cb2431"
                st.markdown(f"<div class='news-box' style='border-color:{color};'><strong>[{stock}]</strong>: {txt}</div>", unsafe_allow_html=True)

except Exception as e:
    st.error(f"Error de sincronización: {e}")
