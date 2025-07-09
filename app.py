import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import bcrypt
import json
import cloudinary
import cloudinary.uploader
from PIL import Image
import io

# Config Google Sheets
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
sheet_users = client.open("Tintos-lovers").worksheet("usuarios")
sheet_lugares = client.open("Tintos-lovers").worksheet("Bares")

# Config Cloudinary
cloudinary.config(
    cloud_name=st.secrets["cloudinary"]["cloud_name"],
    api_key=st.secrets["cloudinary"]["api_key"],
    api_secret=st.secrets["cloudinary"]["api_secret"],
    secure=True,
)


# Funciones de usuarios
def crear_usuario(username, password):
    usuarios = sheet_users.get_all_records()
    for usuario in usuarios:
        if usuario["username"] == username:
            st.warning(f"El usuario '{username}' ya existe.")
            return False
    password_hash = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode(
        "utf-8"
    )
    sheet_users.append_row([username, password_hash])
    st.success(f"Usuario '{username}' creado con éxito.")
    return True


def verificar_usuario(username, password):
    usuarios = sheet_users.get_all_records()
    for usuario in usuarios:
        if usuario["username"] == username:
            password_hash = usuario["password_hash"].encode("utf-8")
            if bcrypt.checkpw(password.encode("utf-8"), password_hash):
                return True
    return False


# Estado sesión
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
if "user" not in st.session_state:
    st.session_state["user"] = ""

# App
st.title("Tintos Lovers 🍷")

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
        st.rerun()

    # Formulario para subir lugar
    st.header("¿Dónde te has tomado el ultimo tinto?🍷")
    with st.form("form_lugar"):
        nombre = st.text_input("Descripción del lugar")
        precio = st.number_input("Precio (€)", min_value=0.0, step=0.1)
        ubicacion = st.text_input("Ubicación")
        foto = st.file_uploader("Sube una foto", type=["jpg", "jpeg", "png"])

        submitted = st.form_submit_button("Guardar lugar")

        if submitted:
            if not nombre or not ubicacion or not foto:
                st.error("Por favor, rellena todos los campos y sube una foto.")
            else:
                # Subir imagen a Cloudinary
                image_bytes = foto.read()
                resultado = cloudinary.uploader.upload(
                    image_bytes, folder="tintos_lovers"
                )
                url_imagen = resultado["secure_url"]

                # Guardar en Google Sheets: nombre, precio, ubicación, url_imagen
                sheet_lugares.append_row([nombre, precio, ubicacion, url_imagen])

                st.success(f"Lugar '{nombre}' guardado con éxito.")
                st.image(url_imagen, caption=nombre)

    # Mostrar lugares guardados
    st.header("Lugares subidos")
    lugares = sheet_lugares.get_all_records()
    for lugar in lugares:
        st.subheader(lugar["nombre"])
        st.write(f"Precio: €{lugar['precio']}")
        st.write(f"Ubicación: {lugar['ubicacion']}")
        st.image(lugar["url_imagen"])
