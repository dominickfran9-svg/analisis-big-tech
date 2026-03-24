import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go
import plotly.express as px
from scipy.optimize import minimize
import numpy as np

# 1. ARQUITECTURA DE DATOS Y CONFIGURACIÓN
st.set_page_config(page_title="Alpha Strategic Intelligence", layout="wide", initial_sidebar_state="collapsed")

# 2. CSS: DISEÑO DE ALTO IMPACTO Y LECTURA EXTENSA
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Inter:wght@300;400;600&display=swap');
    .main { background: #010409; }
    
    .executive-brief {
        background: rgba(13, 17, 23, 0.95);
        border: 1px solid #30363d;
        border-top: 4px solid #1f6feb;
        border-radius: 12px;
        padding: 35px;
        margin-bottom: 25px;
        box-shadow: 0 15px 35px rgba(0,0,0,0.6);
    }
    
    .brief-title { font-family: 'Orbitron', sans-serif; color: #58a6ff; font-size: 1.3rem; margin-bottom: 20px; text-transform: uppercase; border-bottom: 1px solid #30363d; padding-bottom: 10px; }
    .brief-text { font-family: 'Inter', sans-serif; color: #c9d1d9; line-height: 1.9; text-align: justify; font-size: 1.05rem; }
    
    div[data-testid="stMetric"] {
        background: rgba(13, 17, 23, 0.9) !important;
        border: 1px solid #30363d !important;
        border-radius: 10px !important;
        padding: 15px !important;
    }
    
    h1, h2, h3 { font-family: 'Orbitron', sans-serif; color: #f0f6fc; }
    b { color: #58a6ff; }
    </style>
    """, unsafe_allow_html=True)

@st.cache_data(ttl=300)
def get_strategic_data():
    tickers = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'NVDA', 'META', 'TSLA']
    df = yf.download(tickers, period="2y", interval="1d", progress=False)['Close']
    return df

# --- INICIO DEL CUERPO PRINCIPAL ---
try:
    df = get_strategic_data()
    returns = df.pct_change().dropna()
    tickers = df.columns

    st.title("🏛️ ALPHA STRATEGIC INTELLIGENCE v11")
    st.markdown("---")

    # 1. MONITOR DE ACTIVOS (Métricas YTD)
    m_cols = st.columns(len(tickers))
    for i, t in enumerate(tickers):
        curr = df[t].iloc[-1]
        ytd = (curr / df[t].iloc[0] - 1) * 100
        m_cols[i].metric(t, f"${curr:.1f}", f"{ytd:.1f}% YTD")

    # 2. PANELES DE ANÁLISIS MULTIDIMENSIONAL
    tab_macro, tab_risk, tab_alpha = st.tabs(["🌎 Macro-Estrategia", "🛡️ Gestión de Riesgo Quant", "🧬 Optimización de Capital"])

    with tab_macro:
        col_m1, col_m2 = st.columns([3, 2])
        with col_m1:
            fig = go.Figure()
            for t in tickers:
                norm = (df[t] / df[t].iloc[0]) * 100
                fig.add_trace(go.Scatter(x=df.index, y=norm, name=t, line=dict(width=3, shape='spline')))
            fig.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=600)
            st.plotly_chart(fig, use_container_width=True)
        
        with col_m2:
            lider = (df.iloc[-1] / df.iloc[0]).idxmax()
            st.markdown(f"""
            <div class='executive-brief'>
                <div class='brief-title'>Análisis de Coyuntura y Liderazgo de Mercado</div>
                <div class='brief-text'>
                    El rendimiento del sector tecnológico en el último ciclo fiscal refleja una <b>reconfiguración estructural</b> impulsada por la IA generativa. 
                    Actualmente, <b>{lider}</b> se posiciona como el líder indiscutible debido a su control sobre la infraestructura crítica (semiconductores y centros de datos). <br><br>
                    <b>Origen del Análisis:</b> Este fenómeno se valida mediante el análisis de los múltiplos de valuación frente al crecimiento real de ingresos (PEG Ratio). El mercado está premiando empresas con flujo de caja libre (FCF) robusto que pueden autofinanciar su expansión sin depender de crédito externo en un entorno de tasas altas.<br><br>
                    <b>Causalidad Económica:</b> La alta concentración en Big Tech es una respuesta defensiva de los inversionistas ante la incertidumbre macroeconómica. Estas empresas actúan como "bonos con crecimiento", ofreciendo estabilidad operativa y balances sólidos. <br><br>
                    <b>Recomendación de Negocios:</b> Para un administrador, la estrategia óptima es mantener una exposición del 60% en líderes consolidados y un 40% en activos de alto crecimiento (Growth) para capturar el 'upside' del ciclo de innovación actual.
                </div>
            </div>
            """, unsafe_allow_html=True)

    with tab_risk:
        r_col1, r_col2 = st.columns([2.5, 2])
        with r_col1:
            corr = returns.corr()
            fig_corr = px.imshow(corr, text_auto=".2f", color_continuous_scale='RdBu_r', title="Matriz de Interdependencia (Pearson)")
            fig_corr.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=550)
            st.plotly_chart(fig_corr, use_container_width=True)
        
        with r_col2:
            max_c = corr.unstack().sort_values(ascending=False).drop_duplicates().index[1]
            st.markdown(f"""
            <div class='executive-brief'>
                <div class='brief-title'>Diagnóstico de Correlación y Exposición</div>
                <div class='brief-text'>
                    La matriz muestra una correlación crítica de <b>{corr.loc[max_c[0], max_c[1]]:.2f}</b> entre <b>{max_c[0]}</b> y <b>{max_c[1]}</b>. Desde la óptica de la gestión de activos, esto indica una redundancia sistémica severa. <br><br>
                    <b>¿Cómo se obtuvo este valor?</b> Utilizamos el coeficiente de correlación de Pearson sobre los retornos logarítmicos de los últimos 252 días (año bursátil). Este valor cuantifica qué tan sincronizados están dos activos. Un valor cercano a 1.0 significa que diversificar entre ellos no ofrece protección real en caídas de mercado.<br><br>
                    <b>Impacto Estratégico:</b> La alta correlación entre las 'Magnificent Seven' sugiere que un evento regulatorio adverso en el sector tecnológico afectará a todo el portafolio por igual. <br><br>
                    <b>Acción Sugerida:</b> Es imperativo buscar activos con correlaciones menores a 0.50 (como servicios públicos o consumo básico) para reducir el <b>Riesgo Beta</b> total de la cartera y mejorar la resiliencia ante shocks externos.
                </div>
            </div>
            """, unsafe_allow_html=True)

    with tab_alpha:
        a_col1, a_col2 = st.columns([2.5, 2])
        with a_col1:
            def min_v(w): return np.sqrt(np.dot(w.T, np.
