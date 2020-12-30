import streamlit as st
st.set_page_config(layout="wide")

from load_css import local_css
import lasio
import missingno as mno
from multiapp import MultiApp
import pandas as pd
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import plotly.figure_factory as ff

import plotly.express as px

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
    st.title('LAS File Data Info')
    if not las_file:
        st.warning('No file has been uploaded')
    else:
        st.write('**Curve Information**')
        for count, curve in enumerate(las_file.curves):
            # st.write(f"<b>Curve:</b> {curve.mnemonic}, <b>Units: </b>{curve.unit}, <b>Description:</b> {curve.descr}", unsafe_allow_html=True)
            st.write(f"   {curve.mnemonic} ({curve.unit}): {curve.descr}", unsafe_allow_html=True)
        st.write(f"<b>There are a total of: {count+1} curves present within this file</b>", unsafe_allow_html=True)
        
        st.write('<b>Curve Statistics</b>', unsafe_allow_html=True)
        st.write(well_data.describe())
        st.write('<b>Raw Data Values</b>', unsafe_allow_html=True)
        st.dataframe(data=well_data)
            
def plot():
    st.title('LAS File Visualisation')
    st.write('Expand one of the following to visualise your well data.')
    columns = list(well_data.columns)

    #Log plot section
    with st.beta_expander('Log Plot'):    
        curves = st.multiselect('Select Curves To Plot', columns)
        if len(curves) <= 1:
            st.warning('Please select at least 2 curves.')
        else:
            curve_index = 1
            fig = make_subplots(rows=1, cols= len(curves), subplot_titles=curves, shared_yaxes=True)

            for curve in curves:
                fig.add_trace(go.Scatter(x=well_data[curve], y=well_data['DEPTH']), row=1, col=curve_index)
                curve_index+=1
            
            fig.update_layout(height=1000, showlegend=False, yaxis={'title':'DEPTH','autorange':'reversed'})
            fig.layout.template='seaborn'
            st.plotly_chart(fig, use_container_width=True)

    #Histogram Section
    with st.beta_expander('Histograms'):
        col1_h, col2_h = st.beta_columns(2)
        col1_h.write('Options')

        hist_curve = col1_h.selectbox('Select a Curve', columns)
        log_option = col1_h.radio('Select Linear or Logarithmic Scale', ('Linear', 'Logarithmic'))
        
        if log_option == 'Linear':
            log_bool = False
        elif log_option == 'Logarithmic':
            log_bool = True
        
        histogram = px.histogram(well_data, x=hist_curve, log_x=log_bool)
        histogram.layout.template='seaborn'
        col2_h.plotly_chart(histogram, use_container_width=True)

    #Crossplot Section
    with st.beta_expander('Crossplot'):
        col1, col2 = st.beta_columns(2)
        col1.write('Options')

        xplot_x = col1.selectbox('X-Axis', columns)
        xplot_y = col1.selectbox('Y-Axis', columns)
        xplot_col = col1.selectbox('Color By', columns)
        xplot_x_log = col1.radio('X Axis - Linear or Logarithmic', ('Linear', 'Logarithmic'))
        xplot_y_log = col1.radio('Y Axis - Linear or Logarithmic', ('Linear', 'Logarithmic'))

        if xplot_x_log == 'Linear':
            xplot_x_bool = False
        elif xplot_x_log == 'Logarithmic':
            xplot_x_bool = True
        
        if xplot_y_log == 'Linear':
            xplot_y_bool = False
        elif xplot_y_log == 'Logarithmic':
            xplot_y_bool = True

        col2.write('Crossplot')

        xplot = px.scatter(well_data, x=xplot_x, y=xplot_y, color=xplot_col, log_x=xplot_x_bool, log_y=xplot_y_bool)
        xplot.layout.template='seaborn'
        col2.plotly_chart(xplot, use_container_width=True)

        # st.write('plot')

def missing_data():
    st.title('Missing Data')
    missing_data = well_data.copy()


    missing = px.area(well_data, x='DEPTH', y='DT')
    st.plotly_chart(missing)

# Sidebar Options
las_file=None
st.sidebar.write('# LAS Data Explorer')
st.sidebar.write('To begin using the app, load your LAS file using the file upload option below.')

uploadedfile = st.sidebar.file_uploader(' ', type=['las'])
las_file = load_data(uploadedfile)

if las_file:
    st.sidebar.success('File Uploaded Successfully')
    st.sidebar.write(f'<b>Well Name</b>: {las_file.well.WELL.value}',unsafe_allow_html=True)

    # Create the dataframe
    well_data = las_file.df()

    #Assign the dataframe index to a curve
    well_data['DEPTH'] = well_data.index

#Use the Multi App to create menu
app = MultiApp()
st.sidebar.write('**Navigation**')
app.add_app('Home', home)
app.add_app('Header Info', header)
app.add_app('Data Information', raw_data)
app.add_app('Data Visualisation', plot)
app.add_app('Data Coverage', missing_data)

app.run()
