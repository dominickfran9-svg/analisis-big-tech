import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go
import plotly.express as px
from scipy.optimize import minimize
import numpy as np

# 1. CONFIGURACIÓN DEL SISTEMA GERENCIAL
st.set_page_config(page_title="Terminal Gerencial Big Tech", layout="wide", initial_sidebar_state="collapsed")

# 2. CSS DINÁMICO: ADAPTABLE AL TEMA DEL NAVEGADOR
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Inter:wght@300;400;600&display=swap');
    
    /* Contenedores de Información Crítica con transparencia inteligente */
    .info-panel {
        background: rgba(128, 128, 128, 0.08); 
        border: 1px solid rgba(128, 128, 128, 0.2);
        border-radius: 12px;
        padding: 35px;
        margin-bottom: 25px;
        min-height: 500px;
    }
    
    .panel-header {
        font-family: 'Orbitron', sans-serif;
        color: #58a6ff;
        font-size: 1.25rem;
        border-bottom: 2px solid #58a6ff;
        padding-bottom: 12px;
        margin-bottom: 20px;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .panel-body {
        font-family: 'Inter', sans-serif;
        line-height: 1.9;
        text-align: justify;
        font-size: 1.05rem;
    }

    .formula-box {
        background: rgba(0, 0, 0, 0.1);
        padding: 20px;
        border-radius: 10px;
        font-family: 'Courier New', monospace;
        color: #2ea043;
        margin: 20px 0;
        border-left: 5px solid #58a6ff;
    }

    /* Estilo de KPIs Superiores Adaptables */
    div[data-testid="stMetric"] {
        background: rgba(128, 128, 128, 0.05) !important;
        border: 1px solid rgba(128, 128, 128, 0.2) !important;
        border-radius: 10px !important;
        padding: 20px !important;
    }
    </style>
    """, unsafe_allow_html=True)

@st.cache_data(ttl=600)
def load_market_data():
    tickers = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'NVDA', 'META', 'TSLA']
    return yf.download(tickers, period="2y", interval="1d", progress=False)['Close']

try:
    df = load_market_data()
    returns = df.pct_change().dropna()
    tickers = df.columns

    # --- TÍTULO ACTUALIZADO ---
    st.title("🏛️ ANÁLISIS ESTRATÉGICO DE ACCIONES BIG TECH")
    st.markdown("---")

    # KPIs SUPERIORES
    m_cols = st.columns(len(tickers))
    for i, t in enumerate(tickers):
        actual = df[t].iloc[-1]
        ytd = (actual / df[t].iloc[0] - 1) * 100
        m_cols[i].metric(t, f"${actual:.2f}", f"{ytd:.1f}% YTD")

    tabs = st.tabs(["🌎 Desempeño & Ciclos", "🛡️ Matriz de Riesgo", "📈 Optimización de Markowitz", "💰 Calculadora de Capital"])

    # --- TAB 1: MACRO ---
    with tabs[0]:
        c1, c2, c3 = st.columns([3, 2, 2])
        with c1:
            norm = (df / df.iloc[0]) * 100
            st.plotly_chart(px.line(norm, height=550), use_container_width=True)
        with c2:
            st.markdown("""<div class='info-panel'><div class='panel-header'>🔬 Metodología de Normalización</div><div class='panel-body'>
            La <b>Normalización Base 100</b> es un procedimiento estadístico crítico para comparar activos con valores nominales heterogéneos. La fórmula aplicada es: <br>
            <div class='formula-box'>$$P_{norm} = \\frac{P_{t}}{P_{t=0}} \\times 100$$</div>
            Este método permite observar el crecimiento porcentual acumulado, eliminando el sesgo visual que producen las acciones con precios altos frente a las de menor precio. Al fijar el origen en 100, cualquier valor por encima de este nivel representa una ganancia neta, facilitando la identificación de activos con Alpha superior.</div></div>""", unsafe_allow_html=True)
        with c3:
            st.markdown("""<div class='info-panel'><div class='panel-header'>🧠 Análisis de Ciclo Económico</div><div class='panel-body'>
            El rendimiento actual de las Big Tech refleja una reconfiguración estructural masiva. El mercado está premiando la "opcionalidad estratégica" y la integración vertical en inteligencia artificial. <br><br><b>Comparación Estratégica:</b> Mientras que el sector de semiconductores muestra una aceleración exponencial, los servicios en la nube presentan una consolidación necesaria. Se recomienda una postura de acumulación en activos con flujos de caja libre (FCF) crecientes, ya que estos actúan como refugio ante la volatilidad.</div></div>""", unsafe_allow_html=True)

    # --- TAB 2: RIESGO ---
    with tabs[1]:
        cr1, cr2, cr3 = st.columns([3, 2, 2])
        with cr1:
            st.plotly_chart(px.imshow(returns.corr(), text_auto=".2f", color_continuous_scale='RdBu_r', height=550), use_container_width=True)
        with cr2:
            st.markdown("""<div class='info-panel'><div class='panel-header'>📊 Fundamentos de Correlación</div><div class='panel-body'>
            Utilizamos el <b>Coeficiente de Pearson</b> para cuantificar la dependencia lineal entre retornos diarios. La métrica se define como: <br>
            <div class='formula-box'>$$\\rho_{X,Y} = \\frac{\\text{cov}(X,Y)}{\\sigma_X \\sigma_Y}$$</div>
            Un coeficiente cercano a 1 indica un riesgo sistémico compartido, mientras que valores bajos permiten una diversificación efectiva. En este ecosistema, las correlaciones tienden a ser elevadas debido a factores macro comunes, lo que obliga a buscar activos con betas diferenciadas.</div></div>""", unsafe_allow_html=True)
        with cr3:
            st.markdown("""<div class='info-panel'><div class='panel-header'>🛡️ Gestión de Riesgos Sistémicos</div><div class='panel-body'>
            La meta del administrador de riesgos es identificar la mínima covarianza histórica detectada. <br><br><b>Interpretación Gerencial:</b> Al entender qué activos no caen en sincronía, podemos construir un portafolio resiliente. Por ejemplo, la baja correlación relativa entre ciertos activos permite que uno actúe como amortiguador durante correcciones sectoriales. Ignorar estas relaciones resulta en una falsa sensación de diversificación donde todos los activos colapsan simultáneamente.</div></div>""", unsafe_allow_html=True)

    # --- TAB 3: MARKOWITZ ---
    with tabs[2]:
        co1, co2, co3 = st.columns([3, 2, 2])
        n_p = 1000
        p_vol = []
        p_ret = []
        for _ in range(n_p):
            w = np.random.random(len(tickers))
            w /= np.sum(w)
            p_vol.append(np.sqrt(np.dot(w.T, np.dot(returns.cov() * 252, w))))
            p_ret.append(np.sum(returns.mean() * w) * 252)
        
        with co1:
            st.plotly_chart(px.scatter(x=p_vol, y=p_ret, color=p_ret, title="Frontera Eficiente", height=550), use_container_width=True)
        with co2:
            st.markdown("""<div class='info-panel'><div class='panel-header'>🧬 Teoría de Cartera de Markowitz</div><div class='panel-body'>
            La optimización de media-varianza busca el conjunto de carteras que maximizan el retorno esperado para un nivel de riesgo determinado. <br>
            <div class='formula-box'>$$\\text{Minimizar: } \\sigma_p^2 = \\mathbf{w}^T \\mathbf{\\Sigma} \\mathbf{w}$$</div>
            Suerto a que la suma de pesos sea igual a 1. Cada punto en la gráfica representa una combinación posible de inversión. La curva superior es la Frontera Eficiente, donde se encuentran las decisiones racionales.</div></div>""", unsafe_allow_html=True)
        with co3:
            st.markdown("""<div class='info-panel'><div class='panel-header'>🎯 Asimilación de Decisiones</div><div class='panel-body'>
            <b>Análisis de la Frontera:</b> Cualquier punto por debajo de la frontera es ineficiente, pues ofrece menos retorno por el mismo riesgo. <br><br><b>Acción Sugerida:</b> Nuestra terminal se enfoca en el punto de Variancia Mínima. En un entorno de alta incertidumbre, priorizamos la estabilidad sobre el retorno agresivo. Esta estrategia es ideal para inversores que buscan preservar capital manteniendo exposición al crecimiento tech.</div></div>""", unsafe_allow_html=True)

    # --- TAB 4: CALCULADORA ---
    with tabs[3]:
        def min_v(w): return np.sqrt(np.dot(w.T, np.dot(returns.cov() * 252, w)))
        res = minimize(min_v, [1./len(tickers)]*len(tickers), method='SLSQP', bounds=tuple((0,1) for _ in range(len(tickers))), constraints={'type':'eq','fun':lambda x: np.sum(x)-1})
        
        # Mostramos todas las acciones del portafolio (tickers)
        f_lab = list(tickers)
        f_val = list(res.x)

        sc1, sc2, sc3 = st.columns([2.5, 2, 2.5])
        with sc1:
            st.plotly_chart(go.Figure(data=[go.Pie(labels=f_lab, values=f_val, hole=.5)]), use_container_width=True)
        with sc2:
            monto = st.number_input("💵 Capital a Invertir (USD)", min_value=1000, value=10000)
            # Tabla con las 7 acciones
            st.table(pd.DataFrame({'Activo': f_lab, 'Inversión': [v * monto for v in f_val]}).style.format({"Inversión": "${:,.2f}"}))
        with sc3:
            st.markdown(f"""<div class='info-panel'><div class='panel-header'>💰 Recomendación Gerencial Final</div><div class='panel-body
