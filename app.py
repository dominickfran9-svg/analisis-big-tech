import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Big Tech Quantum Analysis", layout="wide", initial_sidebar_state="collapsed")

# CSS de Nivel Profesional con Animaciones de Keyframes
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Inter:wght@300;600&display=swap');
    
    .main {
        background: radial-gradient(circle at 50% 50%, #0f172a 0%, #020617 100%);
    }

    /* Animación de entrada suave */
    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }

    .stApp {
        animation: fadeInUp 0.8s ease-out;
    }

    /* Tarjetas estilo "Cyberpunk Glass" */
    div[data-testid="stMetric"] {
        background: rgba(30, 41, 59, 0.4) !important;
        border: 1px solid rgba(56, 189, 248, 0.2) !important;
        backdrop-filter: blur(12px) !important;
        padding: 20px !important;
        border-radius: 20px !important;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275) !important;
        position: relative;
        overflow: hidden;
    }

    div[data-testid="stMetric"]:hover {
        transform: scale(1.05) !important;
        border-color: #38bdf8 !important;
        box-shadow: 0 0 25px rgba(56, 189, 248, 0.4) !important;
        background: rgba(30, 41, 59, 0.6) !important;
    }

    /* Estilo para el título */
    h1 {
        font-family: 'Orbitron', sans-serif;
        background: linear-gradient(90deg, #fff, #38bdf8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3rem !important;
        text-transform: uppercase;
        letter-spacing: 2px;
    }

    /* Ocultar barra de Streamlit para más limpieza */
    header {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

st.title("⚡ Quantum Tech Metrics")
st.markdown("<p style='color: #7dd3fc; opacity: 0.8;'>Análisis algorítmico de activos de alto rendimiento</p>", unsafe_allow_html=True)

@st.cache_data(ttl=600)
def get_elite_data():
    tickers = ['AAPL', 'MSFT', 'GOOGL', 'AMZN']
    df = yf.download(tickers, period="1mo", interval="1d", progress=False)['Close']
    return df

try:
    df = get_elite_data()
    
    if not df.empty:
        # Fila de métricas con diseño mejorado
        m1, m2, m3, m4 = st.columns(4)
        ts = ['AAPL', 'MSFT', 'GOOGL', 'AMZN']
        slots = [m1, m2, m3, m4]
        
        for i, t in enumerate(ts):
            price = df[t].iloc[-1]
            diff = ((df[t].iloc[-1] / df[t].iloc[0]) - 1) * 100
            slots[i].metric(label=f"NODE: {t}", value=f"${price:.2f}", delta=f"{diff:.2f}%")

        st.markdown("<br>", unsafe_allow_html=True)

        # Gráfico de Área con Diseño de "Holograma"
        fig = go.Figure()

        colors = ['#38bdf8', '#818cf8', '#c084fc', '#fb7185']
        for i, t in enumerate(ts):
            fig.add_trace(go.Scatter(
                x=df.index, y=df[t],
                name=t,
                fill='toself',
                fillcolor=f'rgba({int(i*40)}, 189, 248, 0.05)',
                line=dict(color=colors[i], width=3),
                mode='lines',
                hovertemplate="<b>%{x}</b><br>Price: $%{y:.2f}<extra></extra>"
            ))

        fig.update_layout(
            hovermode="x unified",
            template="plotly_dark",
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(showgrid=False, color="#94a3b8"),
            yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.05)', side="right"),
            legend=dict(orientation="h", y=1.1, x=0.5, xanchor="center"),
            height=500
        )
        
        st.plotly_chart(fig, use_container_width=True)

        # Panel Inferior de Inteligencia
        c1, c2, c3 = st.columns([1,2,1])
        with c2:
            st.markdown("""
                <div style='text-align: center; padding: 20px; border-radius: 10px; border: 1px dashed #38bdf8;'>
                    <span style='color: #38bdf8;'>●</span> SISTEMA ACTIVO <span style='color: #38bdf8; margin-left: 20px;'>●</span> DATOS ENCRIPTADOS <span style='color: #38bdf8; margin-left: 20px;'>●</span> MERCADO ABIERTO
                </div>
            """, unsafe_allow_html=True)

except Exception:
    st.error("Error en el flujo de datos cuánticos.")
