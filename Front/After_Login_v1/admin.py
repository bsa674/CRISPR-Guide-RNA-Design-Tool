import streamlit as st
from streamlit import session_state as ss
import pandas as pd
import os


def admin_dasboard():
    st.title('Admin Dashboard')

    user_files = os.listdir(ss.dir + '/data')

    data = {'User':[],'Number of Projects':[],'Last Login':[]}
    for file in user_files:
        username = file.split(".xlsx")[0]
        excel = pd.read_excel(ss.dir + f'/data/{file}',sheet_name='Summary')
        print(file,excel)
        if excel.empty:
            rows = 0;login='N\A'
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

def regenerate_model():
    print()