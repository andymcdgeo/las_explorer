# LAS Explorer
## Version 0.2.0

The LAS Data Explorer is a tool designed using Python and Streamlit to help you view and gain an understanding of the contents of a LAS file. Current functionality includes:
* Loading LAS files
* Viewing Header Information
* Viewing Curve Information (names, values and statistics)
* Visualising LAS data using an interactive log plot
* Visualising LAS data using an interactive crossplot (scatter plot) and histogram
* Display data coverage

A running version of the app can be accessed at at https://las-explorer.herokuapp.com. The app may run slowly when accessing it. This is due to the hosting and should not affect functionality.

## Notes on Usage
* The app can be cloned and run locally using streamlit: `streamlit run app.py`. When doing this, ensure you have the required modules listed in the requirements file.
* Scales on interactive plots can be changed by double clicking on the lower/upper limit values.

## Bugs, Enhancements and Comments
All comments, bug reports and enhancement requests are welcome. To do so, please submit a new issue and I will investigate it

## Future Functionality
Future functionality will likely include:
* Working with multiple LAS files
* Mapping of wells
