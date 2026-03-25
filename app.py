import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go
import plotly.express as px
from scipy.optimize import minimize
import numpy as np

# 1. CONFIGURACIÓN DEL SISTEMA
st.set_page_config(page_title="Terminal Gerencial Big Tech", layout="wide", initial_sidebar_state="collapsed")

# 2. CSS: ARQUITECTURA DE INMERSIÓN TOTAL (PANELES AMPLIADOS)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Inter:wght@300;400;600&display=swap');
    
    .stApp { background: #0d1117; }
    
    /* Contenedores de Información Crítica */
    .info-panel {
        background: rgba(22, 27, 34, 0.8);
        border: 1px solid #30363d;
        border-radius: 12px;
        padding: 35px;
        margin-bottom: 25px;
        min-height: 450px; /* Asegura espacio para análisis extenso */
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
        color: #c9d1d9;
    }

    .formula-box {
        background: #000000;
        padding: 20px;
        border-radius: 10px;
        font-family: 'Courier New', monospace;
        color: #7ee787;
        margin: 20px 0;
        border-left: 5px solid #58a6ff;
    }

    /* Estilo de KPIs Superiores */
    div[data-testid="stMetric"] {
        background: #161b22 !important;
        border: 1px solid #30363d !important;
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

    st.title("🏛️ ALPHA STRATEGIC INTELLIGENCE - TERMINAL v19")
    st.markdown("---")

    # 1. RESTAURACIÓN DE KPIs SUPERIORES
    m_cols = st.columns(len(tickers))
    for i, t in enumerate(tickers):
        actual = df[t].iloc[-1]
        ytd = (actual / df[t].iloc[0] - 1) * 100
        m_cols[i].metric(t, f"${actual:.2f}", f"{ytd:.1f}% YTD")

    tabs = st.tabs(["🌎 Desempeño & Ciclos", "🛡️ Matriz de Riesgo", "📈 Optimización de Markowitz", "💰 Calculadora de Capital"])

    # TAB 1: MACRO
    with tabs[0]:
        c1, c2, c3 = st.columns([3, 2, 2])
        with c1:
            fig_p = go.Figure()
            for t in tickers:
                norm = (df[t] / df[t].iloc[0]) * 100
                fig_p.add_trace(go.Scatter(x=df.index, y=norm, name=t, line=dict(width=2.5)))
            fig_p.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', height=550)
            st.plotly_chart(fig_p, use_container_width=True)
        with c2:
            st.markdown("""<div class='info-panel'><div class='panel-header'>🔬 Metodología de Normalización</div><div class='panel-body'>
            La <b>Normalización Base 100</b> es un procedimiento estadístico crítico para comparar activos con valores nominales heterogéneos. La fórmula aplicada es: <br>
            <div class='formula-box'>$$P_{norm} = \\frac{P_{t}}{P_{t=0}} \\times 100$$</div>
            Este método permite observar el crecimiento porcentual acumulado, eliminando el sesgo visual que producen las acciones con precios altos (como Google o Microsoft) frente a las de menor precio. Al fijar el origen en 100, cualquier valor por encima de este nivel representa una ganancia neta, facilitando la identificación de activos con <b>Alpha</b> superior en el periodo analizado.</div></div>""", unsafe_allow_html=True)
        with c3:
            st.markdown("""<div class='info-panel'><div class='panel-header'>🧠 Análisis de Ciclo Económico</div><div class='panel-body'>
            El rendimiento actual de las Big Tech refleja una <b>reconfiguración estructural</b> masiva. El mercado está premiando la "opcionalidad estratégica" y la integración vertical en inteligencia artificial. <br><br><b>Comparación Estratégica:</b> Mientras que el sector de semiconductores muestra una aceleración exponencial, los servicios en la nube presentan una consolidación necesaria. Se recomienda una postura de acumulación en activos con <b>flujos de caja libre (FCF)</b> crecientes, ya que estos actúan como refugio ante la volatilidad de las tasas de interés y aseguran la reinversión en I+D necesaria para mantener la ventaja competitiva en la próxima década.</div></div>""", unsafe_allow_html=True)

    # TAB 2: RIESGO
    with tabs[1]:
        cr1, cr2, cr3 = st.columns([3, 2, 2])
        with cr1:
            fig_corr = px.imshow(returns.corr(), text_auto=".2f", color_continuous_scale='RdBu_r')
            fig_corr.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', height=550)
            st.plotly_chart(fig_corr, use_container_width=True)
        with cr2:
            st.markdown("""<div class='info-panel'><div class='panel-header'>📊 Fundamentos de Correlación</div><div class='panel-body'>
            Utilizamos el <b>Coeficiente de Pearson</b> para cuantificar la dependencia lineal entre retornos diarios. La métrica se define como: <br>
            <div class='formula-box'>$$\\rho_{X,Y} = \\frac{\\text{cov}(X,Y)}{\\sigma_X \\sigma_Y}$$</div>
            Un coeficiente cercano a 1 indica un riesgo sistémico compartido, mientras que valores bajos permiten una diversificación efectiva. En este ecosistema tecnológico, las correlaciones tienden a ser elevadas debido a factores macroeconómicos comunes (tasas de la FED), lo que obliga a buscar activos con betas diferenciadas para proteger el capital.</div></div>""", unsafe_allow_html=True)
        with cr3:
            st.markdown("""<div class='info-panel'><div class='panel-header'>🛡️ Gestión de Riesgos Sistémicos</div><div class='panel-body'>
            La meta del administrador de riesgos es identificar la <b>mínima covarianza histórica</b> detectada. <br><br><b>Interpretación Gerencial:</b> Al entender qué activos no caen en sincronía, podemos construir un portafolio resiliente. Por ejemplo, la baja correlación relativa entre TSLA y MSFT en ciertos periodos permite que uno actúe como amortiguador del otro durante correcciones sectoriales. Ignorar estas relaciones resulta en una falsa sensación de diversificación donde todos los activos colapsan simultáneamente ante un shock externo.</div></div>""", unsafe_allow_html=True)

    # TAB 3: MARKOWITZ (RESTAURADO CON PUNTITOS)
    with tabs[2]:
        co1, co2, co3 = st.columns([3, 2, 2])
        
        # Simulación de Frontera Eficiente
        n_portfolios = 1500
        p_weights = np.zeros((n_portfolios, len(tickers)))
        p_ret = np.zeros(n_portfolios)
        p_vol = np.zeros(n_portfolios)
        
        for i in range(n_portfolios):
            weights = np.random.random(len(tickers))
            weights /= np.sum(weights)
            p_weights[i,:] = weights
            p_ret[i] = np.sum(returns.mean() * weights) * 252
            p_vol[i] = np.sqrt(np.dot(weights.T, np.dot(returns.cov() * 252, weights)))
        
        with co1:
            fig_f = px.scatter(x=p_vol, y=p_ret, color=p_ret, labels={'x':'Volatilidad Esperada', 'y':'Retorno Anualizado'}, title="Frontera Eficiente (Monte Carlo)")
            fig_f.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', height=550)
            st.plotly_chart(fig_f, use_container_width=True)
        with co2:
            st.markdown("""<div class='info-panel'><div class='panel-header'>🧬 Teoría de Cartera de Markowitz</div><div class='panel-body'>
            La optimización de media-varianza busca el conjunto de carteras que maximizan el retorno esperado para un nivel de riesgo determinado. <br>
            <div class='formula-box'>$$\\text{Minimizar: } \\sigma_p^2 = \\mathbf{w}^T \\mathbf{\\Sigma} \\mathbf{w}$$</div>
            Sujeto a que la suma de pesos $\\mathbf{w}$ sea igual a 1. Cada punto en la gráfica superior representa una combinación posible de inversión. La curva superior de este conjunto es la <b>Frontera Eficiente</b>, donde se encuentran las decisiones de inversión racionales.</div></div>""", unsafe_allow_html=True)
        with co3:
            st.markdown("""<div class='info-panel'><div class='panel-header'>🎯 Asimilación de Decisiones</div><div class='panel-body'>
            <b>Análisis de la Frontera:</b> Cualquier punto por debajo de la frontera es ineficiente, pues ofrece menos retorno por el mismo riesgo. <br><br><b>Acción Sugerida:</b> Nuestra terminal se enfoca en el punto de <b>Variancia Mínima</b> (el extremo izquierdo). En un entorno de alta incertidumbre, priorizamos la estabilidad sobre el retorno agresivo. Esta estrategia es ideal para inversores institucionales que buscan preservar capital mientras mantienen exposición al crecimiento tecnológico global.</div></div>""", unsafe_allow_html=True)

    # TAB 4: CALCULADORA (CON PIE CHART LIMPIA)
    with tabs[3]:
        def min_v(w): return np.sqrt(np.dot(w.T, np.dot(returns.cov() * 252, w)))
        res = minimize(min_v, [1./len(tickers)]*len(tickers), method='SLSQP', bounds=tuple((0,1) for _ in range(len(tickers))), constraints={'type':'eq','fun':lambda x: np.sum(x)-1})
        
        # FILTRO DE 0% PARA ESTÉTICA
        f_labels = [tickers[i] for i, w in enumerate(res.x) if w > 0.01]
        f_values = [w for w in res.x if w > 0.01]
        
        sc1, sc2, sc3 = st.columns([2.5, 2, 2.5])
        with sc1:
            fig_pie = go.Figure(data=[go.Pie(labels=f_labels, values=f_values, hole=.5, textinfo='percent+label')])
            fig_pie.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', height=500, showlegend=True)
            st.plotly_chart(fig_pie, use_container_width=True)
        with sc2:
            capital = st.number_input("💵 Capital a Invertir (USD)", min_value=1000, value=10000, step=1000)
            st.markdown("---")
            dist_df = pd.DataFrame({'Activo': f_labels, 'Monto Sugerido': [v * capital for v in f_values]})
            st.table(dist_df.style.format({"Monto Sugerido": "${:,.2f}"}))
        with sc3:
            st.markdown(f"""<div class='info-panel'><div class='panel-header'>💰 Recomendación Gerencial Final</div><div class='panel-body'>
            El algoritmo sugiere una concentración principal en <b>{f_labels[np.argmax(f_values)]}</b>. <br><br>
            <b>Estrategia de Ejecución:</b><br>
            1. <b>Dollar Cost Averaging:</b> Divida su entrada en 4 tramos para mitigar el riesgo de "market timing". <br>
            2. <b>Stop-Loss Estratégico:</b> Mantenga una salida activa si el portafolio total retrocede más de un 15%. <br>
            3. <b>Horizonte:</b> Este modelo está calibrado para una ventana mínima de 12-18 meses para permitir que las ventajas competitivas de las Big Tech se materialicen en valor para el accionista.</div></div>""", unsafe_allow_html=True)

    st.markdown("---")
    st.caption("Terminal de Inteligencia Financiera | Universidad Externado de Colombia | Dominick Vargas")

except Exception as e:
    st.error(f"Fallo en el núcleo: {e}")
