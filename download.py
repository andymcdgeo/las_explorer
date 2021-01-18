import streamlit as st
import pandas as pd
import lasio

import os
import base64

from load_css import local_css
local_css("style.css")

def get_binary_file_downloader_html(bin_file, file_label='File'):
    with open(bin_file, 'rb') as f:
        data = f.read()
    bin_str = base64.b64encode(data).decode()
    href = f'<a href="data:application/octet-stream;base64,{bin_str}" download="{os.path.basename(bin_file)}"><button type="button" class="button">Download {file_label}</button></a>'
    return href

def download(las_file, df):
    st.title('Download Your Data')
    if not las_file:
        st.warning('No file has been uploaded')
    else:
        def_filename = las_file.well.WELL.value
        col1dl, col2dl, col3dl = st.beta_columns(3)
        fileformat = col1dl.radio('Select File Format to Download', ['LAS', 'CSV', 'PICKLE', 'JSON'])
        
        if fileformat == 'LAS':
            las_file.set_data(df)
            laswrap = col2dl.radio('Wrapped or Unwrapped?', ['Wrapped', 'Unwrapped'])

            if laswrap == 'Wrapped':
                las_file.version.WRAP = 'YES'
            else:
                las_file.version.WRAP = 'NO'
            
            fname = col3dl.text_input('Enter LAS File Name', def_filename)
            las_file.write(f'{fname}.las', version=2)

            col3dl.markdown(get_binary_file_downloader_html(f'{fname}.las', 'LAS File'), unsafe_allow_html=True)

        if fileformat == 'CSV':
            las_file.set_data(df)
            csv_delimiter = col2dl.radio('Select delimiter', ['Comma', 'Tab'])

            if csv_delimiter == 'Comma':
                separator = ','
            else:
                separator = '\t'

            fname = col3dl.text_input('Enter CSV File Name', def_filename)
            df.to_csv(f'{fname}.csv', sep = separator)

            col3dl.markdown(get_binary_file_downloader_html(f'{fname}.csv', 'CSV File'), unsafe_allow_html=True)

        if fileformat == 'PICKLE':
            fname = col3dl.text_input('Enter Pickle File Name', def_filename)
            df.to_pickle(f'{fname}.pkl')

            col3dl.markdown(get_binary_file_downloader_html(f'{fname}.pkl', 'Pickle File'), unsafe_allow_html=True)

        if fileformat == 'JSON':
            fname = col3dl.text_input('Enter JSON File Name', def_filename)
            df.to_pickle(f'{fname}.json')

            col3dl.markdown(get_binary_file_downloader_html(f'{fname}.json', 'JSON File'), unsafe_allow_html=True)