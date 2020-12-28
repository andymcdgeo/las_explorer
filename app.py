import streamlit as st
from load_css import local_css
import lasio

local_css("style.css")

def load_data(uploadedfile):
    if uploadedfile:
        # uploaded_file = lasio.read(las_file_object)
        
        string = uploadedfile.read().decode()
        number = len(string)
        # st.write(string)

        las_file = lasio.read(string)
        #st.write(las_file.well.WELL.value)

        return las_file
    


st.title('LAS Data Explorer')
st.write('## Welcome to the LAS Data Explorer')
st.write('''LAS Data Explorer is a tool designed in Streamlit to help you view and gain an understanding of the contents of
a LAS file''')
st.write('To begin using the app, load your LAS file using the file upload option below.')

uploadedfile = st.file_uploader(' ', type=['las'])
las_file = load_data(uploadedfile)

if las_file:
    load_success_text = "<div class='load_successful_text'>File Uploaded Successfully!</div>"
    st.write(load_success_text, unsafe_allow_html=True)
    st.write(f'<b>LAS Version:</b> {las_file.version.VERS.value}', unsafe_allow_html=True)
    st.write(f'Well Name: {las_file.well.WELL.value}')
    #st.write(f'API: {las_file.well.API.value}')
    # st.write(f'Field Name: {las_file.well.FIELD.value}')

# Sidebar Options
st.sidebar.write('# LAS Data Explorer')

select_tool = st.sidebar.radio('Make a selection below', ('File Upload', 'LAS Header', 'Curve Details', 'Raw Data', 'Data Visualisation', ' Data Coverage'))


        