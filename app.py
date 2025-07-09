import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import bcrypt
import json
import cloudinary
import cloudinary.uploader

# --- CSS para estilo Instagram ---
st.markdown(
    """
<style>
    .stApp {
        background: linear-gradient(135deg, #722F37, #8B0000, #A0522D);
        min-height: 100vh;
    }

    .stAppDeployButton, .stDecoration, .stRadio, .stSelectbox {
        display: none !important;
    }

    .main-container {
        max-width: 400px;
        margin: 0 auto;
        padding: 2rem;
        text-align: center;
    }

    .title {
        font-size: 2.5rem;
        font-weight: bold;
        color: #FFFFFF;
        margin-bottom: 3rem;
        font-family: 'Cursive', serif;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
    }

    .instagram-button, .login-button {
        padding: 12px 24px;
        border: none;
        border-radius: 25px;
        font-size: 16px;
        font-weight: 600;
        cursor: pointer;
        width: 100%;
        margin: 8px 0;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }

    .instagram-button {
        background: linear-gradient(45deg, #405DE6, #5851DB, #833AB4, #C13584, #E1306C, #FD1D1D);
        color: white;
    }

    .instagram-button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0,0,0,0.3);
    }

    .login-button {
        background: linear-gradient(45deg, #8B0000, #DC143C);
        color: white;
    }

    .login-button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0,0,0,0.3);
    }

    .form-container {
        background: rgba(255, 255, 255, 0.95);
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        margin-top: 2rem;
        backdrop-filter: blur(10px);
    }

    .stTextInput > div > div > input {
        border-radius: 10px;
        border: 2px solid #E1E1E1;
        padding: 12px;
        font-size: 16px;
        background: white;
        color: #333333;
    }

    .stTextInput > div > div > input:focus {
        border-color: #8B0000;
        box-shadow: 0 0 0 2px rgba(139, 0, 0, 0.2);
    }

    .wine-emoji {
        font-size: 3rem;
        margin-bottom: 1rem;
    }

    .stMarkdown p, .stMarkdown h1, .stMarkdown h2, .stMarkdown h3,
    .stApp h1, .stApp h2, .stApp h3 {
        color: #FFFFFF !important;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.5);
    }

    .stButton > button {
        background: linear-gradient(45deg, #FFFFFF, #F0F0F0);
        color: #8B0000;
        border: 2px solid #8B0000;
        border-radius: 25px;
        padding: 12px 24px;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }

    .stButton > button:hover {
        background: linear-gradient(45deg, #8B0000, #DC143C);
        color: white;
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0,0,0,0.3);
    }

    .stTextInput > label, .stNumberInput > label, .stFileUploader > label {
        color: #FFFFFF !important;
        font-weight: 600;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.7);
    }

    .stSuccess, .stError, .stWarning, .stInfo {
        border-radius: 10px;
        color: white;
    }

    .stSuccess { background: rgba(40, 167, 69, 0.9); }
    .stError { background: rgba(220, 53, 69, 0.9); }
    .stWarning { background: rgba(255, 193, 7, 0.9); color: #333333; }
    .stInfo { background: rgba(23, 162, 184, 0.9); }

    .stForm {
        background: rgba(255, 255, 255, 0.1);
        padding: 2rem;
        border-radius: 15px;
        backdrop-filter: blur(10px);
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
    }

    .stFileUploader {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 10px;
        padding: 1rem;
    }

    .nav-menu {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border-radius: 15px;
        padding: 1rem;
        margin-bottom: 2rem;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
    }

    .nav-buttons {
        display: flex;
        gap: 1rem;
        justify-content: center;
        flex-wrap: wrap;
    }

    .nav-button {
        background: rgba(255, 255, 255, 0.9);
        color: #8B0000;
        border: 2px solid rgba(139, 0, 0, 0.3);
        border-radius: 20px;
        padding: 8px 16px;
        font-weight: 600;
        transition: all 0.3s ease;
        cursor: pointer;
        font-size: 14px;
    }

    .nav-button:hover, .nav-button.active {
        background: #8B0000;
        color: white;
        transform: translateY(-2px);
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
    }

    .card {
        position: relative;
        overflow: hidden;
        border-radius: 15px;
        margin-bottom: 2rem;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
    }

    .card img {
        border-radius: 15px;
        width: 100%;
        height: auto;
        object-fit: contain;
    }

    .card-overlay {
        position: absolute;
        bottom: 0;
        width: 100%;
        background: rgba(0, 0, 0, 0.6);
        color: white;
        padding: 1rem;
        border-radius: 0 0 15px 15px;
    }

    .card-overlay h3, .card-overlay p {
        color: white !important;
        margin: 0.5rem 0;
    }
</style>

""",
    unsafe_allow_html=True,
)

# --- Configuración Google Sheets ---
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

