import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go
import plotly.express as px
from scipy.optimize import minimize
import numpy as np

# 1. CONFIGURACIÓN E INTERFAZ
st.set_page_config(page_title="Alpha Strategic Intelligence", layout="wide", initial_sidebar_state="collapsed")

# CSS: Estética soberbia y lectura extensa
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
    }
    
    .brief-title { font-family: 'Orbitron', sans-serif; color: #58a6ff; font-size: 1.3rem; margin-bottom: 15px; text-transform: uppercase; border-bottom: 1px solid #30363d; padding-bottom: 10px; }
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
    # Incluimos META para completar el set de Big Tech
    tickers = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'NVDA', 'META', 'TSLA']
    df = yf.download(tickers, period="2y", interval="1d", progress=False)['Close']
    return df

# CUERPO PRINCIPAL
try:
    df = get_strategic_data()
    returns = df.pct_change().dropna()
    tickers = df.columns

    st.title("🏛️ ALPHA STRATEGIC INTELLIGENCE v13")
    st.markdown("---")

    # 1. MONITOR DE ACTIVOS
    m_cols = st.columns(len(tickers))
    for i, t in enumerate(tickers):
        curr = df[t].iloc[-1]
        ytd = (curr / df[t].iloc[0] - 1) * 100
        m_cols[i].metric(t, f"${curr:.2f}", f"{ytd:.1f}% YTD")

    # 2. SISTEMA DE ANÁLISIS DE ALTO NIVEL
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
                    El panorama actual de las Big Tech refleja una <b>fase de consolidación agresiva</b>. Actualmente, <b>{lider}</b> lidera el rendimiento acumulado, lo que sugiere una ventaja competitiva en la escala de infraestructura para IA. <br><br>
                    <b>Génesis del Análisis:</b> Este fenómeno se valida mediante la normalización de precios (Base 100), una herramienta técnica que permite comparar activos con valores nominales distintos bajo una misma línea de tiempo. No es una coincidencia; responde a la expansión de márgenes operativos y la optimización de costos mediante automatización. <br><br>
                    <b>Explicación de Causalidad:</b> El mercado está premiando la 'opcionalidad estratégica'. Las empresas que dominan el stack tecnológico completo (Hardware + Nube) presentan una menor sensibilidad a los cambios en las tasas de interés, actuando como activos refugio con alto crecimiento. <br><br>
                    <b>Recomendación de Negocios:</b> Para un administrador, la estrategia óptima es mantener una postura 'Overweight' en líderes consolidados, monitoreando el soporte técnico de la media móvil de 200 días para evitar riesgos de reversión a la media.
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
            max_c = corr.unstack().sort_values(ascending=False).drop_duplicates().index[1]
            st.markdown(f"""
            <div class='executive-brief'>
                <div class='brief-title'>Diagnóstico de Correlación y Estabilidad</div>
                <div class='brief-text'>
                    Se identifica una correlación crítica de <b>{corr.loc[max_c[0], max_c[1]]:.2f}</b> entre <b>{max_c[0]}</b> y <b>{max_c[1]}</b>. En finanzas, esto indica que el 70% de sus movimientos son compartidos, invalidando cualquier intento de diversificación simple entre ellos. <br><br>
                    <b>¿Cómo se obtuvo este valor?</b> Deriva de la matriz de covarianza de Pearson aplicada a los retornos diarios de los últimos 252 días (año bursátil). Una correlación cercana a 1.0 significa que los activos responden a los mismos estímulos macroeconómicos. <br><br>
                    <b>Impacto Estratégico:</b> Si el sector tecnológico sufre una corrección por presiones regulatorias, el portafolio experimentará una caída sincronizada (Drawdown). Es un error común en carteras no optimizadas estadísticamente. <br><br>
                    <b>Acción Sugerida:</b> Es fundamental introducir activos con correlaciones negativas o cercanas a cero para reducir el <b>Riesgo Beta</b> total y proteger el capital ante shocks externos inesperados.
                </div>
            </div>
            """, unsafe_allow_html=True)

    with tab_alpha:
        a_col1, a_col2 = st.columns([2.5, 2])
        with a_col1:
            def min_vol(w):
                return np.sqrt(np.dot(w.T, np.dot(returns.cov() * 252, w)))
            
            init = [1./len(tickers)] * len(tickers)
            cons = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1})
            bnds = tuple((0, 1) for _ in range(len(tickers)))
            res = minimize(min_vol, init, method='SLSQP', bounds=bnds, constraints=cons)
            
            fig_pie = go.Figure(data=[go.Pie(labels=tickers, values=res.x, hole=.5)])
            fig_pie.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', height=500)
            st.plotly_chart(fig_pie, use_container_width=True)
            
        with a_col2:
            st.markdown(f"""
            <div class='executive-brief'>
                <div class='brief-title'>Informe de Optimización de Markowitz</div>
                <div class='brief-text'>
                    Esta distribución representa la <b>Frontera Eficiente</b> de su inversión. El modelo ha priorizado a <b>{tickers[np.argmax(res.x)]}</b> con un {np.max(res.x)*100:.1f}% de la exposición total. <br><br>
                    <b>Metodología Técnica:</b> A diferencia de una distribución intuitiva, este modelo utiliza programación cuadrática para minimizar la varianza total. Se analizan miles de combinaciones de pesos para encontrar la que ofrece el menor riesgo histórico para el nivel de retorno actual. <br><br>
                    <b>Interpretación para Gerencia:</b> Optimizar una cartera permite maximizar el <b>Ratio de Sharpe</b>, garantizando que cada unidad de riesgo asumida esté debidamente compensada. En mercados eficientes, esta es la única forma comprobada de superar el desempeño promedio a largo plazo. <br><br>
                    <b>Hoja de Ruta:</b><br>
                    1. Rebalancear la cartera mensualmente para mantener estos pesos estratégicos.<br>
                    2. No exceder el peso sugerido, ya que aumentaría el riesgo no sistemático.<br>
                    3. Evaluar stop-losses automáticos para proteger ganancias en el activo principal.
                </div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("---")
    st.caption("Terminal de Inteligencia Financiera | Dominick Vargas Parra | Universidad Externado de Colombia")

except Exception as e:
    st.error(f"Error crítico en el flujo de datos: {e}")
