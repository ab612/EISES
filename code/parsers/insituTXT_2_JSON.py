### insituTXT_to_JSON converts a data stream txt file (for a year of mlrf1) to A standardized JSON file format for
### fact factories to process

__author__="Madison.Soden"
__date__="Wed Jun 27 11:32:41 2018"
__license__="NA?"
__version__="insituTXT_to_JSON"
__email__="madison.soden@gmail.com"
__status__="Production"

import pandas as pd
import json
import datetime
import numpy as np

filename = "mlrf1h2017"

###########################################################
# 1.PARSING txt file 
###########################################################

with open('../../data/mlrf1_insitu_data/'+ filename+'.txt', 'r') as fin:
    data = fin.read().splitlines(True)
header= data[0]
units= data[1]
data=data[2:]

##Parsing units and header
header= header[1:-1]
headerp= header.split(' ')
headerp= list(filter(None, headerp))

units= units[1:-1]
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
    currdatetime= datetime.datetime(df.iat[index, df.columns.get_loc('YY')],
                                    df.iat[index, df.columns.get_loc('MM')],
                                    df.iat[index, df.columns.get_loc('DD')],
                                    df.iat[index, df.columns.get_loc('hh')],
                                    df.iat[index, df.columns.get_loc('mm')],
                                    0)
    df.at[index, 'datetime']= currdatetime

#setting dummy value for units row
df.at[0, 'datetime']= datetime.datetime(1111, 1, 1, 1, 1, 1)

#debug
#print(df[['YY', 'MM', 'DD', 'hh', 'mm', 'datetime']])

#re indexing df by datetime
df.index= df['datetime']
del df['datetime']
print(df)

#################################################################
# 3. PUTTING DATA FRAME INTO JSON FILE
#################################################################

##Creating json file
jsondf=df.to_json(orient='split')
with open('../../data/mlrf1_insitu_data/'+filename+'.json', 'w') as f:
    f.write(jsondf)

#TO READ JSON string file
#>>import pandas as pd
#>>import json
#>>jsonstring = open("filename.json", 'r').read()
#>>df= pd.read_json(jsonstring, orient='split')
