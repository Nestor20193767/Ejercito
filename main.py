import streamlit as st
import pandas as pd
import os
from io import BytesIO
from datetime import datetime
from streamlit_option_menu import option_menu

# Inicializar variables
if 'username' not in st.session_state:
    st.session_state['username'] = None  # Inicializar con None
    
usuarios_list = st.secrets['usuarios']
PASSWORD = st.secrets['password']
icono_url = "https://raw.githubusercontent.com/Nestor20193767/Ejercito/main/ico_SIREVE-removebg-preview%20(1).png"
logo_url = "https://raw.githubusercontent.com/Nestor20193767/Ejercito/main/PLA___2_-removebg-preview%20(1).png"
st.set_page_config(page_icon=icono_url, page_title='SIREVE', layout="wide")

# Popup window de aviso para descargar cada cierto dia al mes
@st.dialog("Recordatorio")
def recordatorio_descargas():
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
            <img src="https://raw.githubusercontent.com/Nestor20193767/Ejercito/main/PLA___2_-removebg-preview%20(1).png" width="60">
            <h1 style="margin: 0;">SIREVE</h1>
        </div>
        """, unsafe_allow_html=True
    )
        st.write(f"¡Se recomienda descargar la base de datos!")
        #reason = st.text_input("Because...")

        if st.button("Descargar"):
            st.session_state.recordatorio_descargas = 'hola'
            st.rerun()
            
def recordar_descargar_baseDeDatos(dia_exacto):
    hoy = datetime.now()
    dia = hoy.day
    if dia == dia_exacto:
        if "recordatorio_descargas" not in st.session_state:
            recordatorio_descargas()
    
        else:
            st.write('Descargado!')  

        
        
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
        username = st.selectbox("Select option", options=usuarios_list)
        password = st.text_input("Contraseña", type="password")
        submitted = st.form_submit_button("Iniciar Sesión")
        
    if submitted:
        if password == PASSWORD:
            st.session_state['logged_in'] = True
            st.session_state.authenticated = True  # Cambiamos el estado de autenticación
            st.session_state['username'] = username  # Guardar el nombre de usuario en session_state
            st.warning( f"Usted se está Identificando como: {st.session_state['username']}, por lo que será "  
 "monitoreado y almacenado en cualquier cambio realizado. "  
 "Presione Iniciar Sesión una segunda vez si está de acuerdo."  
)  # Mostrar mensaje de bienvenida
            usuario = st.session_state['username']
        else:
            st.error("Contraseña incorrecta.")

# Función para mostrar la página principal
def main_page():
    recordar_descargar_baseDeDatos(25)
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

    # Función para mostrar el menú de edición con los datos ya llenados
    def edit_menu(data, result):
        st.subheader("Edición de Datos")
        
        # Prellenar los campos con los valores actuales
        institucion = st.selectbox("Institución:", ["Policía", "Ejército", "Fuerza Aérea", "Naval"], index=["Policía", "Ejército", "Fuerza Aérea", "Naval"].index(result['Institucion'].values[0]))
        placa = st.text_input("Placa del Vehículo:", result['Placa'].values[0])
        conductor = st.text_input("Conductor Designado:", result['Conductor Designado'].values[0])
        estado = st.selectbox("Estado:", ["Pendiente", "Archivado"], index=["Pendiente", "Archivado"].index(result['Estado'].values[0]))
        preliminar = st.text_input("Preliminar:", result['Preliminar'].values[0])
        expediente = st.text_input("Expediente:", result['Expediente'].values[0])
        tipo_accidente = st.text_area("Tipo de Accidente:", result['Tipo de accidente'].values[0])
        persona_a_cargo = st.text_input("Persona a Cargo:", result['Persona a Cargo'].values[0])
        fecha = st.date_input("Fecha:", datetime.strptime(result['Fecha'].values[0], '%d/%m/%y'))
    
        # Botones
        if st.button("Guardar Cambios"):
            edit_data(data, result['Placa'].values[0], placa, conductor, institucion, estado, preliminar, expediente, tipo_accidente, persona_a_cargo, fecha)
            st.success("Cambios guardados exitosamente.")
        if st.button("Atrás"):
            st.warning("No se han realizado cambios.")

    # Función para actualizar los datos en la base de datos
    def edit_data(data, original_placa, placa, conductor, institucion, estado, preliminar, expediente, tipo_accidente, persona_a_cargo, fecha):
        
        # Buscar el registro de la placa original y modificarlo
        index = data[data['Placa'] == original_placa].index
        if not index.empty:
            data.at[index, 'Placa'] = placa
            data.at[index, 'Conductor Designado'] = conductor
            data.at[index, 'Institucion'] = institucion
            data.at[index, 'Estado'] = estado
            data.at[index, 'Preliminar'] = preliminar
            data.at[index, 'Expediente'] = expediente
            data.at[index, 'Tipo de accidente'] = tipo_accidente
            data.at[index, 'Persona a Cargo'] = persona_a_cargo
            data.at[index, 'Fecha'] = fecha.strftime('%d/%m/%y')
            
            # Guardar cambios en la base de datos
            save_data(data)
        
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
            icons=["card-text", "search","database", "book"],
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
            persona_a_cargo = f"{st.session_state['username']}"
        except Exception as e:
            st.warning("Debes recargar la pagina para agregar el usuario")
        fecha = st.date_input("Fecha", datetime.today(), format="DD/MM/YYYY")

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
                    'Fecha': [fecha.strftime('%d/%m/%y')]
                })
                if data is None:
                    data = new_data
                else:
                    data = pd.concat([data, new_data], ignore_index=True)
                save_data(data)
                st.success(f"Placa {placa} registrada con éxito.")
            else:
                st.error("Debe completar todos los campos para registrar una nueva placa.")

    # Cambios a la placa
    # Actualización en la página "Buscar Placa"
    elif page == "Buscar Placa":
        # Inicializar el estado si es necesario
        if 'edit_menu' not in st.session_state:
            st.session_state['edit_menu'] = False  # Modo de edición está apagado por defecto
            
        st.subheader("Buscar Placa Registrada")
        search_placa = st.text_input("Buscar por Placa:")
        if st.button("Buscar"):
            if data is not None:
                result = data[data['Placa'] == search_placa]
                if not result.empty:
                    st.write(result)
                    Edicion = st.button("Edición de Datos")
                        
                    # Mostrar botón de edición si la placa es encontrada
                    if Edicion:
                        st.session_state['edit_menu'] = True  # Cambiar al modo de edición
                        st.write('Se presionó el botón Edición de Datos')
                        
                        if st.session_state['edit_menu']:
                            edit_menu(data, result)  # Llamar al menú de edición con los datos cargados
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
                fechas_seleccionadas = st.date_input("Fecha", value=datetime.today(), max_value=datetime.today(), format="DD/MM/YYYY")
            
                # Filtro por Conductor
                conductor_seleccionado = st.text_input("Buscar por Conductor:")
            
                # Filtro por Instituciones
                instituciones_unicas = data['Institucion'].unique().tolist()
                instituciones_seleccionadas = st.multiselect("Seleccione las Instituciones:", instituciones_unicas)
            
                # Filtro por Persona a Cargo
                persona_cargo_seleccionada = st.text_input("Buscar por Persona a Cargo:")
                bFiltros = st.button("Aplicar Filtros")
                
                if not data.empty: 
                    st.write(data)
                else:
                    st.warning('Aun no hay base de datos cargada')
                
                if bFiltros:
                    data_filtrada = data.copy()
                    
                    # Filtros
                    if estado_seleccionado != "Todos":
                        st.write('Primer Filtro')
                        data_filtrada = data_filtrada[data_filtrada['Estado'] == estado_seleccionado]
                    
                    if fechas_seleccionadas:
                        st.write('Segundo Filtro')
                        data_filtrada = data_filtrada[data_filtrada['Fecha'] == fechas_seleccionadas.strftime('%d/%m/%y')]
                    
                    if conductor_seleccionado:
                        st.write('Tercer Filtro')
                        data_filtrada = data_filtrada[data_filtrada['Conductor Designado'].str.contains(conductor_seleccionado, case=False)]
                    
                    '''if instituciones_seleccionadas:
                        st.write('Cuarto Filtro')
                        data_filtrada = data_filtrada[data_filtrada['Institucion'].isin(instituciones_seleccionadas)]
                    
                    if persona_cargo_seleccionada:
                        st.write('QUinto Filtro')
                        data_filtrada = data_filtrada[data_filtrada['Persona a Cargo'].str.contains(persona_cargo_seleccionada, case=False)]'''
                    
                    # Mostrar los resultados filtrados
                    if not data_filtrada.empty:
                        st.write('Si deben haber datos')
                        st.write(data_filtrada)
                    else:
                        st.write(data_filtrada)
                        st.warning('No se encontraron resultados con los filtros seleccionados.')

                
        except Exception as e:
                        st.error(f"Aún no hay base de datos ")


    elif page == "Manual de Usuario":
        st.subheader("Manual de Usuario")
        st.write("Aquí irá el manual de usuario ")
        

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


