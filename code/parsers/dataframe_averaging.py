###pdsAveraging.py contains helper functions to calculate average values for
####time series of data stored in a pandas data frame
####usually called by insituTXT_2_JSON.py

__author__= "Madison.Soden"
__date__= "Tue Jul 24, 2018  04:25PM"
__license__= "NA?"
__email__= "madison.soden@gmail.com"
__status__= "Production"

import pandas as pd 
import json 
import datetime
import numpy as np


def cleanDataframe( df):
    df= df.reindex(pd.date_range( df.index[1], df.index[-1], freq='H'))
    return df

def append3Mean( coulmnname, df):
# every third column should be used to avoid overlapping means
    df[coulmnname +'M']= df.rolling(window=3, min_periods= 1)[coulmnname].mean()
    return df

def removeExtraDateTime( df):
    df= df.drop(columns=['YYYY', 'MM', 'DD', 'hh'])
    if('mm' in df.columns.values):
        df= df.drop(columns=['mm'])
    return df

def cuttimeseries( df):
    datetimes= df.index.tolist()

    for i in range(len(datetimes)):
        if datetimes[i].time() == datetime.time( 5, 0, 0):
            start = i
            break
    for i in reversed(range(len(datetimes))):
        if datetimes[i].time() == datetime.time( 5, 0, 0):
            end = i
            break
    df= df[start:(end)]
    return df


