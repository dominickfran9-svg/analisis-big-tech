import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.express as px

# Forzamos a que no busque altair
st.set_page_config(page_title="Big Tech Analysis", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #080a0f; }
    .stMetric { background-color: #111827; padding: 20px; border-radius: 12px; border: 1px solid #1f2937; }
    h1, h3 { color: #ffffff !important; font-family: 'Inter', sans-serif; }
    </style>
    """, unsafe_allow_html=True)

st.title("📊 Análisis Estratégico de las Big Tech")
st.markdown("---")

# Función de carga ultra-segura
@st.cache_data
def get_market_data():
    tickers = ['AAPL', 'MSFT', 'GOOGL', 'AMZN']
    # Pedimos 1 mes para que sea rápido y no nos bloqueen
    df = yf.download(tickers, period="1mo")['Close']
    return df

try:
    df = get_market_data()
    
    if not df.empty:
        # Fila de indicadores
        m1, m2, m3, m4 = st.columns(4)
        t_list = ['AAPL', 'MSFT', 'GOOGL', 'AMZN']
        cols = [m1, m2, m3, m4]
        
        for i, t in enumerate(t_list):
            price = df[t].iloc[-1]
            change = ((df[t].iloc[-1] / df[t].iloc[0]) - 1) * 100
            cols[i].metric(t, f"${price:.2f}", f"{change:.2f}%")

        st.markdown("### Evolución del Mercado")
        
        # USAMOS PLOTLY (No usa altair, así que no dará error)
        fig = px.line(df, template="plotly_dark", 
                     labels={'value': 'Precio (USD)', 'Date': 'Fecha'},
                     color_discrete_sequence=px.colors.qualitative.Pastel)
        fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig, use_container_width=True)
        
    else:
        st.error("Conectando con la base de datos... por favor refresca la página.")

except Exception as e:
    st.info("Optimizando recursos... presiona F5 en unos segundos.")
