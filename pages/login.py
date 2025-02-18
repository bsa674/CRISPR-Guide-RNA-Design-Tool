'''
Author : Pablo Alarcón

File description :
This file contains the Streamlit login.py page to enable the users login with their credentials stored in the Firestore database with the signup.py file. 
The email should be verified using the OTP code sended by SendGrid to the user.
Users must configure their own Firestore and SendGrid API keys, which should be securely stored in an environment variables file (.env)

Date of modified : 18th February, 2025
'''
#Load required libraries and modules
import streamlit as st
from streamlit import session_state as ss
from PIL import Image
import os

img_path = Image.open(os.path.join(os.path.dirname(__file__), '..', 'images', 'circular_logo.png'))

if 'page_state' not in ss.keys():
    ss.page_state = 'login'

if ss.page_state == 'login':
    st.set_page_config(page_title="Castor: A CRISPR Guide RNA Design Tool",
            layout="wide",
            page_icon=img_path, initial_sidebar_state="collapsed")

from traceback import print_exc
import streamlit_authenticator as stauth
from pages.auth import get_auth_credentials
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from dotenv import load_dotenv
from pages.functions import footer,set_background,button_style
from pages.signup import generate_otp,send_otp_email

#Background
set_background("images/castor_bg4.jpg")

#Firestore database key/credentials
private_key = os.getenv('FIREBASE_PRIVATE_KEY')
if private_key is None:
    raise ValueError("FIREBASE_PRIVATE_KEY is missing from the environment variables")

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

database = firestore.client()
collection_fb = database.collection("CASTOR")
users = collection_fb.stream()

#Function to verify the user email account with the OTP sended by email using SendGrid
def update_credentails():
    otp = generate_otp()
    sendgrid_api_key = os.getenv("SENDGRID_API_KEY")  #Load API Key
    if sendgrid_api_key:
        credentials = collection_fb.document(ss.name).get().to_dict()
        send_otp_email(credentials['email'], otp, sendgrid_api_key)
    collection_fb.document(ss.name).update({"email_verification_code": otp})
    credentials = collection_fb.document(ss.name).get().to_dict()
    ss.page_state = 'verify_email'
    st.switch_page("./pages/verify_email.py")

#Get authenticator credentials from Firestore database
auth_credentials = get_auth_credentials()

#Initialize the authenticator object to manage user authentication and session state using cookies
authenticator = stauth.Authenticate(
    auth_credentials,
    cookie_name="castor",
    cookie_key="py_castor987654321",
    cookie_expiry_days=5,
    preauthorized={}
)

if 'logout' in ss.keys():
    ss.logout = True

#Page style
with st.container():
    left_space, login_space, right_space = st.columns(3)
    with login_space:
        st.markdown("<h1 style='text-align: center; color: white;'>Welcome to Castor</h1>", unsafe_allow_html=True)
    with login_space:
        login_column1, login_column2, login_column3 = st.columns(3)
        with login_column2:
            st.image(img_path, width=150, use_container_width=True)
        with login_column2:
            if st.button("Home", icon=":material/home:", use_container_width=True):
                ss.page_state = 'main'
                st.switch_page("./main.py")
            button_style()
            
#Login page using streamlit authenticator
    with login_space:
        try:
            authenticator.login(key='Login', location='main', captcha=True,fields={'Captcha': 'Type the code from the image'})
        except stauth.LoginError as e:
            # Catch the LoginError exception and show custom message
            st.error("The captcha you entered is incorrect. Please try again.")

        authentication_status = st.session_state["authentication_status"]
        if authentication_status is None:  # If user has not attempted login
            pass

        elif authentication_status is False:  # Incorrect credentials
            st.error("Username/password is incorrect.")

        elif authentication_status:  # Successful login
            user = collection_fb.document(ss.name).get().to_dict()
            if not user['email_verified']:
                st.warning("Please verify your email address to continue.")
                update_credentails()
            else:
                ss.page_state = 'home'
                st.switch_page('pages/after_login.py')
        else:
            pass
            
#Additional widgets for the login page
    with login_space:
        col1, col2, col3 = st.columns([1.6,2,2])

        with col1:
            if st.button("Sign up", icon=":material/start:", use_container_width=True):
                ss.page_state = 'signup'
                st.switch_page("./pages/signup.py")

        with col2:
            if st.button("Get Password", icon=":material/key:", use_container_width=True):
                ss.page_state = 'forgot_password'
                st.switch_page("./pages/forgot_password.py")

        with col3:
            if st.button("Get Username", icon=":material/person:", use_container_width=True):
                ss.page_state = 'get_username'
                st.switch_page("./pages/get_username.py")

footer()
