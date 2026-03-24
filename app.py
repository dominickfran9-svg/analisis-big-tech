import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go

# Configuración de Terminal de Alto Rendimiento
st.set_page_config(page_title="Quantum Tech Terminal", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Inter:wght@300;600&display=swap');
    
    .main { background: #020617; }
    
    /* Escáner Láser Dinámico */
    .stApp::before {
        content: ""; position: fixed; top: 0; left: 0; width: 100%; height: 2px;
        background: rgba(56, 189, 248, 0.4); box-shadow: 0 0 20px #38bdf8;
        z-index: 9999; animation: scan 6s linear infinite; pointer-events: none;
    }
    @keyframes scan { 0% { top: -10%; } 100% { top: 110%; } }

    /* Tarjetas con Efecto de Profundidad */
    div[data-testid="stMetric"] {
        background: rgba(15, 23, 42, 0.6) !important;
        border: 1px solid rgba(56, 189, 248, 0.1) !important;
        backdrop-filter: blur(12px) !important;
        border-radius: 20px !important;
        padding: 20px !important;
        transition: all 0.3s ease-in-out;
    }
    div[data-testid="stMetric"]:hover {
        transform: scale(1.02);
        border-color: #38bdf8 !important;
        box-shadow: 0 0 30px rgba(56, 189, 248, 0.2) !important;
    }

    h1, h2 { font-family: 'Orbitron', sans-serif; letter-spacing: 2px; color: #f8fafc; }
    </style>
    """, unsafe_allow_html=True)

st.title("⚡ QUANTUM ANALYSIS TERMINAL")

@st.cache_data(ttl=600)
def get_data():
    ts = ['AAPL', 'MSFT', 'GOOGL', 'AMZN']
    return yf.download(ts, period="1mo", interval="1d", progress=False)['Close']

try:
    df = get_data()
    if not df.empty:
        # Fila de Métricas con Glow
        m1, m2, m3, m4 = st.columns(4)
        ts = ['AAPL', 'MSFT', 'GOOGL', 'AMZN']
        slots = [m1, m2, m3, m4]
        for i, t in enumerate(ts):
            curr = df[t].iloc[-1]
            change = (curr / df[t].iloc[0] - 1) * 100
            slots[i].metric(f"NODE_{t}", f"${curr:.2f}", f"{change:.2f}%")

        # Tabs de Visualización Avanzada
        tab1, tab2 = st.tabs(["🌈 Visualizer Neón", "📊 Comparativa Técnica"])

        with tab1:
            fig = go.Figure()
            colors = ['#00f2ff', '#7000ff', '#ff007b', '#00ff88']
            for i, t in enumerate(ts):
                norm = (df[t] / df[t].iloc[0]) * 100
                fig.add_trace(go.Scatter(
                    x=df.index, y=norm, name=t,
                    mode='lines',
                    line=dict(color=colors[i], width=4, shape='spline'),
                    # Efecto de brillo al pasar el mouse (Neón Focus)
                    hoverlabel=dict(bgcolor=colors[i], font_size=16, font_family="Orbitron"),
                    hovertemplate="<b>" + t + "</b><br>Retorno: %{y:.2f}%<extra></extra>"
                ))
            
            fig.update_layout(
                hovermode="x unified", template="plotly_dark",
                paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                xaxis=dict(showgrid=False), yaxis=dict(side="right", gridcolor='rgba(255,255,255,0.05)')
            )
            st.plotly_chart(fig, use_container_width=True)

        with tab2:
            st.subheader("Cuadro de Mando Estratégico")
            # Tabla estilizada (ahora con matplotlib en requirements no fallará)
            stats = pd.DataFrame({
                "Rendimiento (%)": (df.iloc[-1] / df.iloc[0] - 1) * 100,
                "Volatilidad": df.pct_change().std() * 100,
                "Máximo": df.max(),
                "Mínimo": df.min()
            })
            st.table(stats.style.format("{:.2f}"))

except Exception as e:
    st.info("Sincronizando nodos de datos... por favor espera.")
