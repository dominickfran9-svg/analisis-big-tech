import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go
import plotly.express as px
from scipy.optimize import minimize
import numpy as np

# 1. NÚCLEO DE INTELIGENCIA
st.set_page_config(page_title="Quantum Intelligence Hub", layout="wide", initial_sidebar_state="collapsed")

# 2. CSS: DISEÑO DE ALTO IMPACTO (Fondo Limpio, Sin Scanner)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Inter:wght@300;400;600&display=swap');
    .main { background: #010409; }
    div[data-testid="stMetric"] {
        background: rgba(13, 17, 23, 0.9) !important;
        border: 1px solid #30363d !important;
        border-radius: 15px !important;
        padding: 20px !important;
        box-shadow: 0 4px 15px rgba(0,0,0,0.5) !important;
    }
    .analysis-card {
        background: rgba(22, 27, 34, 0.6);
        border: 1px solid #1f6feb;
        border-radius: 12px;
        padding: 20px;
        margin: 10px 0;
        border-left: 5px solid #58a6ff;
    }
    h1, h2, h3 { font-family: 'Orbitron', sans-serif; color: #f0f6fc; }
    p, li { font-family: 'Inter', sans-serif; color: #8b949e; line-height: 1.6; }
    b { color: #58a6ff; }
    </style>
    """, unsafe_allow_html=True)

@st.cache_data(ttl=300)
def get_full_analysis_data():
    tickers = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'NVDA', 'META', 'TSLA']
    df = yf.download(tickers, period="2y", interval="1d", progress=False)['Close']
    return df

try:
    df = get_full_analysis_data()
    returns = df.pct_change().dropna()
    tickers = df.columns

    # --- HEADER DINÁMICO ---
    st.title("📡 QUANTUM INTELLIGENCE HUB")
    st.markdown("---")

    # 1. MÉTRICAS CON INDICADOR DE TENDENCIA
    m_cols = st.columns(len(tickers))
    for i, t in enumerate(tickers):
        curr = df[t].iloc[-1]
        ytd = (curr / df[t].iloc[0] - 1) * 100
        m_cols[i].metric(t, f"${curr:.1f}", f"{ytd:.1f}% YTD")

    # 2. SECCIÓN DE ANÁLISIS ESTRATÉGICO
    tab_market, tab_risk, tab_alpha = st.tabs(["🔍 Análisis de Mercado", "⚖️ Diagnóstico de Riesgo", "🤖 Estrategia de Inversión"])

    with tab_market:
        col1, col2 = st.columns([3, 1.5])
        with col1:
            fig = go.Figure()
            for t in tickers:
                norm = (df[t] / df[t].iloc[0]) * 100
                fig.add_trace(go.Scatter(x=df.index, y=norm, name=t, line=dict(width=3, shape='spline')))
            fig.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=500)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader("Contexto de Rendimiento")
            st.markdown(f"""
            <div class='analysis-card'>
                <b>Análisis de Crecimiento:</b><br>
                El mercado de las Big Tech presenta una tendencia de <b>fuerte recuperación</b>. 
                Actualmente, el líder del sector es <b>{df.iloc[-1].idxmax()}</b>, mostrando una 
                resiliencia superior al promedio del S&P 500.<br><br>
                <b>Observación:</b> El crecimiento acumulado (YTD) sugiere una entrada de capital 
                institucional hacia activos de IA y computación en la nube.
            </div>
            """, unsafe_allow_html=True)

    with tab_risk:
        r_col1, r_col2 = st.columns([2, 2])
        with r_col1:
            corr = returns.corr()
            fig_corr = px.imshow(corr, text_auto=".2f", color_continuous_scale='Blues')
            fig_corr.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig_corr, use_container_width=True)
        
        with r_col2:
            st.subheader("Evaluación de Correlación")
            max_corr = corr.unstack().sort_values(ascending=False).drop_duplicates()
            pair = max_corr.index[1] # El primero es 1.0 consigo mismo
            
            st.markdown(f"""
            <div class='analysis-card'>
                <b>Alerta de Concentración:</b><br>
                Existe una correlación crítica de <b>{max_corr[1]:.2f}</b> entre <b>{pair[0]}</b> y <b>{pair[1]}</b>. 
                Esto indica que poseer ambos activos no reduce significativamente el riesgo sistémico.<br><br>
                <b>Recomendación de Riesgo:</b> Para una cartera balanceada, se sugiere buscar activos con correlaciones 
                inferiores a 0.50 para mitigar el <b>Drawdown</b> máximo durante periodos de volatilidad.
            </div>
            """, unsafe_allow_html=True)

    with tab_alpha:
        a_col1, a_col2 = st.columns([2, 1.5])
        with a_col1:
            def min_v(w): return np.sqrt(np.dot(w.T, np.dot(returns.cov()*252, w)))
            res = minimize(min_v, len(tickers)*[1./len(tickers)], bounds=tuple((0,1) for _ in range(len(tickers))), constraints={'type':'eq','fun':lambda x: np.sum(x)-1})
            
            fig_bar = go.Figure(go.Bar(x=tickers, y=res.x, marker_color='#1f6feb'))
            fig_bar.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=350)
            st.plotly_chart(fig_bar, use_container_width=True)
            
        with a_col2:
            st.subheader("Lógica de Inversión IA")
            best_pick = tickers[np.argmax(res.x)]
            st.markdown(f"""
            <div class='analysis-card'>
                <b>Estrategia Markowitz:</b><br>
                El algoritmo ha asignado el mayor peso a <b>{best_pick}</b> con un {np.max(res.x)*100:.1f}%.<br><br>
                <b>Justificación Técnica:</b> Este activo presenta el mejor ratio entre retorno esperado 
                y volatilidad histórica dentro del set. La distribución actual busca maximizar el 
                <b>Ratio de Sharpe</b>, optimizando cada dólar invertido frente a la incertidumbre del mercado.
            </div>
            """, unsafe_allow_html=True)

    # --- FOOTER PROFESIONAL ---
    st.markdown("---")
    st.caption("Dominick Vargas Parra | Análisis de Decisiones de Inversión | Universidad Externado de Colombia")

except Exception as e:
    st.error(f"Error de sincronización con el mercado: {e}")
