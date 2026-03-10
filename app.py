import streamlit as st
from google import genai
import os
import base64

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Generador Viral | DIGITALIS IA", page_icon="favicon.png", layout="centered")

# --- MEMORIA DE LA APLICACIÓN ---
if 'red_activa' not in st.session_state:
    st.session_state['red_activa'] = 'TikTok'

def seleccionar_red(red):
    st.session_state['red_activa'] = red

def mostrar_icono_centrado(ruta_imagen, tamaño=45):
    if os.path.exists(ruta_imagen):
        with open(ruta_imagen, "rb") as img_file:
            b64_string = base64.b64encode(img_file.read()).decode()
            html = f"""
            <div style="display: flex; justify-content: center; align-items: center; margin-bottom: 8px;">
                <img src="data:image/png;base64,{b64_string}" style="width: {tamaño}px; height: {tamaño}px; object-fit: contain;">
            </div>
            """
            st.markdown(html, unsafe_allow_html=True)
    else:
        st.markdown(f'<div style="height: {tamaño}px; margin-bottom: 8px;"></div>', unsafe_allow_html=True)

# =========================================================
# --- DISEÑO VISUAL Y ANIMACIONES PREMIUM ---
# =========================================================
st.markdown("""
    <style>
    /* 1. ANIMACIÓN DEL FONDO */
    .stApp {
        background: linear-gradient(-45deg, #050505, #1e0a2d, #0f0518, #000000);
        background-size: 400% 400%;
        animation: gradientBG 15s ease infinite;
    }
    @keyframes gradientBG {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    header {visibility: hidden;}

    /* 2. BOTONES Y LATIDO */
    @keyframes pulse-glow {
        0% { box-shadow: 0 0 0 0 rgba(168, 85, 247, 0.6); }
        70% { box-shadow: 0 0 0 12px rgba(168, 85, 247, 0); }
        100% { box-shadow: 0 0 0 0 rgba(168, 85, 247, 0); }
    }
    button[kind="primary"] {
        background-color: #a855f7 !important;
        color: white !important;
        border: none !important;
        border-radius: 8px;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    div.stButton:last-of-type > button[kind="primary"] {
        animation: pulse-glow 2s infinite;
        font-size: 1.1rem !important;
        padding: 0.75rem !important;
    }
    button[kind="primary"]:hover {
        background-color: #9333ea !important;
        transform: translateY(-2px);
    }
    button[kind="secondary"] {
        border: 1px solid #6b21a8 !important;
        color: #d8b4fe !important;
        background-color: rgba(0,0,0,0.3) !important;
        border-radius: 8px;
        transition: all 0.3s ease;
    }
    button[kind="secondary"]:hover {
        border: 1px solid #a855f7 !important;
        color: white !important;
        background-co
