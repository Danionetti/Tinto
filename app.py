import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import bcrypt

# Configurar acceso a Google Sheets
scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive",
]
creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
client = gspread.authorize(creds)
sheet = client.open("Tintos-lovers").worksheet("usuarios")


def verificar_usuario(username, password):
    usuarios = sheet.get_all_records()
    for usuario in usuarios:
        if usuario["username"] == username:
            # Comprobar contraseña usando bcrypt
            password_hash = usuario["password_hash"].encode("utf-8")
            if bcrypt.checkpw(password.encode("utf-8"), password_hash):
                return True
    return False


def login():
    st.title("Login Tintos Lovers 🍷")

    username = st.text_input("Usuario")
    password = st.text_input("Contraseña", type="password")

    if st.button("Entrar"):
        if verificar_usuario(username, password):
            st.success(f"Bienvenido, {username}!")
            st.session_state["logged_in"] = True
            st.session_state["user"] = username
        else:
            st.error("Usuario o contraseña incorrectos.")


if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if not st.session_state["logged_in"]:
    login()
else:
    st.write(f"¡Hola, {st.session_state['user']}! Ya estás logueado.")
    # Aquí iría el resto de tu app
