import pygrib
import numpy as np
import glob

import pandas as pd
import xlrd

predictors = []

# *********** Loop for the day-0 GEFS forecast *************

directory = '../data/gefs/day-0/'

# Loop through forecast times
for ftime in range(12, 396, 24):

    meanList = []

    # Loop through individual perturbation files
    for filename in glob.glob(f'{directory}*-{ftime}.grb'):

        # Try to open the file and get a mean of its temperature values
        try:
            grbs = pygrib.open(filename)

            # Append the calculated mean of the file to a list
            meanList.append(np.mean(grbs.select(name='Temperature')[0].values))
        except:
            print("{filename} does not exist!")

    # After we have looped through all files for a particular time, calculate mean & append
    fTimeMean = np.mean(meanList)
    predictors.append(fTimeMean)

# ********** Collect data from the prior days ***********

meanList = []

# Loop through the directories containing the prior days we care about
for time in range(1, 6):

    # Loop through the perturbations
    for i in range(1, 21):
        try:
            grbs = pygrib.open(f'../data/gefs/day-{time}/{i}-12.grb')
            meanList.append(np.mean(grbs.select(name='Temperature')[0].values))
            # print(i)
        except:
            print(f"Perturbation {i} may not exist!")

    fTimeMean = np.mean(meanList)
    predictors.append(fTimeMean)

######################
#### Time for gas ####
######################

# Read Gas Prices

gasPrices = pd.read_excel('../data/natgas/dailyprices.xls',sheet_name='Data 1')
gasPrices = gasPrices.drop([0,1]).rename(columns={'Back to Contents':'Date',
                                                  'Data 1: Henry Hub Natural Gas Spot Price (Dollars per Million Btu)':
                                                      'Price'})
gasPrices['Price'] = gasPrices['Price'].astype(float)

# Save gas price history to csv for use with plotting
gasPrices.to_csv('../data/natgas/formattedprices.csv',index=False)

# Get last three entries and append to predictors

lastThree = gasPrices.tail(3)

for i in [2,1,0]:
    print(lastThree['Price'].values[i])
    predictors.append(lastThree['Price'].values[i])

# Calculate and append most recent trends

oneDayTrend = lastThree['Price'].values[2] - lastThree['Price'].values[1]
twoDayTrend = lastThree['Price'].values[2] - lastThree['Price'].values[0]

predictors.append(oneDayTrend)
predictors.append(twoDayTrend)


# Add Gas Storage info

gasStorage = pd.read_excel('../data/natgas/storage.xls',sheet_name='Data 1')
gasStorage = gasStorage.drop([0,1]).drop(['Unnamed: 2','Unnamed: 3','Unnamed: 4','Unnamed: 5','Unnamed: 6','Unnamed: 7',
                                          'Unnamed: 8'],axis=1).rename(columns={'Back to Contents':'Date'})
gasStorage = gasStorage.rename(columns = {'Data 1: Weekly Working Gas in Underground Storage': 'gasStorage'})

predictors.append(gasStorage.tail()['gasStorage'].values[-1])
predictors.append(gasStorage.tail()['gasStorage'].values[-2])


###############################

######## Predictions ##########

from joblib import load

# Import standard scaler object

scaler = load('scaler.bin')

# Reshape predictors list for scaling and then scale

fmatPred = np.asarray(predictors).reshape(1,-1)
scaledVals = scaler.transform(fmatPred)

# Load our xgBoost ls model

model = load('gb_mid50_8jan2019.joblib')

middlePred = model.predict(scaledVals)

# Load our xgBoost lower quantile model

model = load('gb_low25_8jan2019.joblib')

lowerPred = model.predict(scaledVals)

# Load our xgBoost upper quantile model

model = load('gb_up75_8jan2019.joblib')

upperPred = model.predict(scaledVals)


# Save our predictions to another csv

prediction = pd.DataFrame({'middle':middlePred,'upper':upperPred,'lower':lowerPred},index=[0])
prediction.to_csv('../data/prediction/prediction.csv',index=False)



