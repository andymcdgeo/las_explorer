import streamlit as st
from load_css import local_css
import lasio
from multiapp import MultiApp
import pandas as pd

local_css("style.css")

@st.cache
def load_data(uploadedfile):
    if uploadedfile:
        # uploaded_file = lasio.read(las_file_object)
        
        string = uploadedfile.read().decode()
        number = len(string)
        # st.write(string)

        las_file = lasio.read(string)

        return las_file


# Sidebar Options
las_file=None
st.sidebar.write('# LAS Data Explorer')
st.sidebar.write('To begin using the app, load your LAS file using the file upload option below.')

uploadedfile = st.sidebar.file_uploader(' ', type=['las'])
las_file = load_data(uploadedfile)

if las_file:
        st.sidebar.success('File Uploaded Successfully')
        st.sidebar.write(f'<b>Well Name</b>: {las_file.well.WELL.value}',unsafe_allow_html=True)

def home():
    st.title('LAS Data Explorer')
    st.write('## Welcome to the LAS Data Explorer')
    st.write('''LAS Data Explorer is a tool designed in Streamlit to help you view and gain an understanding of the contents of
    a LAS file''')
    st.write('To begin using the app, load your LAS file using the file upload option below.')


def header():
    st.title('LAS File Header Info')
    if not las_file:
        st.warning('No file has been uploaded')
    else:
        for item in las_file.well:
            st.write(f"<b>{item.descr.capitalize()} ({item.mnemonic}):</b> {item.value}", unsafe_allow_html=True)

def raw_data():
    for count, curve in enumerate(las_file.curves):
        st.write(f"<b>Curve:</b> {curve.mnemonic}, <b>Units: </b>{curve.unit}, <b>Description:</b> {curve.descr}", unsafe_allow_html=True)
    st.write(f"<b>There are a total of: {count+1} curves present within this file</b>", unsafe_allow_html=True)
    well_data = las_file.df()
    st.write('<b>Data Statistics</b>', unsafe_allow_html=True)
    st.write(well_data.describe())
    st.write('<b>Raw Data Values</b>', unsafe_allow_html=True)
    st.dataframe(data=well_data)
            

app = MultiApp()
app.add_app('Home', home)
app.add_app('Header Info', header)
app.add_app('Data Information', raw_data)
app.add_app('Data Visualisation', header)
app.add_app('Data Coverage', header)



app.run()
