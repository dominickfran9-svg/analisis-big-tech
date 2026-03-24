import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go
from scipy.optimize import minimize
import numpy as np

# Configuración Pro
st.set_page_config(page_title="Alpha Trading Terminal", layout="wide", initial_sidebar_state="collapsed")

# CSS: Estética de Terminal de Inversión (Sin Scanner)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Inter:wght@300;400;600&display=swap');
    
    .main { background: #010409; }
    
    /* Tarjetas de Métricas con Glow Suave */
    div[data-testid="stMetric"] {
        background: rgba(13, 17, 23, 0.8) !important;
        border: 1px solid #30363d !important;
        border-radius: 12px !important;
        padding: 15px !important;
        transition: 0.3s;
    }
    div[data-testid="stMetric"]:hover {
        border-color: #58a6ff !important;
        box-shadow: 0 0 20px rgba(88, 166, 255, 0.1) !important;
    }

    h1, h2, h3 { font-family: 'Orbitron', sans-serif; color: #f0f6fc; }
    
    .news-box {
        background: rgba(22, 27, 34, 0.5);
        border-left: 5px solid;
        border-radius: 5px;
        padding: 12px;
        margin-bottom: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

@st.cache_data(ttl=300)
def get_terminal_data():
    tickers = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'NVDA', 'META', 'TSLA']
    df = yf.download(tickers, period="1y", interval="1d", progress=False)['Close']
    return df

try:
    data = get_terminal_data()
    returns = data.pct_change().dropna()
    tickers = data.columns
    
    st.title("💹 ALPHA TRADING HUB")
    st.markdown("---")

    # 1. LIVE NODE CONNECTION (Métricas)
    m_cols = st.columns(len(tickers))
    for i, tick in enumerate(tickers):
        val = data[tick].iloc[-1]
        delta = (val / data[tick].iloc[-2] - 1) * 100
        m_cols[i].metric(tick, f"${val:.1f}", f"{delta:.2f}%")

    # 2. PESTAÑAS FUNCIONALES
    tab_chart, tab_opt, tab_news = st.tabs(["🎯 Gráfico Neón", "🧬 Optimización IA", "📰 Inteligencia"])

    with tab_chart:
        selected = st.multiselect("Activos a visualizar", tickers, default=['AAPL', 'NVDA'])
        
        fig = go.Figure()
        colors = ['#58a6ff', '#3fb950', '#d29922', '#f85149', '#bc8cff', '#1f6feb', '#aff5b4']
        
        for i, t in enumerate(selected):
            # Normalización a base 100 para que la comparativa sea justa
            norm = (data[t] / data[t].iloc[0]) * 100
            fig.add_trace(go.Scatter(
                x=data.index, y=norm, name=t,
                mode='lines',
                line=dict(color=colors[i % len(colors)], width=3, shape='spline'),
                fill='toself', fillcolor=f'rgba({i*30}, 150, 255, 0.02)', # Glow sutil bajo la línea
                hovertemplate="<b>%{x}</b><br>Retorno: %{y:.2f}%<extra></extra>"
            ))

        fig.update_layout(
            hovermode="x unified", template="plotly_dark",
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            height=500, xaxis=dict(showgrid=False),
            yaxis=dict(title="Crecimiento Relativo (%)", side="right", gridcolor='rgba(255,255,255,0.05)')
        )
        st.plotly_chart(fig, use_container_width=True)

    with tab_opt:
        col_o1, col_o2 = st.columns([2, 1])
        with col_o1:
            cash = st.number_input("Capital total (USD)", value=5000)
            def min_v(w): return np.sqrt(np.dot(w.T, np.dot(returns.cov()*252, w)))
            res = minimize(min_v, len(tickers)*[1./len(tickers)], bounds=tuple((0,1) for _ in range(len(tickers))), constraints={'type':'eq','fun':lambda x: np.sum(x)-1})
            
            fig_bar = go.Figure(go.Bar(x=tickers, y=res.x, marker_color='#58a6ff'))
            fig_bar.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=350)
            st.plotly_chart(fig_bar, use_container_width=True)
        with col_o2:
            st.markdown("<br><br>", unsafe_allow_html=True)
            st.info("**Distribución Recomendada:**")
            for i, t in enumerate(tickers):
                if res.x[i] > 0.01: # Solo mostrar si la inversión es relevante
                    st.write(f"• **{t}**: ${cash * res.x[i]:,.2f}")

    with tab_news:
        noticias = [
            ("NVDA", "Dominio absoluto en chips de IA impulsa el sector.", "ALCISTA"),
            ("TSLA", "Presión en márgenes por competencia asiática.", "BAJISTA"),
            ("GOOGL", "Nuevas funciones de búsqueda con IA generan confianza.", "ALCISTA")
        ]
        for stock, txt, sent in noticias:
            color = "#3fb950" if sent == "ALCISTA" else "#f85149"
            st.markdown(f"<div class='news-box' style='border-color:{color};'><strong>[{stock}]</strong>: {txt}</div>", unsafe_allow_html=True)

except Exception as e:
    st.error(f"Error de red: {e}")
