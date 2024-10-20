import streamlit as st

# Configuración de la contraseña
PASSWORD = "tu_contraseña"  # Cambia esto a la contraseña deseada

# Función para mostrar la página principal
def main_page():
    st.title("Página Principal")
    st.write("¡Has iniciado sesión correctamente!")
    # Aquí puedes agregar más contenido para la página principal

# Función para mostrar el formulario de inicio de sesión
def login_page():
    st.title("Iniciar Sesión")

    # Crear un formulario para el inicio de sesión
    with st.form("login_form"):
        username = st.text_input("Usuario")
        password = st.text_input("Contraseña", type="password")
        submitted = st.form_submit_button("Iniciar Sesión")

        # Validar la contraseña
        if submitted:
            if password == PASSWORD:
                st.session_state["authenticated"] = True
                st.session_state()  # Reiniciar la app para mostrar la página principal
            else:
                st.error("Contraseña incorrecta")

# Comprobar si el usuario ya está autenticado
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

# Si está autenticado, mostrar la página principal
if st.session_state["authenticated"]:
    main_page()
else:
    # Si no está autenticado, mostrar la página de inicio de sesión
    login_page()

