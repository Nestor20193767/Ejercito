import streamlit as st
import pandas as pd
import os
from io import BytesIO
from datetime import datetime

# Sheet creada: https://www.youtube.com/watch?v=jeZWv5PQJAk
# Configuración de la contraseña
PASSWORD = st.secrets['password'] # Cambia esto a la contraseña deseada
# Iconos y Logos para las paginas
icono_url = "https://raw.githubusercontent.com/Nestor20193767/Ejercito/main/ico_SIREVE-removebg-preview%20(1).png"
logo_url = "https://raw.githubusercontent.com/Nestor20193767/Ejercito/main/PLA___2_-removebg-preview%20(1).png"
st.set_page_config(page_icon = icono_url, page_title='SIREVE')
# Función para mostrar la página principal
def main_page():
    #st.title("SIREVE: Sistema de Registro de Placas de Vehículos")
    
    #st.set_page_config(page_icon = icono_url, page_title='SIREVE')
    
    st.markdown(
        """
        <style>
        .header {
            display: flex;
            align-items: center;
        }
        .header img {
            margin-right: 20px; /* Espaciado entre la imagen y el título */
        }
        </style>
        <div class="header">
            <img src="https://raw.githubusercontent.com/Nestor20193767/Ejercito/main/PLA___2_-removebg-preview%20(1).png" width="80">
            <h1 style="margin: 0;">SIREVE</h1>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # Cargar la base de datos
    DATABASE_FILE = 'database.txt'

    def load_data():
        if os.path.exists(DATABASE_FILE) and os.path.getsize(DATABASE_FILE) > 0:
            return pd.read_csv(DATABASE_FILE, sep='|')
        else:
            return pd.DataFrame(columns=['Placa', 'Nombre', 'Tipo', 'Incidencias'])

    def save_data(data):
        data.to_csv(DATABASE_FILE, sep='|', index=False)

    def filter_by_type(data, tipo):
        return data[data['Tipo'] == tipo]

        # Función para descargar el archivo de Excel en formato .xlsx
    def download_excel(data, download_option):
        # Obtener la fecha actual en el formato deseado
        today = datetime.today().strftime('%d_%m_%y')
    
        # Crear el nombre del archivo en el formato dd_mm_aa_nombre
        file_name = f"{today}_{download_option}.xlsx"
    
        # Crear el archivo Excel en memoria (en formato .xlsx)
        output = BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:  # Usar xlsxwriter para generar archivos .xlsx
            data.to_excel(writer, index=False, sheet_name='Sheet1')
    
        output.seek(0)  # Mover el puntero al inicio del archivo en memoria

        # Crear un boton de descarga
        Descarga = st.download_button(
            label=f'Descargar {download_option}.xlsx',
            data=output,
            file_name=file_name,
            mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        
    # Iniciar la app
    data = load_data()

    # Crear un menú de navegación
    st.sidebar.markdown(
        """
        <style>
        .header {
            display: flex;
            align-items: center;
        }
        .header img {
            margin-right: 20px; /* Espaciado entre la imagen y el título */
        }
        </style>
        <div class="header">
            <img src="https://raw.githubusercontent.com/Nestor20193767/Ejercito/main/PLA___2_-removebg-preview%20(1).png" width="80">
            <h1 style="margin: 0;">SIREVE: Sistema de Registro de Placas de Vehículos</h1>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    st.sidebar.title("Navegación")
    page = st.sidebar.radio("Seleccione una página:", ["Registrar Placa", "Buscar Placa", "Contadores", "Mostrar Base de Datos"])

    if page == "Registrar Placa":
        st.subheader("Registrar Nueva Placa")
        placa = st.text_input("Placa del Vehículo:")
        nombre = st.text_input("Nombre del Dueño:")
        tipo = st.selectbox("Tipo de Vehículo:", ["Policía", "Ejército", "Fuerza Aérea", "Naval"])
        incidencias = st.number_input("Número de Incidencias:", min_value=0, step=1)

        if st.button("Registrar"):
            if placa and nombre:
                new_data = pd.DataFrame({
                    'Placa': [placa],
                    'Nombre': [nombre],
                    'Tipo': [tipo],
                    'Incidencias': [incidencias]
                })
                data = pd.concat([data, new_data], ignore_index=True)
                save_data(data)
                st.success(f"Placa {placa} registrada con éxito.")
            else:
                st.error("Debe completar todos los campos para registrar una nueva placa.")

    elif page == "Buscar Placa":
        st.subheader("Buscar Placa Registrada")
        search_placa = st.text_input("Buscar por Placa:")
        if st.button("Buscar"):
            result = data[data['Placa'] == search_placa]
            if not result.empty:
                st.write(result)
            else:
                st.error("Placa no encontrada.")

    elif page == "Contadores":
        st.subheader("Contadores de Placas por Tipo")
        tipo_count = {
            "Policía": len(filter_by_type(data, 'Policía')),
            "Ejército": len(filter_by_type(data, 'Ejército')),
            "Fuerza Aérea": len(filter_by_type(data, 'Fuerza Aérea')),
            "Naval": len(filter_by_type(data, 'Naval')),
            "Conteo Total de Placas": len(data)
        }
        selected_type = st.selectbox("Seleccione el tipo de vehículo:", list(tipo_count.keys()))
        st.write(f"**Placas de {selected_type}:** {tipo_count[selected_type]}")

    elif page == "Mostrar Base de Datos":
        st.subheader("Base de Datos de Placas Registradas")
        if not data.empty:
            st.write(data)
        else:
            st.error("No hay datos disponibles.")

    # Descargar registros filtrados o completos
    st.sidebar.subheader("Descargar Registros")
    download_option = st.sidebar.selectbox("Seleccione qué registros desea descargar:", ["Registro completo", "Policía", "Ejército", "Fuerza Aérea", "Naval"])
    
    if st.sidebar.button("Descargar"):
        if download_option == "Registro completo":
            download_excel(data, download_option)
            st.success("Archivo de registro completo descargado.")
        else:
            filtered_data = filter_by_type(data, download_option)
            download_excel(filtered_data, download_option)
            st.success(f"Archivo de registros de {download_option} descargado.")

# Función para mostrar el formulario de inicio de sesión
def login_page():
    #st.title("Iniciar Sesión")
    st.markdown(
        """
        <style>
        .header {
            display: flex;
            align-items: center;
        }
        .header img {
            margin-right: 20px; /* Espaciado entre la imagen y el título */
        }
        </style>
        <div class="header">
            <img src="https://raw.githubusercontent.com/Nestor20193767/Ejercito/main/PLA___2_-removebg-preview%20(1).png" width="80">
            <h1 style="margin: 0;">Iniciar Sesión</h1>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    #st.set_page_config(page_icon = icono_url, page_title='SIREVE')
    
    # Crear un formulario para el inicio de sesión
    with st.form("login_form"):
        username = st.text_input("Usuario")
        password = st.text_input("Contraseña", type="password")
        submitted = st.form_submit_button("Iniciar Sesión")

        # Validar la contraseña
        if submitted:
            if password == PASSWORD:
                st.session_state.authenticated = True  # Cambiamos el estado de autenticación
            else:
                st.error("Contraseña incorrecta")

# Comprobar si el usuario ya está autenticado
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

# Si está autenticado, mostrar la página principal
if st.session_state.authenticated:
    main_page()
else:
    # Si no está autenticado, mostrar la página de inicio de sesión
    login_page()

