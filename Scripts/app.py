import streamlit as st
import pandas as pd
import numpy as np
import csvcomparetool
from csvcomparetool import CSVComparer
import json
from csv_diff import load_csv, compare
import warnings
warnings.filterwarnings("ignore")

st.set_page_config('CSV Compare', page_icon="🏛️", layout='wide')
def title(url):
    st.markdown(f'<p style="color:#2f0d86;font-size:22px;border-radius:2%;"><br><br><br>{url}</p>', unsafe_allow_html=True)
def title_main(url):
    st.markdown(f'<h1 style="color:#230c6e;font-size:42px;border-radius:2%;"><br>{url}</h1>', unsafe_allow_html=True)
def success_df(html_str):
    html_str = f"""
        <p style='background-color:#baffc9;
        color: #313131;
        font-size: 15px;
        border-radius:5px;
        padding-left: 12px;
        padding-top: 10px;
        padding-bottom: 12px;
        line-height: 18px;
        border-color: #03396c;
        text-align: left;'>
        {html_str}</style>
        <br></p>"""
    st.markdown(html_str, unsafe_allow_html=True)
title_main("CSV Compare")

import tempfile
from tempfile import NamedTemporaryFile
from pathlib import Path
uploaded_file_1 = st.file_uploader("Upload the original CSV file", type=["csv"])
if (uploaded_file_1 is not None) and (Path(uploaded_file_1.name).suffix != ".csv"):
      #suffix_1 = Path(uploaded_file_1.name).suffix
                st.write("Please upload a CSV file.")
uploaded_file_2 = st.file_uploader("Upload the changed CSV file", type=["csv"])
if uploaded_file_2 is not None and (Path(uploaded_file_2.name).suffix != ".csv"):
      #suffix_2 = Path(uploaded_file_1.name).suffix
                st.error("Please upload a CSV file.")

#import tempfile
import os
if uploaded_file_1 and uploaded_file_2:
    temp_dir = tempfile.mkdtemp()
    path_1 = os.path.join(temp_dir, uploaded_file_1.name)
    with open(path_1, "wb") as f:
                f.write(uploaded_file_1.getvalue())
    df_1 = pd.read_csv(uploaded_file_1)
    
    path_2 = os.path.join(temp_dir, uploaded_file_2.name)
    with open(path_2, "wb") as f:
                f.write(uploaded_file_2.getvalue())
    df_2 = pd.read_csv(uploaded_file_2)
    lst_columns = list(df_1.columns.values)
    #lst_columns_2 = list(df_2.columns.values)
    #lst_columns = list(set(lst_columns_1).intersection(lst_columns_2))
    key_column = st.multiselect('Select column to compare', lst_columns, placeholder='Choose 1', max_selections=2)
    if key_column:
            print(key_column)
            key_select=key_column[0]
            #df_1 = df_1[[lst_columns[0],key_column[0]]]
            #df_2 = df_2[[lst_columns[0],key_column[0]]]

    if st.button("Compare"):
        comparer = CSVComparer(df_1, df_2, key_column[0])
        #if not comparer.validate_paths() or not comparer.validate_columns():
            #st("CSV file paths invalid, or column identifier does not exist. Check file paths and columns, try again.")
        #else:
            #differences = comparer.find_differences()
        diff = compare(
            load_csv(open(path_1), key=key_column[0]),
            load_csv(open(path_2), key=key_column[0])
        )
    
        json_output = json.dumps(diff) # Convert the dictionary to a JSON string
        data = json.loads(json_output) # Load the JSON output into a Python dictionary

        changes = [] # Initialize an empty list to store the changes
        added_data = data['added']
        removed_data = data['removed']

        df_added = pd.DataFrame(added_data)
        df_removed = pd.DataFrame(removed_data)
    
        # Iterate over the 'changed' section of the JSON output
        for item in data['changed']:
            # Extract the key (name) and changes
            key = item['key']
            changes_dict = item['changes']
    
            # Iterate over the changes
            for field, values in changes_dict.items():
                # Extract the old and new values
                old_value = values[0]
                new_value = values[1]
        
                # Append the change to the list
                changes.append({
                    'Name': key,
                    'Field': field,
                    'Old Value': old_value,
                    'New Value': new_value
                })

        df_changes = pd.DataFrame(changes) # Convert the list of changes to a pandas DataFrame
        if len(df_changes) > 0:
            st.write("Changes:")
            st.dataframe(df_changes) # Print the DataFrame if there are any changes
        st.write("Changed Data:")
        st.dataframe(df_added)
        st.write("\nOriginal Data:")
        st.dataframe(df_removed)
        success_df("CSV files are successfully compared.")

footer_html = """
    <div class="footer">
    <style>
        .footer {
            position: fixed;
            bottom: 0;
            left: 0;
            right: 0;
            background-color: #f0f2f6;
            padding: 10px 20px;
            text-align: center;
        }
        .footer a {
            color: #4a4a4a;
            text-decoration: none;
        }
        .footer a:hover {
            color: #3d3d3d;
            text-decoration: underline;
        }
    </style>
        All rights reserved @2024. Cogent Holdings IT Solutions.      
    </div>
"""
st.markdown(footer_html,unsafe_allow_html=True)
#https://github.com/simonw/csv-diff
