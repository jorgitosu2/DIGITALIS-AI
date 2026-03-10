import streamlit as st
from google import genai # <--- Esta es la nueva herramienta oficial

st.set_page_config(page_title="Generador Viral | DIGITALIS IA", page_icon="⚡", layout="centered")

# --- CONEXIÓN NUEVA VERSIÓN ---
try:
    API_KEY = st.secrets["GEMINI_API_KEY"].strip()
    # Así se conecta ahora con la nueva actualización de Google
    client = genai.Client(api_key=API_KEY) 
except Exception as e:
    st.error("🚨 ERROR CRÍTICO con la API KEY. Revisa los Secrets de Streamlit.")
    st.stop()

# --- DISEÑO VISUAL ---
st.markdown("""
    <h1 style='text-align: center;'>
        <span style='color: #4ade80;'>GENERADOR DE IDEAS VIRALES</span><br>
        <span style='font-size: 0.5em; color: #e2e8f0; font-weight: normal;'>By DIGITALIS IA</span>
    </h1>
    """, unsafe_allow_html=True)

st.markdown("<p style='text-align: center; color: #cbd5e1;'>Introduce un tema y recibe ideas de contenido para TikTok, Instagram y YouTube listas para grabar.</p>", unsafe_allow_html=True)

nicho_cliente = st.text_input("¿De qué trata tu negocio o qué quieres vender?", placeholder="Ej: Vendo propiedades en Madrid")

col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 1])
with col_btn2:
    boton_generar = st.button("Generar Ideas", use_container_width=True)

if boton_generar:
    if nicho_cliente:
        with st.spinner('Digitalis IA está generando magia viral...'):
            prompt_secreto = f"""
            Eres el Director Creativo experto en viralidad de la agencia DIGITALIS IA. 
            El cliente dice: "{nicho_cliente}".
            Dame 2 ideas para TikTok, 2 para Instagram Reels y 2 para YouTube Shorts.
            Incluye: Título gancho, guion de 15 segundos y 3 hashtags.
            REGLA: Responde SOLO en Español. Tono profesional.
            """
            
            try:
                # --- NUEVA FORMA DE LLAMAR A LA IA ---
                respuesta = client.models.generate_content(
                    model='gemini-2.5-flash', # Usamos el modelo más nuevo y estable
                    contents=prompt_secreto
                )
                
                st.success("¡Ideas generadas con éxito por Digitalis IA!")
                st.write(respuesta.text)
            
            except Exception as e:
                st.error("❌ ERROR DE CONEXIÓN CON GOOGLE")
                st.warning(f"Detalle técnico: {e}")
    else:
        st.warning("Por favor, escribe un tema primero para poder ayudarte.")

st.markdown("---")
st.markdown("<p style='text-align: center; font-size: 14px; color: gray;'>Desarrollado con ❤️ por <b>DIGITALIS IA</b></p>", unsafe_allow_html=True)
