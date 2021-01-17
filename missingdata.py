import missingno as mno
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

# Plotly imports
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import plotly.figure_factory as ff
import plotly.express as px


def missing(las_file, well_data):
    st.title('LAS File Missing Data')
    
    if not las_file:
        st.warning('No file has been uploaded')
    
    else:
        st.write("""The following plot can be used to identify the depth range of each of the logging curves.
         To zoom in, click and drag on one of the tracks with the left mouse button. 
         To zoom back out double click on the plot.""")

        data_nan = well_data.notnull().astype('int')
        # Need to setup an empty list for len check to work
        curves = []
        columns = list(well_data.columns)
        columns.pop(-1) #pop off depth

        col1_md, col2_md= st.beta_columns(2)

        selection = col1_md.radio('Select all data or custom selection', ('All Data', 'Custom Selection'))
        fill_color_md = col2_md.color_picker('Select Fill Colour', '#9D0000')
        # top_depth = col3_md.number_input('Top Depth', step=50.0, value=min_depth, min_value=min_depth, max_value=max_depth)
        # bottom_depth = col4_md.number_input('Bottom Depth', step=50.0, value=max_depth, min_value=min_depth, max_value=max_depth)

        if selection == 'All Data':
            curves = columns
        else:
            curves = st.multiselect('Select Curves To Plot', columns)

        if len(curves) <= 1:
            st.warning('Please select at least 2 curves.')
        else:
            curve_index = 1
            fig = make_subplots(rows=1, cols= len(curves), subplot_titles=curves, shared_yaxes=True, horizontal_spacing=0.02)

            for curve in curves:
                fig.add_trace(go.Scatter(x=data_nan[curve], y=well_data['DEPTH'], 
                    fill='tozerox',line=dict(width=0), fillcolor=fill_color_md), row=1, col=curve_index)
                fig.update_xaxes(range=[0, 1], visible=False)
                fig.update_xaxes(range=[0, 1], visible=False)
                curve_index+=1
            
            fig.update_layout(height=1000, showlegend=False, yaxis={'title':'DEPTH','autorange':'reversed'})
            # rotate all the subtitles of 90 degrees
            for annotation in fig['layout']['annotations']: 
                    annotation['textangle']=-90
            fig.layout.template='seaborn'
            st.plotly_chart(fig, use_container_width=True)