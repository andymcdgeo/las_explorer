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

def editing(las_file, df):
    st.title('LAS File Header Info')
    if not las_file:
        st.warning('No file has been uploaded')
    else:
        output = df.to_csv('test.csv', sep=',', encoding='utf-8')

        # df['GAMN_avg'] = df['GR'].rolling(int(1 / las_file.well.STEP.value), center=True).mean()

        las_file.set_data(df)
        las_file.write('testingappendq.las', version=2)
        

        # las_file.write('testing.las', version=2.0)

        st.markdown(get_binary_file_downloader_html('test.csv', 'CSV File'), unsafe_allow_html=True)
        st.markdown(get_binary_file_downloader_html('testingappendq.las', 'LAS File'), unsafe_allow_html=True)

