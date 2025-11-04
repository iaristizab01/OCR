import streamlit as st
import cv2
import numpy as np
import pytesseract
from PIL import Image

# --- CONFIGURACIÓN DE ESTILO ---
st.set_page_config(page_title="La Máquina que Lee", page_icon="🪶", layout="centered")

# CSS personalizado para estética minimalista
st.markdown("""
    <style>
    body {
        background-color: white;
        color: black;
        font-family: 'Helvetica Neue', sans-serif;
    }
    .stApp {
        background-color: white;
        color: black;
    }
    h1 {
        text-align: center;
        font-size: 2.2em;
        margin-bottom: 0.3em;
        color: #111;
    }
    .stRadio > label {
        color: #111 !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- NARRATIVA Y ENCABEZADO ---
st.title("“La máquina que lee lo que el ojo ignora”")
st.caption("Experimento sobre cómo una red neuronal interpreta el lenguaje visual.")

st.write(
    """
    Captura una imagen.  
    La máquina la observará, descompondrá la luz y reconstruirá tus palabras.  
    A veces fiel, a veces errante.
    """
)

# --- SIDEBAR INTERACTIVO ---
with st.sidebar:
    st.header("Ajustes de percepción 🧠")
    filtro = st.radio("Modo de visión", ('Con Filtro', 'Sin Filtro'))
    st.markdown("---")
    st.write(
        "“El filtro invierte la luz, como si el ojo de la máquina viera desde la sombra.”"
    )

# --- CAPTURA DE IMAGEN ---
img_file_buffer = st.camera_input("Observa el mundo desde la lente de la máquina:")

# --- PROCESAMIENTO Y OCR ---
if img_file_buffer is not None:
    bytes_data = img_file_buffer.getvalue()
    cv2_img = cv2.imdecode(np.frombuffer(bytes_data, np.uint8), cv2.IMREAD_COLOR)
    
    # Aplicar filtro
    if filtro == 'Con Filtro':
        cv2_img = cv2.bitwise_not(cv2_img)
    else:
        cv2_img = cv2_img

    # Convertir a RGB
    img_rgb = cv2.cvtColor(cv2_img, cv2.COLOR_BGR2RGB)
    
    # Extracción de texto
    text = pytesseract.image_to_string(img_rgb)
    
    st.image(img_rgb, caption="Imagen procesada por la máquina", use_column_width=True)
    
    # Mostrar resultado
    st.subheader("🪶 Resultado del experimento:")
    st.write(f"“{text.strip()}”" if text.strip() else "_La máquina no encontró palabras en la imagen._")
    
    st.caption("Reflexión: ¿Qué tanto comprendemos de lo que observamos?")
