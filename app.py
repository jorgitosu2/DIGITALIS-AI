import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Generador Viral | DIGITALIS IA", page_icon="⚡", layout="centered")

# --- SISTEMA ANTIBALAS PARA LA API KEY ---
try:
    # El .strip() elimina espacios invisibles al principio o al final que arruinan la clave
    API_KEY = st.secrets["GEMINI_API_KEY"].strip()
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel('gemini-pro')
except KeyError:
    st.error("🚨 ERROR CRÍTICO: No encuentro la clave 'GEMINI_API_KEY' en los Secrets de Streamlit.")
    st.stop()
except Exception as e:
    st.error(f"🚨 ERROR AL LEER LA CLAVE: {e}")
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
            
            # --- DETECTOR DE ERRORES AL HABLAR CON GOOGLE ---
            try:
                respuesta = model.generate_content(prompt_secreto)
                st.success("¡Ideas generadas con éxito por Digitalis IA!")
                st.write(respuesta.text)
            
            except Exception as e:
                st.error("❌ ERROR DE CONEXIÓN CON GOOGLE")
                st.warning(f"Detalle técnico: {e}")
                st.info("💡 CONSEJO: Si dice 'API key not valid' o 'InvalidArgument', significa que la clave que pusiste en Streamlit Secrets no es la correcta, está incompleta o la borraste en Google AI Studio.")
                
                # Comprobación de seguridad
                if len(API_KEY) < 30 or not API_KEY.startswith("AIza"):
                    st.error("⚠️ Tu clave actual parece sospechosa. Las claves reales empiezan por 'AIza' y tienen casi 40 caracteres.")
            
    else:
        st.warning("Por favor, escribe un tema primero para poder ayudarte.")

st.markdown("---")
st.markdown("<p style='text-align: center; font-size: 14px; color: gray;'>Desarrollado con ❤️ por <b>DIGITALIS IA</b></p>", unsafe_allow_html=True)
