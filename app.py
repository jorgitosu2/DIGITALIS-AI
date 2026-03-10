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

def mostrar_icono_centrado(ruta_imagen, tamaño=40):
    if os.path.exists(ruta_imagen):
        with open(ruta_imagen, "rb") as img_file:
            b64_string = base64.b64encode(img_file.read()).decode()
            html = f"""
            <div style="display: flex; justify-content: center; align-items: center; margin-bottom: 5px;">
                <img src="data:image/png;base64,{b64_string}" style="width: {tamaño}px; height: {tamaño}px; object-fit: contain;">
            </div>
            """
            st.markdown(html, unsafe_allow_html=True)
    else:
        st.markdown(f'<div style="height: {tamaño}px; margin-bottom: 5px;"></div>', unsafe_allow_html=True)

# =========================================================
# --- DISEÑO CLON DE GOOGLE AI STUDIO (TEMA PÚRPURA) ---
# =========================================================
st.markdown("""
    <style>
    /* 1. Fondo principal súper oscuro (casi negro) */
    .stApp {
        background-color: #0e0e0e;
    }
    header {visibility: hidden;}

    /* 2. Estilo de la Caja de Texto (Gris Oscuro) */
    div[data-baseweb="input"] {
        background-color: #1e1e1e !important; 
        border: 1px solid #333 !important;
        border-radius: 8px !important;
        transition: all 0.3s ease;
    }
    div[data-baseweb="input"] input {
        color: #e2e8f0 !important;
        padding: 14px !important;
        font-size: 1rem !important;
    }
    /* Brillo púrpura sutil al hacer clic para escribir */
    div[data-baseweb="input"]:focus-within {
        border-color: #a855f7 !important;
        background-color: #252525 !important;
        box-shadow: 0 0 10px rgba(168, 85, 247, 0.2) !important;
    }

    /* 3. Estilo del Botón "Generar Ideas" (Igual a la foto pero púrpura) */
    button[kind="primary"] {
        background-color: #475569 !important; /* Gris azulado por defecto */
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        font-weight: bold;
        height: 100% !important; /* Igualar altura con la caja de texto */
        padding: 0px !important;
        /* EL SECRETO: El brillo de neón por debajo del botón */
        box-shadow: 0 12px 20px -8px rgba(168, 85, 247, 0.8) !important;
        transition: all 0.3s ease;
    }
    button[kind="primary"]:hover {
        background-color: #a855f7 !important; /* Se vuelve púrpura entero al pasar el ratón */
        box-shadow: 0 15px 25px -5px rgba(168, 85, 247, 1) !important;
    }

    /* 4. Línea de neón brillante en la parte inferior de la "Tarjeta" */
    hr.glow-line {
        border: none;
        height: 2px;
        background: linear-gradient(90deg, transparent, #a855f7, transparent);
        box-shadow: 0 5px 25px 2px rgba(168, 85, 247, 0.8);
        margin-top: 40px;
        margin-bottom: 40px;
    }

    /* 5. Estilo de los botones selectores de red (inactivos) */
    button[kind="secondary"] {
        border: 1px solid #333 !important;
        color: #888 !important;
        background-color: #1a1a1a !important;
        border-radius: 8px;
    }
    button[kind="secondary"]:hover {
        border: 1px solid #a855f7 !important;
        color: white !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- CONEXIÓN CON GOOGLE ---
try:
    API_KEY = st.secrets["GEMINI_API_KEY"].strip()
    client = genai.Client(api_key=API_KEY)
except Exception as e:
    st.error("🚨 ERROR CRÍTICO: Revisa los Secrets de Streamlit.")
    st.stop()

# --- 🎯 ZONA DEL LOGO DE LA EMPRESA ---
col_logo1, col_logo2, col_logo3 = st.columns([1, 1.2, 1])
with col_logo2:
    if os.path.exists("digi ai.png"):
        st.image("digi ai.png", use_container_width=True)

st.markdown("<br>", unsafe_allow_html=True)

# =========================================================
# --- ZONA CLONADA DE TU IMAGEN ---
# =========================================================

#
