import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go
import plotly.express as px
from scipy.optimize import minimize
import numpy as np

# 1. CONFIGURACIÓN DEL SISTEMA GERENCIAL
st.set_page_config(page_title="Terminal Gerencial Big Tech", layout="wide", initial_sidebar_state="collapsed")

# 2. CSS: ARQUITECTURA DE PANELES EXTENSOS
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Inter:wght@300;400;600&display=swap');
    
    /* Paneles de Información Maximizados */
    .info-container {
        background: rgba(13, 17, 23, 0.7);
        border: 1px solid #30363d;
        border-radius: 12px;
        padding: 30px;
        margin-bottom: 25px;
        min-height: 400px;
    }
    
    .header-box {
        font-family: 'Orbitron', sans-serif;
        color: #58a6ff;
        font-size: 1.3rem;
        margin-bottom: 20px;
        border-bottom: 2px solid #58a6ff;
        padding-bottom: 10px;
        text-transform: uppercase;
    }
    
    .body-text {
        font-family: 'Inter', sans-serif;
        line-height: 2.1;
        text-align: justify;
        font-size: 1.05rem;
        color: #c9d1d9;
    }
    
    .formula-block {
        background: rgba(0,0,0,0.3);
        padding: 15px;
        border-radius: 8px;
        font-family: 'Courier New', monospace;
        color: #79c0ff;
        margin: 15px 0;
        border-left: 4px solid #58a6ff;
    }
    
    /* Ajuste de KPIs */
    div[data-testid="stMetric"] {
        background: rgba(13, 17, 23, 0.5) !important;
        border: 1px solid #30363d !important;
        padding: 20px !important;
    }
    </style>
    """, unsafe_allow_html=True)

@st.cache_data(ttl=600)
def get_data():
    tickers = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'NVDA', 'META', 'TSLA']
    return yf.download(tickers, period="2y", interval="1d", progress=False)['Close']

try:
    df = get_data()
    returns = df.pct_change().dropna()
    tickers = df.columns

    st.title("🏛️ ALPHA ELITE TERMINAL: DEEP STRATEGY")
    st.markdown("---")

    # 1. KPIs SUPERIORES RESTAURADOS
    m_cols = st.columns(len(tickers))
    for i, t in enumerate(tickers):
        actual = df[t].iloc[-1]
        ytd = (actual / df[t].iloc[0] - 1) * 100
        m_cols[i].metric(t, f"${actual:.2f}", f"{ytd:.1f}% YTD")

    tabs = st.tabs(["🌎 Macro & Ciclos", "🛡️ Riesgo & Correlación", "📈 Frontera de Markowitz", "💰 Calculadora & Proyección"])

    with tabs[0]:
        c1, c2, c3 = st.columns([2.5, 2, 2])
        with c1:
            fig_p = go.Figure()
            for t in tickers:
                norm = (df[t] / df[t].iloc[0]) * 100
                fig_p.add_trace(go.Scatter(x=df.index, y=norm, name=t))
            st.plotly_chart(fig_p, use_container_width=True)
        with c2:
            st.markdown("""<div class='info-container'><div class='header-box'>🔬 Metodología de Normalización</div><div class='body-text'>
            La <b>Normalización Base 100</b> es una herramienta fundamental en el análisis técnico comparativo. La fórmula aplicada es: <br>
            <div class='formula-block'>P_norm = (P_actual / P_inicial) * 100</div>
            Esto elimina el sesgo del precio nominal, permitiendo que una acción de $600 y una de $150 se midan bajo el mismo estándar de crecimiento porcentual. Sin este ajuste, la volatilidad de los activos más caros dominaría visualmente el gráfico, ocultando el rendimiento real de activos con precios más bajos pero mayor potencial de Alpha.</div></div>""", unsafe_allow_html=True)
        with c3:
            st.markdown("""<div class='info-container'><div class='header-box'>🧠 Análisis de Tendencia Sectorial</div><div class='body-text'>
            El mercado de las Big Tech atraviesa una <b>reconfiguración estructural</b>. Observamos que el rendimiento no es uniforme; existe una divergencia clara entre las empresas que dominan la infraestructura de IA y aquellas que se centran en el consumo masivo. <br><br><b>Comparación Gerencial:</b> Mientras que los activos de hardware muestran una pendiente parabólica, el software de servicios se consolida lateralmente. Se recomienda una postura de acumulación en activos que demuestren flujos de caja libre (FCF) crecientes, ya que estos actúan como refugio ante la volatilidad de las tasas de interés y la incertidumbre macroeconómica global.</div></div>""", unsafe_allow_html=True)

    with tabs[1]:
        cr1, cr2, cr3 = st.columns([2.5, 2, 2])
        with cr1:
            fig_corr = px.imshow(returns.corr(), text_auto=".2f", color_continuous_scale='RdBu_r')
            st.plotly_chart(fig_corr, use_container_width=True)
        with cr2:
            st.markdown("""<div class='info-container'><div class='header-box'>📊 Teoría de Correlación</div><div class='body-text'>
            Utilizamos el <b>Coeficiente de Correlación de Pearson</b> para medir la fuerza de la relación lineal entre pares de activos. La fórmula es: <br>
            <div class='formula-block'>ρ = cov(X,Y) / (σX * σY)</div>
            Un valor de 1.0 implica que los activos se mueven en perfecta armonía, mientras que valores cercanos a 0 indican independencia. En este set de Big Tech, las correlaciones suelen ser altas (>0.6), lo que dificulta la diversificación pura dentro de un mismo sector.</div></div>""", unsafe_allow_html=True)
        with cr3:
            st.markdown("""<div class='info-container'><div class='header-box'>🛡️ Gestión de Riesgos Sistémicos</div><div class='body-text'>
            El análisis de riesgo busca identificar la <b>Mínima Covarianza Histórica</b>. Al entender qué activos no caen al mismo tiempo, podemos construir un portafolio que resista eventos de "cisne negro" en la industria. <br><br><b>Asimilación Técnica:</b> Si un activo presenta una correlación baja con el resto (como tradicionalmente MSFT o GOOGL en ciertos ciclos), se convierte en el ancla del portafolio. La meta no es eliminar el riesgo, sino gestionarlo para que una caída en un subsector (ej. semiconductores) sea compensada por la estabilidad en otro (ej. computación en la nube).</div></div>""", unsafe_allow_html=True)

    with tabs[2]:
        co1, co2, co3 = st.columns([2.5, 2, 2])
        
        # Simulación Monte Carlo para Frontera Eficiente (LOS PUNTITOS)
        results = []
        for _ in range(1000):
            w = np.random.random(len(tickers))
            w /= np.sum(w)
            ret = np.sum(returns.mean() * w) * 252
            vol = np.sqrt(np.dot(w.T, np.dot(returns.cov() * 252, w)))
            results.append([vol, ret])
        f_df = pd.DataFrame(results, columns=['Volatilidad', 'Retorno'])
        
        with co1:
            fig_f = px.scatter(f_df, x='Volatilidad', y='
