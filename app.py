import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go
import plotly.express as px
from scipy.optimize import minimize
import numpy as np

# 1. CONFIGURACIÓN DE PÁGINA
st.set_page_config(page_title="Terminal Gerencial Big Tech", layout="wide", initial_sidebar_state="collapsed")

# 2. ESTILOS VISUALES (Mantenemos el diseño elegante y profesional)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Inter:wght@300;400;600&display=swap');
    .info-panel {
        background: rgba(128, 128, 128, 0.08); 
        border: 1px solid rgba(128, 128, 128, 0.2);
        border-radius: 12px;
        padding: 30px;
        margin-bottom: 20px;
        min-height: 450px;
    }
    .panel-header {
        font-family: 'Orbitron', sans-serif;
        color: #58a6ff;
        font-size: 1.2rem;
        border-bottom: 2px solid #58a6ff;
        padding-bottom: 10px;
        margin-bottom: 15px;
        text-transform: uppercase;
    }
    .panel-body { font-family: 'Inter', sans-serif; line-height: 1.7; text-align: justify; }
    .formula-box {
        background: rgba(0, 0, 0, 0.2);
        padding: 15px;
        border-radius: 8px;
        font-family: 'Courier New', monospace;
        color: #2ea043;
        margin: 15px 0;
        border-left: 4px solid #58a6ff;
    }
    div[data-testid="stMetric"] {
        background: rgba(128, 128, 128, 0.05);
        border: 1px solid rgba(128, 128, 128, 0.2);
        border-radius: 10px;
        padding: 15px;
    }
    </style>
    """, unsafe_allow_html=True)

@st.cache_data(ttl=600)
def load_market_data():
    tickers = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'NVDA', 'META', 'TSLA']
    data = yf.download(tickers, period="2y", interval="1d", progress=False)['Close']
    return data

try:
    df = load_market_data()
    returns = df.pct_change().dropna()
    tickers_list = sorted(df.columns)

    # --- TÍTULO REQUERIDO ---
    st.title("🏛️
