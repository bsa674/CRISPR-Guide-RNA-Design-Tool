'''
Author : Raghvendra Agrawal
Function :
This file contains the functions that are used to view the results of the projects and perform CRUD operations on the projects.
Date of Modified : 17th February, 2025
'''


# Required Libraries
import streamlit as st
from streamlit import session_state as ss
import os
import pandas as pd

#Functions
from pages.functions import footer, show_results, download_all_results,download_bt_style, selectbox_style

# Actions
from pages.actions import modify, delete

def check(*args):
    ss.Delete_Project = None
    if args[0]:
        delete(args[1])
#        st.success(f'{args[1]} deleted!')
    return

@st.fragment
def view_results():
    """View the results of the projects
    """
    project_names = ss.data['Summary']['Project Name'].tolist()


    if os.path.exists(ss.datapath):
        if pd.read_excel(ss.datapath,sheet_name='Summary').empty:
            st.info('No Results to display!')
            os.remove(ss.datapath)
        else:
            download_bt_style()
            st.download_button(
                label="*Click to download all results to your local system",
                data=download_all_results(ss.datapath),
                file_name=f"Results.zip",
                mime="application/zip",
                use_container_width=True,
                help=f'Upon clicking, the {ss.data["Summary"].shape[0]} project results (guide RNAs & Plots) as a *.zip file will be downloaded!' if ss.data["Summary"].shape[0]>1 else
                        f'Upon Clicking, The Project result (Guide RNAs & corresponding plots) as a *.zip file will be downloaded!'
            )
            st.divider()

            st.subheader('View Project Results',help='Select the project name to look at the corresponding results')
            view_project = st.selectbox('',(project_names),index=None,key='View_Project')
            if view_project:
                show_results(ss.data[view_project],view_project)
            st.divider()

            st.subheader('Modify Project',help='Upon making any change, it cannot be reverted back!')
            modify_project = st.selectbox('',(project_names),index=None,key='Modify_Project')
            if modify_project:
                ss.page_state = 'modify'
                modify(modify_project)
            st.divider()

            st.subheader('Delete Project',help='Be-Careful')
            st.info('Warning : Once deleted, cannot be retreived')
            delete_project = st.selectbox('',(project_names),index=None,key='Delete_Project')
            if delete_project and delete_project!='Select a Project':
                ss.page_state = 'delete'
                st.warning(" Are you sure?", icon="⚠️")
                st.button('Yes',on_click=check,args=[True,delete_project])
                st.rerun(scope='fragment')
            footer()

    else:
        st.info('No Results to display!')
