import streamlit as st
import time
from cryptography.fernet import Fernet

# --- MEMORIA DEL SISTEMA ---
if 'llave_maestra' not in st.session_state:
    st.session_state.llave_maestra = None
if 'archivo_encriptado' not in st.session_state:
    st.session_state.archivo_encriptado = None

# --- ESTILO ---
st.set_page_config(page_title="Spark Aeterna - Prototipo", page_icon="✨")
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: #f8f9fa; }
    .stButton>button { background-color: #d4af37; color: black; border-radius: 10px; font-weight: bold; width: 100%; border: none; }
    h1, h2, h3 { color: #d4af37 !important; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

st.title("🛡️ SPARK AETERNA")
st.write("### *Legado Digital Inteligente*")

tab1, tab2 = st.tabs(["🔒 PROTEGER", "🔑 REVELAR"])

# --- TAB 1: ENCRIPTAR ---
with tab1:
    st.write("#### Paso 1: Crea tu Legado")
    archivo = st.file_uploader("Sube tu mensaje", type=["mp4", "mov", "jpg", "png"])
    
    if archivo:
        if st.button("🌟 BLINDAR CON EL NEXO"):
            llave = Fernet.generate_key()
            f = Fernet(llave)
            contenido = archivo.read()
            
            # Guardamos en la memoria de la App
            st.session_state.archivo_encriptado = f.encrypt(contenido)
            st.session_state.llave_maestra = llave.decode()
            
            with st.status("Generando protección cuántica...", expanded=False):
                time.sleep(2)
            
            st.success("✅ ¡Blindado! La llave ha sido enviada a la memoria segura.")
            st.info(f"Llave generada: {st.session_state.llave_maestra[:10]}...")

# --- TAB 2: DESENCRIPTAR ---
with tab2:
    st.write("#### Paso 2: El Regreso del Mensaje")
    
    if st.session_state.llave_maestra:
        st.write("🔒 **Estado:** Llave detectada en el Nexo (Simulando Biometría)")
        
        if st.button("🔓 REVELAR LEGADO"):
            try:
                f = Fernet(st.session_state.llave_maestra.encode())
                original = f.decrypt(st.session_state.archivo_encriptado)
                
                with st.spinner("Sincronizando..."):
                    time.sleep(1.5)
                
                st.success("Acceso concedido.")
                # Muestra el video directamente
                st.video(original)
            except:
                st.error("Error en la sincronización.")
    else:
        st.warning("No hay ningún mensaje protegido en memoria. Ve a la pestaña 'PROTEGER' primero.")