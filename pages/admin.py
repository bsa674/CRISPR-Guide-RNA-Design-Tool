'''
Author : Raghvendra Agrawal & Pablo Ismael Alarcon
Function :
This file contains the admin dashboard, user directory functions and model regeneration functions.

Date of Modified : 17th February, 2025
'''



import streamlit as st
from streamlit import session_state as ss
import pandas as pd
import os
from PIL import Image

if 'page_state' not in ss.keys():
    ss.admin = 'admin'


img_path = Image.open(os.path.join(os.path.dirname(__file__), '..', 'images', 'circular_logo.png'))
if ss.page_state == 'admin':
    st.set_page_config(page_title="Castor: A CRISPR Guide RNA Design Tool",
                    layout="wide",
                    page_icon=img_path, initial_sidebar_state="collapsed")


from pages.functions import footer
from main import set_background
from Backend.model_generator import main
import firebase_admin
from firebase_admin import credentials, firestore, auth





def admin_dasboard():
    """Admin Dashboard which contains the user statistics
    """
    set_background("images/castor_bg4.jpg")
    st.title('Admin Dashboard')

    user_files = os.listdir(os.getcwd()+'/data')
    if user_files == []:
        st.info('No user data to display!')
        return

    data = {'User':[],'Number of Projects':[],'Last Login':[]}
    for file in user_files:
        username = file.split(".xlsx")[0]
        excel = pd.read_excel(os.getcwd() + f'/data/{file}',sheet_name='Summary')
        if excel.empty:
            rows = 0;login=r'N\A'
        else:
            rows = excel.shape[0]
            login = excel.iloc[0]['Timestamp']
            # Number of total downlaods by the user
            # Number of Logins
        data['User'].append(username)
        data['Number of Projects'].append(rows)
        data['Last Login'].append(login)

    st.subheader('User Information')
    st.dataframe(data)
    footer()

@st.fragment()
def regenerate_model():
    """Regenerate the model with new dataset
    """
    model_path = 'Backend/stacking_model.pkl'
    print('Check :',os.path.exists(model_path+'.tmp'))
    if os.path.exists(model_path+'.tmp'):
        st.write('Please Confirm to regenerate/Reject the model')
        if st.button('Regenerate Model'):
            os.remove(model_path)
            os.rename(model_path+'.tmp', model_path)
            st.success('Model regenerated successfully!')
            st.rerun(scope='fragment')
        if st.button('Reject Model'):
            os.remove(model_path+'.tmp')
#            os.rename(model_path+'.tmp', model_path)
            st.success('Model rejected successfully!')
            st.rerun(scope='fragment')

    else:
        uploaded_file = st.file_uploader("Upload New Dataset", type=['csv'], help='Upload the new dataset to train the model')
        if st.button("Train Model"):
            if uploaded_file is not None:
                df = pd.read_csv(uploaded_file)
                required_columns = ['gRNA_PAM', 'efficacy']  # Replace with actual column names from model.py
                if all(column in df.columns for column in required_columns):
                    col1 = set(''.join(df['gRNA_PAM'].to_list()))
                    if not any([False if i not in set('ACGT') else True for i in col1]): # Check if all characters are valid
                        unknown_char = ','.join([i for i in col1 if i not in set('ACGT')])
                        st.error(f"gRNA_PAM column seems to have invalid characters : {unknown_char}")
                    else:
                        if not pd.api.types.is_numeric_dtype(df['efficacy']): # Check if all values are numeric
                            st.error(f'Efficacy column contains non-numeric values!')
                        else:
                            if df[df['efficacy'].isna()].index.tolist() == []: # Check if there are any NaN values
                                st.success("File uploaded successfully and contains all necessary columns.")
                                print("Running Model")
                                mse, mae, r2 = main(df)
                                st.write(f"Mean Squared Error: {mse}")
                                st.write(f"Mean Absolute Error: {mae}")
                                st.write(f"R2 Score: {r2}")
                                print('Plotting')
                                for plot in os.listdir('feature_plots'):
                                    st.image(f'feature_plots/{plot}')  # Display all plots

                #                deploy = st.radio("Do you want to deploy this model for your users?", ('No', 'Yes'),index=None)
                                with st.container():
                                    st.write("Do you want to deploy this model for your users?")
                                    tab1,tab2,tab3,tab4,tab5,tab6 = st.columns(6)

                                    with tab1:
                                        if st.button('Yes'):
                                            if os.path.exists(model_path):
                                                os.remove(model_path)
                                            os.rename(model_path+'.tmp', model_path)
                                            st.success("The model has been deployed successfully.")
                                    with tab2:
                                        if st.button('No'):
                                            os.remove(model_path+'.tmp')
                                            st.info("The model has not been deployed.")
                                            print("Model not deployed.")
                            else:
                                print(df[df["efficacy"].isna()])
                                st.error(f'Efficacy column contains NaN values at index {df[df["efficacy"].isna()].index.tolist()}')
                else:
                    st.error(f"The uploaded file columns : {list(df.columns)} | Required : {required_columns}")

def user_directory():
    """User directory to manage user accounts
    """
    if not firebase_admin._apps:
        cred = credentials.Certificate({
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
        })
        firebase_admin.initialize_app(cred)

    # Initialize Firestore database
    database = firestore.client()

    users_ref = database.collection("CASTOR")
    users = users_ref.stream()

    user_list = []
    for user in users:
        user_data = user.to_dict()
        user_list.append(user_data)

    if user_list:
        st.subheader("Registered Users")
        for user in user_list:
            if user['username'].lower() == ss.username:
                continue
            else:
                with st.expander(user['username']):
                    username = user['username']
                    user_data_path = f'data/{username}.xlsx'
                    if os.path.exists(user_data_path):
                        projects = pd.read_excel(user_data_path,sheet_name='Summary').shape[0]
                        st.write(f"**Projects:** {projects}")
                        from datetime import datetime
                        modified_date = datetime.utcfromtimestamp(os.path.getmtime(user_data_path)).strftime('%Y-%m-%d %H:%M:%S')
                        st.write(f"**Last Login:** {modified_date}")
                    else:
                        st.write(f"**Projects:** 0")
                        st.write(f"**Last Login:** N/A")

                    # Delete user button
                    if st.button(f"Delete {user['username']}", key=f"delete_{user['username']}"):
                        try:
                            database.collection("CASTOR").document(user["username"]).delete()
                            st.success(f"User {user['username']} deleted successfully!")
                            st.rerun()
                        except Exception as e:
                            st.error(f"Error deleting user: {e}")

    st.info("Only the administrator can manage user accounts.")