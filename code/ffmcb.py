### ffmcb.py is a prototype fact factory implementation, meant to help provide an
#       example for a future, inherited fact factory implementation that would apply to
#       any ecoforecast. Not just MCB for MLRF1

__author__= "Madison.Soden" 
__date__= "Tue Jul 24, 2018  11:53AM"
__license__= "NA?"
__email__= "madison.soden@gmail.com"
__status__= "Production"

import pyknow as pk
import pandas as pd
import json
import csv
import rangedict as rdi
import os.path
import numpy as np
import datetime
import os

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



def factfactory( filen= 'mlrf1h2017', stationn= 'mlrf1'):
    #TO READ JSON string file
    if os.path.exists('../data/mlrf1_insitu_data/'+filen+".json"):
        jsonstring= open('../data/mlrf1_insitu_data/'+filen+".json", 'r').read()
        df= pd.read_json(jsonstring, orient='split')
        factorySort( df, filen, stationn)
    else: 
        assert MyException(' '+filen+' data input file does not exist')
        return

def factorySort( df, filen, stationn):
    factlist= df.columns.values
    for datatype in factlist:
        if data2fact(datatype) != 'NA':
            factory( df[datatype], datatype, filen, stationn)

def factory( datadf, datatype, filen, stationn):
    #if there is no specific range list for [locus][facttype] exit factory function
    if not rdi.ranges[stationn][data2fact(datatype)]:
        assert MyException( 'datatype locus combination: '\
            +datatype+'/'+stationn+' does not have specified range file.\
            Cannot factize.')
        return

    #else continue to factize datadf
    first= datadf.index.values[0]
    first= pd.Timestamp(first)
    first= pd.to_datetime(first)
    first= first.strftime('%m_%d_%y')
    currdate= first
    factlist= []

    for index in datadf.index.values:
        indexloc= datadf.index.get_loc(index)
        i=pd.Timestamp(index)
        i=pd.to_datetime(i)
        intensity= datadf.iat[ indexloc]
        if (i.strftime('%m_%d_%y')==currdate):
            if not np.isnan( intensity):
                factlist.append( data2function(datatype)( intensity, i, stationn))
        else:
            #save and export facts using datatype
            factoryStore( factlist, data2fact(datatype), filen, currdate)
            currdate= i.strftime('%m_%d_%y')
            factlist= []
            if not np.isnan( intensity):
                factlist.append( data2function(datatype)(intensity, i, stationn))

def factoryStore( factlist, factname, filen, date):
    if not os.path.exists(os.path.dirname('../data/fffacts/'+filen+'/'+date+'/'+factname+'.json')):
        os.makedirs(os.path.dirname('../data/fffacts/'+filen+'/'+date+'/'+factname+'.json'))
    with open('../data/fffacts/'+filen+'/'+date+'/'+factname+'.json', 'w') as fout:
        json.dump( factlist, fout)

def fuzzyTod( t):
    #round to nearest hour
    t= t.hour +t.minute//30
    xcoor= rdi.times['mlrf1'][0]
    ycoor= range(len( xcoor))
    y= np.floor( np.interp( t, xcoor, ycoor))
    fuzzyT=rdi.standardtime[ int(y)]
    return fuzzyT

def fuzzyI( intensity, stationn, factn): 
    xcoor= rdi.ranges[ stationn][ factn][0]
    ycoor= range(len( xcoor))
    y= np.floor( np.interp( intensity, xcoor, ycoor, left=-99, right= 99))
    y= int( y)
    if(y== -99):
        return 'ulow'
    elif(y== 99):
        return 'uhigh'
    else: 
        return rdi.ranges[ stationn][ factn][ 1][ y]

def winddirGen( intensity, dt, stationn):
    ##calculating fuzzyI 
    fI= fuzzyI( intensity, stationn, 'winddir')
    ## calculating fuzzyTod
    fTod= fuzzyTod( dt.time())
    return winddir(fuzzyI=fI, fuzzyTod= fTod, date= dt.strftime('%m/%d/%Y'), locus= stationn)

def windspGen( intensity, dt, stationn):
    ##calculating fuzzyI
    fI= fuzzyI( intensity, stationn, 'windsp')
    ## calculating fuzzyTod
    fTod= fuzzyTod( dt.time())
    return windsp(fuzzyI=fI, fuzzyTod= fTod, date= dt.strftime('%m/%d/%Y'), locus= stationn)

def windguGen( intensity, dt, stationn):
    ##calculating fuzzyI
    fI= fuzzyI( intensity, stationn, 'windgu')
    ## calculating fuzzyTod
    fTod= fuzzyTod( dt.time())
    return windgu(fuzzyI=fI, fuzzyTod= fTod, date= dt.strftime('%m/%d/%Y'), locus= stationn)

def baromGen( intensity, dt, stationn):
    ##calculating fuzzyI
    fI= fuzzyI( intensity, stationn, 'barom')
    ## calculating fuzzyTod
    fTod= fuzzyTod( dt.time())
    return barom(fuzzyI=fI, fuzzyTod= fTod, date= dt.strftime('%m/%d/%Y'), locus= stationn)

def airtGen( intensity, dt, stationn):
    ##calculating fuzzyI
    fI= fuzzyI( intensity, stationn, 'airt')
    ## calculating fuzzyTod
    fTod= fuzzyTod( dt.time())
    return airt(fuzzyI=fI, fuzzyTod= fTod, date= dt.strftime('%m/%d/%Y'), locus= stationn)

def seandbcGen( intensity, dt, stationn):
    ##calculating fuzzyI
    fI= fuzzyI( intensity, stationn, 'seandbc')
    ## calculating fuzzyTod
    fTod= fuzzyTod( dt.time())
    return seandbc(fuzzyI=fI, fuzzyTod= fTod, date= dt.strftime('%m/%d/%Y'), locus= stationn)
