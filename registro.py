import gspread
from oauth2client.service_account import ServiceAccountCredentials
import bcrypt
import streamlit as st
import json

# Configurar acceso a Google Sheets
scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive",
]


def get_credentials():
    try:
        # Intentamos cargar secretos de Streamlit (en deploy)
        creds_dict = st.secrets["google"]
        creds = ServiceAccountCredentials.from_json_keyfile_dict(
            dict(creds_dict), scope
        )
    except Exception:
        # Si falla (p.ej. ejecución local sin Streamlit) cargamos json local
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
            print(f"El usuario '{username}' ya existe.")
            return
    password_hash = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode(
        "utf-8"
    )
    sheet.append_row([username, password_hash])
    print(f"Usuario '{username}' creado con éxito.")


if __name__ == "__main__":
    username = input("Usuario: ")
    password = input("Contraseña: ")
    crear_usuario(username, password)
