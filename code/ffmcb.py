### ffmcb.py is a prototype fact factory implementation, meant to help provide an
#       example for a future, inherited fact factory implementation that would apply to
#       any ecoforecast. Not just MCB for MLRF1

##Last modified: Tue Jul 17, 2018  04:04PM
__author__ = "Madison.Soden" 
__license__ = "NA?"
__version__ = "mcb"
__email__ = "madison.soden@gmail.com"
__status__ = "Production"

import pyknow as pk
import pandas as pd
import json
import csv
import rangedict as rdi
import os.path

filename= 'mlrf1h2017'

def data2function( index):
    dataDict= {
            'WDIR': winddirGen,
            'WSPD': windspGen,
            'GST': windguGen,
            'WVHT': 'NA',
            'DPD': 'NA',
            'APD': 'NA',
            'MWD': 'NA',
            'PRES': baromGen,
            'ATMP': airtGen,
            'WTMP': seandbcGen,
            'DEWP': 'NA',
            'VIS': 'NA', 
            'TIDE': 'NA',
            'ATMPM': 'NA',
            'WTMPM': 'NA'}
    return dataDict. get( index, 'unregistered data time series')

def data2fact( index):
    dataDict= { 
            'WDIR': 'winddir',
            'WSPD': 'windsp',
            'GST': 'windgu',
            'WVHT': 'NA',
            'DPD': 'NA',
            'APD': 'NA',
            'MWD': 'NA',
            'PRES': 'barom',
            'ATMP': 'airt',
            'WTMP': 'seandbc',
            'DEWP': 'NA',
            'VIS': 'NA', 
            'TIDE': 'NA',
            'ATMPM': 'NA',
            'WTMPM': 'NA'}
    return dataDict. get( index, 'unregistered data time series')

class MyException(Exception):
    pass

class winddir(pk.Fact):
    #wind direction
    pass

class windsp(pk.Fact):
    #wind speed
    pass

class windgu(pk.Fact):
    #wind gust
    pass

class barom(pk.Fact):
    #barometric pressure
    pass

class airt(pk.Fact):
    #air temperature
    pass

class seandbc(pk.Fact):
    #sea temperature measured by ndbc
    pass



def factfactory( filen= filename):
    #TO READ JSON string file
    if os.path.exists(file_path):
        jsonstring= open('../data/mlrf1_insitu_data/'+filename +".json", 'r').read()
        df= pd.read_json(jsonstring, orient='split')
        factorySort( df)
    else: 
        assert MyException(' '+filen+' data input file does not exist')
        return

def factorySort( df):
    factlist= df.columns.values
    for datatype in factlist:
        if dataDict(datatype) != 'NA':
            factory( df[datatype], datatype)

def factory( datadf, datatype):
    #if there is no specific range list for [locus][facttype] exit factory function
    if not ranges[filename[:5]][dataDict[datatype]]:
        assert MyException( 'datatype locus combination: '\
            +datatype+'/'+filename+' does not have specified range file.\
            Cannot factize.')
        return

    #else continue to factize datadf
    factlist= []
    for index in datadf.index.values:
        factlist.append( data2function[datatype](datadf.iat[index, 0], index))
    
    #save/export facts using datatype 
    factoryStore( factlist, data2fact(datatype))

def factoryStore( factlist, factname):
    with open('../data/fffacts/'+filename+'/'+factname+'.json', 'w') as fout:
        json.dump( factlist, fout)


def winddirGen( intensity, dt):
    
    return winddir(fuzzyI=fI, fuzzyTod= fTod, date= dt.date(), locus= filename[:5])

def windspGen( intensity, dt):
    
    return windsp(fuzzyI=fI, fuzzyTod= fTod, date= dt.date(), locus= filename[:5])

def windguGen( intensity, dt):
    
    return windgu(fuzzyI=fI, fuzzyTod= fTod, date= dt.date(), locus= filename[:5])

def baromGen( intensity, dt):
    
    return barom(fuzzyI=fI, fuzzyTod= fTod, date= dt.date(), locus= filename[:5])

def airtGen( intensity, dt):
    
    return airt(fuzzyI=fI, fuzzyTod= fTod, date= dt.date(), locus= filename[:5])

def seandbcGen( intensity, dt):
    
    return seandbc(fuzzyI=fI, fuzzyTod= fTod, date= dt.date(), locus= filename[:5])
