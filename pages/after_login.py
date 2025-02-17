'''
Author : Raghvendra Agrawal
Function :
This file is active when the user successfully logins and the user is redirected to the home page which contains the following tabs:
1. Homepage
2. New Project
3. Results
4. About
5. Profile Settings
6. Logout

And incase the Admin logins, the following tabs are displayed:
1. User Statistics
2. User Directory
3. Model Updation
4. Logout

Date of Modified : 17th February, 2025
'''



import streamlit as st
from streamlit import session_state as ss
from PIL import Image
import os
img_path = Image.open(os.path.join(os.path.dirname(__file__), '..', 'images', 'circular_logo.png'))

if 'page_state' not in ss.keys():
    ss.page_state = 'home'

if ss.page_state == 'home':
    st.set_page_config(page_title="Castor: A CRISPR Guide RNA Design Tool",
                   layout="wide",
                   page_icon=img_path, initial_sidebar_state="collapsed")

import streamlit_authenticator as stauth
from pages.auth import get_auth_credentials
from streamlit import session_state as ss
import pandas as pd

# Static Pages
from pages.Static_pages import homepage, change_details, about

# required functions
from pages.actions import new_project, delete
from pages.results import view_results
from pages.admin import admin_dasboard, regenerate_model, user_directory
from main import set_background
from pages.functions import tab_style

auth_credentials = get_auth_credentials()

# Initialize authenticator
authenticator = stauth.Authenticate(
    auth_credentials,
    cookie_name="castor",
    cookie_key="py_castor987654321",
    cookie_expiry_days=5,
    preauthorized={}
)

try:
    os.makedirs('data', exist_ok=True)
    if ss.username!='admin':
        if 'datapath' not in ss.keys():
            ss.datapath = os.path.join(os.getcwd(),f'data/{ss.username}.xlsx')

        if 'data' not in ss.keys():
            ss.data = pd.read_excel(ss.datapath,sheet_name=None) if os.path.exists(ss.datapath) else {'Summary':pd.DataFrame(columns = ['Project Name', 'Sequence', 'Base pairs', 'Timestamp'])}

        if os.path.exists(ss.datapath):
            # Remove any project that is in the Summary sheet but not as sheet
            projects = ss.data['Summary']['Project Name'].values
            for project in projects:
                if project not in ss.data.keys():
                    ss.data['Summary'] = ss.data['Summary'][ss.data['Summary']['Project Name'] != project]

            # Remove any project that is not in the Summary sheet
            projects_to_delete = []
            for project in ss.data.keys():
                if project not in ['Summary'] + ss.data['Summary']['Project Name'].to_list():
                    projects_to_delete.append(project)
            for project in projects_to_delete:
                delete(project)

            if ss.data['Summary'].shape[0] == 0:
                os.remove(ss.datapath)

        tab1, tab4, tab5, tab2, tab6, tab3 = st.tabs(["Homepage :derelict_house_building:", 'New Project:bulb:', 'Results :chart_with_upwards_trend:', "About :technologist:", 'Profile Settings :gear:', "Logout :arrow_right_hook:"])
        with tab1:
            set_background("images/castor_bg4.jpg")
        #    print("Entered Home Page")
            homepage(ss.username)

        with tab4:
            set_background("images/castor_bg4.jpg")
        #    print("Entered New Project")
            new_project()

        with tab5:
            set_background("images/castor_bg4.jpg")
        #    print("Entered Results ")
            view_results()

        with tab6:
            set_background("images/castor_bg4.jpg")
        #    print("Entered Profile Settings")
            change_details()

        with tab2:
            set_background("images/castor_bg4.jpg")
        #    print("Entered About")
            about()

        with tab3:
            set_background("images/castor_bg4.jpg")
        #    print("Entered Logout")
            ss.page_state='logout'
            st.subheader('Are you sure ?:crying_cat_face:')
            if st.button("logout"):
                authenticator.logout()
                ss.page_state = 'login'
                ss.logout = True
                ss.authentication_status = None
                ss.username = None
                st.switch_page("pages/thank_you.py")  # Redirect back to login
    else:
        tab1,tab4,tab2,tab3 = st.tabs(['User Statistics','User Directory','Model Updation','logout'])
        ss.page_state = 'admin'
        with tab1:
        #    set_background("images/castor_bg4.jpg")
        #    print("Entered Admin Dashboard")
            admin_dasboard()

        with tab2:
        #    print("Model Updation")
            st.title('Model Updation')
            regenerate_model()
#            st.subheader('This part is under development')


        with tab4:
        #    print("User Directory")
            st.title('User Directory')
            user_directory()
#            st.subheader('This is under development')

        with tab3:
        #    print("Entered Logout")
            ss.page_state='logout'
            st.subheader('Are you sure ?:crying_cat_face:')
            if st.button("logout"):
                ss.page_state = 'login'
                authenticator.logout()
                ss.logout = True
                ss.authentication_status = None
                ss.username = None
                st.switch_page("pages/thank_you.py")  # Redirect back to login
    tab_style()

except KeyboardInterrupt:
    print("Entered KeyBoard Interrupt")
    authenticator.logout()
    ss.logout = True
    ss.clear()
    print('Exiting now!')
# else:
#     st.warning("You need to log in first.")
#     st.switch_page("pages/login.py")  # Redirect to login if not authenticated

