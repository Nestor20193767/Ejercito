import pandas as pd
import os
import streamlit as st
import streamlit_authenticator as stauth
from io import BytesIO  # Asegúrate de importar esto si no está ya importado

# Se llama a la contraseña desde secrets
PASSWORD = st.secrets["password"]

# Configuración de las credenciales
credentials = {
    "usernames": {
        "USUARIO": {  # Cambia 'USUARIO' por el nombre que deseas usar
            "name": "Nombre del Usuario",  # Cambia esto según sea necesario
            "password": PASSWORD  # Usando la contraseña desde st.secrets
        }
    }
}

# Crear el objeto de autenticación
authenticator = stauth.Authenticate(
    credentials,
    cookie_name="nombre_cookie",
    cookie_key="clave_cookie",
    cookie_expiry_days=30,
)

# Autenticación
name, authentication_status = authenticator.login()  # Cambiado a 'sidebar'

# Configuración del archivo de base de datos
DATABASE_FILE = 'database.txt'

# Cargar la base de datos
def load_data():
    if os.path.exists(DATABASE_FILE) and os.path.getsize(DATABASE_FILE) > 0:
        return pd.read_csv(DATABASE_FILE, sep='|')
    else:
        return pd.DataFrame(columns=['Placa', 'Nombre', 'Tipo', 'Incidencias'])

# Guardar datos en el archivo
def save_data(data):
    data.to_csv(DATABASE_FILE, sep='|', index=False)

# Filtrar por tipo
def filter_by_type(data, tipo):
    return data[data['Tipo'] == tipo]

# Descargar datos como Excel
def download_excel(data, download_option):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        data.to_excel(writer, index=False, sheet_name='Sheet1')
    output.seek(0)
    st.download_button(f'Descargar {download_option}.xlsx', output, 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

# Iniciar la app
if authentication_status:
    st.success(f"Bienvenido, {name}!")  # Mensaje de bienvenida
    st.title("Sistema de Registro de Placas de Vehículos")
    
    # Cargar la base de datos
    data = load_data()
    
    # Crear un menú de navegación
    st.sidebar.title("Navegación")
    page = st.sidebar.radio("Seleccione una página:", ["Registrar Placa", "Buscar Placa", "Contadores", "Mostrar Base de Datos"])

    if page == "Registrar Placa":
        # Registro de nueva placa
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
        # Buscar placas registradas
        st.subheader("Buscar Placa Registrada")
        search_placa = st.text_input("Buscar por Placa:")
        if st.button("Buscar"):
            result = data[data['Placa'] == search_placa]
            if not result.empty:
                st.write(result)
            else:
                st.error("Placa no encontrada.")

    elif page == "Contadores":
        # Contadores por tipo
        st.subheader("Contadores de Placas por Tipo")
        tipo_count = {
            "Policía": len(filter_by_type(data, 'Policía')),
            "Ejército": len(filter_by_type(data, 'Ejército')),
            "Fuerza Aérea": len(filter_by_type(data, 'Fuerza Aérea')),
            "Naval": len(filter_by_type(data, 'Naval')),
            "Conteo Total de Placas": len(data)  # Sumar total de placas
        }
        
        # Menú desplegable para ver los contadores
        selected_type = st.selectbox("Seleccione el tipo de vehículo:", list(tipo_count.keys()))
        st.write(f"**Placas de {selected_type}:** {tipo_count[selected_type]}")

    elif page == "Mostrar Base de Datos":
        # Mostrar todo el contenido de la base de datos
        st.subheader("Base de Datos de Placas Registradas")
        if not data.empty:
            st.write(data)
        else:
            st.write("No hay datos disponibles.")

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

else:
    st.warning("Por favor ingrese sus credenciales.")  # Mensaje si la autenticación falla

