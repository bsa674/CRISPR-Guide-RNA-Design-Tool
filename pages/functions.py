'''
Author : Raghvendra Agrawal
Function :
This file contains the all the major css functions for styling and other functions required for pre-processing and post processing the sequence data

Date of Modified : 17th February, 2025
'''


import streamlit as st
from streamlit import session_state as ss
import pandas as pd
import os
from datetime import datetime
import io
import zipfile
from Backend.model_usage import visualize_features
from Bio import SeqIO
from io import StringIO
import base64

def form_glass_bg():
    glassmorphism_css = """<style>
    /* Glassmorphic Form Styling */
    [data-testid="stForm"] {
        background: rgba(255, 255, 255, 0.1); /* Semi-transparent white */
        border-radius: 15px; /* Rounded corners */
        padding: 20px;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1); /* Soft shadow */
        backdrop-filter: blur(10px); /* Blur effect */
        -webkit-backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.3); /* Light border */
    }

    /* Improve text visibility */
    input, label {
        color: white !important;
    }

    /* Style the submit button */
    div[data-testid="stFormSubmitButton"] button {
        background: linear-gradient(135deg, #6a11cb, #2575fc);
        color: white;
        border-radius: 25px;
        padding: 12px 20px;
        font-size: 16px;
        border: none;
        cursor: pointer;
        transition: all 0.3s ease;
    }

    div[data-testid="stFormSubmitButton"] button:hover {
        background: linear-gradient(135deg, #2575fc, #6a11cb);
        transform: scale(1.05);
    }
</style>
    """
    st.markdown(glassmorphism_css, unsafe_allow_html=True)

def tab_style():
    css = """
    <style>
    /* Tab container */
    div[data-testid="stTabs"] [data-baseweb="tab-list"] {
        gap: 5px;
    }

    /* Tab button (default state) */
    div[data-testid="stTabs"] [data-baseweb="tab"] {
        height: 50px;
        width: 200px;
        background-color: #6a11cb !important;  /* Same as button */
        border-radius: 25px 25px 0px 0px;
        padding-top: 10px;
        padding-bottom: 10px;
        color: white !important;
        font-size: 18px;
        font-weight: bold;
        transition: all 0.3s ease;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }

    /* Hover effect */
    div[data-testid="stTabs"] [data-baseweb="tab"]:hover {
        background-color: #2575fc !important;  /* Same as button hover */
        transform: translateY(-3px);
        box-shadow: 0 6px 8px rgba(0, 0, 0, 0.15);
    }

    /* Active (selected) tab */
    div[data-testid="stTabs"] [aria-selected="true"] {
        background-color: white !important;
        color: #6a11cb !important;
        border-bottom: 3px solid #6a11cb;
        transform: translateY(0);
        box-shadow: none;
    }

    /* Tab text styling */
    div[data-testid="stTabs"] [data-baseweb="tab-list"] button [data-testid="stMarkdownContainer"] p {
        font-size: 1.2rem;
        text-align: center;
        color: inherit;
    }
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

def selectbox_style():
    css = """
    <style>
    /* Target the main select box container */
    div[data-baseweb="select"] > div:first-child {
        background-color: #333333 !important;
        color: white !important;
        padding: 10px !important;
        border: 2px solid #555555 !important;
        border-radius: 8px !important;
        font-size: 16px !important;
        cursor: pointer !important;
        transition: all 0.3s ease !important;
    }

    /* Hover state */
    div[data-baseweb="select"] > div:first-child:hover {
        background-color: #444444 !important;
        border-color: #777777 !important;
    }

    /* Focus state */
    div[data-baseweb="select"] > div:first-child:focus-within {
        border-color: #999999 !important;
        box-shadow: 0 0 5px rgba(255, 255, 255, 0.5) !important;
    }

    /* Dropdown popover */
    div[role="listbox"] {
        background-color: #333333 !important;
        color: white !important;
        border: 2px solid #555555 !important;
        border-radius: 8px !important;
    }

    /* Dropdown options */
    div[role="option"] {
        padding: 12px !important;
        font-size: 16px !important;
    }

    /* Selected option */
    div[role="option"][aria-selected="true"] {
        background-color: #444444 !important;
        color: #FFD700 !important;
    }

    /* Hovered option */
    div[role="option"]:hover {
        background-color: #555555 !important;
    }

    /* Label styling */
    label[data-testid="stWidgetLabel"] p {
        font-size: 18px !important;
        font-weight: bold !important;
        color: white !important;
    }
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

def download_bt_style():
    css = """
    <style>
    /* More specific styling for download button */
    div[data-testid="stDownloadButton"] button {
        background-color: #ff6b00 !important;  /* Orange shade */
        color: white !important;
        padding: 15px 30px;
        border: none;
        border-radius: 25px;
        font-size: 18px;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }

    /* Hover effect */
    div[data-testid="stDownloadButton"] button:hover {
        background-color: #e65c00 !important;  /* Slightly darker orange */
        transform: translateY(-3px);
        box-shadow: 0 6px 8px rgba(0, 0, 0, 0.15);
    }

    /* Active effect */
    div[data-testid="stDownloadButton"] button:active {
        transform: translateY(0);
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

def button_style():
    style = """<style>
