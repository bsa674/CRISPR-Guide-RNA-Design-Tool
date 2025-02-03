import streamlit as st
from streamlit import session_state as ss
import pandas as pd
import os
from datetime import datetime
import plotly.express as px
import time
import io
import zipfile
from openpyxl import load_workbook
from Working_part.Model_usage import visualize_predictions



def footer():
    """Adds a Footer to the page!
    """
    st.divider()
    st.caption('Made with :heart: by Team 18')

def check_name(df,project_name):
    """Checking if the project name already exists?
    """
    if project_name == '':
        st.error(f'Project Name cannot be blank!')
        return False

    if df.empty or df.shape[0] == 0 or 'Project Name' not in df.columns:
        return True

    if project_name not in df['Project Name'].unique():
        return True

    st.error(f'{project_name} already exists (try something like "name_v1.1")')
    return False


def validate_fasta(data):
    """Checking the data is in fasta format and is a DNA sequence
    """
    if data.startswith(">"):
        seq = data.split("\n")[1]
        if all([False if i not in ['A','T','C','G'] else True for i in set(seq)]):
            return True
        else:
            unknown_char = [i for i in set(seq) if i not in ['A','T','C','G']]
            st.error("Looks like the sequence has nucleotides other than A,T,C,G")
            st.error("Unknown characters : " + ",".join(unknown_char))
    else:
        st.error("This doesn't look like FASTA format ('>' is not present in the first line). Please check the file!")
        st.error("Kindly refer - https://www.ncbi.nlm.nih.gov/genbank/fastaformat/ to know more about FASTA format")

    return False

def dummy(sequence):
    """Dummy process with progress bar
    """
    steps = ["Reading Sequence", "Calculating Stats", "Generating Results"]
    time_required = [2, 3, 4]  # Example times per step

    progress_bar = st.progress(0)
    progress_text = st.empty()

    for i, step in enumerate(steps):
        progress_text.text(step)
        time.sleep(time_required[i])
        progress_bar.progress((i + 1) / len(steps))

    return pd.read_excel("D:\Masters\Courses\Sem 1\Python Programming for Data Science\Project\dummy_result.xlsx")

def check_dup_rows(df, new_row):
    """Check for duplicate rows and update or append accordingly
    """
    if new_row['Project Name'] in df['Project Name'].unique():
        df.update(df.loc[df['Project Name'] == new_row['Project Name']].assign(**new_row))
    else:
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    return df

def save_project(project_name, ip, op, df):
    """Save project details and results to an Excel file
    """
    now = datetime.now()
    timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
    new_row = {
        'Project Name': project_name,
        'Sequence': ip,
        'Base pairs': len(ip),
        'Timestamp': timestamp
    }

    df['Summary'] = pd.concat([df['Summary'], pd.DataFrame([new_row])], ignore_index=True) # New entry added to Summary sheet
    df[project_name] = op

    # Write all sheets back to the file
    with pd.ExcelWriter(ss.datapath, engine="openpyxl") as writer:
        for sheet_name, sheet in df.items():
            sheet.to_excel(writer, sheet_name=sheet_name, index=False)

    return df

def plots(df):
    """Generate bar plots for Efficacy and GC Content."""
    plots = visualize_predictions(df)
    return {'Efficacy Scores': plots[0], 'Feature HeatMap': plots[1], 'GC Content':plots[2]}


def show_results(df, project_name):
    """Display results and provide a downloadable ZIP file with plots and data."""
    figures = plots(df)
    st.markdown(f"## Results: {project_name}")
    st.markdown(df[['gRNA_PAM',"predicted_efficacy","GC_content","seq_length","entropy"]].style.hide(axis="index").to_html(), unsafe_allow_html=True)
    st.markdown("### Summary")
    st.plotly_chart(figures['Efficacy Scores'])
    st.plotly_chart(figures['Feature HeatMap'])
    st.plotly_chart(figures['GC Content'])

    # Create ZIP buffer for download
    with io.BytesIO() as zip_buffer:
        with zipfile.ZipFile(zip_buffer, "w") as zip_file:
            # Add CSV data
            zip_file.writestr(f"{project_name}_results.csv", df.to_csv(index=False).encode("utf-8"))

            # Add plots as PNGs
            for name, fig in figures.items():
                zip_file.writestr(f"{project_name}_{name.lower()}_plot.png", fig.to_image(format="png", width=800, height=600, scale=2))

        # Stream download button
        st.download_button(
            label="Download Results (*.ZIP)",
            data=zip_buffer.getvalue(),
            file_name=f"{project_name}_results.zip",
            mime="application/zip"
        )

def download_all_results(path):
    """Downloads all the results the user has
    """
    zip_buffer = io.BytesIO()

    with zipfile.ZipFile(zip_buffer, "w") as zip_file:
        # Save the Excel file to a BytesIO buffer
        with io.BytesIO() as excel_output:
            with pd.ExcelWriter(excel_output, engine='xlsxwriter') as writer:
                # Read all sheets as a dictionary and write each sheet individually
                sheets = pd.read_excel(path, sheet_name=None)
                for sheet_name, sheet_df in sheets.items():
                    sheet_df.to_excel(writer, sheet_name=sheet_name, index=False)
            excel_output.seek(0)
            zip_file.writestr("All_Results.xlsx", excel_output.read())

        # Process sheets and generate plots
        with pd.ExcelFile(path) as excel_file:
            for sheet_name in excel_file.sheet_names:
                if sheet_name != 'Summary':
                    sheet_df = excel_file.parse(sheet_name)
                    for plot_name, plot in plots(sheet_df).items():
                        zip_file.writestr(f"{sheet_name}_{plot_name.lower()}_plot.png", plot.to_image(format="png", width=800, height=600, scale=2))

    return zip_buffer.getvalue()

def change_project_name(df,old,new):
    now = datetime.now()
    timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
    df['Summary'].loc[df['Summary']["Project Name"] == old, 'Timestamp'] = timestamp
    df['Summary'].loc[df['Summary']["Project Name"] == old, 'Project Name'] = new # Changed name in Summary sheet
    df[new] = df.pop(old) # renamed the old sheet with new sheet name
    return df
