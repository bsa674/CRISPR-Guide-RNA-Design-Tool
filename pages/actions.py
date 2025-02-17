'''
Author : Raghvendra Agrawal
Function :
This file contains the functions that are used to create new projects, modify existing projects and delete projects.

Date of Modified : 17th February, 2025
'''


import streamlit as st
from streamlit import session_state as ss
from time import sleep
import pandas as pd
import os
from traceback import print_exc
from Bio import SeqIO
from io import StringIO

from pages.functions import footer, check_name, validate_fasta, save_project, show_results, change_project_name, form_glass_bg,selectbox_style
from Backend.model_usage import predict_efficacy_scores

def new_project(name = ''):
    """Adds a new project for that user"""
    option = None
    data = None
    results = 0
    fasta_data = ''
    with st.form(f"upload_func_{ss.page_state}"):
        st.markdown("## Insert FASTA Sequence",help="Upload DNA sequence in FASTA format")
        project_name = st.text_input("Project Name", value='Project 1' if name == '' else name,help='Set a Unique Name for future accessibility').strip()

        if ss.page_state != 'modify':
            if not ss.data['Summary'].empty:
                selectbox_style()
                option = st.selectbox('Previously Loaded Project Inputs',(ss.data['Summary']['Project Name']),index=None)

            st.markdown('<div style="text-align: center;">or</div>', unsafe_allow_html=True)
            fasta_file = st.file_uploader("Upload FASTA File",type=['txt','fasta'],help='Click on upload and select fasta/text file of your choice')

            st.markdown('<div style="text-align: center;">or</div>', unsafe_allow_html=True)

            if option:
                sequence = ss.data['Summary'][ss.data['Summary']["Project Name"]==option]['Sequence'].iloc[0]
                data = f'>{option}\n{sequence}'
                fasta_text = st.text_area("Insert DNA sequence as a FASTA format",value = data)
            else:
                fasta_text = st.text_area("Insert DNA sequence as a FASTA format",help='Must be in FASTA format!')

        else:
            fasta_file = st.file_uploader("Upload FASTA File",type=['txt','fasta'],help='Click on upload and select fasta/text file of your choice')
            sequence = ss.data['Summary'][ss.data['Summary']['Project Name']==name]['Sequence'].to_list()[0]
            fasta_data = f'>{name}\n{sequence}'
            fasta_text = st.text_area("Insert DNA sequence as a FASTA format", value=fasta_data, help='Must be in FASTA format!')

        submit = st.form_submit_button("Submit", use_container_width=True,help='Please check before submitting')
        form_glass_bg()

        if submit:
            print('Submitted')
            if project_name == '':
                st.error('Project Name cannot be blank!')
                return

            data = fasta_text if fasta_text else fasta_file.read().decode("utf-8") if fasta_file!=None else ''

            if data == '':
                st.error('No data was recorded! Please Try Again')
                return
            # This part comes into picture only when the project is being modified
            if (fasta_data == data and project_name == name and name != ''):
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
                    data = str(list(SeqIO.parse(StringIO(data), "fasta"))[0].seq)
#                    print('Data:',data)
                    st.success(f"Submitted")
                    df = predict_efficacy_scores(data)
                    print(df)
                    results = 1
            else:
                return

    if results == 1:
        st.success("Processing complete! Redirecting to results...")
        try:
#            print('While Saving Data:',data)
            ss.data = save_project(project_name, data, df, ss.data) # Save's Data and also updates ss.data
        except:
            st.error("Failed to Save! Fix Code")
            print_exc()

#        sleep(5)
        try:
            show_results(df, project_name)
        except:
            st.error("No results to display! Fix Code")
            delete(project_name)
            print_exc()

    footer()

def modify(name):
    """"Modifies the project name/sequence"""
    new_project(name=name.strip())

def delete(sheet_name_to_remove):
    """Deletes the selected project and updates the Summary sheet.
    """
    ss.data['Summary'] = ss.data['Summary'][ss.data['Summary']["Project Name"] != sheet_name_to_remove] # Removed from the Summary sheet

    if sheet_name_to_remove in ss.data.keys():
        del ss.data[sheet_name_to_remove] # Removed sheet from session_state as well

    if os.path.exists(ss.datapath):
        os.remove(ss.datapath)

    with pd.ExcelWriter(ss.datapath,engine='openpyxl',mode='w') as writer: # Saving the updated data!
        for name,sheet in ss.data.items():
            sheet.to_excel(writer,sheet_name=name,index=False)
