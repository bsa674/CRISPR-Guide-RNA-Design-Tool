import streamlit as st
from streamlit import session_state as ss
from time import sleep
import pandas as pd
import os

from functions import footer, check_name, validate_fasta, save_project, show_results, change_project_name
from Working_part.Model_usage import run_ML

def new_project(name = ''):
    """Adds a new project for that user"""
    option = None
    data = None
    results = 0
    fasta_data = ''

    with st.form("upload_func"):
        st.markdown("## Insert FASTA Sequence",help="Upload DNA sequence in FASTA format")
        project_name = st.text_input("Project Name", value='Project 1' if name == '' else name,help='Set a Unique Name for future accessibility').strip()

        if ss.page_state == 'add':
            if not ss.data['Summary'].empty:
                option = st.selectbox('Previously Loaded Project Inputs',(ss.data['Summary']['Project Name']),index=None)

            st.markdown('<div style="text-align: center;">or</div>', unsafe_allow_html=True)
            fasta_file = st.file_uploader("Upload FASTA File",type=['txt','fasta'],help='Click on upload and select fasta/text file of your choice')
            st.markdown('<div style="text-align: center;">or</div>', unsafe_allow_html=True)

            if option:
                sequence = ss.data['Summary'][ss.data['Summary']["Project Name"]==option]['Sequence'].iloc[0]
                data = f'>{option}\n{sequence}'
                fasta_text = st.text_area("Insert DNA sequence as a FASTA format",value = data).strip()
            else:
                fasta_text = st.text_area("Insert DNA sequence as a FASTA format",help='Must be in FASTA format!').strip()

        elif ss.page_state == 'modify':
            fasta_file = st.file_uploader("Upload FASTA File",type=['txt','fasta'],help='Click on upload and select fasta/text file of your choice')
            sequence = ss.data['Summary'][ss.data['Summary']['Project Name']==name]['Sequence'].to_list()[0]
            fasta_data = f'>{name}\n{sequence}'
            fasta_text = st.text_area("Insert DNA sequence as a FASTA format", value=fasta_data, help='Must be in FASTA format!').strip()

        submit = st.form_submit_button("Submit", use_container_width=True,help='Please check before submitting')
        if submit:
            if project_name.strip() == '':
                st.error(f'Project Name cannot be blank!')
                return

            data = fasta_text.strip() if fasta_text else fasta_file.read().decode("utf-8").strip() if fasta_file else None
            # This part comes into picture only when the project is being modified
            if (fasta_data.strip() == data.strip() and project_name == name and name != ''):
                st.info('No changes were noticed!')
                return

            # This part comes into picture only when the project is being modified
            elif (fasta_data.strip() == data.strip() and project_name != name and name != ''):
                if check_name(ss.data['Summary'],project_name):
                    st.write('Only project name was changed')
                    ss.data = change_project_name(ss.data,name,project_name)
                    st.success('Project Name was changed to '+project_name)
                    return

            # This part comes into picture when a new project is being added or modfied as well!
            elif check_name(ss.data['Summary'],project_name) or name == project_name:
                if validate_fasta(data.strip()):
                    st.success(f"Submitted")
                    df = run_ML(data)
                    df = df.sort_values(by='predicted_efficacy',ascending=False).reset_index().drop(columns=['index'])
                    results = 1
            else:
                return

    if results == 1:
        st.success("Processing complete! Redirecting to results...")
        ss.data = save_project(project_name, data.split("\n")[1], df, ss.data) # Save's Data and also updates ss.data
        sleep(5)
        show_results(df, project_name)
    footer()

def modify(name):
    """"Modifies the project name/sequence"""
    new_project(name=name.strip())

def delete(sheet_name_to_remove):
    """Deletes the selected project and updates the Summary sheet.
    """
    ss.data['Summary'] = ss.data['Summary'][ss.data['Summary']["Project Name"] != sheet_name_to_remove] # Removed from the Summary sheet
    del ss.data[sheet_name_to_remove] # Removed sheet from session_state as well

    if os.path.exists(ss.datapath):
        os.remove(ss.datapath)

    with pd.ExcelWriter(ss.datapath,engine='openpyxl',mode='w') as writer: # Saving the updated data!
        for name,sheet in ss.data.items():
            sheet.to_excel(writer,sheet_name=name,index=False)
