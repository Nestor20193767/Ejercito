import streamlit as st
import pandas as pd
import os
from io import BytesIO
from datetime import datetime
from streamlit_option_menu import option_menu
username = ''
PASSWORD = st.secrets['password']
icono_url = "https://raw.githubusercontent.com/Nestor20193767/Ejercito/main/ico_SIREVE-removebg-preview%20(1).png"
logo_url = "https://raw.githubusercontent.com/Nestor20193767/Ejercito/main/PLA___2_-removebg-preview%20(1).png"
st.set_page_config(page_icon=icono_url, page_title='SIREVE', layout="wide")

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
            <h1 style="margin: 0;">SIREVE</h1>
        </div>
        """, unsafe_allow_html=True
    )

    st.subheader("Iniciar Sesión")

    #password_input = st.text_input("Ingrese la contraseña:", type="password")
    # Crear un formulario para el inicio de sesión
    with st.form("login_form"):
        username = st.text_input("Usuario")
        password = st.text_input("Contraseña", type="password")
        submitted = st.form_submit_button("Iniciar Sesión")
        
    if submitted:
        if password == PASSWORD:
            st.session_state['logged_in'] = True
            st.session_state.authenticated = True  # Cambiamos el estado de autenticación
        else:
            st.error("Contraseña incorrecta.")

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

    # Cargar los datos de la base de datos
    def load_data():
        if os.path.exists(DATABASE_FILE) and os.path.getsize(DATABASE_FILE) > 0:
            return pd.read_csv(DATABASE_FILE, sep='|')
        else:
            # Si no existe el archivo o está vacío, devolver None
            return None

    # Guardar los datos de la base de datos
    def save_data(data):
        data.to_csv(DATABASE_FILE, sep='|', index=False)

    # Filtrar los datos por institución
    def filter_by_type(data, institucion):
        return data[data['Institucion'] == institucion]

    # Función para descargar los datos en formato Excel
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
        #persona_a_cargo = st.text_input("Persona a Cargo:")
        try:
            persona_a_cargo = username
        except Exception as e:
            st.warning("Debes recargar la pagina para agregar el usuario")
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
                if data is None:
                    data = new_data
                else:
                    data = pd.concat([data, new_data], ignore_index=True)
                save_data(data)
                st.success(f"Placa {placa} registrada con éxito.")
            else:
                st.error("Debe completar todos los campos para registrar una nueva placa.")

    elif page == "Buscar Placa":
        st.subheader("Buscar Placa Registrada")
        search_placa = st.text_input("Buscar por Placa:")
        if st.button("Buscar"):
            if data is not None:
                result = data[data['Placa'] == search_placa]
                if not result.empty:
                    st.write(result)
                else:
                    st.error("Placa no encontrada.")
            else:
                st.error("Aún no hay una base de datos.")

    elif page == "Base de Datos":
        try:
            st.subheader("Base de Datos de Placas Registradas - Filtros")
        
            if data is None:
                st.error("Aún no hay una base de datos.")
            else:
                # Mostrar cantidad total de placas en la parte superior con tamaño de letra aumentado
                st.write(f"<h2 style='font-size: 24px;'>Cantidad de Placas Totales: {len(data)}</h2>", unsafe_allow_html=True)
                
                # Filtro por Estado
                estado_seleccionado = st.selectbox("Seleccione el Estado:", ["Todos", "Pendiente", "Archivado"])
            
                # Filtro por Fecha
                fechas_seleccionadas = st.date_input("Fecha", value=datetime.today(), max_value=datetime.today())
            
                # Filtro por Conductor
                conductor_seleccionado = st.text_input("Buscar por Conductor:")
            
                # Filtro por Instituciones
                instituciones_unicas = data['Institucion'].unique().tolist()
                instituciones_seleccionadas = st.multiselect("Seleccione las Instituciones:", instituciones_unicas)
            
                # Filtro por Persona a Cargo
                persona_cargo_seleccionada = st.text_input("Buscar por Persona a Cargo:")
            
                # Mostrar la base de datos completa o filtrada
                if st.button("Aplicar Filtros"):
                    data_filtrada = data.copy()  # Hacer una copia de los datos originales
                
                    # Aplicar filtro por Estado
                    if estado_seleccionado != "Todos":
                        data_filtrada = data_filtrada[data_filtrada['Estado'] == estado_seleccionado]
            
                    # Aplicar filtro por Fecha
                    if fechas_seleccionadas:
                        data_filtrada = data_filtrada[data_filtrada['Fecha'] == pd.to_datetime(fechas_seleccionadas)]
    
                    # Aplicar filtro por Conductor
                    if conductor_seleccionado:
                        data_filtrada = data_filtrada[data_filtrada['Conductor Designado'].str.contains(conductor_seleccionado, case=False)]
            
                    # Aplicar filtro por Instituciones
                    if instituciones_seleccionadas:
                        data_filtrada = data_filtrada[data_filtrada['Institucion'].isin(instituciones_seleccionadas)]
            
                    # Aplicar filtro por Persona a Cargo
                    if persona_cargo_seleccionada:
                        data_filtrada = data_filtrada[data_filtrada['Persona a Cargo'].str.contains(persona_cargo_seleccionada, case=False)]
                        
                    # Mostrar cantidad de placas con los filtros aplicados
                    st.write(f"### Cantidad de Placas Filtradas: {len(data_filtrada)}")
                    
                    # Mostrar los resultados filtrados
                    if not data_filtrada.empty:
                        st.write(data_filtrada)
                    else:
                        #st.error("No se encontraron registros con los filtros aplicados.")
                        st.write(data)
        except Exception as e:
            st.error(f"Ocurrió un error: {e}")


    elif page == "Manual de Usuario":
        st.subheader("Manual de Usuario")
        st.write("Aquí irá el manual de usuario")

    st.sidebar.subheader("Descargar Registros")
    download_option = st.sidebar.selectbox("Seleccione qué registros desea descargar:", ["Registro completo", "Policía", "Ejército", "Fuerza Aérea", "Naval"])
    
    if st.sidebar.button("Descargar"):
        if data is not None:
            if download_option == "Registro completo":
                download_excel(data, download_option)
                st.success("Archivo de registro completo descargado.")
            else:
                filtered_data = filter_by_type(data, download_option)
                download_excel(filtered_data, download_option)
                st.success(f"Archivo de registros de {download_option} descargado.")
        else:
            st.error("Aún no hay una base de datos.")



# Verificar si el usuario ya inició sesión
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

if st.session_state['logged_in']:
    main_page()
else:
    login_page()

