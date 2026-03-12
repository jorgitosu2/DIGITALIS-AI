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

# --- FUNCIÓN MÁGICA 4.0: DESCARGA DIRECTA AL NAVEGADOR (ANTI-BLOQUEOS) ---
def generar_url_imagen(prompt):
    """No descarga la imagen en el servidor, solo genera la URL exacta para que el navegador del cliente la cargue."""
    # Limpiamos el texto por si Gemini mete saltos de línea raros que rompen el enlace
    prompt_limpio = prompt.replace('\n', ' ').replace('\r', '')
    prompt_mejorado = f"{prompt_limpio}, masterpiece, ultra detailed, 8k resolution, highly cinematic"
    prompt_url = urllib.parse.quote(prompt_mejorado)
    semilla = random.randint(1, 1000000)
    
    # Usamos el modelo 'flux' que es el más nuevo, rápido y realista del mercado Open Source
    url = f"https://image.pollinations.ai/prompt/{prompt_url}?model=flux&nologo=true&seed={semilla}&width=1024&height=1024"
    return url

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

    button[data-baseweb="tab"] {
        font-size: 1.1rem !important;
        color: #cbd5e1 !important;
    }
    button[data-baseweb="tab"][aria-selected="true"] {
        color: #a855f7 !important;
        font-weight: bold !important;
    }
    div[data-baseweb="tab-highlight"] {
        background-color: #a855f7 !important;
    }
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