/* Button styling with hover effects */
.stButton>button {
    background-color: #6a11cb;
    color: white;
    padding: 15px 30px;
    border: none;
    border-radius: 25px;
    font-size: 18px;
    cursor: pointer;
    transition: all 0.3s ease;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.stButton>button:hover {
    background-color: #2575fc;
    transform: translateY(-3px);
    box-shadow: 0 6px 8px rgba(0, 0, 0, 0.15);
}

.stButton>button:active {
    transform: translateY(0);
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

/* Text animation */
@keyframes slideIn {
    from { transform: translateX(-100%); opacity: 0; }
    to { transform: translateX(0); opacity: 1; }
}

.animated-text {
    animation: slideIn 1.5s ease-out;
}

/* Image hover effect */
.image-hover {
    transition: transform 0.3s ease;
}

.image-hover:hover {
    transform: scale(1.1);
}
</style>
    """
    st.markdown(style, unsafe_allow_html=True)

def set_background(img_background):
    with open(img_background, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode()
    app_background = f"""
    <style>
    .stApp {{
        background-image: url("data:image/jpg;base64,{encoded_string}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background_color: rgba(0, 0, 0, 0);
    }}
    </style>
    """
    st.markdown(app_background, unsafe_allow_html=True)

def footer():
    """Adds a Footer to the page!
    """
    st.divider()
    with st.container():
        space1,space2,space3,space4,space5,space6,space7,space8,space9,space10,space11,space12,space13 = st.columns(13)
        with space13:
            st.caption('Made with :heart: by Team 18')
        with space1:
            st.markdown("<p style='text-align: right; color: white;'>© 2025 Castor<p>", unsafe_allow_html=True)


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
        records = list(SeqIO.parse(StringIO(data), "fasta"))
        if len(records) > 1:
            st.error("More than one sequence found in the file. Please provide only one sequence")
            return False

        record = records[0]
        if all([False if i not in ['A','T','C','G'] else True for i in set(str(record.seq))]):
            return True
        else:
            unknown_char = [i for i in set(str(record.seq)) if i not in ['A','T','C','G','a','t','c','g']]
            st.error("Looks like the sequence has nucleotides other than A,T,C,G")
            st.error("Unknown characters : " + ",".join(unknown_char))
    else:
        print()
        st.error("This doesn't look like FASTA format ('>' is not present in the first line). Please check the file!")
        st.error("Kindly refer - https://www.ncbi.nlm.nih.gov/genbank/fastaformat/ to know more about FASTA format")

    return False

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

#    print(ss.datapath)
    # print(df.columns)

    with pd.ExcelWriter(ss.datapath, engine="openpyxl") as writer:
        for sheet_name, sheet in df.items():
            if sheet_name == project_name:
                continue
            sheet.to_excel(writer, sheet_name=sheet_name, index=False)

    return df

def show_results(df, project_name):
    """Display results and provide a downloadable ZIP file with plots and data."""
    figures = visualize_features(df)
    st.markdown(f"## Results: {project_name}")
    st.markdown("""
    <style>
        .centered-table {
            margin-left: auto;
            margin-right: auto;
            text-align: center;
            width: 80%; /* Adjust width */
            border-radius: 10px;
            overflow: hidden;
            background: rgba(255, 255, 255, 0.2); /* Translucent white */
            backdrop-filter: blur(10px); /* Blur effect */
            -webkit-backdrop-filter: blur(10px); /* Safari support */
            padding: 15px;
            box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1); /* Soft shadow */
        }

        .centered-table th, .centered-table td {
            text-align: center !important;
            color: white !important; /* Ensure text is readable */
            padding: 10px;
        }

        .centered-table th {
            background: rgba(255, 255, 255, 0.3); /* Slightly darker for contrast */
        }
    </style>
    """, unsafe_allow_html=True)
    st.markdown(df[['k-mer', 'Predicted_Efficacy']]
            .head(10)  # Selecting top 10 entries
            .style.hide(axis="index")  # Hide index
            .set_table_attributes('class="centered-table"')  # Apply CSS class
            .to_html(),
            unsafe_allow_html=True)
    st.markdown("### Summary")
    for figure in figures.values():
        st.plotly_chart(figure)
    # Create ZIP buffer for download
    with io.BytesIO() as zip_buffer:
        with zipfile.ZipFile(zip_buffer, "w") as zip_file:
            # Add CSV data
            zip_file.writestr(f"{project_name}_results.csv", df[['k-mer', 'Predicted_Efficacy']].to_csv(index=False).encode("utf-8"))

            # Add plots as PNGs
            for name, fig in figures.items():
                # print(name)
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
                    if sheet_name!='Summary':
                        sheet_df = sheet_df[['k-mer', 'Predicted_Efficacy']]
                    sheet_df.to_excel(writer, sheet_name=sheet_name, index=False)
            excel_output.seek(0)
            zip_file.writestr("All_Results.xlsx", excel_output.read())

        # Process sheets and generate plots
        with pd.ExcelFile(path) as excel_file:
            for sheet_name in excel_file.sheet_names:
                if sheet_name != 'Summary':
                    sheet_df = excel_file.parse(sheet_name)
                    for plot_name, plot in visualize_features(sheet_df).items():
                        zip_file.writestr(f"{sheet_name}_{plot_name.lower()}_plot.png", plot.to_image(format="png", width=800, height=600, scale=2))

    return zip_buffer.getvalue()

def change_project_name(df,old,new):
    now = datetime.now()
    timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
    df['Summary'].loc[df['Summary']["Project Name"] == old, 'Timestamp'] = timestamp
    df['Summary'].loc[df['Summary']["Project Name"] == old, 'Project Name'] = new # Changed name in Summary sheet
    df[new] = df.pop(old) # renamed the old sheet with new sheet name
    return df
