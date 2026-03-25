import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go
import plotly.express as px
from scipy.optimize import minimize
import numpy as np

# 1. CONFIGURACIÓN INICIAL
st.set_page_config(page_title="Terminal Big Tech", layout="wide", initial_sidebar_state="collapsed")

# 2. ESTILOS CSS (Adaptable a tema claro/oscuro)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Inter:wght@300;400;600&display=swap');
    .info-panel {
        background: rgba(128, 128, 128, 0.08); 
        border: 1px solid rgba(128, 128, 128, 0.2);
        border-radius: 12px;
        padding: 25px;
        margin-bottom: 20px;
    }
    .panel-header {
        font-family: 'Orbitron', sans-serif;
        color: #58a6ff;
        font-size: 1.1rem;
        border-bottom: 2px solid #58a6ff;
        padding-bottom: 8px;
        margin-bottom: 15px;
        text-transform: uppercase;
    }
    .panel-body { font-family: 'Inter', sans-serif; line-height: 1.6; text-align: justify; }
    .formula-box {
        background: rgba(0, 0, 0, 0.2);
        padding: 12px;
        border-radius: 8px;
        font-family: 'Courier New', monospace;
        color: #2ea043;
        margin: 10px 0;
        border-left: 4px solid #58a6ff;
    }
    div[data-testid="stMetric"] {
        background: rgba(128, 128, 128, 0.05);
        border: 1px solid rgba(128, 128, 128, 0.2);
        border-radius: 10px;
        padding: 15px;
    }
    </style>
    """, unsafe_allow_html=True)

@st.cache_data(ttl=600)
def get_data():
    tks = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'NVDA', 'META', 'TSLA']
    d = yf.download(tks, period="2y", interval="1d", progress=False)['Close']
    return d

try:
    df = get_data()
    rets = df.pct_change().dropna()
    t_list = sorted(df.columns)

    # TÍTULO PRINCIPAL
    st.title("🏛️ ANÁLISIS ESTRATÉGICO DE ACCIONES BIG TECH")
    st.markdown("---")

    # MÉTRICAS SUPERIORES
    kpi_cols = st.columns(len(t_list))
    for idx, t in enumerate(t_list):
        last_p = df[t].iloc[-1]
        chg = (last_p / df[t].iloc[0] - 1) * 100
        kpi_cols[idx].metric(t, f"${last_p:.2f}", f"{chg:.1f}% YTD")

    tbs = st.tabs(["🌎 Desempeño", "🛡️ Riesgo", "📈 Markowitz", "💰 Calculadora"])

    with tbs[0]:
        c1, c2 = st.columns([3, 2])
        with c1:
            st.plotly_chart(px.line((df / df.iloc[0]) * 100, height=450), use_container_width=True)
        with c2:
            st.markdown("""<div class='info-panel'><div class='panel-header'>Ciclo Económico</div><div class='panel-body'>
            Normalización Base 100 aplicada para comparativa directa.<br>
            <div class='formula-box'>$$P_{norm} = \\frac{P_{t}}{P_{0}} \\times 100$$</div>
            Se premia la integración vertical y la eficiencia operativa.</div></div>""", unsafe_allow_html=True)

    with tbs[1]:
        cr1, cr2 = st.columns([3, 2])
        with cr1:
            st.plotly_chart(px.imshow(rets.corr(), text_auto=".2f", color_continuous_scale='RdBu_r', height=450), use_container_width=True)
        with cr2:
            st.markdown("""<div class='info-panel'><div class='panel-header'>Matriz de Correlación</div><div class='panel-body'>
            Medición de dependencia lineal mediante Pearson.<br>
            <div class='formula-box'>$$\\rho = \\frac{cov(X,Y)}{\\sigma_X \\sigma_Y}$$</div></div></div>""", unsafe_allow_html=True)

    with tbs[2]:
        co1, co2 = st.columns([3, 2])
        sims = 1000
        res_s = []
        for _ in range(sims):
            w = np.random.random(len(t_list))
            w /= np.sum(w)
            res_s.append([np.sqrt(np.dot(w.T, np.dot(rets.cov() * 252, w))), np.sum(rets.mean() * w) * 252])
        s_df = pd.DataFrame(res_s, columns=['Vol', 'Ret'])
        with co1:
            st.plotly_chart(px.scatter(s_df, x='Vol', y='Ret', color='Ret', height=450), use_container_width=True)
        with co2:
            st.markdown("""<div class='info-panel'><div class='panel-header'>Frontera Eficiente</div><div class='panel-body'>
            Optimización de media-varianza para maximizar retornos ajustados.<br>
            <div class='formula-box'>$$\\sigma_p^2 = \\mathbf{w}^T \\mathbf{\\Sigma} \\mathbf{w}$$</div></div></div>""", unsafe_allow_html=True)

    with tbs[3]:
        def min_var(w): return np.sqrt(np.dot(w.T, np.dot(rets.cov() * 252, w)))
        opt = minimize(min_var, [1./len(t_list)]*len(t_list), method='SLSQP', bounds=tuple((0,1) for _ in range(len(t_list))), constraints={'type':'eq','fun':lambda x: np.sum(x)-1})
        
        sc1, sc2, sc3 = st.columns([2, 2, 2])
        with sc1:
            st.plotly_chart(go.Figure(data=[go.Pie(labels=t_list, values=opt.x, hole=.4)]), use_container_width=True)
        with sc2:
            amt = st.number_input("Capital (USD)", min_value=100, value=10000)
            res_t = pd.DataFrame({'Activo': t_list, 'Sugerencia': [v * amt for v in opt.x]})
            st.table(res_t.style.format({"Sugerencia": "${:,.2f}"}))
        with sc3:
            st.markdown("""<div class='info-panel'><div class='panel-header'>Sugerencia Final</div><div class='panel-body'>
            Estrategia de Mínima Varianza histórica.<br><br>
            1. Entradas escalonadas.<br>
            2. Horizonte 12+ meses.<br>
            3. Stop-loss 15%.</div></div>""", unsafe_allow_html=True)

    st.markdown("---")
    st.caption("Terminal Gerencial | Universidad Externado de Colombia | Dominick Vargas")

except Exception as e:
    st.error(f"Fallo: {e}")
