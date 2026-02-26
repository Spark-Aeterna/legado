import streamlit as st
import time
import sqlite3
from datetime import date
from cryptography.fernet import Fernet

# --- CONFIGURACIÓN DE LA "PIEDRA" (BASE DE DATOS) ---
def conectar_db():
    conn = sqlite3.connect('legados_eternos.db', check_same_thread=False)
    return conn

def crear_tablas():
    conn = conectar_db()
    c = conn.cursor()
    # Creamos la tabla si no existe (Nombre, Vínculo, Fecha, Contenido Encriptado, Llave)
    c.execute('''CREATE TABLE IF NOT EXISTS chispas 
                 (id INTEGER PRIMARY KEY, categoria TEXT, nombre TEXT, fecha TEXT, contenido BLOB, llave TEXT, archivo TEXT)''')
    conn.commit()
    conn.close()

crear_tablas()

# --- CONFIGURACIÓN VISUAL ---
st.set_page_config(page_title="Spark Aeterna - Memoria de Piedra", page_icon="✨")
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: #f8f9fa; }
    .stButton>button { background-color: #d4af37; color: black; border-radius: 10px; font-weight: bold; width: 100%; }
    h1, h2, h3 { color: #d4af37 !important; text-align: center; }
    .stExpander { background-color: #1e2130; border: 1px solid #d4af37; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

st.title("🛡️ SPARK AETERNA")
st.write("### *El Santuario que Nunca Olvida*")

tab1, tab2 = st.tabs(["🔥 CREAR LEGADO", "🔑 BÓVEDA ETERNA"])

# --- TAB 1: ESCRIBIR EN LA PIEDRA ---
with tab1:
    st.write("#### Configura un nuevo mensaje eterno")
    col1, col2 = st.columns(2)
    with col1:
        categoria = st.selectbox("Vínculo", ["Hija/Hijo", "Esposa/Esposo", "Madre/Padre", "Hermanas/Hermanos", "Otro"])
    with col2:
        nombre_destinatario = st.text_input("Nombre de la persona")
        
    fecha_revelacion = st.date_input("¿Cuándo debe revelarse?", min_value=date.today())
    archivo = st.file_uploader("Cargar video o imagen", type=["mp4", "mov", "jpg", "png"])
    
    if archivo and nombre_destinatario:
        if st.button(f"✨ GRABAR EN LA PIEDRA PARA {nombre_destinatario.upper()}"):
            # Encriptación
            llave = Fernet.generate_key()
            f = Fernet(llave)
            contenido_encriptado = f.encrypt(archivo.read())
            
            # Guardar en Base de Datos
            conn = conectar_db()
            c = conn.cursor()
            c.execute("INSERT INTO chispas (categoria, nombre, fecha, contenido, llave, archivo) VALUES (?,?,?,?,?,?)",
                      (categoria, nombre_destinatario, str(fecha_revelacion), contenido_encriptado, llave.decode(), archivo.name))
            conn.commit()
            conn.close()
            
            with st.status("Tallando en la base de datos...", expanded=False):
                time.sleep(2)
            st.success(f"✅ Legado de {nombre_destinatario} grabado para la eternidad.")
            st.balloons()

# --- TAB 2: LEER LA PIEDRA ---
with tab2:
    conn = conectar_db()
    c = conn.cursor()
    c.execute("SELECT DISTINCT nombre FROM chispas")
    nombres = [fila[0] for fila in c.fetchall()]
    
    if not nombres:
        st.warning("La bóveda está esperando su primera inscripción.")
    else:
        seleccion = st.selectbox("¿De quién buscas el legado?", nombres)
        
        c.execute("SELECT categoria, nombre, fecha, contenido, llave, archivo FROM chispas WHERE nombre = ?", (seleccion,))
        legados = c.fetchall()
        
        for leg en legados:
            with st.expander(f"📦 {leg[0]} - {leg[1]} ({leg[5]})"):
                hoy = str(date.today())
                if hoy < leg[2]:
                    st.error(f"⏳ BLOQUEADO hasta el {leg[2]}")
                else:
                    st.success("✨ LISTO PARA REVELAR")
                    if st.button(f"🔓 ABRIR MENSAJE", key=f"btn_{leg[5]}"):
                        f = Fernet(leg[4].encode())
                        original = f.decrypt(leg[3])
                        st.video(original)
    conn.close()
