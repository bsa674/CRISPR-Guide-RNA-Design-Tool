import streamlit as st
from PIL import Image
import streamlit_authenticator as stauth
from pages.auth import get_auth_credentials
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import os
from dotenv import load_dotenv

load_dotenv()
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
    getuser_lspace, getuser_space, getuser_rspace = st.columns(3)

    with getuser_space:
        st.markdown("<h1 style='text-align: center; color: black;'>Retrieve Your Username</h1>", unsafe_allow_html=True)

        getuser_column1, getuser_column2, getuser_column3 = st.columns(3)
        with getuser_column2:
            st.image(img_path, width=150, use_container_width=True)
        with getuser_column2:
            if st.button('Login', icon=":material/login:", use_container_width=True):
                st.switch_page("./pages/login.py")
    with getuser_space:
        try:
            username_of_forgotten_username, email_of_forgotten_username = authenticator.forgot_username(
                captcha=True, fields={'Captcha': 'Type the code from the image'}
            )

            if username_of_forgotten_username:
                st.success("Username found. Sending email...")

                # Send the username via email
                if sendgrid_api_key:
                    subject = "Your Username Recovery"
                    message = f"""
                    Hello,

                    Your username associated with this email is: {username_of_forgotten_username}

                    If you did not request this, please ignore this email.

                    Regards,  
                    Castor Team
                    """

                    try:
                        sg = SendGridAPIClient(sendgrid_api_key)
                        email_message = Mail(
                            from_email="castorguiderna@hotmail.com",  # Verified sender email
                            to_emails=email_of_forgotten_username,
                            subject=subject,
                            plain_text_content=message
                        )
                        response = sg.send(email_message)

                        if response.status_code == 202:
                            st.success("Your username has been sent to your email. Check your inbox.")
                        else:
                            st.error(f"Failed to send email. Status code: {response.status_code}")

                    except Exception as e:
                        st.error(f"Error sending email: {e}")

                else:
                    st.error("SendGrid API Key not found. Please check your environment variables.")

            elif username_of_forgotten_username is False:
                st.error("Email not found. Please check your input.")

        except Exception as e:
            st.error(f"An error occurred: {e}")


