import streamlit as st
import pandas as pd
import os
from io import BytesIO
import streamlit_authenticator as stauth
from datetime import timedelta

# Configuración del usuario y contraseña (guardada en st.secrets)
USER_NAME = "USUARIO"
PASSWORD = st.secrets["password"]

# Lista de usuarios y contraseñas (en este caso, solo un usuario)
credentials = {
    'usernames': {
        'USUARIO': {
            'name': 'Ejercito',
            'password': PASSWORD  # Acceder a la contraseña desde secrets
        }
    }
}

# Crear una instancia del autenticador
authenticator = stauth.Authenticate(
    credentials,
    cookie_name="authenticator_cookie",  # Nombre de la cookie
    key="authenticator_key",  # Clave secreta para la cookie
    cookie_expiry_days=30  # Caducidad de la cookie en 30 días
)

# Autenticación
authentication_status = authenticator.login(location="main")
# name, username
if authentication_status:
    # Si la autenticación es exitosa
    st.success(f"Bienvenido !")

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

    def download_excel(data, download_option):
        output = BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            data.to_excel(writer, index=False, sheet_name='Sheet1')
        output.seek(0)
        st.download_button(f'Descargar {download_option}.xlsx', output, 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

    # Iniciar la app
    st.title("Sistema de Registro de Placas de Vehículos")
    data = load_data()

    # Crear un menú de navegación
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

elif authentication_status == False:
    st.error("Usuario o contraseña incorrecta.")

elif authentication_status is None:
    st.warning("Por favor ingrese sus credenciales.")
