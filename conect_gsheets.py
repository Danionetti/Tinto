import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Definimos el alcance (scopes) que necesitamos
scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive",
]

# Cargamos las credenciales desde el archivo JSON
creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)

# Autenticamos y abrimos la hoja de cálculo
client = gspread.authorize(creds)

# Abrimos la hoja por su nombre
sheet = client.open("Tintos-lovers").worksheet("usuarios")

# Leemos todos los datos
datos = sheet.get_all_records()

print("Datos en la hoja usuarios:")
print(datos)
