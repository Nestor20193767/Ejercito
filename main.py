import streamlit as st
import pandas as pd
import os

# Contraseña inicial para usar la app
PASSWORD = "Ejercito2024"

# Archivo de base de datos
DATABASE_FILE = 'database.txt'

# Función para leer la base de datos del archivo
def load_data():
    if os.path.exists(DATABASE_FILE):
        return pd.read_csv(DATABASE_FILE, sep='|')
    else:
        return pd.DataFrame(columns=['Placa', 'Nombre', 'Tipo', 'Incidencias'])

# Función para guardar la base de datos en el archivo
def save_data(df):
    df.to_csv(DATABASE_FILE, sep='|', index=False)

# Función para filtrar por tipo de fuerza
def filter_by_type(df, tipo):
    return df[df['Tipo'] == tipo]

# Función para crear el archivo Excel descargable
def download_excel(df, tipo="Registro completo"):
    return df.to_excel(f"{tipo}.xlsx", index=False)

# Iniciar la app con autenticación de contraseña
st.title("Sistema de Registro de Placas de Vehículos")

# Autenticación
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    password = st.text_input("Ingrese la contraseña:", type="password")
    if password == PASSWORD:
        st.session_state.authenticated = True
        st.success("Contraseña correcta. Accediendo al sistema.")
    else:
        if password:
            st.error("Contraseña incorrecta.")
else:
    st.subheader("Registro de Placas de Vehículos")

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
            st.download_button(
                label="Descargar Registro Completo",
                data=download_excel(data),
                file_name="registro_completo.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
        else:
            filtered_data = filter_by_type(data, download_option)
            st.download_button(
                label=f"Descargar Registros de {download_option}",
                data=download_excel(filtered_data, download_option),
                file_name=f"registro_{download_option.lower()}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
