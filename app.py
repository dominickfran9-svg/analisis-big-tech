import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go

# 1. CONFIGURACIÓN DE PÁGINA ELITE
st.set_page_config(page_title="Quantum Tech Terminal", layout="wide", initial_sidebar_state="collapsed")

# 2. CSS DINÁMICO (Corrección de Sintaxis y Animaciones)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Inter:wght@300;600&display=swap');
    
    .main { background: #020617; }

    /* Animación de barrido láser (Scanner) */
    @keyframes scanLine {
        0% { top: 0%; opacity: 0; }
        50% { opacity: 0.5; }
        100% { top: 100%; opacity: 0; }
    }

    /* Línea de escaneo dinámica */
    .stApp::before {
        content: "";
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 4px;
        background: linear-gradient(to right, transparent, #38bdf8, transparent);
        box-shadow: 0 0 15px #38bdf8;
        z-index: 9999;
        animation: scanLine 6s linear infinite;
        pointer-events: none;
    }

    /* Tarjetas Flotantes con Glow */
    div[data-testid="stMetric"] {
        background: rgba(15, 23, 42, 0.6) !important;
        border: 1px solid rgba(56, 189, 248, 0.2) !important;
        backdrop-filter: blur(10px) !important;
        border-radius: 15px !important;
        padding: 20px !important;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1) !important;
    }

    div[data-testid="stMetric"]:hover {
        transform: translateY(-8px) !important;
        border-color: #38bdf8 !important;
        box-shadow: 0 0 25px rgba(56, 189, 248, 0.4) !important;
    }

    h1 {
        font-family: 'Orbitron', sans-serif;
        color: #f8fafc;
        text-align: center;
        letter-spacing: 5px;
        text-shadow: 0 0 10px rgba(56, 189, 248, 0.5);
    }
    </style>
    """, unsafe_allow_html=True)

st.title("⚡ QUANTUM_CORE_v2")

# 3. EXTRACCIÓN DE DATOS
@st.cache_data(ttl=600)
def get_live_data():
    tickers = ['AAPL', 'MSFT', 'GOOGL', 'AMZN']
    data = yf.download(tickers, period="1mo", interval="1d", progress=False)['Close']
    return data

try:
    df = get_live_data()
    
    if not df.empty:
        # Fila de métricas
        cols = st.columns(4)
        ts = ['AAPL', 'MSFT', 'GOOGL', 'AMZN']
        for i, t in enumerate(ts):
            current = df[t].iloc[-1]
            prev = df[t].iloc[0]
            change = ((current / prev) - 1) * 100
            cols[i].metric(label=f"NODE_{t}", value=f"${current:.2f}", delta=f"{change:.2f}%")

        st.markdown("###")

        # 4. GRÁFICO DINÁMICO (Spline Animado)
        fig = go.Figure()
        colors = ['#38bdf8', '#818cf8', '#c084fc', '#fb7185']
        
        for i, t in enumerate(ts):
            fig.add_trace(go.Scatter(
                x=df.index, y=df[t], name=t,
                mode='lines',
                line=dict(color=colors[i], width=3, shape='spline'),
                fill='tonexty',
                fillcolor=f'rgba({56+i*20}, 189, 248, 0.02)'
            ))

        fig.update_layout(
            hovermode="x unified",
            template="plotly_dark",
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=0, r=0, t=20, b=0),
            height=550,
            xaxis=dict(showgrid=False),
            yaxis=dict(gridcolor='rgba(255,255,255,0.05)', side="right")
        )
        
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("<div style='text-align: center; color: #38bdf8; opacity: 0.5; font-family: monospace;'>[ ENCRYPTION_STABLE // DOMINICK_VP ]</div>", unsafe_allow_html=True)

except Exception as e:
    st.error(f"Error de conexión: {e}")
