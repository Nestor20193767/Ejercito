import pandas as pd
import os
from io import BytesIO
# Se llama a la contraseña
PASSWORD = st.secrets["password"]
# Función para autenticar al usuario
def authenticate():
    st.title("Autenticación")
    password_input = st.text_input("Ingrese la contraseña:", type='password')
    
    if password_input == PASSWORD:
        return True
    else:
        st.error("Contraseña incorrecta.")
        return False
# Configuración del archivo de base de datos
DATABASE_FILE = 'database.txt'

@@ -44,83 +57,82 @@ def download_excel(data, download_option):
    )

# Iniciar la app
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
if authenticate():  # Solo si la autenticación es correcta, se procede
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

