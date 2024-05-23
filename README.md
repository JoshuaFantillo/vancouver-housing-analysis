# Vancouver Housing Market Analysis Tool

## Overview
This project develops an advanced analytical tool that leverages machine learning to predict housing and property values, and an interactive tool for visualizing these predictions in the Greater Vancouver area. The project is designed to aid a wide range of stakeholders, from residents and potential homebuyers to policymakers and businesses, by providing accessible insights into housing market trends and future price predictions.

### Motivation
The motivation behind this project stems from the significant impact housing has on various aspects of life, including employment opportunities, social connections, and overall quality of life. Vancouver, known for its high rents and property prices relative to income, presents a unique challenge and opportunity for detailed housing market analysis. This project aims to demystify the complexities of the housing market and provide clear, actionable insights.

### Methodology
The project follows a comprehensive data science pipeline that includes the following stages:

### Data Collection
Data is sourced from multiple municipal open data portals, including those for Vancouver, Surrey, and Langley. Additional data such as bus stop locations and demographic information is sourced from various other platforms.

### Datasets Utilized
- Vancouver Data, Vancouver Open Data Portal, https://opendata.vancouver.ca/pages/home/ 
- Surrey Data, City of Surrey, https://data.surrey.ca
- Rental Data, Zillow Inc, https://www.zillow.com/homes/Vancouver,-BC_rb/
- Bus Stop Locations, Abacus Library UBC, https://abacus.library.ubc.ca/file.xhtml?persistentId=hdl:11272.1/AB2/LMLPT1/IRPWHQ&version=2.0
- Postal Code Conversion, Service Objects, https://www.serviceobjects.com/blog/free-zip-code-and-postal-code-database-with-geocoordinates/
- Langley Addresses, Langley Open Data Portal, https://data-langleycity.opendata.arcgis.com/datasets/80dcd2c96b7f4fd8b80546494230fdf4_182/explore?location=49.099919%2C-122.654029%2C13.82  
- Migration Data, BC Statistics, https://catalogue.data.gov.bc.ca/dataset/inter-provincial-and-international-migration  
- Immgration Data, BC Statistics, https://catalogue.data.gov.bc.ca/dataset/inter-provincial-and-international-migration/resource/c99d63f6-5ec4-4ac0-9c07-c0352f2f1928  

### Data Cleaning and Processing
The data undergoes detailed cleaning processes which involve reformatting, normalization, and aggregation to ensure consistency and usability across different data sets.

### Machine Learning Model
A Random Forest regression model is employed to predict future property values based on historical data. The model uses a variety of features including previous years' property values and other relevant metrics.

### Interactive Tool Development
The interactive tool is developed using Flask, allowing users to explore data through a dynamic map interface. The tool enables users to visualize property values across different regions and predict future trends based on the machine learning model's output.

## TESTING INSTRUCTIONS

#### Testing the Machine Learning Model:
The code for the machine learning model is packaged in a file titled "ML_HOUSING_MODEL.ipynb" in the "ML model folder" of the "Code" section.   

A basic test can be done simply by running all of the code cells in the notebook in order, but please not that this will require retraining the model, which may take a few minutes depending on your system specs and current model parameter values. More detailed testing can be done by altering the LOOKBACK_YEARS and TRAINING_YEARS parameters in the model itself. These values are in a cell of their own with documentation discussing allowable values and what affects they'll have on the model, but in short, a higher number for LOOKBACK_YEARS will cause the model to add more previous years of property value data (both land value and improvement value) in each feature vector, while adding valid years to TRAINING_YEARS causes the model to create feature vectors to train on from a larger number of years out of our whole table. Using a large value for LOOKBACK_YEARS and/or a large number of TRAINING_YEARS will significanty increase the time the model takes to train, so it's suggested that you start small.  

For each training run, the notebook is set to automatically print out the feature importances of all the features used in the model. With this in mind, one special case worth testing specifically is when LOOKBACK_YEARS is set to 0. This means the model won't be predicting based on property values at all.
This understandably reduces the accuracy, but it allows us to see which other features most influential: when property values are included they are (somewhat obviously) the dominant features, since past price is a great predictor of future price.  

The last cell in the model is where the model is used to make predictions for the future. You can change future_prediction_year to any year later than 2024 to get predictions for that year. To examine the results, uncomment one of the last three lines: one shows the property value predictions only, one shows the updated values of the input dataframe (potentially including predictions for more-recent future years, depending on parameter values) and one shows the two of them combined.  

#### Getting Started With The Interactive Tool
To use this tool, you will need to set up a local environment with the required dependencies in 'Interactive Tool/scripts/run-map.py'.  

Once dependencies are setup navigate to the 'Interactive Tool' folder and run 'python3 scripts/run-map.py'  

Once running you can access on your local host on port 5000 in your web browser.  


### Acknowledgements
We acknowledge the support from the municipal data providers and all contributors who have helped in data collection, cleaning, and tool development.

### Project Video 
- https://www.youtube.com/watch?v=KLs9jWV99I8

### Project Report
You can find the detailed report in this [PDF file](Analyzing%20Housing%20Affordability%20in%20Metro%20Vancouver.pdf).

### Contact
For any inquiries or further information, please contact us at  
[gunnar_miller@sfu.ca](mailto:gunnar_miller@sfu.ca)  
[joshua_fantillo@sfu.ca](mailto:joshua_fantillo@sfu.ca)  
[houli_huang@sfu.ca](mailto:houli_huang@sfu.ca)  
[zha92@sfu.ca](mailto:zha92@sfu.ca)  
[tayaba_abbasi@sfu.ca](mailto:tayaba_abbasi@sfu.ca)  

