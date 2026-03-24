import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go
import plotly.express as px
from scipy.optimize import minimize
import numpy as np

# 1. CONFIGURACIÓN DEL SISTEMA GERENCIAL
st.set_page_config(page_title="Sistema de Optimización Big Tech", layout="wide", initial_sidebar_state="collapsed")

# 2. CSS: ARQUITECTURA VISUAL "EXECUTIVE DARK"
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

# --- CUERPO PRINCIPAL ---
try:
    df = get_strategic_data()
    returns = df.pct_change().dropna()
    tickers = df.columns

    st.title("🏛️ SISTEMA DE OPTIMIZACIÓN DE PORTAFOLIOS BIG TECH")
    st.markdown("---")

    # 1. MONITOR DE ACTIVOS (KPIs)
    m_cols = st.columns(len(tickers))
    for i, t in enumerate(tickers):
        curr = df[t].iloc[-1]
        ytd = (curr / df[t].iloc[0] - 1) * 100
        m_cols[i].metric(t, f"${curr:.2f}", f"{ytd:.1f}% YTD")

    # 2. PANELES DE ANÁLISIS ESTRATÉGICO
    tab_macro, tab_risk, tab_alpha, tab_frontier = st.tabs([
        "🌎 Desempeño Macro", "🛡️ Gestión de Riesgo", "🧬 Optimización Markowitz", "📈 Frontera Eficiente"
    ])

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
            st.markdown(f"""
            <div class='executive-brief'>
                <div class='brief-title'>Análisis de Ciclo Económico</div>
                <div class='brief-text'>
                    El rendimiento actual de las Big Tech refleja una <b>reconfiguración estructural</b> impulsada por la eficiencia operativa y la IA. 
                    Este fenómeno se valida mediante la normalización de precios (Base 100), permitiendo una comparativa directa de crecimiento porcentual 
                    independiente del valor nominal de cada acción.<br><br>
                    <b>Justificación de la Tendencia:</b> El mercado está premiando la "opcionalidad estratégica". Las empresas con mayor integración vertical 
                    están logrando capturar márgenes que antes se diluían en la cadena de suministro. <br><br>
                    <b>Recomendación Gerencial:</b> Se aconseja mantener una postura de acumulación en activos con flujos de caja libre (FCF) crecientes, 
                    ya que actúan como refugio ante la volatilidad de las tasas de interés.
                </div>
            </div>
            """, unsafe_allow_html=True)

    with tab_risk:
        r_col1, r_col2 = st.columns([2.5, 2])
        with r_col1:
            corr = returns.corr()
            fig_corr = px.imshow(corr, text_auto=".2f", color_continuous_scale='RdBu_r')
            fig_corr.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=550)
            st.plotly_chart(fig_corr, use_container_width=True)
        
        with r_col2:
            st.markdown(f"""
            <div class='executive-brief'>
                <div class='brief-title'>Diagnóstico de Correlación y Beta</div>
                <div class='brief-text'>
                    La matriz de covarianza revela una interdependencia crítica en el sector. Una correlación superior a 0.70 indica que los activos 
                    responden de forma casi idéntica a shocks macroeconómicos, lo que anula la diversificación tradicional.<br><br>
                    <b>Metodología:</b> Estos valores se obtienen mediante el Coeficiente de Pearson sobre retornos logarítmicos. Es una medida 
                    estadística pura que cuantifica el grado en que dos activos se mueven en tándem.<br><br>
                    <b>Acción Estratégica:</b> Para mitigar el Riesgo Beta, se recomienda la inclusión de activos descorrelacionados que protejan 
                    el portafolio durante eventos de "cisne negro" en el sector tecnológico.
                </div>
            </div>
            """, unsafe_allow_html=True)

    with tab_alpha:
        a_col1, a_col2 = st.columns([2.5, 2])
        with a_col1:
            def min_vol(w): return np.sqrt(np.dot(w.T, np.dot(returns.cov() * 252, w)))
            res = minimize(min_vol, [1./len(tickers)]*len(tickers), method='SLSQP', bounds=tuple((0,1) for _ in range(len(tickers))), constraints={'type':'eq','fun':lambda x: np.sum(x)-1})
            fig_pie = go.Figure(data=[go.Pie(labels=tickers, values=res.x, hole=.5, marker=dict(colors=px.colors.sequential.Electric))])
            fig_pie.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', height=500)
            st.plotly_chart(fig_pie, use_container_width=True)
            
        with a_col2:
            st.markdown(f"""
            <div class='executive-brief'>
                <div class='brief-title'>Optimización Eficiente de Markowitz</div>
                <div class='brief-text'>
                    Este modelo busca el <b>Portafolio de Variancia Mínima</b>. El algoritmo redistribuye el capital basándose en la 
                    Teoría Moderna de Portafolio para minimizar el riesgo total sin sacrificar la exposición al mercado.<br><br>
                    <b>Lógica Técnica:</b> Se utiliza programación cuadrática para encontrar el punto exacto donde la covarianza combinada 
                    de los activos es la menor posible. Esto maximiza el <b>Ratio de Sharpe</b>, que mide cuánto retorno obtenemos por cada 
                    unidad de riesgo asumido.<br><br>
                    <b>Hoja de Ruta:</b> Rebalanceo mensual obligatorio para mantener los pesos sugeridos y evitar la concentración 
                    accidental por movimientos de precios.
                </div>
            </div>
            """, unsafe_allow_html=True)

    with tab_frontier:
        f_col1, f_col2 = st.columns([3, 2])
        with f_col1:
            # Generación de portafolios aleatorios para la Frontera
            results = []
            for _ in range(1000):
                w = np.random.random(len(tickers))
                w /= np.sum(w)
                r = np.sum(returns.mean() * w) * 252
                v = np.sqrt(np.dot(w.T, np.dot(returns.cov() * 252, w)))
                results.append([v, r])
            
            f_df = pd.DataFrame(results, columns=['Riesgo (Volatilidad)', 'Retorno Esperado'])
            fig_f = px.scatter(f_df, x='Riesgo (Volatilidad)', y='Retorno Esperado', color='Retorno Esperado', color_continuous_scale='Viridis')
            fig_f.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=550)
            st.plotly_chart(fig_f, use_container_width=True)
            
        with f_col2:
            st.markdown(f"""
            <div class='executive-brief'>
                <div class='brief-title'>Análisis de Frontera Eficiente</div>
                <div class='brief-text'>
                    Esta visualización representa el <b>Conjunto de Oportunidades de Inversión</b>. Cada punto es una combinación posible 
                    de las acciones de Big Tech analizadas.<br><br>
                    <b>Interpretación de Datos:</b> Los puntos en el borde superior izquierdo representan los portafolios más eficientes; 
                    aquellos que ofrecen el máximo retorno para un nivel dado de riesgo. Como administrador, su objetivo es desplazar 
                    su inversión hacia esa curva "límite".<br><br>
                    <b>Metodología:</b> Simulamos 1,000 combinaciones aleatorias de pesos (Monte Carlo simple) para mapear el espectro 
                    de riesgo-retorno. Esto permite visualizar la relación entre la volatilidad anualizada y la rentabilidad proyectada.<br><br>
                    <b>Decisión Estratégica:</b> Los activos que se encuentran lejos de la frontera (hacia la derecha) están aportando 
                    riesgo innecesario al portafolio sin una compensación justa en retorno.
                </div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("---")
    st.caption("Sistema de Optimización | Dominick Vargas Parra | Universidad Externado de Colombia")

except Exception as e:
    st.error(f"Fallo en el núcleo de datos: {e}")
