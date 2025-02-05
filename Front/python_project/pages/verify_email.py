import streamlit as st
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from PIL import Image
import os
from dotenv import load_dotenv

img_path = Image.open(os.path.join(os.path.dirname(__file__), '..', 'images', 'circular_logo.png'))
if __name__ == "__main__":
    st.set_page_config(page_title="Castor: A CRISPR Guide RNA Design Tool",
                   layout="wide",
                   page_icon=img_path, initial_sidebar_state="auto")
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


def verify_email():
    username = st.text_input("Username", placeholder="Enter your username")
    otp_input = st.text_input("Enter OTP", placeholder="Enter the 6-digit code", max_chars=6)

    if st.button("Verify"):
        user_doc = collection_fb.document(username).get()

        if user_doc.exists:
            user_data = user_doc.to_dict()
            stored_otp = user_data.get("email_verification_code")

            if stored_otp and stored_otp == otp_input:
                collection_fb.document(username).update({"email_verified": True})
                st.success("Email verified successfully! You can now log in.")
            else:
                st.error("Invalid OTP. Please try again.")
        else:
            st.error("User not found.")

with st.container():
    left_verify_space, verify_space, right_verify_space = st.columns(3)
    with verify_space:
        st.markdown("<h1 style='text-align: center; color: black;'>Verify your email account</h1>", unsafe_allow_html=True)
        verify_column1, verify_column2, verify_column3 = st.columns(3)
        with verify_column2:
            st.image(img_path, width=150, use_container_width=True)
        with verify_column2:
            if st.button("Login", icon=":material/login:", use_container_width=True):
                st.switch_page("./pages/login.py")
    with verify_space:
        verify_email()
