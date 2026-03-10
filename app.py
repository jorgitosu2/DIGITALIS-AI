import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Generador Viral | DIGITALIS IA", page_icon="⚡", layout="centered")

# --- CONEXIÓN ---
try:
    API_KEY = st.secrets["GEMINI_API_KEY"].strip()
    genai.configure(api_key=API_KEY)
    # Volvemos al nombre clásico temporalmente
    model = genai.GenerativeModel('gemini-pro') 
except Exception as e:
    st.error("🚨 ERROR CRÍTICO con la API KEY")
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
                respuesta = model.generate_content(prompt_secreto)
                st.success("¡Ideas generadas con éxito por Digitalis IA!")
                st.write(respuesta.text)
            
            except Exception as e:
                st.error("❌ ERROR DE CONEXIÓN CON GOOGLE")
                st.warning(f"Detalle técnico: {e}")
                st.info("💡 CONSEJO: Abre el 'Modo Diagnóstico' abajo para ver qué modelos permite tu clave.")
    else:
        st.warning("Por favor, escribe un tema primero para poder ayudarte.")

st.markdown("---")
st.markdown("<p style='text-align: center; font-size: 14px; color: gray;'>Desarrollado con ❤️ por <b>DIGITALIS IA</b></p>", unsafe_allow_html=True)

# --- MODO DIAGNÓSTICO SECRETO ---
st.markdown("<br><br>", unsafe_allow_html=True)
with st.expander("🛠️ Modo Diagnóstico (Solo para DIGITALIS IA)"):
    st.write("Haz clic aquí para preguntarle a Google exactamente qué modelos están disponibles para tu clave API en este momento.")
    if st.button("Buscar Modelos Disponibles"):
        with st.spinner("Consultando a los servidores de Google..."):
            try:
                modelos_disponibles = []
                for m in genai.list_models():
                    if 'generateContent' in m.supported_generation_methods:
                        modelos_disponibles.append(m.name)
                
                if modelos_disponibles:
                    st.success("¡Lista obtenida! Google dice que SÍ tienes acceso a estos:")
                    st.write(modelos_disponibles)
                    st.info("Copia el que diga algo como 'models/gemini-1.5-flash' y envíamelo.")
                else:
                    st.error("Tu clave es válida, pero Google dice que NO tienes ningún modelo disponible. Esto suele pasar si usas un correo de empresa que tiene bloqueada la IA.")
            except Exception as e:
                st.error(f"Error al intentar listar modelos: {e}")
