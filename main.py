import streamlit as st
import pandas as pd
import os
from io import BytesIO

# Archivo de base de datos
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
def download_excel(data):
    if data.empty:
        st.warning("No hay datos para descargar.")
        return
    # Crear un objeto BytesIO
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        data.to_excel(writer, index=False, sheet_name='Sheet1')
    # Posicionar el puntero al principio del archivo
    output.seek(0)
    # Descargar el archivo
    st.download_button(
        label="Descargar Excel",
        data=output,
        file_name='database.xlsx',
        mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )

# Iniciar la app
st.title("Sistema de Registro de Placas de Vehículos")

# Cargar la base de datos
data = load_data()

# Mostrar la cantidad de registros totales
st.write(f"**Total de placas registradas: {len(data)}**")

# Contadores por tipo
st.write(f"**Placas de Policía:** {len(filter_by_type(data, 'Policía'))}")
st.write(f"**Placas de Ejército:** {len(filter_by_type(data, 'Ejército'))}")
st.write(f"**Placas de Fuerza Aérea:** {len(filter_by_type(data, 'Fuerza Aérea'))}")
st.write(f"**Placas de Naval:** {len(filter_by_type(data, 'Naval'))}")

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

# Buscar placas registradas
st.subheader("Buscar Placa Registrada")
search_placa = st.text_input("Buscar por Placa:")
if st.button("Buscar"):
    result = data[data['Placa'] == search_placa]
    if not result.empty:
        st.write(result)
    else:
        st.error("Placa no encontrada.")

# Descargar registros filtrados o completos
st.subheader("Descargar Registros")
download_option = st.selectbox("Seleccione qué registros desea descargar:", ["Registro completo", "Policía", "Ejército", "Fuerza Aérea", "Naval"])

if st.button("Descargar"):
    if download_option == "Registro completo":
        download_excel(data)
        st.success("Archivo de registro completo descargado.")
    else:
        filtered_data = filter_by_type(data, download_option)
        download_excel(filtered_data, download_option)
        st.success(f"Archivo de registros de {download_option} descargado.")

