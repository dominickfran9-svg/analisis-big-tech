import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go
import plotly.express as px
from scipy.optimize import minimize
import numpy as np

# 1. CONFIGURACIÓN DEL SISTEMA GERENCIAL
st.set_page_config(page_title="Terminal Gerencial Big Tech", layout="wide", initial_sidebar_state="collapsed")

# 2. CSS: ARQUITECTURA VISUAL ADAPTABLE (FIX PARA TEMAS Y KPI BOXES)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Inter:wght@300;400;600&display=swap');
    
    /* Contenedores Adaptables: Se ajustan al color de fondo del tema del navegador */
    div[data-testid="stMetric"], .executive-brief {
        background: rgba(13, 17, 23, 0.05) !important;
        border: 1px solid #30363d !important;
        border-radius: 12px;
        padding: 25px;
        margin-bottom: 25px;
        transition: 0.3s;
    }
    
    /* Ajuste de tipografía para visibilidad en temas claros y oscuros */
    h1, h2, h3 { font-family: 'Orbitron', sans-serif; letter-spacing: 2px; }
    .brief-title { font-family: 'Orbitron', sans-serif; color: #58a6ff; font-size: 1.2rem; margin-bottom: 15px; text-transform: uppercase; border-bottom: 1px solid #30363d; padding-bottom: 10px; }
    .brief-text { font-family: 'Inter', sans-serif; line-height: 1.8; text-align: justify; font-size: 1rem; }
    b { color: #58a6ff; }
    .formula { font-family: 'Courier New', monospace; background: rgba(88, 166, 255, 0.1); padding: 2px 5px; border-radius: 4px; }
    </style>
    """, unsafe_allow_html=True)

@st.cache_data(ttl=600)
def get_clean_data():
    tickers = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'NVDA', 'META', 'TSLA']
    # Descarga de datos históricos de los últimos 2 años
    df = yf.download(tickers, period="2y", interval="1d", progress=False)['Close']
    return df

# --- NÚCLEO DE PROCESAMIENTO ---
try:
    df = get_clean_data()
    returns = df.pct_change().dropna()
    tickers = df.columns

    st.title("🏛️ SISTEMA DE OPTIMIZACIÓN DE PORTAFOLIOS BIG TECH")
    st.markdown("---")

    # 1. MONITOR DE ACTIVOS (KPIs)
    m_cols = st.columns(len(tickers))
    for i, t in enumerate(tickers):
        actual = df[t].iloc[-1]
        ytd = (actual / df[t].iloc[0] - 1) * 100
        m_cols[i].metric(t, f"${actual:.2f}", f"{ytd:.1f}% YTD")

    # 2. PANELES DE ANÁLISIS DE ALTA PROFUNDIDAD
    tabs = st.tabs(["🌎 Desempeño Macro", "🛡️ Gestión de Riesgo", "🧬 Optimización Markowitz", "📈 Frontera Eficiente"])

    with tabs[0]:
        c1, c2 = st.columns([3, 2])
        with c1:
            fig_p = go.Figure()
            for t in tickers:
                # Normalización Base 100 para comparativa directa
                norm = (df[t] / df[t].iloc[0]) * 100
                fig_p.add_trace(go.Scatter(x=df.index, y=norm, name=t, line=dict(width=2.5)))
            fig_p.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=550)
            st.plotly_chart(fig_p, use_container_width=True)
        
        with c2:
            st.markdown(f"""
            <div class='executive-brief'>
                <div class='brief-title'>Análisis de Normalización Base 100</div>
                <div class='brief-text'>
                    <b>¿Cómo se obtuvo esta gráfica?</b> Se aplica la fórmula <span class='formula'>(Precio_t / Precio_0) * 100</span>. Esto permite comparar activos con precios nominales muy distantes (como acciones de $170 vs $600) bajo una misma métrica de crecimiento porcentual.<br><br>
                    <b>Guía de Lectura:</b> El punto de partida de todas las líneas es 100. Si una línea alcanza los 150, el activo ha rendido un 50% de beneficio acumulado en el periodo.<br><br>
                    <b>Interpretación Gerencial:</b> Observe la dispersión de las líneas. Una mayor separación indica que el mercado está diferenciando claramente el valor de cada compañía, rompiendo la tendencia de crecimiento sincronizado del sector.
                </div>
            </div>
            """, unsafe_allow_html=True)

    with tabs[1]:
        cr1, cr2 = st.columns([2.5, 2])
        with cr1:
            corr_m = returns.corr()
            fig_c = px.imshow(corr_m, text_auto=".2f", color_continuous_scale='RdBu_r')
            fig_c.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=500)
            st.plotly_chart(fig_c, use_container_width=True)
        
        with cr2:
            st.markdown(f"""
            <div class='executive-brief'>
                <div class='brief-title'>Interpretación de Matriz de Correlación</div>
                <div class='brief-text'>
                    <b>Metodología:</b> Se utiliza el <b>Coeficiente de Pearson</b>. El término <b>Ticker</b> en los ejes representa las siglas de las empresas.<br><br>
                    <b>Cómo leer los números:</b><br>
                    • <b>1.00:</b> Relación perfecta (el activo consigo mismo).<br>
                    • <b>0.70+:</b> Alta correlación. Si una acción cae, la otra probablemente también lo hará.<br>
                    • <b>Cerca de 0:</b> Movimientos independientes.<br><br>
                    <b>Uso Estratégico:</b> Un administrador busca correlaciones bajas para evitar que todo el portafolio sufra simultáneamente ante una noticia negativa del sector tecnológico.
                </div>
            </div>
            """, unsafe_allow_html=True)

    with tabs[2]:
        co1, co2 = st.columns([2.5, 2])
        with co1:
            # Algoritmo de Variancia Mínima de Markowitz
            def min_v(w): return np.sqrt(np.dot(w.T, np.dot(returns.cov() * 252, w)))
            res = minimize(min_v, [1./len(tickers)]*len(tickers), method='SLSQP', bounds=tuple((0,1) for _ in range(len(tickers))), constraints={'type':'eq','fun':lambda x: np.sum(x)-1})
            
            # Filtro para limpiar el "empaste" visual de etiquetas pequeñas
            v_weights = [w if w > 0.01 else 0 for w in res.x]
            fig_o = go.Figure(data=[go.Pie(labels=tickers, values=v_weights, hole=.5)])
            fig_o.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', height=500, showlegend=True)
            st.plotly_chart(fig_o, use_container_width=True)
        
        with co2:
            lider_p = tickers[np.argmax(res.x)]
            st.markdown(f"""
            <div class='executive-brief'>
                <div class='brief-title'>Asignación Inteligente de Capital</div>
                <div class='brief-text'>
                    <b>Origen de los Datos:</b> Esta gráfica es el resultado de resolver un problema de optimización matemática que busca la <b>Mínima Variancia</b> histórica del conjunto.<br><br>
                    <b>Qué representan los sectores:</b> Cada color es la proporción del capital que el modelo sugiere invertir en cada empresa para reducir el riesgo total. En este momento, la mayor concentración se sugiere en <b>{lider_p}</b> debido a su estabilidad relativa frente al grupo.<br><br>
                    <b>Interpretación:</b> Si un activo tiene un sector muy pequeño o no aparece, es porque su volatilidad o alta correlación con los demás lo hacen ineficiente para este modelo de protección de capital.
                </div>
            </div>
            """, unsafe_allow_html=True)

    with tabs[3]:
        cf1, cf2 = st.columns([3, 2])
        with cf1:
            results = []
            for _ in range(800): # Simulación Monte Carlo
                w = np.random.random(len(tickers))
                w /= np.sum(w)
                r_sim = np.sum(returns.mean() * w) * 252
                v_sim = np.sqrt(np.dot(w.T, np.dot(returns.cov() * 252, w)))
                results.append([v_sim, r_sim])
            
            f_df = pd.DataFrame(results, columns=['Volatilidad (Riesgo)', 'Retorno'])
            fig_f = px.scatter(f_df, x='Volatilidad (Riesgo)', y='Retorno', color='Retorno', color_continuous_scale='Viridis')
            fig_f.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=550)
            st.plotly_chart(fig_f, use_container_width=True)
            
        with cf2:
            st.markdown(f"""
            <div class='executive-brief'>
                <div class='brief-title'>Análisis de Frontera Eficiente</div>
                <div class='brief-text'>
                    <b>Metodología:</b> Se simulan 800 combinaciones aleatorias de portafolios para mapear todas las posibilidades de riesgo-retorno.<br><br>
                    <b>Guía de Interpretación:</b> <br>
                    • <b>Eje X:</b> Representa el riesgo (volatilidad). Cuanto más a la derecha, más "nervioso" es el portafolio.<br>
                    • <b>Eje Y:</b> Representa el retorno esperado.<br><br>
                    <b>Decisión Gerencial:</b> Los puntos en el borde superior izquierdo son los <b>Portafolios Eficientes</b>. Un administrador inteligente nunca elegiría un punto a la derecha de la curva, ya que estaría asumiendo más riesgo por el mismo nivel de retorno.
                </div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("---")
    st.caption("Terminal Gerencial | Dominick Vargas Parra | Universidad Externado de Colombia")

except Exception as e:
    st.error(f"Fallo en el núcleo de datos: {e}")
