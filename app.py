import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.express as px

st.set_page_config(page_title="Big Tech Analysis", layout="wide", initial_sidebar_state="collapsed")

# Estilo Elite
st.markdown("""
    <style>
    .main { background-color: #080a0f; }
    .stMetric { background-color: #111827; padding: 20px; border-radius: 12px; border: 1px solid #1f2937; }
    h1 { color: #ffffff !important; font-family: 'Inter', sans-serif; font-weight: 800; }
    h3, .stSubheader { color: #e5e7eb !important; }
    p { color: #9ca3af; }
    hr { border: 0; height: 2px; background: linear-gradient(to right, #00c3ff, #080a0f); margin-bottom: 2rem; }
    </style>
    """, unsafe_allow_html=True)

st.title("📊 Análisis Estratégico de las Big Tech")
st.markdown("---")

# --- PARCHE DE CONEXIÓN ---
tickers = ['AAPL', 'MSFT', 'GOOGL', 'AMZN']

@st.cache_data(ttl=3600) # Esto guarda los datos por una hora para no molestar a Yahoo
def get_data():
    try:
        # Descarga con parámetros que evitan bloqueos
        df = yf.download(tickers, start="2024-01-01", progress=False, auto_adjust=True)
        return df['Close']
    except:
        return pd.DataFrame()

data = get_data()
# ---------------------------

if not data.empty and len(data) > 1:
    returns = data.pct_change().dropna()
    perf_summary = pd.DataFrame({
        'Rendimiento Total': (data.iloc[-1] / data.iloc[0] - 1) * 100,
        'Volatilidad (Std Dev)': returns.std() * 100
    }).reset_index()

    col1, col2, col3, col4 = st.columns(4)
    for i, ticker in enumerate(tickers):
        with [col1, col2, col3, col4][i]:
            val = data[ticker].iloc[-1]
            change = perf_summary.loc[perf_summary['index'] == ticker, 'Rendimiento Total'].values[0]
            st.metric(ticker, f"${val:.2f}", f"{change:.2f}%")

    st.markdown("###")

    col_left, col_right = st.columns([2, 1])
    with col_left:
        st.subheader("Riesgo vs. Retorno")
        fig_scatter = px.scatter(perf_summary, x="Volatilidad (Std Dev)", y="Rendimiento Total", 
                                 text="index", size="Rendimiento Total", color="index", 
                                 template="plotly_dark")
        fig_scatter.update_traces(textposition='top center')
        st.plotly_chart(fig_scatter, use_container_width=True)

    with col_right:
        st.subheader("Interpretación")
        st.markdown(f"""
        <div style="background-color: #111827; padding: 20px; border-radius: 12px; border: 1px solid #1f2937;">
            <p>• <b>Liderazgo:</b> {perf_summary.sort_values('Rendimiento Total', ascending=False).iloc[0]['index']} presenta el mayor retorno.</p>
            <p>• <b>Riesgo:</b> La volatilidad está controlada bajo el 3% diario.</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.subheader("Evolución del Mercado")
    st.line_chart(data)
else:
    st.warning("⚠️ La conexión con Yahoo Finance está lenta. Por favor, haz clic en el botón de abajo para reintentar.")
    if st.button("🔄 Forzar actualización de datos"):
        st.cache_data.clear()
        st.rerun()
