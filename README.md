# Using Global Forecast System Ensemble Data to Predict Weekly NatGas Prices

### Description
This repo contains various files that show the development and production of a model that predicts next week's natural gas spot price at the Henry Hub. 

### The Model
Gradient boosting quantile regression was selected after cross-validation analysis of several machine-learning techniques and their associated scores. For more information, see the following notebook: [Testing Regressors](https://github.com/jpicca/natGasPrediction/blob/master/testingRegressors.ipynb)

### Live Version
Sunday through Thursday, singleFHourGrib.sh downloads 850-mb temperatures from forecast-hour 12 of that day's 00Z run of the GEFS. On Friday, gribGrab.sh downloads 850-mb temperatures from all forecast hours of that day's 00Z run. Additionally, gribGrab.sh downloads the most recent daily price and weekly storage information from [EIA](www.eia.gov).

Once all data are downloaded, outputData.py runs to process these data into suitable format to then feed them to our loaded regression models for prediction.

### Front End
Version 5 of d3js is utilized to visualize the historical data (over the last 90 days) and plot the forecast range for next week's values. See the live version here: [Natural Gas Price Prediction](http://untoldsky.com/natGasPrediction/)

![Front End Example](https://github.com/jpicca/natGasPrediction/blob/master/Screenshot%202020-02-19%2016.33.34.png)
