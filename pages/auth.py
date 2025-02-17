import streamlit as st
from pages.signup import fetch_users  # Ensure fetch_users() is correctly defined

def get_auth_credentials():
    users = fetch_users()
    if not users:
        st.warning("No users found in the database. Please create a user first.")
        st.stop()

    auth_credentials = {"usernames": {}}
    for user in users:
        if 'username' in user and 'email' in user and 'password' in user:
            auth_credentials["usernames"][user["username"]] = {
                "name": user["username"],
                "password": user["password"],
                "email": user["email"]
            }
        else:
            st.error(f"Invalid user entry: {user}")

    return auth_credentials
