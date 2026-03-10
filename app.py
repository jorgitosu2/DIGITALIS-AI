import streamlit as st
from google import genai
import os # Importante para que el sistema busque tu logo

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Generador Viral | DIGITALIS IA", page_icon="⚡", layout="centered")

# --- DISEÑO VISUAL PERSONALIZADO (TEMA PÚRPURA) ---
st.markdown("""
    <style>
    div[role="radiogroup"] > label {
        display: none !important;
    }
    .stRadio p {
        color: #d8b4fe !important;
        font-weight: bold;
        font-size: 16px;
    }
    div.stButton > button:first-child {
        background-color: #9333ea !important;
        color: white !important;
        border: 1px solid #d8b4fe !important;
        border-radius: 8px;
    }
    div.stButton > button:first-child:hover {
        background-color: #7e22ce !important;
        border: 1px solid #white !important;
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
# Usamos columnas para que el logo quede perfectamente centrado y no sea gigante
col1, col2, col3 = st.columns([1, 1.5, 1])
with col2:
    # El sistema busca si subiste el archivo 'logo.png'
    if os.path.exists("logo.png"):
        st.image("logo.png", use_container_width=True)
    else:
        # Si no lo has subido aún, te deja este aviso pequeñito (tus clientes no lo verán una vez lo subas)
        st.caption("📌 Sube tu 'logo.png' a GitHub para verlo aquí.")

# --- TÍTULO PRINCIPAL ---
st.markdown("""
    <h1 style='text-align: center; margin-top: -10px;'>
        <span style='color: #9333ea; text-shadow: 1px 1px 2px black;'>GENERADOR DE IDEAS VIRALES</span><br>
        <span style='font-size: 0.5em; color: #d8b4fe; font-weight: normal;'>By DIGITALIS IA</span>
    </h1>
    """, unsafe_allow_html=True)

st.markdown("<p style='text-align: center; color: #e2e8f0; margin-bottom: 30px;'>Selecciona tu red social, introduce tu nicho y recibe guiones listos para grabar.</p>", unsafe_allow_html=True)

# --- LAS PESTAÑAS (PREVIA ELECCIÓN) ---
red_elegida = st.radio(
    "Selecciona la red social:",
    ["🎵 TikTok", "📸 Instagram Reels", "▶️ YouTube Shorts"],
    horizontal=True
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
