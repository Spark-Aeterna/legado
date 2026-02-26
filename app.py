import streamlit as st
import time
from datetime import date
from cryptography.fernet import Fernet

# --- INICIALIZACIÓN DE LA BÓVEDA ---
if 'biblioteca_legados' not in st.session_state:
    st.session_state.biblioteca_legados = []

# --- CONFIGURACIÓN VISUAL (ESTILO NEXO) ---
st.set_page_config(page_title="Spark Aeterna - Bóveda", page_icon="✨")
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: #f8f9fa; }
    .stButton>button { background-color: #d4af37; color: black; border-radius: 10px; font-weight: bold; border: none; }
    h1, h2, h3 { color: #d4af37 !important; text-align: center; }
    .stExpander { background-color: #1e2130; border: 1px solid #d4af37; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

st.title("🛡️ SPARK AETERNA")
st.write("### *El Santuario de los Perfiles Eternos*")

tab1, tab2 = st.tabs(["🔥 CREAR LEGADO", "🔑 BÓVEDA DE PERFILES"])

# --- TAB 1: CREAR (EL ORIGEN) ---
with tab1:
    st.write("#### Selecciona el Destinatario de esta Chispa")
    perfil = st.selectbox("Perfil del Destinatario", ["Hijo", "Esposa", "Padre/Madre", "Hermanas", "Otro"])
    if perfil == "Otro":
        perfil = st.text_input("Especifica el nombre del perfil:")
        
    fecha_revelacion = st.date_input("¿Cuándo se encenderá esta hoguera?", min_value=date.today())
    archivo = st.file_uploader("Sube el mensaje eterno", type=["mp4", "mov", "jpg", "png"])
    
    if archivo and perfil:
        if st.button(f"✨ SPARKEAR PARA {perfil.upper()}"):
            # Proceso de Encriptación
            llave = Fernet.generate_key()
            f = Fernet(llave)
            nuevo_legado = {
                "perfil": perfil,
                "fecha": fecha_revelacion,
                "contenido": f.encrypt(archivo.read()),
                "llave": llave.decode(),
                "nombre_archivo": archivo.name
            }
            # Guardamos en la lista (La Biblioteca)
            st.session_state.biblioteca_legados.append(nuevo_legado)
            
            with st.status("Blindando legado en la Bóveda...", expanded=False):
                time.sleep(2)
            st.success(f"✅ ¡Chispa guardada con éxito para {perfil}!")
            st.balloons()

# --- TAB 2: BÓVEDA (LOS PERFILES) ---
with tab2:
    if not st.session_state.biblioteca_legados:
        st.warning("La bóveda está vacía. Inicia una hoguera primero.")
    else:
        st.write("### 🔑 Acceder a un Legado Custodiado")
        
        # Agrupamos por perfil para que se vea organizado
        perfiles_disponibles = list(set([l['perfil'] for l in st.session_state.biblioteca_legados]))
        seleccion_perfil = st.selectbox("¿De quién buscas el legado?", perfiles_disponibles)
        
        # Filtramos los mensajes de ese perfil
        mensajes_perfil = [l for l in st.session_state.biblioteca_legados if l['perfil'] == seleccion_perfil]
        
        for idx, legado in enumerate(mensajes_perfil):
            with st.expander(f"📦 Legado #{idx+1}: {legado['nombre_archivo']}"):
                hoy = date.today()
                if hoy < legado['fecha']:
                    st.error(f"⏳ BLOQUEADO hasta el {legado['fecha']}")
                else:
                    st.success("✨ LISTO PARA REVELAR")
                    if st.button(f"🔓 ABRIR MENSAJE #{idx+1}", key=f"btn_{idx}"):
                        try:
                            f = Fernet(legado['llave'].encode())
                            original = f.decrypt(legado['contenido'])
                            st.video(original)
                        except:
                            st.error("Error al sincronizar con el Nexo.")
