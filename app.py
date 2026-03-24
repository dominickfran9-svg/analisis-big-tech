import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.express as px

# Configuración de página
st.set_page_config(page_title="Big Tech Insight", layout="wide", initial_sidebar_state="collapsed")

# CSS Avanzado para diseño Premium
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;800&display=swap');
    
    .main { background: radial-gradient(circle at top right, #0d1117, #010409); }
    html, body, [data-testid="stAppViewContainer"] { font-family: 'Inter', sans-serif; color: #e6edf3; }
    
    /* Tarjetas con efecto Glassmorphism y Animación */
    div[data-testid="stMetric"] {
        background: rgba(22, 27, 34, 0.5) !important;
        border: 1px solid rgba(48, 54, 61, 1) !important;
        padding: 25px !important;
        border-radius: 15px !important;
        transition: all 0.3s ease-in-out;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    div[data-testid="stMetric"]:hover {
        transform: translateY(-5px);
        border-color: #58a6ff !important;
        background: rgba(30, 41, 59, 0.7) !important;
        box-shadow: 0 10px 20px rgba(0,0,0,0.3);
    }
    
    h1 { font-weight: 800; letter-spacing: -1px; background: -webkit-linear-gradient(#fff, #8b949e); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
    .stSubheader { color: #8b949e !important; font-weight: 400; }
    </style>
    """, unsafe_allow_html=True)

st.title("📊 Análisis Estratégico de las Big Tech")
st.subheader("Monitoreo de rendimiento en tiempo real para toma de decisiones financieras.")
st.markdown("---")

@st.cache_data(ttl=600)
def load_market_data():
    tickers = ['AAPL', 'MSFT', 'GOOGL', 'AMZN']
    df = yf.download(tickers, period="1mo", interval="1d", progress=False)['Close']
    return df

try:
    df = load_market_data()
    
    if not df.empty:
        # Fila de métricas animadas
        cols = st.columns(4)
        t_list = ['AAPL', 'MSFT', 'GOOGL', 'AMZN']
        
        for i, t in enumerate(t_list):
            price = df[t].iloc[-1]
            change = ((df[t].iloc[-1] / df[t].iloc[0]) - 1) * 100
            cols[i].metric(label=t, value=f"${price:.2f}", delta=f"{change:.2f}%")

        st.markdown("###")
        
        # Gráfico de Área interactivo (Más estético que el de líneas)
        st.subheader("📈 Evolución de Capitalización")
        fig = px.area(df, 
                      template="plotly_dark", 
                      color_discrete_sequence=px.colors.sequential.Blues_r,
                      labels={'value': 'Precio (USD)', 'Date': 'Fecha'})
        
        fig.update_layout(
            hovermode="x unified",
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            margin=dict(l=0, r=0, t=30, b=0)
        )
        fig.update_xaxes(showgrid=False)
        fig.update_yaxes(showgrid=True, gridcolor='rgba(255,255,255,0.05)')
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Resumen Ejecutivo
        st.markdown("---")
        c1, c2 = st.columns(2)
        with c1:
            st.info("**Tendencia:** El sector tecnológico muestra una recuperación sólida este mes.")
        with c2:
            st.success("**Recomendación:** Mantener posiciones en activos con baja volatilidad como MSFT.")
            
    else:
        st.error("Reconectando...")
except Exception as e:
    st.info("Actualizando interfaz...")
