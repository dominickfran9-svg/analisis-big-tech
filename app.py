import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go
from scipy.optimize import minimize
import numpy as np

# 1. SETUP DE TERMINAL DE GRADO BANCARIO
st.set_page_config(page_title="Alpha Trading Terminal", layout="wide", initial_sidebar_state="collapsed")

# 2. CSS AVANZADO: GLASSMORPHISM Y MICRO-INTERACCIONES
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Inter:wght@300;400;600&display=swap');
    
    /* Fondo limpio y oscuro */
    .main { background: #010409; }
    
    /* ELIMINADO EL EFECTO SCANNER (stApp::before) */

    /* Tarjetas Dinámicas con Glow Adaptativo (Micro-Interacción) */
    div[data-testid="stMetric"] {
        background: rgba(13, 17, 23, 0.8) !important;
        border: 1px solid #30363d !important;
        backdrop-filter: blur(12px) !important;
        border-radius: 20px !important;
        padding: 20px !important;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275) !important;
        position: relative;
        overflow: hidden;
    }

    div[data-testid="stMetric"]::after {
        content: ""; position: absolute; top: 0; left: 0; width: 100%; height: 100%;
        background: radial-gradient(circle at center, transparent, rgba(88, 166, 255, 0.05));
        opacity: 0; transition: opacity 0.3s;
    }

    /* Animación de elevación y Glow Adaptativo al pasar el mouse */
    div[data-testid="stMetric"]:hover {
        transform: translateY(-8px) scale(1.02) !important;
        box-shadow: 0 0 30px rgba(56, 189, 248, 0.3) !important;
    }

    /* Colores de Glow específicos por empresa (Simulado, pero estético) */
    div[data-testid="stMetric"]:has(label:contains('AAPL')):hover { border-color: #aff5b4 !important; box-shadow: 0 0 30px rgba(175, 245, 180, 0.3) !important; }
    div[data-testid="stMetric"]:has(label:contains('NVDA')):hover { border-color: #7000ff !important; box-shadow: 0 0 30px rgba(112, 0, 255, 0.3) !important; }
    div[data-testid="stMetric"]:has(label:contains('MSFT')):hover { border-color: #1f6feb !important; box-shadow: 0 0 30px rgba(31, 111, 235, 0.3) !important; }
    div[data-testid="stMetric"]:has(label:contains('TSLA')):hover { border-color: #f85149 !important; box-shadow: 0 0 30px rgba(248, 81, 73, 0.3) !important; }

    h1, h2, h3 { font-family: 'Orbitron', sans-serif; color: #f0f6fc; text-transform: uppercase; letter-spacing: 2px; }
    
    /* Estilo para las Noticias */
    .news-box {
        background: rgba(22, 27, 34, 0.5);
        border-left: 5px solid;
        border-radius: 10px;
        padding: 15px;
        margin-bottom: 12px;
        transition: 0.2s;
    }
    .news-box:hover { transform: translateX(5px); background: rgba(22, 27, 34, 0.7); }
    </style>
    """, unsafe_allow_html=True)

@st.cache_data(ttl=300)
def get_live_data():
    tickers = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'NVDA', 'META', 'TSLA']
    df = yf.download(tickers, period="1mo", interval="1d", progress=False)['Close']
    return df

try:
    data = get_live_data()
    returns = data.pct_change().dropna()
    tickers = data.columns
    
    # --- HEADER ---
    head1, head2 = st.columns([3, 1])
    head1.title("📡 QUANTUM TRADING TERMINAL")
    head2.status("DATA FEED ACTIVE", state="running")
    st.markdown("---")

    # 1. MÉTRICAS DINÁMICAS (Micro-interacciones activadas)
    m_cols = st.columns(len(tickers))
    for i, tick in enumerate(tickers):
        val = data[tick].iloc[-1]
        delta = (val / data[tick].iloc[-2] - 1) * 100
        m_cols[i].metric(label=f"SYS::{tick}", value=f"${val:.1f}", delta=f"{delta:.2f}%")

    st.markdown("<br>", unsafe_allow_html=True)

    # 2. ZONA DE VISUALIZACIÓN NEÓN 2.0
    st.subheader("Visualizador de Activos de Alto Rendimiento")
    tab_chart, tab_opt, tab_news = st.tabs(["⚡ Gráfico Neón", "🧬 Optimización IA", "📰 Inteligencia"])

    with tab_chart:
        # Gráfico con líneas curvas (spline) y glow adaptativo
        fig = go.Figure()
        colors = ['#00f2ff', '#7000ff', '#ff007b', '#aff5b4', '#d29922', '#1f6feb', '#f85149']
        
        for i, t in enumerate(tickers):
            # Normalización a base 100 (Estándar Profesional)
            norm = (data[t] / data[t].iloc[0]) * 100
            fig.add_trace(go.Scatter(
                x=data.index, y=norm, name=t,
                mode='lines',
                line=dict(color=colors[i % len(colors)], width=4, shape='spline'), # Líneas curvas
                fill='tonexty', fillcolor=f'rgba({i*30}, 242, 255, 0.02)', # Glow traslúcido
                # Micro-interacción: Iluminar la línea intensamente al pasar el mouse
                hoverlabel=dict(bgcolor=colors[i % len(colors)], font_size=16, font_family="Orbitron"),
                hovertemplate="<b>%{x}</b><br>Retorno: %{y:.2f}%<extra></extra>"
            ))

        fig.update_layout(
            hovermode="x unified", template="plotly_dark",
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            height=600, xaxis=dict(showgrid=False),
            yaxis=dict(side="right", gridcolor='rgba(255,255,255,0.05)', title="Crecimiento Relativo (%)")
        )
        st.plotly_chart(fig, use_container_width=True)

    with tab_opt:
        col_o1, col_o2 = st.columns([2, 1])
        with col_o1:
            cash = st.number_input("Capital a Optimizar (USD)", value=10000)
            def min_v(w): return np.sqrt(np.dot(w.T, np.dot(returns.cov()*252, w)))
            res = minimize(min_v, len(tickers)*[1./len(tickers)], bounds=tuple((0,1) for _ in range(len(tickers))), constraints={'type':'eq','fun':lambda x: np.sum(x)-1})
            
            fig_bar = go.Figure(go.Bar(x=tickers, y=res.x, marker_color='#38bdf8'))
            fig_bar.update_layout(template="plotly_dark", title="Distribución de Riesgo Mínimo (Márkaris)", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=400)
            st.plotly_chart(fig_bar, use_container_width=True)
        with col_o2:
            st.markdown("<br><br>", unsafe_allow_html=True)
            st.success("**Recomendación del Algoritmo**")
            for i, t in enumerate(tickers):
                if res.x[i] > 0.01:
                    st.write(f"• **{t}**: ${cash * res.x[i]:,.2f}")

    with tab_news:
        noticias = [
            ("NVDA", "Resultados trimestrales superan expectativas por demanda de IA.", "ALCISTA"),
            ("TSLA", "Nuevas regulaciones impactan margen neto.", "BAJISTA"),
            ("MSFT", "Anunciada integración masiva de ChatGPT en Office 2026.", "ALCISTA"),
            ("AAPL", "Rumores de retraso en el nuevo iPhone por cadena de suministro.", "BAJISTA")
        ]
        for stock, txt, sent in noticias:
            color = "#2ea44f" if sent == "ALCISTA" else "#cb2431"
            st.markdown(f"""
            <div class='news-box' style='border-color: {color};'>
                <strong>[{stock}]</strong> - {txt}
            </div>
            """, unsafe_allow_html=True)

    # --- FOOTER TERMINAL ---
    st.markdown("---")
    st.markdown(f"<div style='text-align: right; color: #475569; font-family: monospace;'>SYSTEM_USER: VARGAS_PARRA | SESSION: {np.random.randint(1000,9999)}</div>", unsafe_allow_html=True)

except Exception as e:
    st.error(f"Error en la red de trading: {e}")
