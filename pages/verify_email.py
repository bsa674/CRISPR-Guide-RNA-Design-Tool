'''
Author : Pablo Alarcón

File description :
This file contains the Streamlit verify_email.py page to enable the users verify their email after the signup. 
When a new user is created, the email should be verified using the OTP code sended by SendGrid to the user.
Users must configure their own Firestore and SendGrid API keys, which should be securely stored in an environment variables file (.env)

Date of modified : 18th February, 2025
'''
#Load required libraries and modules
import streamlit as st
from streamlit import session_state as ss
import os
from PIL import Image

img_path = Image.open(os.path.join(os.path.dirname(__file__), '..', 'images', 'circular_logo.png'))
if ss.page_state == 'verify_email':
    st.set_page_config(page_title="Castor: A CRISPR Guide RNA Design Tool",
                   layout="wide",
                   page_icon=img_path, initial_sidebar_state="auto")

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from dotenv import load_dotenv
from pages.functions import set_background, button_style

#Load Firestore database and SendGrid keys/credentials
load_dotenv()
private_key = os.getenv('FIREBASE_PRIVATE_KEY')
if private_key is None:
    raise ValueError("FIREBASE_PRIVATE_KEY is missing from the environment variables")
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

#Function to verify the email with an OTP code and Update the Firestore database
def verify_email():
    st.info('Please find the OTP in your mailbox by castorguiderna@hotmail.com and enter it below.')
    username = st.text_input("Username", placeholder="Enter your username")
    otp_input = st.text_input("Enter OTP", placeholder="Enter the 6-digit code", max_chars=6)
    button_style()
    if st.button("Verify"):
        user_doc = collection_fb.document(username).get()

        if user_doc.exists:
            user_data = user_doc.to_dict()
            stored_otp = user_data.get("email_verification_code")

            if stored_otp and stored_otp == otp_input:
                collection_fb.document(username).update({"email_verified": True})
                st.switch_page("./pages/login.py")
                st.success("Email verified successfully! You can now log in.")
            else:
                st.error("Invalid OTP. Please try again.")
        else:
            st.error("User not found.")
#Page style
set_background("images/castor_bg4.jpg")
with st.container():
    left_verify_space, verify_space, right_verify_space = st.columns(3)
    with verify_space:
        st.markdown("<h1 style='text-align: center; color: black;'>Verify your email account</h1>", unsafe_allow_html=True)
        verify_column1, verify_column2, verify_column3 = st.columns(3)
        with verify_column2:
            st.image(img_path, width=150, use_container_width=True)
        # with verify_column2:
        #     if st.button("Login", icon=":material/login:", use_container_width=True):
        #         ss.page_state = 'login'
        #         st.switch_page("./pages/login.py")
    with verify_space:
        verify_email()

from pages.functions import footer
footer()
