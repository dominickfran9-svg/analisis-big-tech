import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go

st.set_page_config(page_title="Big Tech Quantum", layout="wide", initial_sidebar_state="collapsed")

# CSS Avanzado: Animaciones de Escaneo y Glow Dinámico
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Inter:wght@300;600&display=swap');
    
    .main { background: #020617; }

    /* Animación de barrido láser (Scanner) */
    @keyframes scan {
        0% { background-position: 0% 50%; }
        100% { background-position: 100% 50%; }
    }

    /* Tarjetas Dinámicas con Glow */
    div[data-testid="stMetric"] {
        background: rgba(15, 23, 42, 0.8) !important;
        border: 1px solid rgba(56, 189, 248, 0.3) !important;
        backdrop-filter: blur(15px) !important;
        border-radius: 20px !important;
        padding: 25px !important;
        transition: all 0.5s cubic-bezier(0.4, 0, 0.2, 1) !important;
        position: relative;
    }

    div[data-testid="stMetric"]:hover {
        transform: translateY(-10px) scale(1.02) !important;
        border-color: #38bdf8 !important;
        box-shadow: 0 0 30px rgba(56, 189, 248, 0.6) !important;
    }

    /* Título con Gradiente Animado */
    h1 {
        font-family: 'Orbitron', sans-serif;
        background: linear-gradient(270deg, #38bdf8, #818cf8, #38bdf8);
        background-size: 200% 200%;
        animation: scan
