import streamlit as st
import google.generativeai as genai

# 1. Configuración de la página
st.set_page_config(page_title="Generador Viral | DIGITALIS IA", page_icon="⚡", layout="centered")

# 2. Conectar la API Key desde los "Secretos" de Streamlit
API_KEY = st.secrets["GEMINI_API_KEY"]
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-pro')

# 3. DISEÑO VISUAL
st.markdown("""
    <h1 style='text-align: center;'>
        <span style='color: #4ade80;'>GENERADOR DE IDEAS VIRALES</span><br>
        <span style='font-size: 0.5em; color: #e2e8f0; font-weight: normal;'>By DIGITALIS IA</span>
    </h1>
    """, unsafe_allow_html=True)

st.markdown("<p style='text-align: center; color: #cbd5e1;'>Introduce un tema y recibe ideas de contenido para TikTok, Instagram y YouTube listas para grabar.</p>", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

# 4. La caja de texto y el botón
nicho_cliente = st.text_input("¿De qué trata tu negocio o qué quieres vender?", placeholder="Ej: Vendo propiedades en Madrid")

# Centrar el botón
col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 1])
with col_btn2:
    boton_generar = st.button("Generar Ideas", use_container_width=True)

if boton_generar:
    if nicho_cliente:
        with st.spinner('Digitalis IA está generando magia viral...'):
            
            prompt_secreto = f"""
            Eres el Director Creativo experto en viralidad de la agencia DIGITALIS IA. 
            El cliente dice: "{nicho_cliente}".
            
            Tu tarea es generar ideas de contenido altamente virales.
            Dame 2 ideas para TikTok, 2 para Instagram Reels y 2 para YouTube Shorts.
            Para cada idea incluye: 
            - 🎯 Un título gancho persuasivo.
            - 📝 Un guion breve de 15 segundos (qué decir y qué mostrar).
            - #️⃣ 3 hashtags estratégicos.
            
            REGLA DE ORO: Tu respuesta debe estar ÚNICA Y EXCLUSIVAMENTE en idioma Español. 
            Usa un tono entusiasta, moderno y profesional.
            """
            
            respuesta = model.generate_content(prompt_secreto)
            
            st.success("¡Ideas generadas con éxito por Digitalis IA!")
            st.write(respuesta.text)
            
    else:
        st.warning("Por favor, escribe un tema primero para poder ayudarte.")

st.markdown("---")
st.markdown("<p style='text-align: center; font-size: 14px; color: gray;'>Desarrollado con ❤️ por <b>DIGITALIS IA</b></p>", unsafe_allow_html=True)
