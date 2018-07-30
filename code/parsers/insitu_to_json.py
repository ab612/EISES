#!/usr/bin/env python3

### insituTXT_to_JSON converts a data stream txt file (for a year of mlrf1) to A standardized JSON file format for
#### fact factories to process

__author__= "Madison.Soden"
__date__= "Thu Jul 26, 2018  02:56PM"
__license__= "NA?"
__email__= "madison.soden@gmail.com"
__status__= "Production"

import pandas as pd
import json
import datetime
import numpy as np
from .dataframe_averaging import * 
from IPython import embed

def main(filename):
    ###########################################################
    # 1.PARSING txt file 
    ###########################################################

    with open('/Users/soden/AOMLworkspace/mcb/data/mlrf1_insitu_data/'+ filename+'.txt', 'r') as fin:
        data = fin.read().splitlines(True)
    header= data[0]
    units= data[1]
    data=data[2:]
    
    ##Parsing units and header
    header= header[:-1]
    headerp= header.split(' ')
    headerp= list(filter(None, headerp))
    #fix name discontinuity between years
    for i in range(len(headerp)):
        if(headerp[i]=='BAR'):
            headerp[i]= 'PRES'
        if(headerp[i]=='WD'):
            headerp[i]= 'WDIR'

    units= units[:-1]
    unitsp= units.split(' ')
    unitsp= list(filter(None, unitsp))

    ##initializing  data frame with header and units
    unitsp=[unitsp]
    df= pd.DataFrame(unitsp, columns=headerp)

    ##parsing the rest of data into properly formatted lists
    datal= len(data)
    i=0
    while (i < datal):
        datap= data[i]
        datap=datap[:-1]
        datap=datap.split(' ')
        datap= list(filter(None, datap))
        data[i]= datap
        i= i+1

    df1= pd.DataFrame(data, columns=headerp)
    df= df.append(df1)
    df = df.reset_index(drop=True)

    #################################################################
    # 2. CLEANING AND CONVERTING DATA FRAME
   #################################################################

    #converting all strings in data frame into ints of floats
    for column in list(df):
        df[column][1:]= pd.to_numeric(df[column][1:])

    #creating a datetime column
    df['datetime']= np.nan
    for index in list(df.index.values)[1:]:
        #translate 2 digit years into four digit years
        year= df.iat[index, 0]
        if(year< 60):
            year= year +2000
        elif(year< 100):
            year= year+1900
        #create datetime
        currdatetime= datetime.datetime(year, #column name = "YY"
                                        df.iat[index, 1], #column name = 'MM'
                                        df.iat[index, 2], #column name = 'DD'
                                        df.iat[index, 3], #column name = 'hh'
                                        0, #column name = 'mm'
                                        0)
        df.at[index, 'datetime']= currdatetime

    #setting dummy value for units row
    df.at[0, 'datetime']= datetime.datetime(1111, 1, 1, 1, 1, 1)


    #re indexing df by datetime
    df.index= df['datetime']
    del df['datetime']

    namedict= { 'YYYY': ['year', 'years', 1111],
                'MM': ['month', 'months', np.nan],
                'DD': ['day', 'days', np.nan],
                'hh': ['hour', 'hours', np.nan],
                'mm': [ 'minuet', 'minuets', np.nan],
                'WDIR': ['Wind Direction', 'degrees "T"', 999],
                'WSPD': ['Wind Speed', 'm/s', 99.0],
                'GST': ['Wind Gust', 'm/s', 99.0],
                'WVHT': ['Wave Height', 'm', 99.00],
                'DPD': ['Dominant Wave Period', 'sec', 99.00],
                'APD': ['Average Wave Period', 'sec', 99.00],
                'MWD': ['Mean wave Direction', 'degrees', 999],
                'PRES': ['Air Pressure', 'hPa', 9999.0],
                'ATMP': ['Air Temperature', 'degC', 999.0],
                'WTMP': ['Water Temperature', 'degC', 999.0],
                'DEWP': ['Dew Point', 'degC', 999.0],
                'VIS': ['Visibility', 'nmi', 99.0],
                'TIDE': ['Tide', 'ft', 99.00]}


    ##adding appropriate Nan values to replace dummy values in time series
    for column in range(len(headerp)):
        for index in list(df.index.values):
            if(df.iat[df.index.get_loc(index), column] ==
                    namedict[headerp[column]][2]):
                df.at[index, headerp[column]]= np.nan

    #create hourly time series with no gaps
    df = cleanDataframe( df)

    #slice data frame to begin an end on day intervals
    df= cuttimeseries( df)

    #drop extra datetime info columns now that information is stored in index
    df= removeExtraDateTime( df)

    #create 3 hour mean time series
    ##use every third column when accessing means
    df= append3Mean( 'ATMP', df)
    df= append3Mean('WTMP', df)


    #################################################################
    # 3. PUTTING DATA FRAME INTO JSON FILE
    #################################################################

    ##Creating json file
    jsondf= df.to_json(orient='split')
    with open('/Users/soden/AOMLworkspace/mcb/data/mlrf1_insitu_data/'+filename+'.json', 'w') as f:
        f.write(jsondf)

#TO READ JSON string file
#>>import pandas as pd
#>>import json
#>>jsonstring = open("filename.json", 'r').read()
#>>df= pd.read_json(jsonstring, orient='split')