# --- 🎯 TÍTULO PRINCIPAL ---
st.markdown("""
    <h1 style='text-align: center; margin-top: -15px;'>
        <span style='color: #a855f7; text-shadow: 2px 2px 4px rgba(0,0,0,0.8);'>GENERADOR DE IDEAS VIRALES</span><br>
        <span style='font-size: 0.5em; color: #d8b4fe; font-weight: normal; text-shadow: 1px 1px 2px black;'>By DIGITALIS IA</span>
    </h1>
    """, unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

# =========================================================
# --- SISTEMA DE PESTAÑAS (TABS) TODO EN UNO ---
# =========================================================
tab_guiones, tab_imagenes = st.tabs(["📝 Generador de Guiones", "🎨 Creador de Imágenes"])

# ---------------------------------------------------------
# PESTAÑA 1: GENERADOR DE GUIONES VIRALES
# ---------------------------------------------------------
with tab_guiones:
    st.markdown("<br>", unsafe_allow_html=True)
    
    st.markdown("<h3 style='text-align: center; color: #f8fafc; font-size: 1.4rem; margin-top: -10px; text-shadow: 1px 1px 4px black;'>1º Selecciona tu Red Social</h3>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #cbd5e1; font-size: 0.95rem; margin-bottom: 20px; text-shadow: 1px 1px 2px black;'>Elige la plataforma para la que quieres crear contenido.</p>", unsafe_allow_html=True)

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

    st.markdown("<hr style='border:1px solid rgba(168, 85, 247, 0.2); margin: 30px 0;'>", unsafe_allow_html=True)

    st.markdown("<h3 style='text-align: center; color: #f8fafc; font-size: 1.4rem; text-shadow: 1px 1px 4px black;'>2º Describe tu Negocio al Detalle</h3>", unsafe_allow_html=True)
    
    nicho_cliente = st.text_area(
        "Oculto 1", 
        placeholder='Ej: "Soy entrenador personal online y quiero vender retos de 30 días para perder peso en casa. Mi público objetivo son madres ocupadas..."', 
        label_visibility="collapsed",
        height=140 
    )

    st.markdown("<br>", unsafe_allow_html=True)

    col_esp1, col_btn_gen, col_esp2 = st.columns([1, 1.5, 1])
    with col_btn_gen:
        boton_generar = st.button("✨ Generar Guiones Virales", type="primary", use_container_width=True, key="btn_ideas")

    if boton_generar:
        if nicho_cliente:
            red_elegida = st.session_state['red_activa']
            with st.spinner(f'Digitalis IA está generando magia para {red_elegida}...'):
                prompt_secreto = f"""Eres el Director Creativo de DIGITALIS IA. El cliente dice: "{nicho_cliente}". Genera 3 ideas virales EXCLUSIVAMENTE para {red_elegida}. Incluye: Título gancho, guion de 15s y 3 hashtags. REGLA DE ORO: Responde SOLO en Español."""
                try:
                    respuesta = client.models.generate_content(model='gemini-2.5-flash', contents=prompt_secreto)
                    st.success(f"¡Aquí tienes tus ideas para {red_elegida}!")
                    st.write(respuesta.text)
                except Exception as e:
                    st.error("❌ ERROR DE CONEXIÓN CON GOOGLE")
        else:
            st.warning("Por favor, describe tu negocio primero en la caja de texto.")

# ---------------------------------------------------------
# PESTAÑA 2: CREADOR DE IMÁGENES (ANTI-BLOQUEOS DEFINITIVO)
# ---------------------------------------------------------
with tab_imagenes:
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center; color: #f8fafc; font-size: 1.4rem; text-shadow: 1px 1px 4px black;'>Creador de Imágenes por IA</h3>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #cbd5e1; font-size: 0.95rem; margin-bottom: 20px; text-shadow: 1px 1px 2px black;'>Sube una foto de referencia o simplemente describe lo que quieres crear.</p>", unsafe_allow_html=True)

    imagen_subida = st.file_uploader("Sube tu imagen (Opcional)", type=["png", "jpg", "jpeg"])

    prompt_imagen = st.text_area(
        "Oculto 2", 
        placeholder='Ej: "Basándote en mi foto, ponle una gorra negra con logo de JEEP" o "Un gato ninja en la luna"...', 
        label_visibility="collapsed",
        height=100
    )

    st.markdown("<br>", unsafe_allow_html=True)

    col_esp_img1, col_btn_img, col_esp_img2 = st.columns([1, 1.5, 1])
    with col_btn_img:
        boton_imagen = st.button("🎨 Crear Imagen Mágica", type="primary", use_container_width=True, key="btn_img")

    if boton_imagen:
        if prompt_imagen or imagen_subida:
            
            texto_final_para_ia = prompt_imagen

            # 1. Gemini analiza la foto y crea un resumen INGLÉS y CORTÍSIMO
            if imagen_subida is not None:
                with st.spinner("👁️ Analizando la foto de referencia con Google Gemini..."):
                    try:
                        img_pil = Image.open(imagen_subida)
                        prompt_gemini = f"Actúa como un experto en prompts de imágenes. Describe esta foto y aplícale ESTA MODIFICACIÓN: '{prompt_imagen}'. REGLA ESTRICTA: Escribe máximo 20 palabras. Solo en INGLÉS. Sin comillas ni caracteres raros."
                        
                        respuesta_gemini = client.models.generate_content(
                            model='gemini-2.5-flash', 
                            contents=[img_pil, prompt_gemini]
                        )
                        texto_final_para_ia = respuesta_gemini.text
                        
                    except Exception as e:
                        st.error("Hubo un error al leer tu imagen de referencia.")
            
            # 2. Generar el enlace visual
            if texto_final_para_ia:
                st.success("¡Obra de arte en proceso!")
                st.info("💡 Tu navegador está descargando la imagen. Puede tardar de 5 a 15 segundos en aparecer justo aquí abajo 👇")
                
                url_final = generar_url_imagen(texto_final_para_ia)
                
                # Le decimos a Streamlit que muestre la URL. Esto obliga al navegador del usuario a cargarla, saltando cualquier bloqueo.
                st.image(url_final, caption="Tu nueva imagen generada por IA", use_container_width=True)

                st.markdown(f"""
                <div style="display: flex; justify-content: center; margin-top: 15px;">
                    <a href="{url_final}" target="_blank" style="padding: 10px 20px; background-color: #a855f7; color: white; text-decoration: none; border-radius: 8px; font-weight: bold; box-shadow: 0 5px 15px rgba(0,0,0,0.5);">⬇️ Abrir imagen en Alta Calidad</a>
                </div>
                """, unsafe_allow_html=True)

        else:
            st.warning("Por favor, describe qué quieres que la IA pinte o sube una imagen.")

# --- PIE DE PÁGINA ---
st.markdown("<p style='text-align: center; font-size: 13px; color: #a855f7; margin-top: 60px;'>Desarrollado con 💜 por <b>DIGITALIS IA</b></p>", unsafe_allow_html=True)
