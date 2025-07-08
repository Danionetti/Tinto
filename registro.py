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
