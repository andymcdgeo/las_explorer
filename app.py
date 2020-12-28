import streamlit as st
import lasio

st.title('LAS Data Explorer')
st.write('Welcome to the LAS Data Explorer.....')
st.write('To begin using the explorer load your LAS file on sidebar and choose the relevant option.')

# Sidebar Options
st.sidebar.write('# LAS Data Explorer')
st.sidebar.write('LAS Explorer is a tool designed to help you visualise the contents of your LAS file.')

st.sidebar.write('Select a LAS file.')
uploadedfile = st.sidebar.file_uploader(' ', type=['las'])

select_tool = st.sidebar.radio('Select an option', ('LAS Header', 'Curve Details', 'Plotting', ' Data Extent'))

if uploadedfile:
    # uploaded_file = lasio.read(las_file_object)
    
    string = uploadedfile.read().decode()
    number = len(string)
    # st.write(string)

    las_file = lasio.read(string)
    st.write(las_file.well.WELL.value)

    for item in las_file.well:
        st.write(item.descr)
        