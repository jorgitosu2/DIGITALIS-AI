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

# 1. Caja de búsqueda y botón alineados horizontalmente
col_input, col_btn = st.columns([4, 1.2]) # La caja es 4 veces más grande que el botón

with col_input:
    # Usamos label_visibility="collapsed" para ocultar el título y que quede alineado perfecto con el botón
    nicho_cliente = st.text_input(
        "Oculto", 
        placeholder='Ej: "viralidad, negocios", "recetas virales"...',
        label_visibility="collapsed"
    )

with col_btn:
    boton_generar = st.button("Generar Ideas", type="primary", use_container_width=True)

st.markdown("<br>", unsafe_allow_html=True)

# 2. Textos centrados (Igual a la imagen)
st.markdown("<h3 style='text-align: center; color: white; font-size: 1.4rem;'>Genera Ideas para TikTok, Instagram, YouTube</h3>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #cbd5e1; font-size: 0.95rem; margin-top: -10px;'>Introduce palabras clave para recibir ideas de contenido listas para grabar.</p>", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# 3. Selector de Redes Sociales
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

# 4. Línea de neón final que cierra el diseño de "Tarjeta"
st.markdown('<hr class="glow-line">', unsafe_allow_html=True)

# =========================================================
# --- LA MAGIA DE LA IA ---
# =========================================================
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
st.markdown("<p style='text-align: center; font-size: 14px; color: #555; margin-top: 50px;'>Desarrollado con 💜 por <b>DIGITALIS IA</b></p>", unsafe_allow_html=True)
