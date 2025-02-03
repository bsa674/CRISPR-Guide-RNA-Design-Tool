import streamlit as st
from streamlit import session_state as ss
import os
import pandas as pd

# required functions
from actions import new_project
from results import view_results
from admin import admin_dasboard

# Adding path to session state
if 'dir' not in ss.keys():
    ss.dir= os.getcwd()
if 'username' not in ss.keys():
    ss.username = 'Admin'

if ss.username != 'Admin':
    if 'datapath' not in ss.keys():
        ss.datapath = ss.dir + f'/data/{ss.username}.xlsx'

    if 'data' not in ss.keys():
        ss.data = pd.read_excel(ss.datapath,sheet_name=None) if os.path.exists(ss.datapath) else {'Summary':pd.DataFrame(columns = ['Project Name', 'Sequence', 'Base pairs', 'Timestamp'])}

if "page_state" not in ss.keys():
    ss.page_state = None

# Static Pages
from Static_pages import homepage, change_details, logout, about

def add_new_project():
    ss.page_state = 'add'
    st.title('Start a New Project')
    new_project()

def results():
    ss.page_state = 'results'
    global path,old_df
    st.title("Results")
    st.divider()

    if not os.path.exists(ss.datapath):
        st.error("No Results available!")
    else:
        if ss.data['Summary'].shape[0]==0:
            st.error("No Results available!")
        else:
            view_results()

if ss.username != 'Admin':
    pg = st.navigation([st.Page(homepage,title='Homepage'),
                        st.Page(add_new_project,title='New Project'),
                        st.Page(results,title='Results'),
                        st.Page(change_details,title='Profile Settings'),
                        st.Page(about,title='Developer Information'),
                        st.Page(logout,title='Sign Out')
                        ])

    pg.run()

else:
    pg = st.navigation([st.Page(admin_dasboard,title='Admin Dashboard')])
    pg.run()