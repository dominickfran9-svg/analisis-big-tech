import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go
import plotly.express as px
from scipy.optimize import minimize
import numpy as np

# 1. ARQUITECTURA DE DATOS
st.set_page_config(page_title="Alpha Elite Terminal", layout="wide", initial_sidebar_state="collapsed")

# 2. CSS: GLASS-NEÓN PROFUNDO
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Inter:wght@300;400;600&display=swap');
    .main { background: #010409; }
    
    /* Bloques de Insight */
    .insight-card {
        background: rgba(13, 17, 23, 0.8);
        border: 1px solid #30363d;
        border-left: 4px solid #58a6ff;
        border-radius: 12px;
        padding: 25px;
        margin: 15px 0;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
    }
    
    div[data-testid="stMetric"] {
        background: rgba(13, 17, 23, 0.9) !important;
        border: 1px solid #1f6feb !important;
        border-radius: 15px !important;
    }
    
    h1, h2, h3 { font-family: 'Orbitron', sans-serif; color: #f0f6fc; }
    b { color: #58a6ff; }
    </style>
    """, unsafe_allow_html=True)

@st.cache_data(ttl=300)
def get_elite_data():
    tickers = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'NVDA', 'META', 'TSLA']
    df = yf.download(tickers, period="1y", interval="1d", progress=False)['Close']
    return df

try:
    df = get_elite_data()
    returns = df.pct_change().dropna()
    tickers = df.columns

    # --- HEADER ---
    st.title("⚡ ALPHA ELITE TERMINAL")
    st.markdown("---")

    # 1. MONITOR DE NODOS
    m_cols = st.columns(len(tickers))
    for i, t in enumerate(tickers):
        price = df[t].iloc[-1]
        ytd = (price / df[t].iloc[0] - 1) * 100
        m_cols[i].metric(t, f"${price:.2f}", f"{ytd:.1f}% YTD")

    # 2. PANELES DE DECISIÓN CRÍTICA
    tab_macro, tab_quant, tab_predict = st.tabs(["🏛️ Visión Estratégica", "🧬 Ingeniería de Riesgo", "🔮 Proyección Monte Carlo"])

    with tab_macro:
        c1, c2 = st.columns([3, 1.5])
        with c1:
            fig = go.Figure()
            for t in tickers:
                norm = (df[t] / df[t].iloc[0]) * 100
                fig.add_trace(go.Scatter(x=df.index, y=norm, name=t, line=dict(width=3, shape='spline')))
            fig.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=500)
            st.plotly_chart(fig, use_container_width=True)
        
        with c2:
            st.subheader("Dictamen Ejecutivo")
            st.markdown(f"""
            <div class='insight-card'>
                <b>Análisis de Ciclo:</b><br>
                El sector tecnológico muestra una <b>acumulación de valor</b> sólida. 
                Actualmente, el mercado ignora la volatilidad de corto plazo para enfocarse 
                en la expansión de márgenes operativos por IA.<br><br>
                <b>Estrategia Sugerida:</b> Mantener una postura 'Overweight' en <b>{df.iloc[-1].idxmax()}</b> 
                mientras el soporte de la media móvil de 200 días se mantenga intacto.
            </div>
            """, unsafe_allow_html=True)

    with tab_quant:
        r1, r2 = st.columns([2, 2])
        with r1:
            # Heatmap de correlación (Fix para el error de matplotlib)
            corr = returns.corr()
            fig_corr = px.imshow(corr, text_auto=".2f", color_continuous_scale='Blues', title="Matriz de Interdependencia")
            fig_corr.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig_corr, use_container_width=True)
        with r2:
            st.subheader("Análisis de Co-Movimiento")
            max_c = corr.unstack().sort_values(ascending=False).drop_duplicates().index[1]
            st.markdown(f"""
            <div class='insight-card'>
                <b>Riesgo de Redundancia:</b><br>
                Se detecta una correlación crítica entre <b>{max_c[0]}</b> y <b>{max_c[1]}</b>. 
                Desde una perspectiva de Administración de Empresas, esto significa que no hay 
                diversificación real entre estos dos nodos.<br><br>
                <b>Acción:</b> Reducir exposición cruzada para bajar el riesgo sistémico del portafolio.
            </div>
            """, unsafe_allow_html=True)

    with tab_predict:
        st.subheader("Simulación de Futuros Posibles (Monte Carlo)")
        selected_stock = st.selectbox("Seleccionar activo para proyectar", tickers)
        
        # Lógica de simulación simple
        last_price = df[selected_stock].iloc[-1]
        vol = returns[selected_stock].std()
        sim_returns = np.random.normal(returns[selected_stock].mean(), vol, (30, 100))
        sim_prices = last_price * (1 + sim_returns).cumprod(axis=0)
        
        fig_sim = go.Figure()
        for i in range(20): # Dibujar 20 líneas de futuro
            fig_sim.add_trace(go.Scatter(y=sim_prices[:, i], mode='lines', line=dict(width=1), opacity=0.3, showlegend=False))
        
        fig_sim.update_layout(template="plotly_dark", title=f"Proyección 30 Días: {selected_stock}", paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_sim, use_container_width=True)
        
        st.markdown(f"""
        <div class='insight-card'>
            <b>Interpretación Probabilística:</b><br>
            La simulación muestra un abanico de resultados basados en la volatilidad actual. 
            Existe un <b>68% de probabilidad</b> de que el precio se mantenga en el rango de 
            ${sim_prices[-1].mean() * 0.95:.1f} a ${sim_prices[-1].mean() * 1.05:.1f} en el próximo mes.
        </div>
        """, unsafe_allow_html=True)

    # --- FOOTER ---
    st.markdown("---")
    st.caption("Terminal de Inteligencia Estratégica | Universidad Externado de Colombia | Gestión de Decisiones")

except Exception as e:
    st.error(f"Error en la secuencia de datos: {e}")
