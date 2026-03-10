import streamlit as st
from google import genai
import os

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Generador Viral | DIGITALIS IA", page_icon="favicon.png", layout="centered")

# --- MEMORIA DE LA APLICACIÓN ---
if 'red_activa' not in st.session_state:
    st.session_state['red_activa'] = 'TikTok'

def seleccionar_red(red):
    st.session_state['red_activa'] = red

# --- DISEÑO VISUAL PREMIUM (Ajustado) ---
st.markdown("""
    <style>
    /* Botones Activos y Botón Principal (Púrpura) */
    button[kind="primary"] {
        background-color: #a855f7 !important;
        color: white !important;
        border: none !important;
        border-radius: 8px;
        font-weight: bold;
    }
    button[kind="primary"]:hover {
        background-color: #9333ea !important;
    }
    
    /* Botones Inactivos */
    button[kind="secondary"] {
        border: 1px solid #6b21a8 !important;
        color: #d8b4fe !important;
        background-color: transparent !important;
        border-radius: 8px;
    }
    button[kind="secondary"]:hover {
        border: 1px solid #a855f7 !important;
        color: white !important;
    }

    /* Centrar perfectamente las imágenes de los iconos */
    [data-testid="stImage"] {
        display: flex;
        justify-content: center;
        margin-bottom: 5px;
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
        <span style='color: #a855f7; text-shadow: 1px 1px 2px black;'>GENERADOR DE IDEAS VIRALES</span><br>
        <span style='font-size: 0.5em; color: #d8b4fe; font-weight: normal;'>By DIGITALIS IA</span>
    </h1>
    """, unsafe_allow_html=True)

st.markdown("<p style='text-align: center; color: #e2e8f0; margin-bottom: 25px;'>Introduce tu nicho y recibe guiones listos para grabar.</p>", unsafe_allow_html=True)

# =========================================================
# --- PANEL DE SELECCIÓN (ALINEACIÓN A PRUEBA DE FALLOS) ---
# =========================================================
st.markdown("<p style='text-align: center; color: #d8b4fe; font-weight: bold; margin-bottom: 10px;'>Selecciona la red social:</p>", unsafe_allow_html=True)

# Ajustamos los márgenes para que la separación sea perfecta
espacio_izq, col_tk, col_ig, col_yt, espacio_der = st.columns([1, 1.5, 1.5, 1.5, 1])

# BLOQUE INVISIBLE (Se usa para mantener la altura si falta una imagen)
bloque_invisible = "<div style='height: 45px; width: 45px; margin: 0 auto; margin-bottom: 5px;'></div>"

with col_tk:
    if os.path.exists("tiktok.png"):
        st.image("tiktok.png", width=45)
    else:
        st.markdown(bloque_invisible, unsafe_allow_html=True)
        
    tipo_tk = "primary" if st.session_state['red_activa'] == 'TikTok' else "secondary"
    st.button("TikTok", on_click=seleccionar_red, args=('TikTok',), type=tipo_tk, use_container_width=True)

with col_ig:
    # AQUI ESTÁ LA PROTECCIÓN PARA INSTAGRAM
    if os.path.exists("instagram.png"):
        st.image("instagram.png", width=45)
    else:
        # Si no la encuentra, pone un bloque invisible para que el botón no se suba
        st.markdown(bloque_invisible, unsafe_allow_html=True)
        
    tipo_ig = "primary" if st.session_state['red_activa'] == 'Instagram Reels' else "secondary"
    st.button("Instagram", on_click=seleccionar_red, args=('Instagram Reels',), type=tipo_ig, use_container_width=True)

with col_yt:
    if os.path.exists("youtube.png"):
        st.image("youtube.png", width=45)
    else:
        st.markdown(bloque_invisible, unsafe_allow_html=True)
        
    tipo_yt = "primary" if st.session_state['red_activa'] == 'YouTube Shorts' else "secondary"
    st.button("YouTube", on_click=seleccionar_red, args=('YouTube Shorts',), type=tipo_yt, use_container_width=True)

st.markdown("<br>", unsafe_allow_html=True)

# --- CAJA DE TEXTO Y BOTÓN GENERAR ---
nicho_cliente = st.text_input("¿De qué trata tu negocio o qué quieres vender?", placeholder="Ej: Vendo propiedades en Madrid")

col_btn1, col_btn2, col_btn3 = st.columns([1, 1.5, 1])
with col_btn2:
    boton_generar = st.button("Generar Ideas Virales", type="primary", use_container_width=True)

# --- LA MAGIA DE LA IA ---
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
        st.warning("Por favor, escribe de qué trata tu negocio primero.")

# --- PIE DE PÁGINA ---
st.markdown("---")
st.markdown("<p style='text-align: center; font-size: 14px; color: #d8b4fe;'>Desarrollado con 💜 por <b>DIGITALIS IA</b></p>", unsafe_allow_html=True)
