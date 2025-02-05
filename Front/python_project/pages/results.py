import streamlit as st
from PIL import Image
import streamlit_authenticator as stauth
from pages.auth import get_auth_credentials
import os

img_path = Image.open(os.path.join(os.path.dirname(__file__), '..', 'images', 'circular_logo.png'))
st.set_page_config(page_title="Castor: A CRISPR Guide RNA Design Tool",
                   layout="wide",
                   page_icon=img_path, initial_sidebar_state="auto")

auth_credentials = get_auth_credentials()

# Initialize authenticator
authenticator = stauth.Authenticate(
    auth_credentials,
    cookie_name="castor",
    cookie_key="py_castor987654321",
    cookie_expiry_days=5,
    preauthorized={}
)

# Check authentication status
if "authentication_status" in st.session_state and st.session_state["authentication_status"]:
    st.title("Welcome to the Results Page 🎉")

    # Logout button
    if st.button("Logout"):
        authenticator.logout()
        st.switch_page("pages/login.py")  # Redirect back to login

else:
    st.warning("You need to log in first.")
    st.switch_page("pages/login.py")  # Redirect to login if not authenticated
