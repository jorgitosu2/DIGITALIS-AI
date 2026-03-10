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
    /* 1. Fondo principal súper oscuro */
    .stApp { background-color: #0e0e0e !important; }
    header { visibility: hidden; }

    /* 2. Estilo de la Caja de Texto (Gris Oscuro Minimalista) */
    div[data-baseweb="input"] {
        background-color: #1e1e1e !important; 
        border: 1px solid #333 !important;
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
        background-color: #252525 !important;
        box-shadow: 0 0 10px rgba(168, 85, 247, 0.2) !important;
    }

    /* 3. Estilo del Botón "Generar Ideas" (Igual a tu foto, pero con luz púrpura) */
    button[kind="primary"] {
        background-color: #334155 !important; /* Gris azulado apagado */
        color: white !important;
        border: 1px solid #475569 !important;
        border-radius: 8px !important;
        font-weight: bold;
        height: 48px !important; /* Misma altura que la caja */
        padding: 0px !important;
        box-shadow: 0 10px 25px -5px rgba(168, 85, 247, 0.6) !important; /* Brillo de neón inferior */
        transition: all 0.3s ease;
    }
    button[kind="primary"]:hover {
        background-color: #a855f7 !important; /* Se enciende al pasar el ratón */
        box-shadow: 0 15px 30px -5px rgba(168, 85, 247, 0.9) !important;
    }

    /* 4. Estilo de los botones selectores de red */
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

# --- 🎯 ZONA DEL LOGO (PROTEGIDA CONTRA ESPACIOS INVISIBLES) ---
# Usamos HTML directo para obligar al logo a ser compacto y no empujar la página
if os.path.exists("digi ai.png"):
    with open("digi ai.png", "rb") as img_file:
        b64_logo = base64.b64encode(img_file.read()).decode()
    st.markdown(f'''
        <div style="display: flex; justify-content: center; margin-bottom: 40px; margin-top: -20px;">
            <img src="data:image/png;base64,{b64_logo}" style="max-height: 70px; object-fit: contain;">
        </div>
    ''', unsafe_allow_html=True)

# =========================================================
# --- ZONA CLONADA EXACTA DE TU IMAGEN ---
# =========================================================

# 1. Caja de búsqueda y botón en la misma línea
col_input, col_btn = st.columns([3, 1]) 

with col_input:
    nicho_cliente = st.text_input(
        "Oculto", 
        placeholder='Ej: "viralidad, negocios", "recetas virales"...',
        label_visibility="collapsed"
    )

with col_btn:
    boton_generar = st.button("Generar Ideas", type="primary", use_container_width=True)

st.markdown("<br>", unsafe_allow_html=True)

# 2. Textos centrados debajo de la caja (Clon exacto)
st.markdown("<h3 style='text-align: center; color: #f8fafc; font-size: 1.3rem; margin-top: 10px;'>Genera Ideas para TikTok, Instagram, YouTube</h3>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #94a3b8; font-size: 0.95rem; margin-top: -10px; margin-bottom: 30px;'>Introduce palabras clave para recibir ideas de contenido listas para grabar.</p>", unsafe_allow_html=True)

# 3. Selector de Redes Sociales (Alineación perfecta)
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
    tipo_yt = "primary" if st.session_state['red_activa'] == 'YouTube Shorts' else "secondary"
    st.button("YouTube", on_click=seleccionar_red, args=('YouTube Shorts',), type=tipo_yt, use_container_width=True)

# =========================================================
# --- LA MAGIA DE LA IA ---
# =========================================================
st.markdown("<br>", unsafe_allow_html=True)

if boton_generar:
    if nicho_cliente:
        red_elegida = st.session_state['red_activa']
        with st.spinner(f'Digitalis IA está generando magia para {red_elegida}...'):
            
            prompt_secreto = f"""
            Eres el Director Creativo experto en viralidad de la agencia DIGITALIS IA. 
            El cliente dice: "{nicho_cliente}".
            
            Tu tarea es generar 3 ideas de contenido altamente virales EXCLUSIVAMENTE para {red_elegida}.
            Para cada idea incluye: 
            - 🎯 Un título gancho persuasivo.
            - 📝 Un guion breve de 15 segundos (qué decir y qué mostrar).
            - #️⃣ 3 hashtags estratégicos perfectos para {red_elegida}.
            
            REGLA DE ORO: Responde SOLO en Español. Usa un tono entusiasta, moderno y profesional.
            """
            
            try:
                respuesta = client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=prompt_secreto
                )
                
                st.success(f"¡Aquí tienes tus ideas para {red_elegida}!")
                st.write(respuesta.text)
            
            except Exception as e:
                st.error("❌ ERROR DE CONEXIÓN CON GOOGLE")
                st.warning(f"Detalle técnico: {e}")
    else:
        st.warning("Por favor, introduce palabras clave primero.")

# --- PIE DE PÁGINA ---
st.markdown("<p style='text-align: center; font-size: 13px; color: #444; margin-top: 60px;'>Desarrollado con 💜 por <b>DIGITALIS IA</b></p>", unsafe_allow_html=True)
