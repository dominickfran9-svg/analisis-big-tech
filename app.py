import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.express as px

# Configuración look Premium
st.set_page_config(page_title="Big Tech Analysis", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #080a0f; }
    .stMetric { background-color: #111827; padding: 20px; border-radius: 12px; border: 1px solid #1f2937; }
    h1 { color: #ffffff !important; font-family: 'Inter', sans-serif; }
    h3, .stSubheader { color: #e5e7eb !important; }
    p { color: #9ca3af; }
    hr { border: 0; height: 2px; background: linear-gradient(to right, #00c3ff, #080a0f); margin-bottom: 2rem; }
    </style>
    """, unsafe_allow_html=True)

st.title("📊 Análisis Estratégico de las Big Tech")
st.markdown("---")

@st.cache_data(ttl=600)
def load_market_data():
    tickers = ['AAPL', 'MSFT', 'GOOGL', 'AMZN']
    try:
        # El truco: pedimos el último mes con intervalo de 1 día para no activar alarmas
        data = yf.download(tickers, period="1mo", interval="1d", progress=False)['Close']
        return data
    except:
        return pd.DataFrame()

df = load_market_data()

if not df.empty and df.isna().sum().sum() < (len(df) * 0.5):
    # Cálculos
    rets = df.pct_change().dropna()
    perf = pd.DataFrame({
        'Retorno': (df.iloc[-1] / df.iloc[0] - 1) * 100,
        'Riesgo': rets.std() * 100
    }).reset_index().rename(columns={'index': 'Empresa'})

    # Fila de métricas
    m1, m2, m3, m4 = st.columns(4)
    metrics = [m1, m2, m3, m4]
    for i, t in enumerate(['AAPL', 'MSFT', 'GOOGL', 'AMZN']):
        metrics[i].metric(t, f"${df[t].iloc[-1]:.2f}", f"{perf.iloc[i, 1]:.2f}%")

    st.markdown("###")
    
    # Gráficos de alta calidad
    c1, c2 = st.columns([2, 1])
    with c1:
        st.subheader("Riesgo vs. Retorno Mensual")
        fig = px.scatter(perf, x="Riesgo", y="Retorno", text="Empresa", color="Empresa",
                         size="Retorno", template="plotly_dark", height=450)
        st.plotly_chart(fig, use_container_width=True)
    
    with c2:
        st.subheader("Tendencia")
        st.line_chart(df)
        st.info("Gráfica comparativa de precios normalizada.")
else:
    st.error("⚠️ Yahoo Finance está bloqueando la conexión temporalmente.")
    st.markdown("Como es un proyecto académico, si el bloqueo persiste, podrías subir un archivo CSV con los datos para que la página sea 100% estable.")
    if st.button("🔄 Reintentar Conexión"):
        st.cache_data.clear()
        st.rerun()
