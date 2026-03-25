import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go
import plotly.express as px
from scipy.optimize import minimize
import numpy as np

# 1. CONFIGURACIÓN DEL SISTEMA GERENCIAL
st.set_page_config(page_title="Terminal Gerencial Big Tech", layout="wide", initial_sidebar_state="collapsed")

# 2. CSS: ARQUITECTURA VISUAL "CYBER-LUXURY" RESTAURADA
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Inter:wght@300;400;600&display=swap');
    
    .stApp { background: var(--background-color); }
    
    /* Contenedores de KPIs y Análisis ADAPTABLES */
    div[data-testid="stMetric"], .analysis-panel {
        background: rgba(13, 17, 23, 0.05) !important;
        border: 1px solid #30363d !important;
        border-radius: 12px;
        padding: 25px;
        margin-bottom: 25px;
        transition: 0.3s;
    }
    
    .panel-title { font-family: 'Orbitron', sans-serif; color: #58a6ff; font-size: 1.1rem; margin-bottom: 15px; text-transform: uppercase; border-bottom: 1px solid #30363d; padding-bottom: 10px; }
    .panel-text { font-family: 'Inter', sans-serif; line-height: 1.9; text-align: justify; font-size: 1rem; color: var(--text-color); }
    h1, h2, h3 { font-family: 'Orbitron', sans-serif; color: var(--text-color); }
    b { color: #58a6ff; }
    .methodology-tag { color: #f85149; font-weight: bold; font-family: 'Orbitron', sans-serif; font-size: 0.8rem; }
    </style>
    """, unsafe_allow_html=True)

@st.cache_data(ttl=600)
def get_full_market_data():
    tickers = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'NVDA', 'META', 'TSLA']
    df = yf.download(tickers, period="2y", interval="1d", progress=False)['Close']
    return df

try:
    df = get_full_market_data()
    returns = df.pct_change().dropna()
    tickers = df.columns

    st.title("🏛️ ALPHA STRATEGIC INTELLIGENCE v17")
    st.markdown("---")

    # 1. RESTAURACIÓN DE KPIs SUPERIORES
    m_cols = st.columns(len(tickers))
    for i, t in enumerate(tickers):
        actual = df[t].iloc[-1]
        ytd = (actual / df[t].iloc[0] - 1) * 100
        m_cols[i].metric(t, f"${actual:.2f}", f"{ytd:.1f}% YTD")

    # 2. PANELES DE ALTA PROFUNDIDAD
    tab_m, tab_r, tab_opt, tab_sim = st.tabs([
        "🌎 Desempeño Macro", "🛡️ Matriz de Riesgo", "🧬 Optimización Markowitz", "💰 Calculadora de Capital"
    ])

    with tab_m:
        col1, col2 = st.columns([3, 2])
        with col1:
            fig_p = go.Figure()
            for t in tickers:
                norm = (df[t] / df[t].iloc[0]) * 100
                fig_p.add_trace(go.Scatter(x=df.index, y=norm, name=t, line=dict(width=3)))
            fig_p.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=600)
            st.plotly_chart(fig_p, use_container_width=True)
        with col2:
            st.markdown(f"""<div class='analysis-panel'><div class='panel-title'>Análisis de Ciclo Económico</div><div class='panel-text'>
            <b>Metodología:</b> Aplicamos normalización Base 100 (Precio_t / Precio_0 * 100). <br><br>
            <b>Análisis Estratégico:</b> El rendimiento actual refleja una reconfiguración impulsada por la IA. Las empresas con mayor integración vertical capturan márgenes que antes se diluían. Se aconseja una postura de acumulación en activos con flujos de caja (FCF) crecientes.</div></div>""", unsafe_allow_html=True)

    with tab_r:
        r_col1, r_col2 = st.columns([2.5, 2])
        with r_col1:
            # RESTAURACIÓN DE GRÁFICA DE RIESGOS (CORRELACIÓN)
            corr = returns.corr()
            fig_corr = px.imshow(corr, text_auto=".2f", color_continuous_scale='RdBu_r')
            fig_corr.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=550)
            st.plotly_chart(fig_corr, use_container_width=True)
        with r_col2:
            st.markdown(f"""<div class='analysis-panel'><div class='panel-title'>Ingeniería de Riesgo</div><div class='panel-text'>
            <b>Parámetros:</b> Coeficiente de Pearson sobre retornos logarítmicos. <br><br>
            <b>Briefing:</b> Una correlación superior a 0.70 indica que diversificar no ofrece protección real. Buscamos la mínima covarianza histórica para proteger el portafolio contra caídas sistémicas del sector tecnológico.</div></div>""", unsafe_allow_html=True)

    with tab_opt:
        o_col1, o_col2 = st.columns([2.5, 2.5])
        def min_vol(w): return np.sqrt(np.dot(w.T, np.dot(returns.cov() * 252, w)))
        res = minimize(min_vol, [1./len(tickers)]*len(tickers), method='SLSQP', bounds=tuple((0,1) for _ in range(len(tickers))), constraints={'type':'eq','fun':lambda x: np.sum(x)-1})
        
        # FIX DEFINITIVO PARA ETIQUETAS 0%
        filtered_indices = [i for i, w in enumerate(res.x) if w > 0.01]
        f_labels = [tickers[i] for i in filtered_indices]
        f_values = [res.x[i] for i in filtered_indices]

        with o_col1:
            fig_o = go.Figure(data=[go.Pie(labels=f_labels, values=f_values, hole=.5, textinfo='percent+label')])
            fig_o.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', height=550, showlegend=True)
            st.plotly_chart(fig_o, use_container_width=True)
        with o_col2:
            lider = f_labels[np.argmax(f_values)]
            st.markdown(f"""<div class='analysis-panel'><div class='panel-title'>Asignación Inteligente de Capital</div><div class='panel-text'>
            <span class='methodology-tag'>MODELO MARKOWITZ</span><br>
            Esta gráfica optimiza la relación riesgo-retorno mediante programación cuadrática. <br><br>
            <b>Estrategia:</b> Para minimizar el riesgo, el algoritmo concentra la inversión en <b>{lider}</b>. Posee la mejor covarianza negativa frente al resto del set. Esta cartera preserva capital mientras captura el crecimiento tech.</div></div>""", unsafe_allow_html=True)

    with tab_sim:
        st.subheader("💰 Calculadora de Inversión y Proyección")
        s_col1, s_col2 = st.columns([1, 2])
        with s_col1:
            monto = st.number_input("Capital a Invertir (USD)", min_value=1000, value=10000, step=1000)
            st.markdown("---")
            dist = pd.DataFrame({'Activo': f_labels, 'Monto Sugerido': [v * monto for v in f_values]})
            st.table(dist.style.format({"Monto Sugerido": "${:,.2f}"}))
        with s_col2:
            st.markdown(f"""<div class='analysis-panel'><div class='panel-title'>Recomendación del Asesor</div><div class='panel-text'>
            <b>Estrategia Sugerida:</b> Concentre su posición en <b>{lider}</b> debido a su estabilidad ante la volatilidad de las tasas de interés. <br><br>
            <b>Consejos de Inversión:</b> <br>
            1. No invierta todo de golpe; use entradas escalonadas. <br>
            2. Mantenga un horizonte de mínimo 12 meses para que el interés compuesto actúe. <br>
            3. Revise la correlación trimestralmente para ajustar los pesos.</div></div>""", unsafe_allow_html=True)

    st.markdown("---")
    st.caption("Terminal Gerencial | Universidad Externado de Colombia | Dominick Vargas")

except Exception as e:
    st.error(f"Error en el sistema: {e}")
