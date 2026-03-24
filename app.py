import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go
import plotly.express as px
from scipy.optimize import minimize
import numpy as np

# 1. CONFIGURACIÓN DE NÚCLEO
st.set_page_config(page_title="Alpha Quantum Terminal", layout="wide", initial_sidebar_state="collapsed")

# 2. CSS: ARQUITECTURA VISUAL "DEEP DARK"
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=JetBrains+Mono:wght@300;500&display=swap');
    
    .main { background: #010409; }
    
    /* Tarjetas con Efecto de Profundidad y Borde de Neón Reactivo */
    div[data-testid="stMetric"] {
        background: linear-gradient(145deg, #0d1117, #161b22) !important;
        border: 1px solid #30363d !important;
        border-radius: 16px !important;
        padding: 24px !important;
        transition: all 0.5s cubic-bezier(0.4, 0, 0.2, 1) !important;
        box-shadow: 10px 10px 20px #010409, -5px -5px 15px #161b22 !important;
    }

    div[data-testid="stMetric"]:hover {
        transform: translateY(-10px) scale(1.03) !important;
        border-color: #58a6ff !important;
        box-shadow: 0 0 25px rgba(88, 166, 255, 0.2) !important;
    }

    h1, h2, h3 { font-family: 'Orbitron', sans-serif; color: #f0f6fc; letter-spacing: 3px; }
    .stTabs [data-baseweb="tab-list"] { gap: 15px; }
    .stTabs [data-baseweb="tab"] { 
        background: #0d1117; border-radius: 10px; border: 1px solid #30363d; padding: 10px 25px;
    }
    .stTabs [aria-selected="true"] { background: #1f6feb !important; border-color: #58a6ff !important; }
    </style>
    """, unsafe_allow_html=True)

@st.cache_data(ttl=300)
def get_advanced_data():
    tickers = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'NVDA', 'META', 'TSLA']
    df = yf.download(tickers, period="1y", interval="1d", progress=False)['Close']
    return df

try:
    data = get_advanced_data()
    returns = data.pct_change().dropna()
    tickers = data.columns
    
    # --- HEADER ESTRATÉGICO ---
    c1, c2, c3 = st.columns([3, 1, 1])
    c1.title("💹 QUANTUM HUB v6")
    volatilidad_global = returns.std().mean() * 100 * np.sqrt(252)
    c2.metric("MARKET VOL (VIX)", f"{volatilidad_global:.2f}%", "-1.2%")
    c3.metric("NODES ACTIVE", "7/7", "STABLE")

    st.markdown("---")

    # 1. PANEL DE MÉTRICAS AVANZADAS
    m_cols = st.columns(len(tickers))
    for i, tick in enumerate(tickers):
        curr = data[tick].iloc[-1]
        ytd_ret = (curr / data[tick].iloc[0] - 1) * 100
        m_cols[i].metric(label=tick, value=f"${curr:.1f}", delta=f"{ytd_ret:.1f}% YTD")

    st.markdown("<br>", unsafe_allow_html=True)

    # 2. PANELES DE ALTA INTELIGENCIA
    tab_vis, tab_risk, tab_alpha = st.tabs(["🚀 Gráfico de Precisión", "⚖️ Análisis de Riesgo", "🤖 Optimizador Alpha"])

    with tab_vis:
        col_v1, col_v2 = st.columns([4, 1])
        with col_v1:
            # Gráfico con área sombreada y curvas spline mejoradas
            fig = go.Figure()
            for i, t in enumerate(tickers):
                norm = (data[t] / data[t].iloc[0]) * 100
                fig.add_trace(go.Scatter(
                    x=data.index, y=norm, name=t, mode='lines',
                    line=dict(width=4, shape='spline'),
                    fill='tonexty', fillcolor='rgba(88, 166, 255, 0.01)'
                ))
            fig.update_layout(
                hovermode="x unified", template="plotly_dark", height=550,
                paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                xaxis=dict(showgrid=False), yaxis=dict(side="right", gridcolor='rgba(255,255,255,0.05)')
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col_v2:
            st.subheader("Leaderboard")
            # Ranking de rendimiento real
            ranking = ((data.iloc[-1] / data.iloc[0] - 1) * 100).sort_values(ascending=False)
            for rank, (name, val) in enumerate(ranking.items()):
                st.write(f"#{rank+1} **{name}**: {val:.1f}%")

    with tab_risk:
        col_r1, col_r2 = st.columns(2)
        with col_r1:
            st.subheader("Mapa de Correlación")
            corr = returns.corr()
            fig_corr = px.imshow(corr, text_auto=".2f", color_continuous_scale='Blues')
            fig_corr.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig_corr, use_container_width=True)
        with col_r2:
            st.subheader("Distribución de Retornos")
            fig_dist = go.Figure()
            for t in tickers[:3]: # Solo top 3 para no saturar
                fig_dist.add_trace(go.Histogram(x=returns[t], name=t, opacity=0.6))
            fig_dist.update_layout(barmode='overlay', template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig_dist, use_container_width=True)

    with tab_alpha:
        # Optimizador de Markowitz para Administración de Empresas
        st.subheader("Simulación de Cartera Eficiente")
        cash = st.number_input("Inversión Total (USD)", value=10000, step=1000)
        
        def obj_func(w):
            return np.sqrt(np.dot(w.T, np.dot(returns.cov()*252, w))) # Minimizar Volatilidad

        res = minimize(obj_func, len(tickers)*[1./len(tickers)], 
                       bounds=tuple((0,1) for _ in range(len(tickers))), 
                       constraints={'type':'eq','fun': lambda x: np.sum(x)-1})
        
        res_cols = st.columns(len(tickers))
        for i, t in enumerate(tickers):
            peso = res.x[i]
            res_cols[i].metric(t, f"{peso*100:.1f}%", f"${cash*peso:,.0f}")

    # --- FOOTER ---
    st.markdown("---")
    st.caption("Terminal de Análisis Estratégico | Universidad Externado de Colombia | Business Admin Edition")

except Exception as e:
    st.error(f"Error de sincronización con el mercado: {e}")
