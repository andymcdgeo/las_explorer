import streamlit as st

def home():
    pweb = """<a href='http://andymcdonald.scot' target="_blank">http://andymcdonald.scot</a>"""
    sm_li = """<a href='https://www.linkedin.com/in/andymcdonaldgeo/' target="_blank"><img src='https://cdn.exclaimer.com/Handbook%20Images/linkedin-icon_32x32.png'></a>"""
    sm_tw = """<a href='https://twitter.com/geoandymcd' target="_blank"><img src='https://cdn.exclaimer.com/Handbook%20Images/twitter-icon_32x32.png'></a>"""
    sm_med = """<a href='https://medium.com/@andymcdonaldgeo/' target="_blank"><img src='https://cdn.exclaimer.com/Handbook%20Images/Medium_32.png'></a>"""

    st.title('LAS Data Explorer - Version 0.2.0')
    st.write('## Welcome to the LAS Data Explorer')
    st.write('### Created by Andy McDonald')
    st.write('''LAS Data Explorer is a tool designed using Python and Streamlit to help you view and gain an understanding of the contents of
    a LAS file.''')
    st.write('To begin using the app, load your LAS file using the file upload option on the sidebar. Once you have done this, you can navigate to the relevant tools using the Navigation menu.')
    st.write('\n')
    st.write('## Sections')
    st.write('**Header Info:** Information from the LAS file header.')
    st.write('**Data Information:** Information about the curves contained within the LAS file, including names, statisics and raw data values.')
    st.write('**Data Visualisation:** Visualisation tools to view las file data on a log plot, crossplot and histogram.')
    st.write('**Missing Data Visualisation:** Visualisation tools understand data extent and identify areas of missing values.')
    st.write('## Get in Touch')
    st.write(f'\nIf you want to get in touch, you can find me on Social Media at the links below or visit my website at: {pweb}.', unsafe_allow_html=True)
    
    st.write(f'{sm_li}  {sm_med}  {sm_tw}', unsafe_allow_html=True)

    st.write('## Source Code, Bugs, Feature Requests')
    githublink = """<a href='https://github.com/andymcdgeo/las_explorer' target="_blank">https://github.com/andymcdgeo/las_explorer</a>"""
    st.write(f'\n\nCheck out the GitHub Repo at: {githublink}. If you find any bugs or have suggestions, please open a new issue and I will look into it.', unsafe_allow_html=True)