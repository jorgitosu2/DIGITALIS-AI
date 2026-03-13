import streamlit as st
from google import genai
import os
import base64
import urllib.parse
import random
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


# =========================================================
# --- DISEÑO VISUAL PREMIUM ---
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

    div[data-baseweb="input"], div[data-baseweb="textarea"] {
        background-color: rgba(20, 20, 25, 0.7) !important; 
        backdrop-filter: blur(10px); 
        border: 1px solid rgba(168, 85, 247, 0.3) !important;
        border-radius: 8px !important;
        transition: all 0.3s ease;
    }
    div[data-baseweb="input"] input, div[data-baseweb="textarea"] textarea {
        color: #e2e8f0 !important;
        padding: 15px !important;
        font-size: 1.05rem !important;
        line-height: 1.5 !important;
    }
    div[data-baseweb="input"]:focus-within, div[data-baseweb="textarea"]:focus-within {
        border-color: #a855f7 !important;
        background-color: rgba(30, 20, 40, 0.9) !important;
        box-shadow: 0 0 15px rgba(168, 85, 247, 0.4) !important;
    }

    [data-testid="stFileUploader"] {
        background-color: rgba(20, 20, 25, 0.7) !important;
        border: 1px dashed rgba(168, 85, 247, 0.5) !important;
        border-radius: 8px;
        padding: 15px;
    }

    button[kind="primary"] {
        background-color: #334155 !important; 
        color: white !important;
        border: 1px solid #475569 !important;
        border-radius: 8px !important;
        font-weight: bold;
        height: 50px !important; 
        padding: 0px !important;
        box-shadow: 0 10px 25px -5px rgba(168, 85, 247, 0.8) !important; 
        transition: all 0.3s ease;
        font-size: 1.1rem !important;
    }
    button[kind="primary"]:hover {
        background-color: #a855f7 !important; 
        box-shadow: 0 15px 30px -5px rgba(168, 85, 247, 1) !important;
        transform: translateY(-2px);
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

    button[data-baseweb="tab"] { font-size: 1.1rem !important; color: #cbd5e1 !important; }
    button[data-baseweb="tab"][aria-selected="true"] { color: #a855f7 !important; font-weight: bold !important; }
    div[data-baseweb="tab-highlight"] { background-color: #a855f7 !important; }
    </style>
""", unsafe_allow_html=True)

# --- CONEXIÓN CON GOOGLE ---
try:
    API_KEY_GOOGLE = st.secrets["GEMINI_API_KEY"].strip()
    client = genai.Client(api_key=API_KEY_GOOGLE)
except Exception as e:
    st.error("🚨 ERROR CRÍTICO: Revisa tu clave de Google en los Secrets.")
    st.stop()

# --- 🎯 ZONA DEL LOGO ---
col_logo1, col_logo2, col_logo3 = st.columns([1, 1.2, 1])
with col_logo2:
    if os.path.exists("digi ai.png"):
        st.image("digi ai.png", use_container_width=True)

st.markdown("<div style='margin-top: -30px;'></div>", unsafe_allow_html=True)
st.markdown("""
    <h1 style='text-align: center; margin-top: -15px;'>
        <span style='color: #a855f7; text-shadow: 2px 2px 4px rgba(0,0,0,0.8);'>GENERADOR DE IDEAS VIRALES</span><br>
        <span style='font-size: 0.5em; color: #d8b4fe; font-weight: normal; text-shadow: 1px 1px 2px black;'>By DIGITALIS IA</span>
    </h1><br>
    """, unsafe_allow_html=True)

# =========================================================
# --- SISTEMA DE PESTAÑAS ---
# =========================================================
tab_guiones, tab_imagenes = st.tabs(["📝 Generador de Guiones", "🎨 Creador de Imágenes"])

# ---------------------------------------------------------
# PESTAÑA 1: GENERADOR DE GUIONES VIRALES
# ---------------------------------------------------------
with tab_guiones:
    st.markdown("<br><h3 style='text-align: center; color: #f8fafc; font-size: 1.4rem; margin-top: -10px;'>1º Selecciona tu Red Social</h3>", unsafe_allow_html=True)
    
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

    st.markdown("<hr style='border:1px solid rgba(168, 85, 247, 0.2); margin: 30px 0;'><h3 style='text-align: center; color: #f8fafc; font-size: 1.4rem;'>2º Describe tu Negocio al Detalle</h3>", unsafe_allow_html=True)
    
    nicho_cliente = st.text_area("Oculto 1", placeholder='Ej: "Soy entrenador personal online..."', label_visibility="collapsed", height=140)

    st.markdown("<br>", unsafe_allow_html=True)
    col_esp1, col_btn_gen, col_esp2 = st.columns([1, 1.5, 1])
    with col_btn_gen:
        boton_generar = st.button("✨ Generar Guiones Virales", type="primary", use_container_width=True)

    if boton_generar and nicho_cliente:
        red_elegida = st.session_state['red_activa']
        with st.spinner(f'Digitalis IA está generando magia para {red_elegida}...'):
            prompt_secreto = f"""Eres el Director Creativo de DIGITALIS IA. El cliente dice: "{nicho_cliente}". Genera 3 ideas virales para {red_elegida}. Incluye: Título gancho, guion de 15s y 3 hashtags. Responde en Español."""
            try:
                respuesta = client.models.generate_content(model='gemini-2.5-flash', contents=prompt_secreto)
                st.success(f"¡Aquí tienes tus ideas para {red_elegida}!")
                st.write(respuesta.text)
            except Exception as e:
                st.error("❌ ERROR DE CONEXIÓN CON GOOGLE")

# ---------------------------------------------------------
# PESTAÑA 2: CREADOR DE IMÁGENES (HTML DIRECTO)
# ---------------------------------------------------------
with tab_imagenes:
    st.markdown("<br><h3 style='text-align: center; color: #f8fafc; font-size: 1.4rem;'>Creador de Imágenes por IA</h3>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #cbd5e1; font-size: 0.95rem; margin-bottom: 20px;'>Sube una foto de referencia o simplemente describe lo que quieres crear.</p>", unsafe_allow_html=True)

    imagen_subida = st.file_uploader("Sube tu imagen (Opcional)", type=["png", "jpg", "jpeg"])
    prompt_imagen = st.text_area("Oculto 2", placeholder='Ej: "ponle un fondo de playa" o "Un gato ninja en la luna"...', label_visibility="collapsed", height=100)

    st.markdown("<br>", unsafe_allow_html=True)
    col_esp_img1, col_btn_img, col_esp_img2 = st.columns([1, 1.5, 1])
    with col_btn_img:
        boton_imagen = st.button("🎨 Crear Imagen Mágica", type="primary", use_container_width=True)

    if boton_imagen and (prompt_imagen or imagen_subida):
        texto_final = prompt_imagen

        # 1. Gemini analiza la foto con una CORREA MUY CORTA
        if imagen_subida is not None:
            with st.spinner("👁️ Analizando foto con Inteligencia Artificial..."):
                try:
                    img_pil = Image.open(imagen_subida)
                    # Instrucción super estricta para evitar errores de enlace
                    prompt_gemini = f"Observa al sujeto principal. Aplica este cambio: '{prompt_imagen}'. TRADÚCELO AL INGLÉS. REGLA ESTRICTA: Escribe MÁXIMO 15 PALABRAS. SIN comillas. SIN puntos. Solo palabras clave separadas por comas."
                    
                    respuesta_gemini = client.models.generate_content(model='gemini-2.5-flash', contents=[img_pil, prompt_gemini])
                    
                    # Limpiamos el texto para que no rompa el enlace de internet
                    texto_final = respuesta_gemini.text.replace('"', '').replace('\n', ' ').strip()
                    
                except Exception as e:
                    st.error("Hubo un error al leer tu imagen.")
        
        # 2. Mostramos la imagen usando HTML puro (El navegador la descarga, no el servidor)
        if texto_final:
            st.success("¡Tu petición se ha enviado al cerebro de la IA!")
            st.info("💡 Tu navegador está descargando la imagen en HD. Aparecerá aquí debajo en unos 5 segundos...")
            
            # Formateamos el texto para la URL
            texto_url = urllib.parse.quote(f"{texto_final}, masterpiece, 8k resolution, cinematic lighting")
            semilla = random.randint(1, 1000000)
            
            # Construimos la URL mágica de Pollinations
            url_imagen_final = f"https://image.pollinations.ai/prompt/{texto_url}?nologo=true&seed={semilla}&width=1024&height=1024"
            
            # Inyectamos HTML para forzar a tu Google Chrome a mostrar la foto
            codigo_html = f"""
            <div style="display: flex; flex-direction: column; align-items: center; justify-content: center; margin-top: 20px;">
                <img src="{url_imagen_final}" alt="Cargando obra de arte..." style="width: 80%; max-width: 600px; border-radius: 12px; box-shadow: 0 10px 25px rgba(168,85,247,0.5);">
                <br>
                <a href="{url_imagen_final}" target="_blank" style="padding: 10px 20px; background-color: #a855f7; color: white; text-decoration: none; border-radius: 8px; font-weight: bold; font-family: sans-serif;">⬇️ Ver en Alta Calidad</a>
            </div>
            """
            st.markdown(codigo_html, unsafe_allow_html=True)

# --- PIE DE PÁGINA ---
st.markdown("<p style='text-align: center; font-size: 13px; color: #a855f7; margin-top: 60px;'>Desarrollado con 💜 por <b>DIGITALIS IA</b></p>", unsafe_allow_html=True)
