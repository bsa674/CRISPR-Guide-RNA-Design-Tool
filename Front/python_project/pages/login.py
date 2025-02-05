#Login page
import streamlit as st
from PIL import Image
import os
import streamlit_authenticator as stauth
from pages.auth import get_auth_credentials
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from dotenv import load_dotenv

# Use relative path to load the image
img_path = Image.open(os.path.join(os.path.dirname(__file__), '..', 'images', 'circular_logo.png'))

private_key = os.getenv('FIREBASE_PRIVATE_KEY')
if private_key is None:
    raise ValueError("FIREBASE_PRIVATE_KEY is missing from the environment variables")

if __name__ == "__main__":
    st.set_page_config(page_title="Castor: A CRISPR Guide RNA Design Tool",
                   layout="wide",
                   page_icon=img_path, initial_sidebar_state="auto")
#Paths
load_dotenv()
firebase_credential = {
    "type": "service_account",
    "project_id": os.getenv('FIREBASE_PROJECT_ID'),
    "private_key_id": os.getenv('FIREBASE_PRIVATE_KEY_ID'),
    "private_key": os.getenv('FIREBASE_PRIVATE_KEY').replace("\\n", "\n"),  # handle multiline keys
    "client_email": os.getenv('FIREBASE_CLIENT_EMAIL'),
    "client_id": os.getenv('FIREBASE_CLIENT_ID'),
    "auth_uri": os.getenv('FIREBASE_AUTH_URI'),
    "token_uri": os.getenv('FIREBASE_TOKEN_URI'),
    "auth_provider_x509_cert_url": os.getenv('FIREBASE_CERT_URL'),
    "client_x509_cert_url": os.getenv('FIREBASE_CLIENT_CERT_URL')
}


if not firebase_admin._apps:
    cred = credentials.Certificate(firebase_credential)
    firebase_admin.initialize_app(cred)

#Firebase data base
database = firestore.client()
collection_fb = database.collection("CASTOR")

#Fetch user
auth_credentials = get_auth_credentials()

if "authentication_status" in st.session_state:
    del st.session_state["authentication_status"]
if "username" in st.session_state:
    del st.session_state["username"]

authenticator = stauth.Authenticate(
    auth_credentials,
    cookie_name="castor",
    cookie_key="py_castor987654321",
    cookie_expiry_days=5,
    preauthorized={}
)
with st.container():
    left_space, login_space, right_space = st.columns(3)
    with login_space:
        st.markdown("<h1 style='text-align: center; color: black;'>Welcome to Castor</h1>", unsafe_allow_html=True)
    with login_space:
        login_column1, login_column2, login_column3 = st.columns(3)
        with login_column2:
            st.image(img_path, width=150, use_container_width=True)
        with login_column2:
            if st.button("Home", icon=":material/home:", use_container_width=True):
                st.switch_page("./main.py")
    with login_space:
        try:
            authenticator.login(key='Login', location='main', captcha=True,
                                fields={'Captcha': 'Type the code from the image'})

            # Ensure authentication_status exists before checking it
            authentication_status = st.session_state.get("authentication_status")
            username = st.session_state.get("username", "")
            name = st.session_state.get("name", "")

            if authentication_status is None:  # If user has not attempted login
                st.warning("Please enter your username and password.")

            elif authentication_status is False:  # Incorrect credentials
                st.error("Username/password is incorrect.")

            elif authentication_status:  # Successful login
                st.success(f"Welcome {name}! You have successfully logged in.")
                st.switch_page("pages/results.py")  # Redirect to results page
        except stauth.LoginError as e:
            # Catch the LoginError exception and show custom message
            st.error("The captcha you entered is incorrect. Please try again.")
    with login_space:
        account_sp1, account_sp2 = st.columns([0.6, 0.4])
        with account_sp1:
            st.text("Don't have an account?")
        with account_sp2:
            if st.button("Sign up", icon=":material/start:", use_container_width=True):
                st.switch_page("./pages/signup.py")
    with login_space:
        password_sp1, password_sp2 = st.columns([0.6, 0.4])
        with password_sp1:
            st.text("Forgot your password?")
        with password_sp2:
            if st.button("Reset your password", icon=":material/key:", use_container_width=True):
                st.switch_page("./pages/forgot_password.py")

    with login_space:
        user_sp1, user_sp2 = st.columns([0.6, 0.4])
        with user_sp1:
            st.text("Forgot your username?")
        with user_sp2:
            if st.button("Get your username", icon=":material/person:", use_container_width=True):
                st.switch_page("./pages/get_username.py")




