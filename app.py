import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go
import numpy as np

# Configuración de Terminal de Grado Profesional
st.set_page_config(page_title="Quantum Trading Terminal", layout="wide", initial_sidebar_state="collapsed")

# CSS: Interfaz de Trading de Alta Gama
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Inter:wght@300;400;600&display=swap');
    
    .main { background: #010409; }
    
    /* Efecto Scanner de Fondo */
    .stApp::before {
        content: ""; position: fixed; top: 0; left: 0; width: 100%; height: 2px;
        background: rgba(56, 189, 248, 0.3); box-shadow: 0 0 20px #38bdf8;
        z-index: 9999; animation: scan 10s linear infinite; pointer-events: none;
    }
    @keyframes scan { 0% { top: -10%; } 100% { top: 110%; } }

    /* Tarjetas de Acción Estilo Glassmorphism */
    div[data-testid="stMetric"] {
        background: rgba(13, 17, 23, 0.8) !important;
        border: 1px solid #30363d !important;
        border-radius: 12px !important;
        padding: 15px !important;
        transition: 0.3s;
    }
    div[data-testid="stMetric"]:hover {
        border-color: #58a6ff !important;
        box-shadow: 0 0 20px rgba(88, 166, 255, 0.2) !important;
    }

    h1, h2, h3 { font-family: 'Orbitron', sans-serif; color: #f0f6fc; }
    .stTabs [data-baseweb="tab-list"] { gap: 10px; }
    .stTabs [data-baseweb="tab"] { 
        background: #0d1117; border: 1px solid #30363d; 
        border-radius: 8px 8px 0 0; color: #8b949e; padding: 10px 20px;
    }
    .stTabs [aria-selected="true"] { background: #1f6feb !important; color: white !important; }
    </style>
    """, unsafe_allow_html=True)

# Lógica de Datos
@st.cache_data(ttl=300)
def get_trading_data():
    tickers = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'NVDA', 'TSLA']
    df = yf.download(tickers, period="6mo", interval="1d", progress=False)['Close']
    return df

try:
    data = get_trading_data()
    
    # --- HEADER ---
    c1, c2 = st.columns([3, 1])
    with c1:
        st.title("📡 QUANTUM TRADING HUB")
    with c2:
        st.markdown("<br>", unsafe_allow_html=True)
        st.status("MERCADO ABIERTO", state="running")

    # --- MÉTRICAS EN TIEMPO REAL ---
    st.markdown("### Market Overview")
    cols = st.columns(len(data.columns))
    for i, ticker in enumerate(data.columns):
        price = data[ticker].iloc[-1]
        change = (price / data[ticker].iloc[-2] - 1) * 100
        cols[i].metric(ticker, f"${price:.2f}", f"{change:.2f}%")

    st.markdown("---")

    # --- ZONA DE ANÁLISIS ---
    tab_chart, tab_comp, tab_signals = st.tabs(["🎯 Gráfico de Precisión", "⚖️ Comparador Beta", "🤖 Señales IA"])

    with tab_chart:
        selected_stock = st.selectbox("Seleccionar Activo Principal", data.columns)
        fig = go.Figure()
        
        # Línea de la acción seleccionada con efecto Neón
        fig.add_trace(go.Scatter(
            x=data.index, y=data[selected_stock],
            name=selected_stock,
            line=dict(color='#58a6ff', width=4),
            fill='toself', fillcolor='rgba(88, 166, 255, 0.05)'
        ))
        
        # Medias móviles para toque profesional
        ma20 = data[selected_stock].rolling(20).mean()
        fig.add_trace(go.Scatter(x=data.index, y=ma20, name="MA20", line=dict(dash='dot', color='#30363d')))

        fig.update_layout(
            hovermode="x unified", template="plotly_dark",
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            height=500, xaxis=dict(showgrid=False), yaxis=dict(side="right")
        )
        st.plotly_chart(fig, use_container_width=True)

    with tab_comp:
        st.subheader("Rendimiento Acumulado")
        # Normalización a base 100
        norm_df = (data / data.iloc[0]) * 100
        fig_comp = go.Figure()
        for col in norm_df.columns:
            fig_comp.add_trace(go.Scatter(x=norm_df.index, y=norm_df[col], name=col, line=dict(width=2)))
        
        fig_comp.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_comp, use_container_width=True)

    with tab_signals:
        st.subheader("Análisis Técnico Algorítmico")
        rec_cols = st.columns(3)
        
        # Lógica simple de recomendación (RSI Simplificado)
        for i, ticker in enumerate(data.columns[:3]): # Ejemplo con las primeras 3
            current = data[ticker].iloc[-1]
            avg = data[ticker].mean()
            
            with rec_cols[i]:
                if current < avg * 0.95:
                    st.success(f"**{ticker}: COMPRA**")
                    st.caption("Activo subvalorado respecto al promedio mensual.")
                elif current > avg * 1.05:
                    st.error(f"**{ticker}: VENTA**")
                    st.caption("Posible sobrecompra detectada.")
                else:
                    st.warning(f"**{ticker}: NEUTRAL**")
                    st.caption("Consolidación de precio en curso.")

    # --- SIMULADOR DE INVERSIÓN (PIE DE PÁGINA) ---
    st.markdown("---")
    with st.expander("🧮 Calculadora de Retorno Proyectado"):
        inv_col1, inv_col2 = st.columns(2)
        monto = inv_col1.number_input("Monto a invertir (USD)", value=1000)
        stock_sim = inv_col2.selectbox("En la acción:", data.columns, key="sim")
        
        retorno_total = (data[stock_sim].iloc[-1] / data[stock_sim].iloc[0] - 1)
        ganancia = monto * retorno_total
        st.write(f"Si hubieras invertido **${monto}** hace 6 meses en **{stock_sim}**, hoy tendrías **${monto + ganancia:.2f}**.")

except Exception as e:
    st.error(f"Error de conexión con la red de trading: {e}")
