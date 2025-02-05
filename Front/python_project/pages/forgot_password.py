import streamlit as st
from PIL import Image
import streamlit_authenticator as stauth
from pages.auth import get_auth_credentials
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import os
from dotenv import load_dotenv
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

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
cred = credentials.Certificate(firebase_credential)

if not firebase_admin._apps:
    app = firebase_admin.initialize_app(cred)

database = firestore.client()
collection_fb = database.collection("CASTOR")



sendgrid_api_key = os.getenv("SENDGRID_API_KEY")


img_path = Image.open(os.path.join(os.path.dirname(__file__), '..', 'images', 'circular_logo.png'))
if __name__ == "__main__":
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
with st.container():
    forgot_lspace, forgot_space, forgot_rspace = st.columns(3)

    with forgot_space:
        st.markdown("<h1 style='text-align: center; color: black;'>Reset your password</h1>", unsafe_allow_html=True)

    with forgot_space:
        forgot_column1, forgot_column2, forgot_column3 = st.columns(3)
        with forgot_column2:
            st.image(img_path, width=150, use_container_width=True)
        with forgot_column2:
            if st.button('Login', icon=":material/login:", use_container_width=True):
                st.switch_page("./pages/login.py")

    with forgot_space:
        try:
            username_of_forgotten_password, email_of_forgotten_password, new_random_password = authenticator.forgot_password(
                captcha=True, fields={'Captcha': 'Type the code from the image'}
            )

            if username_of_forgotten_password:
                st.success('New password generated. Updating database...')

                # Hash the new password before storing it
                hashed_new_password = stauth.Hasher.hash(new_random_password)

                # Update Firestore with the new password
                try:
                    user_ref = collection_fb.document(username_of_forgotten_password)
                    user_ref.update({"password": hashed_new_password})

                    st.success("Password updated successfully in Firestore. Sending email...")

                    # Send the new password via email
                    if sendgrid_api_key:
                        subject = "Your New Password"
                        message = f"""
                        Hello {username_of_forgotten_password},

                        Your new password is: {new_random_password}

                        Please log in and change it immediately.

                        Regards,
                        Castor Team
                        """

                        try:
                            sg = SendGridAPIClient(sendgrid_api_key)
                            email_message = Mail(
                                from_email="castorguiderna@hotmail.com",  # Verified sender email
                                to_emails=email_of_forgotten_password,
                                subject=subject,
                                plain_text_content=message
                            )
                            response = sg.send(email_message)

                            if response.status_code == 202:
                                st.success("New password sent to your email. Check your inbox.")
                            else:
                                st.error(f"Failed to send email. Status code: {response.status_code}")

                        except Exception as e:
                            st.error(f"Error sending email: {e}")

                    else:
                        st.error("SendGrid API Key not found. Please check your environment variables.")

                except Exception as e:
                    st.error(f"Error updating password in Firestore: {e}")

            elif username_of_forgotten_password is False:
                st.error("Username not found. Please check your input.")

        except Exception as e:
            st.error(f"An error occurred: {e}")
