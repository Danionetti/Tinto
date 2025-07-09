import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import bcrypt
import json

# Configurar acceso a Google Sheets
scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive",
]


def get_credentials():
    try:
        creds_dict = st.secrets["google"]
        creds = ServiceAccountCredentials.from_json_keyfile_dict(
            dict(creds_dict), scope
        )
    except Exception:
        with open("credentials.json") as f:
            creds_dict = json.load(f)
        creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
    return creds


creds = get_credentials()
client = gspread.authorize(creds)
sheet = client.open("Tintos-lovers").worksheet("usuarios")


def crear_usuario(username, password):
    usuarios = sheet.get_all_records()
    for usuario in usuarios:
        if usuario["username"] == username:
            st.warning(f"El usuario '{username}' ya existe.")
            return False
    password_hash = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode(
        "utf-8"
    )
    sheet.append_row([username, password_hash])
    st.success(f"Usuario '{username}' creado con éxito.")
    return True


def verificar_usuario(username, password):
    usuarios = sheet.get_all_records()
    for usuario in usuarios:
        if usuario["username"] == username:
            password_hash = usuario["password_hash"].encode("utf-8")
            if bcrypt.checkpw(password.encode("utf-8"), password_hash):
                return True
    return False


# Inicializar variables de sesión
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
if "user" not in st.session_state:
    st.session_state["user"] = ""

st.title("Tintos Lovers 🍷")

# Registrarse o loguearse
mode = st.radio("Selecciona una opción", ("Login", "Registro"))

if not st.session_state["logged_in"]:
    if mode == "Registro":
        st.header("Registro de nuevo usuario")
        new_user = st.text_input("Nombre de usuario", key="reg_user")
        new_password = st.text_input("Contraseña", type="password", key="reg_pass")
        if st.button("Crear usuario"):
            if new_user and new_password:
                creado = crear_usuario(new_user, new_password)
                if creado:
                    st.info("Ahora puedes iniciar sesión.")
            else:
                st.error("Por favor, rellena ambos campos.")
    else:
        st.header("Iniciar sesión")
        username = st.text_input("Usuario", key="login_user")
        password = st.text_input("Contraseña", type="password", key="login_pass")
        if st.button("Entrar"):
            if verificar_usuario(username, password):
                st.success(f"Bienvenido, {username}!")
                st.session_state["logged_in"] = True
                st.session_state["user"] = username
            else:
                st.error("Usuario o contraseña incorrectos.")
else:
    st.write(f"¡Hola, {st.session_state['user']}! Ya estás logueado.")
    if st.button("Cerrar sesión"):
        st.session_state["logged_in"] = False
        st.session_state["user"] = ""
        st.experimental_rerun()

    # App
    st.write("Este es el contenido exclusivo para usuarios logueados.")
