import streamlit as st
from google import genai
import os
import base64
import requests
from io import BytesIO
from PIL import Image

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Herramientas Virales | DIGITALIS IA", page_icon="favicon.png", layout="centered")

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

# --- FUNCIÓN: GENERAR IMÁGENES GRATIS (HUGGING FACE) MEJORADA ---
def generar_imagen_gratis(prompt, api_key):
    API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"
    headers = {"Authorization": f"Bearer {api_key}"}
    
    prompt_mejorado = f"masterpiece, best quality, highly detailed, {prompt}"
    payload = {"inputs": prompt_mejorado}
    
    try:
        response = requests.post(API_URL, headers=headers, json=payload, timeout=60)
        
        if response.status_code == 200:
            return Image.open(BytesIO(response.content))
        elif response.status_code == 401:
            st.error("🔑 ERROR DE CLAVE: Tu clave de Hugging Face es inválida o no la has puesto bien en los Secrets de Streamlit.")
            return None
        elif response.status_code == 503:
            st.warning("⏳ EL SERVIDOR ESTÁ DESPERTANDO. La IA gratuita tarda unos 20 segundos en arrancar. Espera un momento y vuelve a darle a Crear Imagen.")
            return None
        else:
            st.error(f"❌ Error técnico del servidor de imágenes. Detalles: {response.text}")
            return None
    except Exception as e:
        st.error(f"Error de conexión de red: {e}")
        return None

