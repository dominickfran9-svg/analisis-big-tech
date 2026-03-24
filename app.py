import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go
from scipy.optimize import minimize
import numpy as np

# Configuración de Terminal Pro (1. Sin Scanner Visual)
st.set_page_config(page_title="Alpha Trading Terminal", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=JetBrains+Mono:wght@300;500&display=swap');
    
    /* Fondo limpio y oscuro */
    .main { background: #0d1117; }
    
    /* ELIMINADO EL EFECTO SCANNER (stApp::before) */

    /* Estilo de contenedores */
    div[data-testid="stMetric"] {
        background: rgba(22, 27, 34, 0.7) !important;
        border: 1px solid #30363d !important;
        border-radius: 12px !important;
        padding: 15px !important;
        transition: 0.3s;
    }
    div[data-testid="stMetric"]:hover {
        border-color: #58a6ff !important;
        box-shadow: 0 0 20px rgba(88, 166, 255, 0.1) !important;
    }

    h1, h2, h3 { font-family: 'Orbitron', sans-serif; color: #58a6ff; }
    code { font-family: 'JetBrains Mono', monospace; }
    
    /* Estilo para las Noticias */
    .news-box {
        background: rgba(22, 27, 34, 0.5);
        border-left: 5px solid;
        border-radius: 5px;
        padding: 10px;
        margin-bottom: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

@st.cache_data(ttl=300)
def get_terminal_data():
    tickers = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'NVDA', 'META', 'TSLA']
    df = yf.download(tickers, period="2y", interval="1d", progress=False)['Close']
    return df

try:
    data = get_terminal_data()
    returns = data.pct_change().dropna()
    tickers = data.columns
    
    # --- HEADER ---
    st.title("💹 ALPHA TRADING TERMINAL v5")
    st.markdown("---")

    # --- MÉTRICAS EN TIEMPO REAL ---
    m_cols = st.columns(len(tickers))
    for i, tick in enumerate(tickers):
        val = data[tick].iloc[-1]
        delta = (val / data[tick].iloc[-2] - 1) * 100
        m_cols[i].metric(tick, f"${val:.1f}", f"{delta:.2f}%")

    st.markdown("<br>", unsafe_allow_html=True)

    # --- ZONA DE ANÁLISIS ---
    tab_opt, tab_news = st.tabs(["🧬 Optimización Inteligente", "📰 Inteligencia de Contexto"])

    with tab_opt:
        col_opt1, col_opt2 = st.columns([2, 1])
        
        with col_opt1:
            st.subheader("Cálculo de Portafolio Eficiente (Frontera)")
            cash_opt = st.number_input("Capital a Optimizar (USD)", value=10000)
            
            # --- LÓGICA DE OPTIMIZACIÓN DE PORTAFOLIO (NIVEL EXTERNADO PRO) ---
            def get_ret_vol_sharpe(weights):
                weights = np.array(weights)
                ret = np.sum(returns.mean() * weights) * 252 # Retorno anualizado
                vol = np.sqrt(np.dot(weights.T, np.dot(returns.cov() * 252, weights))) # Volatilidad anualizada
                sharpe = ret / vol # Ratio de Sharpe simplificado
                return np.array([ret, vol, sharpe])

            # Minimizar la volatilidad negativa (que es maximizar el Ratio de Sharpe)
            def minimize_volatility(weights):
                return get_ret_vol_sharpe(weights)[1] # Queremos minimizar la vol

            num_tickers = len(tickers)
            init_guess = num_tickers * [1.0/num_tickers] # Suposición inicial: todo igual
            bounds = tuple((0,1) for _ in range(num_tickers)) # No shorts: pesos entre 0 y 1
            cons = ({'type':'eq', 'fun': lambda x: np.sum(x)-1}) # La suma de pesos debe ser 1

            # Ejecutar optimizador
            opt_results = minimize(minimize_volatility, init_guess, method='SLSQP', bounds=bounds, constraints=cons)
            opt_weights = opt_results.x
            
            # Visualización
            fig_opt = go.Figure()
            fig_opt.add_trace(go.Bar(x=tickers, y=opt_weights, marker_color='#38bdf8'))
            fig_opt.update_layout(template="plotly_dark", title="Distribución de Pesos Sugerida", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig_opt, use_container_width=True)
        
        with col_opt2:
            st.markdown("<br><br>", unsafe_allow_html=True)
            st.success("**Recomendación IA**")
            # Mostrar pesos en USD
            for i, tick in enumerate(tickers):
                st.write(f"• Invertir **${cash_opt * opt_weights[i]:,.2f}** en {tick}")

    with tab_news:
        col_n1, col_n2 = st.columns([1, 2])
        
        with col_n1:
            st.subheader("Simulador de Sentimiento")
            st.info("Este panel usa PLN (Procesamiento de Lenguaje Natural) simulado para analizar el impacto de noticias en el mercado.")
            st.markdown("<br>", unsafe_allow_html=True)
            
            # Semáforo de Sentimiento
            sentimiento_global = np.random.choice(['ALCISTA', 'NEUTRAL', 'BAJISTA'], p=[0.4, 0.4, 0.2])
            if sentimiento_global == 'ALCISTA':
                st.markdown("<h2 style='color: #2ea44f; text-align: center;'>▲ ALCISTA</h2>", unsafe_allow_html=True)
            elif sentimiento_global == 'BAJISTA':
                st.markdown("<h2 style='color: #cb2431; text-align: center;'>▼ BAJISTA</h2>", unsafe_allow_html=True)
            else:
                st.markdown("<h2 style='color: #dbab09; text-align: center;'>━ NEUTRAL</h2>", unsafe_allow_html=True)
                
        with col_n2:
            st.subheader("Feed de Inteligencia Global")
            # Noticias Simuladas Dinámicas
            noticias_ejemplo = [
                ("NVDA", "Resultados trimestrales superan expectativas por demanda de IA.", "ALCISTA"),
                ("AAPL", "Rumores de retraso en el nuevo iPhone por cadena de suministro.", "BAJISTA"),
                ("MSFT", "Anunciada integración masiva de ChatGPT en Office 2026.", "ALCISTA"),
                ("TSLA", "Apertura exitosa de la nueva Gigafactory en Europa.", "ALCISTA")
            ]
            
            for stock, titular, sent en noticias_ejemplo:
                b_color = "#2ea44f" if sent == "ALCISTA" else "#cb2431"
                st.markdown(f"""
                <div class='news-box' style='border-color: {b_color};'>
                    <strong>[{stock}]</strong> - {titular}
                </div>
                """, unsafe_allow_html=True)

except Exception as e:
    st.error(f"Error en la conexión con el nodo central: {e}")
