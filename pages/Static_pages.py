'''
Author : Raghvendra Agrawal and Pablo Ismel Alacorn
Function :
This file contains the functions that are used to view the static pages of the application like homepage, about and change details.

Date of Modified : 17th February, 2025
'''


import streamlit as st
from PIL import Image
import os
import streamlit_authenticator as stauth
from firebase_admin import firestore
import firebase_admin

if not firebase_admin._apps:
    from firebase_admin import credentials
    firebase_credential = {
        "type": "service_account",
        "project_id": os.getenv('FIREBASE_PROJECT_ID'),
        "private_key_id": os.getenv('FIREBASE_PRIVATE_KEY_ID'),
        "private_key": os.getenv('FIREBASE_PRIVATE_KEY').replace("\\n", "\n"),
        "client_email": os.getenv('FIREBASE_CLIENT_EMAIL'),
        "client_id": os.getenv('FIREBASE_CLIENT_ID'),
        "auth_uri": os.getenv('FIREBASE_AUTH_URI'),
        "token_uri": os.getenv('FIREBASE_TOKEN_URI'),
        "auth_provider_x509_cert_url": os.getenv('FIREBASE_CERT_URL'),
        "client_x509_cert_url": os.getenv('FIREBASE_CLIENT_CERT_URL')
    }
    cred = credentials.Certificate(firebase_credential)
    firebase_admin.initialize_app(cred)

database = firestore.client()
collection_fb = database.collection("CASTOR")

img_path = Image.open(os.path.join(os.path.dirname(__file__), '..', 'images', 'circular_logo.png'))
from pages.functions import footer, set_background

def homepage(name):
    set_background("images/castor_bg4.jpg")
    st.title(f"Welcome, {name}!")
    with st.container():
#        st.write("---")
        text_column, image_column = st.columns((1, 2))

        with text_column:
            st.subheader("Design the perfect gRNA for your research")
            st.markdown("""
            <div style="background: rgba(255, 255, 255, 0.1); padding: 10px; border-radius: 10px;">
            <p style="color: white; font-size: 25px;">
                Clustered Regularly Interspaced Short Palindromic Repeats (CRISPR)-associated protein 9 (Cas9)
                is a powerful genome editing tool utilized across a wide range of organisms,
                from prokaryotes to humans. A crucial component of this system is the guide RNA (gRNA),
                which directs the CRISPR complex to its target sequence.
                Castor—a streamlined tool designed to simplify the gRNA design process for researchers.
                Castor incorporates established algorithms in an intuitive environment,
                making the process of designing and evaluating gRNAs both efficient and widely accessible.
            </p>
            </div>
            """, unsafe_allow_html=True)
        with image_column:
            st.video('https://youtu.be/UKbrwPL3wXE?si=F4Z0_crxVS9BC-nP')
#            st.image(img_path, width=500)
    footer()


def change_details():
    set_background("images/castor_bg4.jpg")
    """Changes Credentails
    """
    st.title('Profile Settings')

    """Allows authenticated users to change their username and password."""

    if "authentication_status" not in st.session_state or not st.session_state["authentication_status"]:
        st.warning("You need to log in first.")
        st.stop()

    username = st.session_state["username"]

    st.subheader("Change your Password")
    new_password = st.text_input("New Password", type="password", placeholder="Enter a new password")
    confirm_password = st.text_input("Confirm Password", type="password", placeholder="Confirm your new password")

    if st.button("Update Credentials"):
        if not new_password or not confirm_password:
            st.error("All fields are required.")
            return

        if new_password != confirm_password:
            st.error("Passwords do not match.")
            return

        try:
            user_ref = collection_fb.document(username)
            user_doc = user_ref.get()

            if not user_doc.exists:
                st.error("User not found.")
                return

            user_data = user_doc.to_dict()
            email = user_data.get("email", "")

            updated_user_data = {
                "email": email,
                "password": stauth.Hasher.hash(new_password),
                "username": username,
                "date_joined": user_data.get("date_joined"),
                "email_verified": user_data.get("email_verified"),
                "email_verification_code": user_data.get("email_verification_code")
            }

            user_ref.delete()
            collection_fb.document(username).set(updated_user_data)

            st.success("Your credentials have been updated successfully. Please log in again.")

            for key in ["authentication_status", "username", "name"]:
                if key in st.session_state:
                    del st.session_state[key]

            st.switch_page("pages/login.py")

        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
    footer()

def about():
    set_background("images/castor_bg4.jpg")
    """Provides Developer Information
    """
    st.title("About :technologist:")
    st.divider()

    st.header('Developer Information')

    st.markdown('### Backend Devs')
    st.markdown("""
    <div style="background: rgba(255, 255, 255, 0.1); padding: 10px; border-radius: 10px; text-align: left;">
        <ul style="font-size: 25px; list-style: none; padding: 0;">
            <li>👨‍💻 Bishal</li>
            <li>👨‍💻 Mateo</li>
            <li>👩‍💻 Zeynep</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('### Frontend Devs')
    st.markdown("""
    <div style="background: rgba(255, 255, 255, 0.1); padding: 10px; border-radius: 10px; text-align: left;">
        <ul style="font-size: 25px; list-style: none; padding: 0;">
            <li>👨‍💻 Pablo</li>
            <li>👨‍💻 Raghvendra</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

    st.divider()
    st.text("Mail to report issues faced - raghvendra.agrawal@stud-uni.goettingen.de")
    footer()