# --- Config Cloudinary ---
cloudinary.config(
    cloud_name=st.secrets["cloudinary"]["cloud_name"],
    api_key=st.secrets["cloudinary"]["api_key"],
    api_secret=st.secrets["cloudinary"]["api_secret"],
    secure=True,
)


# --- Funciones de usuarios ---
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


# --- Estado de sesión ---
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
if "user" not in st.session_state:
    st.session_state["user"] = ""
if "show_form" not in st.session_state:
    st.session_state["show_form"] = None
if "current_page" not in st.session_state:
    st.session_state["current_page"] = "subir_lugar"

# --- App ---
if not st.session_state["logged_in"]:
    # Pantalla de inicio con botones estilo Instagram
    st.markdown('<div class="main-container">', unsafe_allow_html=True)

    # Emoji de vino
    st.markdown('<div class="wine-emoji">🍷</div>', unsafe_allow_html=True)

    # Título
    st.markdown('<h1 class="title">Tintos Lovers</h1>', unsafe_allow_html=True)

    # Botones
    col1, col2 = st.columns(2)

    with col1:
        if st.button("Registrarse", key="reg_btn"):
            st.session_state["show_form"] = "registro"

    with col2:
        if st.button("Iniciar Sesión", key="login_btn"):
            st.session_state["show_form"] = "login"

    # Mostrar formulario según el botón presionado
    if st.session_state["show_form"] == "registro":
        st.markdown('<div class="form-container">', unsafe_allow_html=True)
        st.markdown("### 📝 Crear cuenta nueva")

        new_user = st.text_input("Nombre de usuario", key="reg_user")
        new_password = st.text_input("Contraseña", type="password", key="reg_pass")

        col1, col2 = st.columns(2)
        with col1:
            if st.button("Crear Usuario", key="create_user"):
                if new_user and new_password:
                    creado = crear_usuario(new_user, new_password)
                    if creado:
                        st.info("Ahora puedes iniciar sesión.")
                        st.session_state["show_form"] = "login"
                else:
                    st.error("Por favor, rellena ambos campos.")

        with col2:
            if st.button("Volver", key="back_reg"):
                st.session_state["show_form"] = None

        st.markdown("</div>", unsafe_allow_html=True)

    elif st.session_state["show_form"] == "login":
        st.markdown('<div class="form-container">', unsafe_allow_html=True)
        st.markdown("### 🔐 Iniciar sesión")

        username = st.text_input("Usuario", key="login_user")
        password = st.text_input("Contraseña", type="password", key="login_pass")

        col1, col2 = st.columns(2)
        with col1:
            if st.button("Entrar", key="enter_btn"):
                if verificar_usuario(username, password):
                    st.success(f"¡Bienvenido, {username}!")
                    st.session_state["logged_in"] = True
                    st.session_state["user"] = username
                    st.session_state["show_form"] = None
                else:
                    st.error("Usuario o contraseña incorrectos.")

        with col2:
            if st.button("Volver", key="back_login"):
                st.session_state["show_form"] = None

        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

else:
    # Menú de navegación
    st.markdown('<div class="nav-menu">', unsafe_allow_html=True)
    st.markdown(
        f'<h3 style="color: white; text-align: center; margin-bottom: 1rem;">¡Hola, {st.session_state["user"]}! 🍷</h3>',
        unsafe_allow_html=True,
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("📍 Subir Lugar", key="nav_subir"):
            st.session_state["current_page"] = "subir_lugar"

    with col2:
        if st.button("🗺️ Ver Lugares", key="nav_lugares"):
            st.session_state["current_page"] = "ver_lugares"

    with col3:
        if st.button("🚪 Cerrar Sesión", key="nav_logout"):
            st.session_state["logged_in"] = False
            st.session_state["user"] = ""
            st.session_state["show_form"] = None
            st.session_state["current_page"] = "subir_lugar"
            st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

    # Contenido según la página seleccionada
    if st.session_state["current_page"] == "subir_lugar":
        # Formulario para subir lugar
        st.header("¿Dónde te has tomado el último tinto? 🍷")
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

    elif st.session_state["current_page"] == "ver_lugares":
        # Mostrar lugares guardados
        st.header("Lugares subidos 🗺️")

        # Botón para ir a subir lugar
        if st.button("➕ Agregar Nuevo Lugar", key="add_new_place"):
            st.session_state["current_page"] = "subir_lugar"

        lugares = sheet_lugares.get_all_records()

        if not lugares:
            st.info(
                "No hay lugares subidos aún. ¡Sé el primero en compartir tu lugar favorito!"
            )
        else:
            for lugar in lugares:
                st.markdown(
                    f"""
                    <div class="card">
                        <img src="{lugar['url_imagen']}" alt="{lugar['nombre']}">
                        <div class="card-overlay">
                            <h3>{lugar['nombre']}</h3>
                            <p>🍹 Precio: €{lugar['precio']}</p>
                            <p>📍 Ubicación: {lugar['ubicacion']}</p>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
