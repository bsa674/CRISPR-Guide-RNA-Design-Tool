import streamlit as st
from PIL import Image
import streamlit_authenticator as stauth
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import datetime
import re
import random
import sendgrid
from sendgrid.helpers.mail import Mail, Email, To, Content
from dotenv import load_dotenv
import os

# Load environment variables from the .env file
load_dotenv()
private_key = os.getenv('FIREBASE_PRIVATE_KEY')
if private_key is None:
    raise ValueError("FIREBASE_PRIVATE_KEY is missing from the environment variables")

sendgrid_api_key = os.getenv("SENDGRID_API_KEY").strip()
if sendgrid_api_key is None:
    st.error("SendGrid API key not found. Please set the environment variable.")

img_path = Image.open(os.path.join(os.path.dirname(__file__), '..', 'images', 'circular_logo.png'))
if __name__ == "__main__":
    st.set_page_config(page_title="Castor: A CRISPR Guide RNA Design Tool",
                   layout="wide",
                   page_icon=img_path, initial_sidebar_state="auto")
#Initialize Cloud Firestore in your own server
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

def insert_user(email, password, username, date_joined=str(datetime.datetime.now())):
    try:
        # Insert user data into Firestore (this stores the user info)
        otp = generate_otp()

        user_data = {
            'email': email,
            'password': password,
            'username': username,
            'date_joined': date_joined,
            'email_verified': False,
            'email_verification_code': otp
        }
        # Insert user data into Firestore under the 'username' document
        collection_fb.document(username).set(user_data)

        # Fetch the user's document from Firestore
        user_ref = collection_fb.document(username)
        user_doc = user_ref.get()

        if not user_doc.exists:
            return {"success": False, "message": "User document not found in Firestore."}

            # Send OTP email
        sendgrid_api_key = os.getenv("SENDGRID_API_KEY")  # Load API Key
        if sendgrid_api_key:
            send_otp_email(email, otp, sendgrid_api_key)
            return {"success": True, "message": f"User {email} inserted and OTP sent successfully."}
        else:
            return {"success": False, "message": "SendGrid API Key not found. Please check environment variables."}

    except Exception as e:
        return {"success": False, "message": str(e)}

def fetch_users():
    #For return a dictionary of the users that are stored in Firebase
    try:
        docs = collection_fb.stream()
        users = []
        for doc in docs:
            user_data = doc.to_dict()
            if all(k in user_data for k in ["email", "password", "username"]):
                user_data["id"] = doc.id
                users.append(user_data)
            else:
                print(f"Warning: Skipping document {doc.id} due to missing fields: {user_data}")
        return users
    except Exception as e:
        print(f"An error occurred: {e}")
        return []

def get_user_emails():
    try:
        docs = collection_fb.stream()
        emails = []
        for doc in docs:
            user_data = doc.to_dict()
            if "email" in user_data:
                emails.append(user_data["email"])
        return emails
    except Exception as e:
        print(f"An error occurred: {e}")
        return []
def get_usernames():
    try:
        docs = collection_fb.stream()
        usernames = []
        for doc in docs:
            user_data = doc.to_dict()
            if "username" in user_data:
                usernames.append(user_data["username"])
        return usernames
    except Exception as e:
        print(f"An error occurred: {e}")
        return []

def valid_email(email):
    #For check email validity
    pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    return bool(re.match(pattern, email))

def generate_otp():
    return str(random.randint(100000, 999999))

def send_otp_email(email, otp, sendgrid_api_key):
    try:
        sender_email = "castorguiderna@hotmail.com"  # Your verified sender email in SendGrid

        # Initialize SendGrid client with API Key
        sg = sendgrid.SendGridAPIClient(api_key=sendgrid_api_key)

        # Create the email content
        subject = "Your OTP Verification Code"
        content = f"Your OTP verification code is: {otp}"

        # Create the email message
        from_email = Email(sender_email)  # Your verified sender email
        to_email = To(email)  # Recipient's email
        content = Content("text/plain", content)  # Plain text email body

        # Create the Mail object
        mail = Mail(from_email, to_email, subject, content)

        # Send the email using SendGrid
        response = sg.send(mail)

        # Check response
        if response.status_code == 202:
            st.success(f"OTP email sent to {email} successfully!")
            return True
        else:
            st.error(f"Failed to send email to {email}. Status code: {response.status_code}")
            return False

    except Exception as e:
        st.error(f"Error sending OTP email to {email}: {e}")
        return False

def valid_username(username):
    #For check username validity
    pattern = "^[a-zA-Z0-9_]*$"
    return bool(re.match(pattern, username))


def signup():
    with st.form(key="signup", clear_on_submit=True):
        email = st.text_input("Email", placeholder="Write your email")
        username = st.text_input("Username", placeholder="Write your name")
        password = st.text_input("Password", placeholder="Write a password", type="password")
        password_conf = st.text_input("Password", placeholder="Confirm your password", type="password")

        submit = st.form_submit_button("Sign up")

        if submit:
            if email:
                if valid_email(email):
                    if email not in get_user_emails():
                        if valid_username(username):
                            if username not in get_usernames():
                                if len(username) >= 1:
                                    if len(password) >= 6:
                                        if password == password_conf:
                                            hashed_password = stauth.Hasher.hash(password)
                                            result = insert_user(email, hashed_password, username, date_joined= str(datetime.datetime.now()))
                                            if result["success"]:
                                                st.success("Account created successfully. Check your email for the OTP.")
                                                st.balloons()
                                                st.switch_page("./pages/verify_email.py")
                                            else:
                                                st.error(result["message"])
                                        else:
                                            st.warning("Your passwords don't match")
                                    else:
                                        st.warning("Your password is too short")
                                else:
                                    st.warning("The username you chose is too short")
                            else:
                                st.warning("The username you chose already exists")
                        else:
                            st.warning("Invalid username")
                    else:
                        st.warning("Email already exists")
                else:
                    st.warning("Invalid email")
            else:
                st.warning("Email field is required")

if __name__ == "__main__":
    with st.container():
        l_space, signup_space, r_space = st.columns(3)
        with signup_space:
            st.markdown("<h1 style='text-align: center; color: black;'>Create your account</h1>", unsafe_allow_html=True)
            col1, col2, col3 = st.columns(3)
            with col2:
                st.image(img_path, width=150, use_container_width=True)
            with col2:
                if st.button("Home", icon=":material/home:", use_container_width=True):
                    st.switch_page("./main.py")
        with signup_space:
            signup()
        with signup_space:
            with st.container():
                account_s1,account_s2 = st.columns([0.6, 0.4])
                with account_s1:
                    st.text("Already have an account?")
                with account_s2:
                    if st.button('Login', icon=":material/login:",use_container_width=True):
                        st.switch_page("./pages/login.py")
   
