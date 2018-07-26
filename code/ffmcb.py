### ffmcb.py is a prototype fact factory implementation, meant to help provide an
#       example for a future, inherited fact factory implementation that would apply to
#       any ecoforecast. Not just MCB for MLRF1

__author__= "Madison.Soden" 
__date__= "Thu Jul 26, 2018  02:35PM"
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
from IPython import embed

def data2function( index):
#dictionary function to return a call to fact type specific generating functions given a fact data frame abbreviation
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
    #return system fact type  name given a fact type data frame abbreviation
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

#initialize fact types to be created
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


def factfactory( filen, stationn):
    ##TO READ JSON string file
    #check that user requested filename exists inf file archive
    if os.path.exists('../data/mlrf1_insitu_data/'+filen+".json"):
        #read json file into a pandas data frame
        jsonstring= open('../data/mlrf1_insitu_data/'+filen+".json", 'r').read()
        df= pd.read_json(jsonstring, orient='split')
        embed();
        factorySort( df, filen, stationn)
    else: 
        #if requested file does not exist alert the user
        raise MyException(' '+filen+' data input file does not exist')
        return

def factorySort( df, filen, stationn):
#partition data frame into series containing one fact type and then begin fact creation/storage process for each fact type separately
    factlist= df.columns.values
    embed()
    for datatype in factlist:
        if data2fact(datatype) != 'NA':
            factory( df[datatype], datatype, filen, stationn)

def factory( datadf, datatype, filen, stationn):
    ##if there is no specific range list for [locus][facttype] exit factory function
    if not rdi.ranges[stationn][data2fact(datatype)]:
        #alert user of error
        assert MyException( 'datatype locus combination: '\
            +datatype+'/'+stationn+' does not have specified range file.\
            Cannot factize.')
        return

    ##else continue to factize datadf
    #find initial date for entire fact file and convert into string of form MM_DD_YYYY
    first= datadf.index.values[0]
    first= pd.Timestamp(first)
    first= pd.to_datetime(first)
    first= first.strftime('%m_%d_%y')
    currdate= first
    #initialize empty fact list
    factlist= []

    #iterate through all datetime indexes in series datadf
    for index in datadf.index.values:
        #get int representation of index location
        indexloc= datadf.index.get_loc(index)
        #convert index of type np.datetime to type datetime.datetime
        i=pd.Timestamp(index)
        i=pd.to_datetime(i)
        #get int representation of fact intensity corresponding to current index value
        intensity= datadf.iat[ indexloc]
        #check if current index belongs in previous current date file
        if (i.strftime('%m_%d_%y')==currdate):
            #if so check that fact intensity is recorded i.e not missing data
            if not np.isnan( intensity):
                #and then add to facttype list
                factlist.append( data2function(datatype)( intensity, i, stationn))
        else: #otherwise
            #save and export previous list of date specific facts using data type specific file names
            factoryStore( factlist, data2fact(datatype), filen, currdate)
            #then update current date
            currdate= i.strftime('%m_%d_%y')
            #and empty factlist
            factlist= []
            #check fact intensity is recorded i.e. not missing data
            if not np.isnan( intensity):
                #add to new facttype list
                factlist.append( data2function(datatype)(intensity, i, stationn))

def factoryStore( factlist, factname, filen, date):
    #create directory for corresponding date if one does not already exist
    if not os.path.exists(os.path.dirname('../data/fffacts/'+filen+'/'+date+'/'+factname+'.json')):
        os.makedirs(os.path.dirname('../data/fffacts/'+filen+'/'+date+'/'+factname+'.json'))
    #save list of specific date & fact type as json file
    with open('../data/fffacts/'+filen+'/'+date+'/'+factname+'.json', 'w') as fout:
        json.dump( factlist, fout)

def fuzzyTod( t):
    #round to nearest hour
    t= t.hour +t.minute//30
    #get lists of all fuzzy lower bounds(xcoor) and corresponding positions in list (ycoor) to use in interpolate function
    xcoor= rdi.times['mlrf1'][0]
    ycoor= range(len( xcoor))
    #predict position of time intensity relative to fuzzy lower bounds
    y= np.floor( np.interp( t, xcoor, ycoor))
    #look up corresponding fuzzyTod string value
    fuzzyTod=rdi.standardtime[ int(y)]
    return fuzzyTod

def fuzzyI( intensity, stationn, factn): 
    #get lists of all fuzzy lower bounds(xcoor) and corresponding positions in list (ycoor) to use in interpolate function
    xcoor= rdi.ranges[ stationn][ factn][0]
    ycoor= range(len( xcoor))
    #predict position of time intensity relative to fuzzy lower bounds
    y= np.floor( np.interp( intensity, xcoor, ycoor, left=-99, right= 99))
    y= int( y)
    #look up corresponding fuzzyI string value
    if(y== -99):
        return 'ulow'
    elif(y== 99):
        return 'uhigh'
    elif(y< 9): 
        return rdi.ranges[ stationn][ factn][ 1][ y]
    else:
        embed()

def winddirGen( intensity, dt, stationn):
#generate wind direction type fact
    ##calculating fuzzyI 
    fI= fuzzyI( intensity, stationn, 'winddir')
    ## calculating fuzzyTod
    fTod= fuzzyTod( dt.time())
    return winddir(fuzzyI=fI, fuzzyTod= fTod, date= dt.strftime('%m/%d/%Y'), locus= stationn)

def windspGen( intensity, dt, stationn):
    #generate wind speed type fact
    ##calculating fuzzyI
    fI= fuzzyI( intensity, stationn, 'windsp')
    ## calculating fuzzyTod
    fTod= fuzzyTod( dt.time())
    return windsp(fuzzyI=fI, fuzzyTod= fTod, date= dt.strftime('%m/%d/%Y'), locus= stationn)

def windguGen( intensity, dt, stationn):
    #generate wind gust type fact
    ##calculating fuzzyI
    fI= fuzzyI( intensity, stationn, 'windgu')
    ## calculating fuzzyTod
    fTod= fuzzyTod( dt.time())
    return windgu(fuzzyI=fI, fuzzyTod= fTod, date= dt.strftime('%m/%d/%Y'), locus= stationn)

def baromGen( intensity, dt, stationn):
    #generate barometric pressure type fact
    ##calculating fuzzyI
    fI= fuzzyI( intensity, stationn, 'barom')
    ## calculating fuzzyTod
    fTod= fuzzyTod( dt.time())
    return barom(fuzzyI=fI, fuzzyTod= fTod, date= dt.strftime('%m/%d/%Y'), locus= stationn)

def airtGen( intensity, dt, stationn):
    #generate air temperature type fact
    ##calculating fuzzyI
    fI= fuzzyI( intensity, stationn, 'airt')
    ## calculating fuzzyTod
    fTod= fuzzyTod( dt.time())
    return airt(fuzzyI=fI, fuzzyTod= fTod, date= dt.strftime('%m/%d/%Y'), locus= stationn)

def seandbcGen( intensity, dt, stationn):
    #generate sea temperature (NDBC) type fact
    ##calculating fuzzyI
    fI= fuzzyI( intensity, stationn, 'seandbc')
    ## calculating fuzzyTod
    fTod= fuzzyTod( dt.time())
    return seandbc(fuzzyI=fI, fuzzyTod= fTod, date= dt.strftime('%m/%d/%Y'), locus= stationn)
