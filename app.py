import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.express as px
import datetime

# Configuración look soberbio
st.set_page_config(page_title="Big Tech Analysis", layout="wide")

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

tickers = ['AAPL', 'MSFT', 'GOOGL', 'AMZN']

@st.cache_data(ttl=3600)
def load_data():
    # Intentamos bajar los datos de los últimos 6 meses para asegurar que haya info
    all_data = []
    for t in tickers:
        ticker_obj = yf.Ticker(t)
        # El secreto: pedir el historial directamente con un periodo largo
        hist = ticker_obj.history(period="6mo")
        if not hist.empty:
            hist = hist[['Close']].rename(columns={'Close': t})
            all_data.append(hist)
    
    if all_data:
        return pd.concat(all_data, axis=1).ffill()
    return pd.DataFrame()

data = load_data()

if not data.empty:
    # Cálculos
    perf_summary = pd.DataFrame({
        'Rendimiento Total': (data.iloc[-1] / data.iloc[0] - 1) * 100,
        'Volatilidad': data.pct_change().std() * 100
    }).reset_index().rename(columns={'index': 'Ticker'})

    # Métricas superiores
    cols = st.columns(4)
    for i, t in enumerate(tickers):
        with cols[i]:
            current_price = data[t].iloc[-1]
            change = perf_summary.loc[perf_summary['Ticker'] == t, 'Rendimiento Total'].values[0]
            st.metric(t, f"${current_price:.2f}", f"{change:.2f}%")

    st.markdown("###")
    
    # Gráficos
    c1, c2 = st.columns([2, 1])
    with c1:
        st.subheader("Riesgo vs. Retorno")
        fig = px.scatter(perf_summary, x="Volatilidad", y="Rendimiento Total", text="Ticker", 
                         color="Ticker", size="Rendimiento Total", template="plotly_dark")
        st.plotly_chart(fig, use_container_width=True)
    
    with c2:
        st.subheader("Análisis de Mercado")
        st.write("Datos actualizados al cierre de mercado. Microsoft y Apple mantienen la resiliencia en el sector tecnológico.")
        st.line_chart(data)
else:
    st.error("Error de conexión. Yahoo Finance está limitando las peticiones. Por favor, intenta de nuevo en unos minutos.")
