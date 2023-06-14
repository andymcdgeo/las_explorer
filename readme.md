# LAS-Viewer (ex.LAS Explorer) 
## Version 0.2.1

The LAS Data Explorer is a tool designed using Python and Streamlit to help you view and gain an understanding of the contents of a LAS file. Current functionality includes:
* Loading LAS files
* Viewing Header Information
* Viewing Curve Information (names, values and statistics)
* Visualising LAS data using an interactive log plot
* Visualising LAS data using an interactive crossplot (scatter plot) and histogram
* Display data coverage

Instructions for Running:

* Installing the __Streamlit__ library in the Anaconda terminal: `pip install streamlit`
* Verifying the installation using the command `streamlit hello`. This opens a browser with the interface.
* Installing the necessary additional libraries:
  `lasio` for loading LAS files
  `missingno` used for identifying missing data
  `pandas` for working with dataframes
  `plotly` for displaying interactive plots


* The app can be cloned and run locally using streamlit: `streamlit run app.py`. When doing this, ensure you have the required modules listed in the requirements file.
* Scales on interactive plots can be changed by double clicking on the lower/upper limit values.

## Bugs, Enhancements and Comments
All comments, bug reports and enhancement requests are welcome. To do so, please submit a new issue and I will investigate it
