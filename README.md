# Using Global Forecast System Ensemble Data to Predict Weekly NatGas Prices

#### Description
This repo contains various files that show the development and production of a model that predicts next week's natural gas spot price at the Henry Hub. 

### The Model
Gradient boosting quantile regression was selected after cross-validation analysis of several machine-learning techniques and their associated scores. For more information, see the following notebook: [Testing Regressors](https://github.com/jpicca/natGasPrediction/blob/master/testingRegressors.ipynb)

### Live Version
Sunday through Thursday, singleFHourGrib.sh downloads 850-mb temperatures from forecast-hour 12 of that day's 00Z run of the GEFS. On Friday, gribGrab.sh downloads 850-mb temperatures from all forecast hours of that day's 00Z run. Additionally, gribGrab.sh downloads the most recent daily price and weekly storage information from [EIA](www.eia.gov).
