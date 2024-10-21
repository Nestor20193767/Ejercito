import streamlit as st
import pandas as pd
import os
from io import BytesIO
from datetime import datetime

from streamlit_option_menu import option_menu

PASSWORD = st.secrets['password']
icono_url = "https://raw.githubusercontent.com/Nestor20193767/Ejercito/main/ico_SIREVE-removebg-preview%20(1).png"
logo_url = "https://raw.githubusercontent.com/Nestor20193767/Ejercito/main/PLA___2_-removebg-preview%20(1).png"
st.set_page_config(page_icon=icono_url, page_title='SIREVE', layout="wide")

# Función para mostrar la página principal
def main_page():
    st.markdown(
        """
        <style>
        .header {
            display: flex;
            align-items: center;
        }
        .header img {
            margin-right: 20px;
        }
        </style>
        <div class="header">
            <img src="https://raw.githubusercontent.com/Nestor20193767/Ejercito/main/PLA___2_-removebg-preview%20(1).png" width="80">
            <h1 style="margin: 0;">SIREVE</h1>
        </div>
        """, unsafe_allow_html=True
    ) 
    
    DATABASE_FILE = 'database.txt'

    def load_data():
        if os.path.exists(DATABASE_FILE) and os.path.getsize(DATABASE_FILE) > 0:
            return pd.read_csv(DATABASE_FILE, sep='|')
        else:
            # Nuevos campos de la base de datos
            return pd.DataFrame(columns=['Placa', 'Conductor Designado', 'Institucion', 'Estado', 'Preliminar', 'Expediente', 'Tipo de accidente', 'Persona a Cargo', 'Fecha'])

    def save_data(data):
        data.to_csv(DATABASE_FILE, sep='|', index=False)

    def filter_by_type(data, institucion):
        return data[data['Institucion'] == institucion]

    def download_excel(data, download_option):
        today = datetime.today().strftime('%d_%m_%y')
        file_name = f"{today}_{download_option}.xlsx"
    
        output = BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            data.to_excel(writer, index=False, sheet_name='Sheet1')
    
        output.seek(0)

        st.download_button(
            label=f'Descargar {download_option}.xlsx',
            data=output,
            file_name=file_name,
            mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        
    data = load_data()

    st.sidebar.markdown(
        """
        <style>
        .header {
            display: flex;
            align-items: center;
        }
        .header img {
            margin-right: 20px;
        }
        </style>
        <div class="header">
            <img src="https://raw.githubusercontent.com/Nestor20193767/Ejercito/main/PLA___2_-removebg-preview%20(1).png" width="80">
            <h1 style="margin: 0;">SIREVE: Sistema de Registro de Placas de Vehículos</h1>
        </div>
        """, unsafe_allow_html=True
    )

    with st.sidebar:
        page = option_menu(
            menu_title="Navegación",
            options=["Registrar Placa Oficial", "Buscar Placa", "Base de Datos", "Manual de Usuario"],
            icons=["card-text", "search", "database", "book"],
            default_index=0
        )

    if page == "Registrar Placa Oficial":
        st.subheader("Registrar Nueva Placa")

        # Modificar los campos solicitados
        institucion = st.selectbox("Institución:", ["Policía", "Ejército", "Fuerza Aérea", "Naval"])
        placa = st.text_input("Placa del Vehículo:")
        conductor = st.text_input("Conductor Designado:")
        estado = st.selectbox("Estado:", ["Pendiente", "Archivado"])
        preliminar = st.text_input("Preliminar:")
        expediente = st.text_input("Expediente:")
        tipo_accidente = st.text_area("Tipo de Accidente:")
        persona_a_cargo = st.text_input("Persona a Cargo:")
        fecha = st.date_input("Fecha", datetime.today())

        if st.button("Registrar"):
            if placa and conductor:
                new_data = pd.DataFrame({
                    'Placa': [placa],
                    'Conductor Designado': [conductor],
                    'Institucion': [institucion],
                    'Estado': [estado],
                    'Preliminar': [preliminar],
                    'Expediente': [expediente],
                    'Tipo de accidente': [tipo_accidente],
                    'Persona a Cargo': [persona_a_cargo],
                    'Fecha': [fecha]
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

    elif page == "Base de Datos":
        st.subheader("Base de Datos de Placas por Institución")
        institucion_count = {
            "Policía": len(filter_by_type(data, 'Policía')),
            "Ejército": len(filter_by_type(data, 'Ejército')),
            "Fuerza Aérea": len(filter_by_type(data, 'Fuerza Aérea')),
            "Naval": len(filter_by_type(data, 'Naval')),
            "Conteo Total de Placas": len(data)
        }
        selected_institucion = st.selectbox("Seleccione la institución:", list(institucion_count.keys()))
        st.write(f"**Placas de {selected_institucion}:** {institucion_count[selected_institucion]}")

    elif page == "Mostrar Base de Datos":
        st.subheader("Base de Datos de Placas Registradas")
        if not data.empty:
            st.write(data)
        else:
            st.error("No hay datos disponibles.")

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

# Función de inicio de sesión
def login_page():
    st.markdown(
        """
        <style>
        .header {
            display: flex;
            align-items: center;
        }
        .header img {
            margin-right: 20px;
        }
        </style>
        <div class="header">
            <img src="https://raw.githubusercontent.com/Nestor20193767/Ejercito/main/PLA___2_-removebg-preview%20(1).png" width="80">
            <h1 style="margin: 0;">Iniciar Sesión</h1>
        </div>
        """, unsafe_allow_html=True
    )

    with st.form("login_form"):
        username = st.text_input("Usuario")
        password = st.text_input("Contraseña", type="password")
        submitted = st.form_submit_button("Iniciar Sesión")

        if submitted:
            if password == PASSWORD:
                st.session_state.authenticated = True
            else:
                st.error("Contraseña incorrecta")

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if st.session_state.authenticated:
    main_page()
else:
    login_page()

