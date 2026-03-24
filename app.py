import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go
import plotly.express as px
import numpy as np

# Configuración de Interfaz de Grado Bancario
st.set_page_config(page_title="Alpha Intelligence Terminal", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=JetBrains+Mono:wght@300;500&display=swap');
    
    .main { background: #010409; }
    
    /* Efecto de Escaneo de Datos */
    .stApp::before {
        content: ""; position: fixed; top: 0; left: 0; width: 100%; height: 1px;
        background: rgba(56, 189, 248, 0.5); box-shadow: 0 0 10px #38bdf8;
        z-index: 9999; animation: scan 4s linear infinite; pointer-events: none;
    }
    @keyframes scan { 0% { top: 0%; } 100% { top: 100%; } }

    /* Estilo de contenedores */
    [data-testid="stVerticalBlock"] > div:has(div.stMetric) {
        background: rgba(22, 27, 34, 0.7);
        border: 1px solid #30363d;
        border-radius: 10px;
        padding: 10px;
    }

    h1, h2, h3 { font-family: 'Orbitron', sans-serif; color: #58a6ff; }
    code { font-family: 'JetBrains Mono', monospace; }
    </style>
    """, unsafe_allow_html=True)

@st.cache_data(ttl=300)
def get_pro_data():
    tickers = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'NVDA', 'META', 'TSLA']
    df = yf.download(tickers, period="1y", interval="1d", progress=False)['Close']
    return df

try:
    data = get_pro_data()
    
    # --- DASHBOARD HEADER ---
    head1, head2 = st.columns([4, 1])
    head1.title("💹 ALPHA_STRAT_TERMINAL")
    head2.metric("LATENCY", "14ms", "-2ms")

    # --- TOP TICKER TAPE ---
    st.markdown("### 📡 Live Node Connection")
    m_cols = st.columns(len(data.columns))
    for i, tick in enumerate(data.columns):
        val = data[tick].iloc[-1]
        delta = (val / data[tick].iloc[-2] - 1) * 100
        m_cols[i].metric(tick, f"{val:.1f}", f"{delta:.2f}%")

    # --- CUERPO PRINCIPAL ---
    tab_inv, tab_tech, tab_risk = st.tabs(["🚀 Inversión Inteligente", "🧪 Laboratorio Técnico", "⚠️ Gestión de Riesgo"])

    with tab_inv:
        col_inv1, col_inv2 = st.columns([2, 1])
        
        with col_inv1:
            st.subheader("Simulador de Portafolio")
            cash = st.slider("Capital Inicial (USD)", 1000, 50000, 5000)
            target = st.selectbox("Seleccionar Activo para Backtesting", data.columns)
            
            # Cálculo de Retorno Real
            initial_p = data[target].iloc[0]
            final_p = data[target].iloc[-1]
            profit = cash * (final_p / initial_p - 1)
            
            fig_inv = go.Figure()
            fig_inv.add_trace(go.Scatter(x=data.index, y=(data[target]/initial_p)*cash, 
                                        line=dict(color='#58a6ff', width=3), fill='tozeroy'))
            fig_inv.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=350)
            st.plotly_chart(fig_inv, use_container_width=True)
        
        with col_inv2:
            st.markdown("<br><br>", unsafe_allow_html=True)
            st.metric("Balance Proyectado", f"${cash + profit:,.2f}", f"{((final_p/initial_p)-1)*100:.2f}%")
            st.info(f"Análisis: {target} ha mostrado un crecimiento sólido en el último ciclo.")

    with tab_tech:
        st.subheader("Indicadores de Momento")
        stock_tech = st.selectbox("Analizar Activo:", data.columns, key="tech_sel")
        
        # Cálculo de RSI (Indicador de Fuerza Relativa)
        delta = data[stock_tech].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1+rs))
        
        fig_rsi = go.Figure()
        fig_rsi.add_trace(go.Scatter(x=data.index, y=rsi, name="RSI (14)", line=dict(color='#ff7b72')))
        fig_rsi.add_hline(y=70, line_dash="dot", line_color="red", annotation_text="Sobrecompra")
        fig_rsi.add_hline(y=30, line_dash="dot", line_color="green", annotation_text="Sobreventa")
        fig_rsi.update_layout(template="plotly_dark", height=300, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_rsi, use_container_width=True)

    with tab_risk:
        st.subheader("Mapa de Calor de Correlación")
        # Esto permite ver si tu portafolio está diversificado o si todo se mueve igual
        corr = data.pct_change().corr()
        fig_corr = px.imshow(corr, text_auto=True, aspect="auto", color_continuous_scale='RdBu_r')
        fig_corr.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_corr, use_container_width=True)
        st.caption("Nota: Valores cercanos a 1 indican que los activos se mueven en la misma dirección.")

    # --- FOOTER TERMINAL ---
    st.markdown("---")
    st.markdown(f"<div style='text-align: right; color: #8b949e;'>SYSTEM_USER: D_VARGAS_PARRA | SESSION: {np.random.randint(1000,9999)}</div>", unsafe_allow_html=True)

except Exception as e:
    st.error("Error en la conexión con el nodo central. Reintentando...")