# =========================================================
# --- DISEÑO VISUAL PREMIUM (PÚRPURA & NEÓN) ---
# =========================================================
st.markdown("""
    <style>
    .stApp { 
        background-color: #05000a !important; 
        background-image: 
            radial-gradient(at 15% 15%, rgba(168, 85, 247, 0.4) 0px, transparent 45%),
            radial-gradient(at 85% 20%, rgba(107, 33, 168, 0.45) 0px, transparent 50%),
            radial-gradient(at 50% 85%, rgba(147, 51, 234, 0.4) 0px, transparent 55%),
            radial-gradient(at 80% 90%, rgba(88, 28, 135, 0.5) 0px, transparent 50%),
            radial-gradient(at 10% 80%, rgba(192, 132, 252, 0.25) 0px, transparent 40%) !important;
        background-size: 200% 200% !important;
        animation: movimientoAurora 12s ease-in-out infinite alternate !important;
    }
    @keyframes movimientoAurora {
        0% { background-position: 0% 0%; }
        25% { background-position: 100% 0%; }
        50% { background-position: 100% 100%; }
        75% { background-position: 0% 100%; }
        100% { background-position: 0% 0%; }
    }
    header { visibility: hidden; }

    div[data-baseweb="input"] {
        background-color: rgba(20, 20, 25, 0.7) !important; 
        backdrop-filter: blur(10px); 
        border: 1px solid rgba(168, 85, 247, 0.3) !important;
        border-radius: 8px !important;
        transition: all 0.3s ease;
    }
    div[data-baseweb="input"] input {
        color: #e2e8f0 !important;
        padding: 12px !important;
        font-size: 1rem !important;
    }
    div[data-baseweb="input"]:focus-within {
        border-color: #a855f7 !important;
        background-color: rgba(30, 20, 40, 0.9) !important;
        box-shadow: 0 0 15px rgba(168, 85, 247, 0.4) !important;
    }

    button[kind="primary"] {
        background-color: #334155 !important; 
        color: white !important;
        border: 1px solid #475569 !important;
        border-radius: 8px !important;
        font-weight: bold;
        height: 48px !important; 
        padding: 0px !important;
        box-shadow: 0 10px 25px -5px rgba(168, 85, 247, 0.8) !important; 
        transition: all 0.3s ease;
    }
    button[kind="primary"]:hover {
        background-color: #a855f7 !important; 
        box-shadow: 0 15px 30px -5px rgba(168, 85, 247, 1) !important;
    }

    button[kind="secondary"] {
        border: 1px solid rgba(168, 85, 247, 0.2) !important;
        color: #d8b4fe !important;
        background-color: rgba(10, 5, 15, 0.5) !important;
        backdrop-filter: blur(5px);
        border-radius: 8px;
    }
    button[kind="secondary"]:hover {
        border: 1px solid #a855f7 !important;
        color: white !important;
        background-color: rgba(168, 85, 247, 0.15) !important;
    }

    button[data-baseweb="tab"] {
        font-size: 1.1rem !important;
        color: #cbd5e1 !important;
    }
    button[data-baseweb="tab"][aria-selected="true"] {
        color: #a855f7 !important;
        font-weight: bold !important;
    }
    div[data-baseweb="tab-highlight"] {
        background-color: #a855f7 !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- CONEXIÓN CON LAS LLAVES SECRETAS ---
try:
    API_KEY_GOOGLE = st.secrets["GEMINI_API_KEY"].strip()
    client = genai.Client(api_key=API_KEY_GOOGLE)
    API_KEY_HF = st.secrets.get("HF_API_KEY", "").strip()
except Exception as e:
    st.error("🚨 ERROR CRÍTICO: Revisa los Secrets de Streamlit.")
    st.stop()

# --- 🎯 ZONA DEL LOGO DE LA EMPRESA ---
col_logo1, col_logo2, col_logo3 = st.columns([1, 1.2, 1])
with col_logo2:
    if os.path.exists("digi ai.png"):
        st.image("digi ai.png", use_container_width=True)

st.markdown("<div style='margin-top: -30px;'></div>", unsafe_allow_html=True)

# --- 🎯 EL TÍTULO PRINCIPAL (HA VUELTO) ---
st.markdown("""
    <h1 style='text-align: center; margin-top: -15px;'>
        <span style='color: #a855f7; text-shadow: 2px 2px 4px rgba(0,0,0,0.8);'>GENERADOR DE IDEAS VIRALES</span><br>
        <span style='font-size: 0.5em; color: #d8b4fe; font-weight: normal; text-shadow: 1px 1px 2px black;'>By DIGITALIS IA</span>
    </h1>
    """, unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

# =========================================================
# --- SISTEMA DE PESTAÑAS (TABS) TODO EN UNO ---
# =========================================================

tab_guiones, tab_imagenes = st.tabs(["📝 Generador de Guiones", "🎨 Creador de Imágenes"])

# ---------------------------------------------------------
# PESTAÑA 1: GENERADOR DE GUIONES VIRALES
# ---------------------------------------------------------
with tab_guiones:
    st.markdown("<br>", unsafe_allow_html=True)
    col_input, col_btn = st.columns([3, 1]) 

    with col_input:
        nicho_cliente = st.text_input("Oculto 1", placeholder='Ej: "viralidad, negocios"...', label_visibility="collapsed")

    with col_btn:
        boton_generar = st.button("Generar Ideas", type="primary", use_container_width=True, key="btn_ideas")

    st.markdown("<h3 style='text-align: center; color: #f8fafc; font-size: 1.3rem; margin-top: 10px; text-shadow: 1px 1px 4px black;'>Genera Ideas para TikTok, Instagram, YouTube</h3>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #cbd5e1; font-size: 0.95rem; margin-top: -10px; margin-bottom: 30px; text-shadow: 1px 1px 2px black;'>Introduce palabras clave para recibir ideas de contenido listas para grabar.</p>", unsafe_allow_html=True)

    espacio_izq, col_tk, col_ig, col_yt, espacio_der = st.columns([1, 1.5, 1.5, 1.5, 1])

    with col_tk:
        mostrar_icono_centrado("tiktok.png")
        tipo_tk = "primary" if st.session_state['red_activa'] == 'TikTok' else "secondary"
        st.button("TikTok", on_click=seleccionar_red, args=('TikTok',), type=tipo_tk, use_container_width=True, key="btn_tk")

    with col_ig:
        mostrar_icono_centrado("instagram.png")
        tipo_ig = "primary" if st.session_state['red_activa'] == 'Instagram Reels' else "secondary"
        st.button("Instagram", on_click=seleccionar_red, args=('Instagram Reels',), type=tipo_ig, use_container_width=True, key="btn_ig")

    with col_yt:
        mostrar_icono_centrado("youtube.png")
        tipo_yt = "primary" if st.session_state['red_activa'] == 'YouTube Shorts' else "secondary"
        st.button("YouTube", on_click=seleccionar_red, args=('YouTube Shorts',), type=tipo_yt, use_container_width=True, key="btn_yt")

    st.markdown("<br>", unsafe_allow_html=True)

    if boton_generar:
        if nicho_cliente:
            red_elegida = st.session_state['red_activa']
            with st.spinner(f'Digitalis IA está generando magia para {red_elegida}...'):
                prompt_secreto = f"""Eres el Director Creativo de DIGITALIS IA. El cliente dice: "{nicho_cliente}". Genera 3 ideas virales EXCLUSIVAMENTE para {red_elegida}. Incluye: Título gancho, guion de 15s y 3 hashtags. REGLA DE ORO: Responde SOLO en Español."""
                try:
                    respuesta = client.models.generate_content(model='gemini-2.5-flash', contents=prompt_secreto)
                    st.success(f"¡Aquí tienes tus ideas para {red_elegida}!")
                    st.write(respuesta.text)
                except Exception as e:
                    st.error("❌ ERROR DE CONEXIÓN CON GOOGLE")
        else:
            st.warning("Por favor, introduce palabras clave primero.")

# ---------------------------------------------------------
# PESTAÑA 2: CREADOR DE IMÁGENES (HUGGING FACE)
# ---------------------------------------------------------
with tab_imagenes:
    st.markdown("<br>", unsafe_allow_html=True)
    
    col_input_img, col_btn_img = st.columns([3, 1]) 

    with col_input_img:
        prompt_imagen = st.text_input("Oculto 2", placeholder='Ej: Un astronauta montando a caballo en marte, estilo realista', label_visibility="collapsed")

    with col_btn_img:
        boton_imagen = st.button("Crear Imagen", type="primary", use_container_width=True, key="btn_img")

    st.markdown("<h3 style='text-align: center; color: #f8fafc; font-size: 1.3rem; margin-top: 10px; text-shadow: 1px 1px 4px black;'>Generador de Imágenes por IA</h3>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #cbd5e1; font-size: 0.95rem; margin-top: -10px; margin-bottom: 30px; text-shadow: 1px 1px 2px black;'>Describe la imagen que quieres crear. Cuanto más detallado, mejor (funciona aún mejor en inglés).</p>", unsafe_allow_html=True)

    if boton_imagen:
        if not API_KEY_HF or API_KEY_HF == "":
            st.error("⚠️ Falta la clave de Hugging Face. Añade `HF_API_KEY = 'tu_clave'` en los Secrets de Streamlit.")
        elif prompt_imagen:
            with st.spinner('🎨 Pintando tu obra de arte... (Puede tardar hasta 30 segundos)'):
                imagen_generada = generar_imagen_gratis(prompt_imagen, API_KEY_HF)
                
                if imagen_generada:
                    st.success("¡Imagen creada con éxito!")
                    col_esp1, col_img_centro, col_esp2 = st.columns([0.1, 0.8, 0.1])
                    with col_img_centro:
                        st.image(imagen_generada, caption=f'"{prompt_imagen}"', use_container_width=True)
        else:
            st.warning("Por favor, describe qué quieres que la IA pinte.")

# --- PIE DE PÁGINA ---
st.markdown("<p style='text-align: center; font-size: 13px; color: #a855f7; margin-top: 60px;'>Desarrollado con 💜 por <b>DIGITALIS IA</b></p>", unsafe_allow_html=True)
