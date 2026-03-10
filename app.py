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
        font-size: 1.1rem !important; /* Botón generar más grande */
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
        background-color: rgba(168, 85, 247, 0.1) !important;
    }

    /* ========================================================= */
    /* 3. SUPER CAJA DE TEXTO ESTILO "PROMPT" (NUEVO)            */
    /* ========================================================= */
    
    /* Etiqueta (Pregunta principal) */
    div[data-testid="stTextInput"] label p {
        font-size: 1.3rem !important; /* Letra más grande */
        font-weight: bold !important;
        color: #f3e8ff !important; /* Blanco purpurino brillante */
        text-align: center !important; /* Centrado forzado */
        display: block;
        width: 100%;
        text-shadow: 1px 1px 3px rgba(0,0,0,0.8);
        margin-bottom: 12px;
    }
    
    /* Contenedor de la caja */
    div[data-testid="stTextInput"] div[data-baseweb="input"] {
        background-color: rgba(20, 10, 30, 0.7) !important; /* Fondo cristal oscuro */
        border: 2px solid #6b21a8 !important; /* Borde morado estándar */
        border-radius: 12px !important; /* Bordes muy redondeados */
        transition: all 0.3s ease-in-out;
    }
    
    /* El texto que escribe el usuario */
    div[data-testid="stTextInput"] input {
        color: white !important;
        font-size: 1.1rem !important; /* Letra más grande al escribir */
        padding: 15px !important; /* Más alta y espaciosa */
    }
    
    /* EFECTO MAGIA: Al hacer clic dentro (Focus) */
    div[data-testid="stTextInput"] div[data-baseweb="input"]:focus-within {
        border: 2px solid #d8b4fe !important; /* Borde más claro */
        box-shadow: 0 0 20px rgba(168, 85, 247, 0.5) !important; /* Resplandor neón */
        background-color: rgba(30, 15, 45, 0.9) !important; /* Se oscurece un poco */
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

# --- TÍTULO PRINCIPAL ---
st.markdown("""
    <h1 style='text-align: center; margin-top: -15px;'>
        <span style='color: #a855f7; text-shadow: 2px 2px 4px rgba(0,0,0,0.8);'>GENERADOR DE IDEAS VIRALES</span><br>
        <span style='font-size: 0.5em; color: #d8b4fe; font-weight: normal; text-shadow: 1px 1px 2px black;'>By DIGITALIS IA</span>
    </h1>
    """, unsafe_allow_html=True)

st.markdown("<p style='text-align: center; color: #e2e8f0; margin-bottom: 25px; text-shadow: 1px 1px 2px black;'>Selecciona tu red social, introduce tu nicho y recibe guiones listos para grabar.</p>", unsafe_allow_html=True)

# --- PANEL DE SELECCIÓN ---
espacio_izq, col_tk, col_ig, col_yt, espacio_der = st.columns([1, 1.5, 1.5, 1.5, 1])

with col_tk:
    mostrar_icono_centrado("tiktok.png")
    tipo_tk = "primary" if st.session_state['red_activa'] == 'TikTok' else "secondary"
    st.button("TikTok", on_click=seleccionar_red, args=('TikTok',), type=tipo_tk, use_container_width=True)

with col_ig:
    mostrar_icono_centrado("instagram.png")
    tipo_ig = "primary" if st.session_state['red_activa'] == 'Instagram Reels' else "secondary"
    st.button("Instagram", on_click=seleccionar_red, args=('Instagram Reels',), type=tipo_ig, use_container_width=True)

with col_yt:
    mostrar_icono_centrado("youtube.png")
    tipo_yt = "primary" if st.session_state['red_activa'] ==
