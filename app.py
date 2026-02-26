import streamlit as st
import time
from datetime import date
from cryptography.fernet import Fernet

# --- INICIALIZACIÓN DE LA BÓVEDA ---
if 'biblioteca_legados' not in st.session_state:
    st.session_state.biblioteca_legados = []

# --- CONFIGURACIÓN VISUAL ---
st.set_page_config(page_title="Spark Aeterna", page_icon="✨")
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: #f8f9fa; }
    .stButton>button { background-color: #d4af37; color: black; border-radius: 10px; font-weight: bold; border: none; width: 100%; }
    h1, h2, h3 { color: #d4af37 !important; text-align: center; }
    .stExpander { background-color: #1e2130; border: 1px solid #d4af37; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

st.title("🛡️ SPARK AETERNA")
st.write("### *Santuario de Legados Personales*")

tab1, tab2 = st.tabs(["🔥 CREAR LEGADO", "🔑 BÓVEDA DE PERFILES"])

# --- TAB 1: CREAR (AÑADIMOS NOMBRE) ---
with tab1:
    st.write("#### ¿A quién confías este mensaje?")
    
    # Categoría inclusiva y Nombre personalizado
    col1, col2 = st.columns(2)
    with col1:
        categoria = st.selectbox("Vínculo", ["Hija/Hijo", "Esposa/Esposo", "Madre/Padre", "Hermanas/Hermanos", "Otro"])
    with col2:
        nombre_destinatario = st.text_input("Nombre de la persona", placeholder="Ej. Sofía")
        
    fecha_revelacion = st.date_input("¿Cuándo debe revelarse?", min_value=date.today())
    archivo = st.file_uploader("Cargar video o imagen", type=["mp4", "mov", "jpg", "png"])
    
    if archivo and nombre_destinatario:
        etiqueta_boton = f"✨ SPARKEAR PARA {nombre_destinatario.upper()}"
        if st.button(etiqueta_boton):
            llave = Fernet.generate_key()
            f = Fernet(llave)
            
            # Guardamos con identidad completa
            nuevo_legado = {
                "categoria": categoria,
                "nombre": nombre_destinatario,
                "fecha": fecha_revelacion,
                "contenido": f.encrypt(archivo.read()),
                "llave": llave.decode(),
                "nombre_archivo": archivo.name
            }
            st.session_state.biblioteca_legados.append(nuevo_legado)
            
            with st.status("Sincronizando con el Nexo...", expanded=False):
                time.sleep(2)
            st.success(f"✅ Legado blindado para {nombre_destinatario}.")
            st.balloons()

# --- TAB 2: BÓVEDA (VISUALIZACIÓN POR NOMBRE) ---
with tab2:
    if not st.session_state.biblioteca_legados:
        st.warning("La bóveda está esperando tu primera chispa.")
    else:
        st.write("### 🔑 Archivos Custodiados")
        
        # Lista de nombres para elegir
        nombres_en_boveda = list(set([l['nombre'] for l in st.session_state.biblioteca_legados]))
        seleccion_nombre = st.selectbox("¿De quién buscas el legado?", nombres_en_boveda)
        
        mensajes_filtrados = [l for l in st.session_state.biblioteca_legados if l['nombre'] == seleccion_nombre]
        
        for idx, legado in enumerate(mensajes_filtrados):
            with st.expander(f"📦 {legado['categoria']} - {legado['nombre']} ({legado['nombre_archivo']})"):
                hoy = date.today()
                if hoy < legado['fecha']:
                    st.error(f"⏳ BLOQUEADO hasta el {legado['fecha']}")
                else:
                    st.success("✨ LISTO PARA REVELAR")
                    if st.button(f"🔓 ABRIR MENSAJE", key=f"btn_{idx}_{legado['nombre']}"):
                        f = Fernet(legado['llave'].encode())
                        original = f.decrypt(legado['contenido'])
                        st.video(original)
