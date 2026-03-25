import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go
import plotly.express as px
from scipy.optimize import minimize
import numpy as np

# 1. CONFIGURACIÓN DEL SISTEMA ACADÉMICO
st.set_page_config(page_title="Terminal Gerencial Big Tech", layout="wide", initial_sidebar_state="collapsed")

# 2. CSS: ARQUITECTURA VISUAL ADAPTABLE (FIX PARA TEMA CLARO/OSCURO)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Inter:wght@300;400;600&display=swap');
    
    /* Fondo adaptable al tema del navegador */
    .stApp { background: var(--background-color); }
    
    /* Contenedores de KPIs y Análisis ADAPTABLES (Sin fondo fijo) */
    div[data-testid="stMetric"], .executive-brief {
        background: transparent !important;
        border: 1px solid var(--text-color);
        border-radius: 12px;
        padding: 25px;
        margin-bottom: 25px;
        color: var(--text-color) !important;
        transition: 0.3s;
    }
    
    /* Glow sutil en KPIs al pasar el mouse (Adaptable) */
    div[data-testid="stMetric"]:hover {
        border-color: #58a6ff;
        box-shadow: 0 0 20px rgba(88, 166, 255, 0.2);
    }
    
    /* Tipografía adaptable */
    h1, h2, h3 { font-family: 'Orbitron', sans-serif; color: var(--text-color); letter-spacing: 2px; }
    .stTabs [data-baseweb="tab"] { color: var(--text-color); }
    
    .brief-title { font-family: 'Orbitron', sans-serif; color: #58a6ff; font-size: 1.3rem; margin-bottom: 15px; text-transform: uppercase; border-bottom: 1px solid var(--text-color); padding-bottom: 10px; }
    .brief-text { font-family: 'Inter', sans-serif; line-height: 1.9; text-align: justify; font-size: 1.05rem; }
    b, .methodology { color: #58a6ff; }
    
    /* Estilo para las alertas de texto de la gráfica */
    .label-alert { color: #f85149; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

@st.cache_data(ttl=300)
def get_pro_data():
    tickers = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'NVDA', 'META', 'TSLA']
    df = yf.download(tickers, period="2y", interval="1d", progress=False)['Close']
    return df

# --- CUERPO PRINCIPAL ---
try:
    df = get_pro_data()
    returns = df.pct_change().dropna()
    tickers = df.columns

    st.title("🏛️ TERMINAL GERENCIAL DE PORTAFOLIOS BIG TECH")
    st.markdown("---")

    # 1. MONITOR DE ACTIVOS (KPIs Adaptables)
    m_cols = st.columns(len(tickers))
    for i, t in enumerate(tickers):
        curr = df[t].iloc[-1]
        ytd = (curr / df[t].iloc[0] - 1) * 100
        # Streamlit ajusta automáticamente el color de la métrica según el tema
        m_cols[i].metric(t, f"${curr:.2f}", f"{ytd:.1f}% YTD")

    # 2. PANELES DE ANÁLISIS DE PROFUNDIDAD MÁXIMA
    tab_macro, tab_risk, tab_alpha, tab_frontier = st.tabs([
        "🌎 Desempeño Macro", "🛡️ Gestión de Riesgo", "🧬 Optimización Markowitz", "📈 Frontera Eficiente"
    ])

    with tab_macro:
        col_m1, col_m2 = st.columns([3, 2])
        with col_m1:
            fig = go.Figure()
            for t in tickers:
                norm = (data[t] / data[t].iloc[0]) * 100
                fig.add_trace(go.Scatter(x=data.index, y=norm, name=t, line=dict(width=3, shape='spline')))
            # Plantilla adaptable
            fig.update_layout(
                template="plotly_dark", 
                paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', 
                height=600, font_color=var(--text-color)
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col_m2:
            st.markdown(f"""
            <div class='executive-brief'>
                <div class='brief-title'>Análisis de Ciclo Económico: Normalización</div>
                <div class='brief-text'>
                    <b>1. Metodología de la Gráfica:</b> Esta visualización no utiliza los precios nominales (los $250 o $500 que vale una acción), ya que sería imposible compararlas en una misma escala. Utilizamos la técnica de <b>Normalización a Base 100</b>.<br>
                    <span class='methodology'>Fórmula: Precio<sub>t</sub> / Precio<sub>t0</sub> * 100.</span><br>
                    Esto significa que todos los activos parten de un valor hipotético de "100" en el primer día de datos, permitiéndonos visualizar el crecimiento porcentual real de cada uno independientemente de su valor de mercado. <br><br>
                    <b>2. Guía de Interpretación:</b> El eje Y representa el crecimiento relativo. Si una línea está en 150, significa que ha crecido un 50% desde el inicio de los datos. Como administrador, usted debe buscar qué activo muestra la línea con la pendiente más constante y positiva, identificando al líder del ciclo actual.<br><br>
                    <b>3. Relevancia Gerencial:</b> Esta gráfica permite identificar la rotación de capital sectorial. Nos ayuda a responder: ¿Cuál de las Big Tech es la que realmente está capitalizando la tendencia actual?.
                </div>
            </div>
            """, unsafe_allow_html=True)

    with tab_risk:
        r_col1, r_col2 = st.columns([2.5, 2])
        with r_col1:
            corr = returns.corr()
            fig_corr = px.imshow(corr, text_auto=".2f", color_continuous_scale='RdBu_r')
            fig_corr.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=550)
            st.plotly_chart(fig_corr, use_container_width=True)
        
        with r_col2:
            st.markdown(f"""
            <div class='executive-brief'>
                <div class='brief-title'>Matriz de Correlación: Riesgo Sistémico</div>
                <div class='brief-text'>
                    <b>1. Metodología y Parámetros:</b> Esta matriz cuantifica el grado de sincronía entre los activos. Utilizamos el Coeficiente de Correlación de Pearson, que analiza los retornos logarítmicos diarios durante el último año. El parámetro <b>'ticker'</b> en los ejes X e Y hace referencia a los símbolos bursátiles de las empresas (AAPL, NVDA, etc.).<br><br>
                    <b>2. Guía de Interpretación:</b> <br>
                    • Los valores van de -1.0 a 1.0.<br>
                    • <b>1.0 (Rojo Intenso):</b> Los activos se mueven de forma idéntica.<br>
                    • <b>0.0 (Gris):</b> No hay relación entre sus movimientos.<br>
                    • <b>-1.0 (Azul Intenso):</b> Se mueven en direcciones opuestas.<br>
                    Una correlación superior a 0.70 indica que diversificar entre ellos no ofrece protección real.<br><br>
                    <b>3. Por Qué es Vital:</b> Permite detectar el "Riesgo Beta". Si su portafolio tiene correlaciones muy altas, un evento negativo en el sector tecnológico afectará a todos sus activos por igual, anulando los beneficios de la diversificación.
                </div>
            </div>
            """, unsafe_allow_html=True)

    with tab_alpha:
        a_col1, a_col2 = st.columns([2.5, 2])
        with a_col1:
            def min_vol(w): return np.sqrt(np.dot(w.T, np.dot(returns.cov() * 252, w)))
            res = minimize(min_vol, [1./len(tickers)]*len(tickers), method='SLSQP', bounds=tuple((0,1) for _ in range(len(tickers))), constraints={'type':'eq','fun':lambda x: np.sum(x)-1})
            
            # --- FIX PARA EL EMPASTE DE ETIQUETAS ---
            # Ocultamos etiquetas de activos con peso inferior al 1% (0.01)
            weights_viz = res.x
            labels_viz = tickers
            pie_markers = dict(colors=px.colors.sequential.Electric_r)
            
            # Si el peso es muy pequeño, la etiqueta no se muestra
            fig_pie = go.Figure(data=[go.Pie(
                labels=labels_viz, 
                values=weights_viz, 
                hole=.5, 
                marker=pie_markers,
                textinfo='percent+label' if weights_viz.any() > 0.01 else 'percent' # Fix de visibilidad
            )])
            fig_pie.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', height=500, showlegend=False)
            st.plotly_chart(fig_pie, use_container_width=True)
            
        with a_col2:
            st.markdown(f"""
            <div class='executive-brief'>
                <div class='brief-title'>Optimización Markowitz: Portafolio de Variancia Mínima</div>
                <div class='brief-text'>
                    <b>1. Metodología de la Gráfica:</b> Esta gráfica de anillo representa la distribución de capital sugerida por la **Teoría Moderna de Portafolio de Harry Markowitz**. <br>
                    <span class='methodology'>Objetivo: Encontrar los pesos de inversión (variables dependientes) que minimizan la Volatilidad Anualizada del portafolio total (función objetivo).</span><br>
                    Los parámetros de entrada son la matriz de varianza-covarianza histórica de los activos seleccionados.<br><br>
                    <b>2. Guía de Interpretación:</b> Cada sector del anillo representa el porcentaje exacto de dinero que debe invertir en cada acción. <span class='label-alert'>Nota: Los activos que no aparecen en el anillo tienen pesos menores al 1%, por lo que se ocultaron para evitar el empaste visual.</span>.<br><br>
                    <b>3. Relevancia Gerencial:</b> Esta gráfica responde a: ¿Cómo debo repartir mi dinero para tener el mínimo riesgo posible? Esto maximiza el <b>Ratio de Sharpe</b>, que mide cuánto retorno obtenemos por cada unidad de riesgo asumida.
                </div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("---")
    st.caption("Terminal Gerencial de Portafolios Big Tech | Dominick Vargas Parra | Universidad Externado de Colombia")

except Exception as e:
    st.error(f"Fallo en el núcleo de datos: {e}")
