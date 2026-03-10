import streamlit as st
from google import genai
import os

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Generador Viral | DIGITALIS IA", page_icon="⚡", layout="centered")

# --- DISEÑO VISUAL (AHORA TODO CENTRADO) ---
st.markdown("""
    <style>
    /* Botón principal púrpura */
    div.stButton > button:first-child {
        background-color: #a855f7 !important;
        color: white !important;
        border: none !important;
        border-radius: 8px;
        font-weight: bold;
        padding: 0.5rem 1rem;
    }
    div.stButton > button:first-child:hover {
        background-color: #9333ea !important;
        border: none !important;
    }
    
    /* NUEVO: Forzar a que los botones de radio (TikTok, IG, YT) se centren */
    div[role="radiogroup"] {
        justify-content: center !important;
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
# Recuerda cambiar "tu_logo.png" por el nombre exacto de tu archivo si lo cambiaste
col1, col2, col3 = st.columns([1, 1.2, 1])
with col2:
    if os.path.exists("digi ai.png"):
        st.image("digi ai.png", use_container_width=True)

# --- TÍTULO PRINCIPAL ---
st.markdown("""
    <h1 style='text-align: center; margin-top: -15px;'>
        <span style='color: #a855f7; text-shadow: 1px 1px 2px black;'>GENERADOR DE IDEAS VIRALES</span><br>
        <span style='font-size: 0.5em; color: #d8b4fe; font-weight: normal;'>By DIGITALIS IA</span>
    </h1>
    """, unsafe_allow_html=True)

st.markdown("<p style='text-align: center; color: #e2e8f0; margin-bottom: 20px;'>Introduce tu nicho y recibe guiones listos para grabar.</p>", unsafe_allow_html=True)

# --- LAS PESTAÑAS (CENTRADAS) ---
# Hemos añadido 'text-align: center;' a este texto
st.markdown("<p style='text-align: center; color: #d8b4fe; font-weight: bold; margin-bottom: -10px;'>Selecciona la red social:</p>", unsafe_allow_html=True)

red_elegida = st.radio(
    "Oculto", 
    ["🎵 TikTok", "📸 Instagram Reels", "▶️ YouTube Shorts"],
    horizontal=True,
    label_visibility="collapsed"
)

st.markdown("<br>", unsafe_allow_html=True)

# --- CAJA DE TEXTO Y BOTÓN ---
nicho_cliente = st.text_input("¿De qué trata tu negocio o qué quieres vender?", placeholder="Ej: Vendo propiedades en Madrid")

col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 1])
with col_btn2:
    boton_generar = st.button("Generar Ideas", use_container_width=True)

# --- LA MAGIA DE LA IA ---
if boton_generar:
    if nicho_cliente:
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
