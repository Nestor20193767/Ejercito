import streamlit as st
import pandas as pd
import os
from io import BytesIO
# Se llama a la contraseña
PASSWORD = st.secrets["password"]
# Configuración del archivo de base de datos
DATABASE_FILE = 'database.txt'

# Función para leer la base de datos del archivo
def load_data():
    if os.path.exists(DATABASE_FILE) and os.path.getsize(DATABASE_FILE) > 0:  # Verificar si el archivo existe y no está vacío
        return pd.read_csv(DATABASE_FILE, sep='|')
    else:
        return pd.DataFrame(columns=['Placa', 'Nombre', 'Tipo', 'Incidencias'])

# Función para guardar la base de datos en el archivo
def save_data(df):
    df.to_csv(DATABASE_FILE, sep='|', index=False)

# Función para filtrar por tipo de fuerza
def filter_by_type(df, tipo):
    return df[df['Tipo'] == tipo]

# Función para descargar el DataFrame como archivo Excel
def download_excel(data, download_option):
    if data.empty:
        st.warning("No hay datos para descargar.")
        return
    # Crear un objeto BytesIO
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        data.to_excel(writer, index=False, sheet_name='Sheet1')
    # Posicionar el puntero al principio del archivo
    output.seek(0)
    # Determina el nombre del archivo en función de la opción de descarga
    file_name = f'database_{download_option}.xlsx' if download_option else 'database.xlsx'
    # Descargar el archivo
    st.download_button(
        label="Descargar Excel",
        data=output,
        file_name=file_name,
        mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
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



