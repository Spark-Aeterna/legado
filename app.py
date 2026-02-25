import streamlit as st
import time
from datetime import date
from cryptography.fernet import Fernet

# --- MEMORIA DEL SISTEMA ---
if 'llave_maestra' not in st.session_state:
    st.session_state.llave_maestra = None
if 'archivo_encriptado' not in st.session_state:
    st.session_state.archivo_encriptado = None
if 'metadata' not in st.session_state:
    st.session_state.metadata = {}

# --- CONFIGURACIÓN VISUAL ---
st.set_page_config(page_title="Spark Aeterna", page_icon="✨")
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: #f8f9fa; }
    .stButton>button { background-color: #d4af37; color: black; border-radius: 10px; font-weight: bold; border: none; }
    h1, h2, h3 { color: #d4af37 !important; text-align: center; }
    .stDateInput>div>div>input { background-color: #1e2130; color: #d4af37; border: 1px solid #d4af37; }
    </style>
    """, unsafe_allow_html=True)

st.title("🛡️ SPARK AETERNA")
st.write("### *Donde la chispa enciende la eternidad*")

tab1, tab2 = st.tabs(["🔥 INICIAR HOGUERA", "🔑 REVELAR CHISPA"])

# --- TAB 1: EL ORIGEN (ENCRIPTAR) ---
with tab1:
    st.write("#### Configura tu Legado")
    destinatario = st.text_input("¿Para quién es esta chispa? (Ej. Mi hijo, Mi esposa)")
    fecha_revelacion = st.date_input("¿Cuándo debe encenderse esta hoguera?", min_value=date.today())
    archivo = st.file_uploader("Sube el mensaje eterno", type=["mp4", "mov", "jpg", "png"])
    
    if archivo and destinatario:
        if st.button("✨ GENERAR CHISPA ETERNA"):
            llave = Fernet.generate_key()
            f = Fernet(llave)
            contenido = archivo.read()
            
            # Guardamos en la memoria y la metadata
            st.session_state.archivo_encriptado = f.encrypt(contenido)
            st.session_state.llave_maestra = llave.decode()
            st.session_state.metadata = {
                "destinatario": destinatario,
                "fecha": fecha_revelacion
            }
            
            with st.status("Sincronizando con el Nexo...", expanded=False):
                time.sleep(2)
            
            st.success(f"✅ Chispa creada para {destinatario}.")
            st.info(f"🔒 Bloqueada hasta: {fecha_revelacion}")

# --- TAB 2: EL DESTINO (DESENCRIPTAR) ---
with tab2:
    if st.session_state.llave_maestra:
        meta = st.session_state.metadata
        st.write(f"### Mensaje custodiado para: **{meta['destinatario']}**")
        
        hoy = date.today()
        if hoy < meta['fecha']:
            st.warning(f"⏳ El tiempo no ha llegado. Esta chispa se encenderá el {meta['fecha']}.")
            st.write("*(Simulando bloqueo temporal de legado)*")
        else:
            st.success("✨ ¡El tiempo es ahora! La hoguera puede ser encendida.")
        
        # El botón solo funciona si la identidad es correcta (Simulado)
        if st.button("🔓 ENCENDER HOGUERA"):
            try:
                f = Fernet(st.session_state.llave_maestra.encode())
                original = f.decrypt(st.session_state.archivo_encriptado)
                
                with st.spinner("Liberando el legado..."):
                    time.sleep(1.5)
                
                st.video(original)
                st.balloons()
            except:
                st.error("Error en la sincronización de la chispa.")
    else:
        st.warning("No hay chispas activas en este nexo. Regresa a 'INICIAR HOGUERA'.")
