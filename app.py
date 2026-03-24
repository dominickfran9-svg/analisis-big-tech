import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go
import numpy as np

# 1. SETUP DE LA TERMINAL
st.set_page_config(page_title="Quantum Tech Terminal", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Inter:wght@300;600&display=swap');
    
    .main { background: #020617; }
    
    /* Animación de escaneo láser */
    .stApp::before {
        content: ""; position: fixed; top: 0; left: 0; width: 100%; height: 2px;
        background: rgba(56, 189, 248, 0.4); box-shadow: 0 0 15px #38bdf8;
        z-index: 9999; animation: scan 8s linear infinite; pointer-events: none;
    }
    @keyframes scan { 0% { top: 0%; } 100% { top: 100%; } }

    /* Tarjetas con efecto Glow de profundidad */
    div[data-testid="stMetric"] {
        background: rgba(15, 23, 42, 0.7) !important;
        border: 1px solid rgba(56, 189, 248, 0.2) !important;
        backdrop-filter: blur(12px) !important;
        border-radius: 15px !important;
        padding: 20px !important;
        transition: all 0.4s ease;
    }
    div[data-testid="stMetric"]:hover {
        transform: translateY(-5px);
        border-color: #38bdf8 !important;
        box-shadow: 0 0 30px rgba(56, 189, 248, 0.3) !important;
    }

    h1, h2, h3 { font-family: 'Orbitron', sans-serif; color: #f8fafc; text-transform: uppercase; }
    .stTabs [data-baseweb="tab-list"] { gap: 20px; }
    .stTabs [data-baseweb="tab"] { background: rgba(30, 41, 59, 0.5); border-radius: 10px; padding: 10px 20px; color: #94a3b8; }
    .stTabs [aria-selected="true"] { background: #38bdf8 !important; color: white !important; }
    </style>
    """, unsafe_allow_html=True)

st.title("⚡ QUANTUM ANALYSIS TERMINAL")

@st.cache_data(ttl=600)
def fetch_full_data():
    tickers = ['AAPL', 'MSFT', 'GOOGL', 'AMZN']
    df = yf.download(tickers, period="3mo", interval="1d", progress=False)['Close']
    return df

try:
    df = fetch_full_data()
    
    if not df.empty:
        # --- SECCIÓN 1: MÉTRICAS EN VIVO ---
        m1, m2, m3, m4 = st.columns(4)
        ts = ['AAPL', 'MSFT', 'GOOGL', 'AMZN']
        slots = [m1, m2, m3, m4]
        for i, t in enumerate(ts):
            curr = df[t].iloc[-1]
            change = (curr / df[t].iloc[0] - 1) * 100
            slots[i].metric(t, f"${curr:.2f}", f"{change:.2f}%")

        st.markdown("###")

        # --- SECCIÓN 2: TABS FUNCIONALES ---
        tab1, tab2, tab3 = st.tabs(["📊 Gráfico Neón", "⚖️ Comparativa", "📉 Análisis de Riesgo"])

        with tab1:
            # Gráfico con brillo dinámico al pasar el mouse
            fig = go.Figure()
            colors = ['#38bdf8', '#818cf8', '#c084fc', '#fb7185']
            
            for i, t in enumerate(ts):
                # Normalizamos a base 100 para comparar crecimiento real
                norm_price = (df[t] / df[t].iloc[0]) * 100
                fig.add_trace(go.Scatter(
                    x=df.index, y=norm_price, name=t,
                    mode='lines',
                    line=dict(color=colors[i], width=3, shape='spline'),
                    hovertemplate="<b>%{x}</b><br>Retorno: %{y:.2f}%<extra></extra>",
                    # El brillo se intensifica en el hover nativamente con Plotly Dark
                ))

            fig.update_layout(
                hovermode="x unified", template="plotly_dark",
                paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                height=500, xaxis=dict(showgrid=False),
                yaxis=dict(title="Crecimiento Relativo (%)", gridcolor='rgba(255,255,255,0.05)', side="right")
            )
            st.plotly_chart(fig, use_container_width=True)

        with tab2:
            st.subheader("Cuadro Comparativo de Rendimiento")
            # Tabla de datos técnicos para administración
            returns = df.pct_change().dropna()
            comp_df = pd.DataFrame({
                "Rendimiento Total (%)": (df.iloc[-1] / df.iloc[0] - 1) * 100,
                "Precio Máximo (USD)": df.max(),
                "Precio Mínimo (USD)": df.min(),
                "Volatilidad Diaria (%)": returns.std() * 100
            })
            st.dataframe(comp_df.style.background_gradient(cmap='Blues'), use_container_width=True)

        with tab3:
            st.subheader("Matriz Riesgo vs. Retorno")
            # Gráfico de dispersión funcional para decisiones de inversión
            risk_ret = pd.DataFrame({
                "Retorno": (df.iloc[-1] / df.iloc[0] - 1) * 100,
                "Riesgo": returns.std() * 100
            }).reset_index()
            
            fig_risk = go.Figure()
            fig_risk.add_trace(go.Scatter(
                x=risk_ret["Riesgo"], y=risk_ret["Retorno"],
                mode='markers+text', text=risk_ret["index"],
                textposition="top center",
                marker=dict(size=20, color='#38bdf8', symbol='diamond', line=dict(width=2, color='white'))
            ))
            fig_risk.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig_risk, use_container_width=True)

        # --- PIE DE PÁGINA ---
        st.markdown("<br><hr>", unsafe_allow_html=True)
        st.markdown("<div style='text-align: center; color: #475569;'>Terminal Operativa: Análisis de 4to Semestre - Universidad Externado</div>", unsafe_allow_html=True)

except Exception as e:
    st.error(f"Error en el flujo de datos: {e}")
