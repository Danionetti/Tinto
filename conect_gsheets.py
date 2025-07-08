import gspread
from oauth2client.service_account import ServiceAccountCredentials
import streamlit as st

# Definimos el alcance (scopes) que necesitamos
scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive",
]

# Cargamos las credenciales desde el archivo JSON
creds_dict = st.secrets["google"]
creds = ServiceAccountCredentials.from_json_keyfile_dict(dict(creds_dict), scope)


# Autenticamos y abrimos la hoja de cálculo
client = gspread.authorize(creds)

# Abrimos la hoja por su nombre
sheet = client.open("Tintos-lovers").worksheet("usuarios")

# Leemos todos los datos
datos = sheet.get_all_records()

print("Datos en la hoja usuarios:")
print(datos)
