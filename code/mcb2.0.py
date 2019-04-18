#/usr/bin/env python3
### main function to call knowledge engine based ecoforecast pipeline

__author__= "Madison.Soden"
__date__= "Tue Oct 30, 2018  03:06PM"
__license__= "NA?"
__email__= "madison.soden@gmail.com"
__status__= "Production"

import pyknow as pk
import ffmcb as ff
import kemcb as ke
import json
import os
import os.path
import glob
from  parsers import insitu_to_json
from IPython import embed
import fact
import datetime
import csv

def check_timeframe( lookUpDate):
 ## identifying which function to call to run knowledge engine
    if isinstance(lookUpDate, list):
        if lookUpDate and all(isinstance(s, str) for s in lookUpDate):
            if all(re.match("^(0|1)[1-9]_(0|1|2|3)[0-9]_(19|20)(8|9|0|1)[0-9]$", s) for s in lookUpDate):
                return lookUpDate[-4:], "dates" #call date iterator
            else: 
                 raise ValueError( "3rd function argument must be a list of\
                 strings in  the format MM_DD_YYYY. For years between\
                 1987-2018\n")
        else:
            raise ValueError( "3rd function argument must be a none empty\
                    list of strings. Of the format MM_DD_YYYY for years 1987-2018)\n")
    elif isinstance(lookUpDate, str):
        if re.match("^(19|20)(8|9|0|1)[0-9]$", lookUpDate):
            return lookUpDate, "year" #call year creator
        else:
            raise ValueError("3rd function argument must be a string of the\
                    format YYYY for years 1987-2018.\n")
    else:
        raise ValueError("For 3rd function argument please input list of\ 
                    strings MM_DD_YYYY for 3rd function argument.\
                    Alternatively, input a string YYYY to run a coral\
                    bleaching forecast on the entire year\n")

def create_facts( stationName, year):
    factFileName= stationName+"h"+year+".txt"
    insitu_to_json.main( factFileName) #parse insitu txt file and save as json file
    ff.factfactory( factFileName, stationName) #call fact factory to generate facts

def main( stationName, lookUpDate, run_ff=False):
    
    year, engine_case= check_timeframe(lookUpDate)    
    
   
    if run_ff: #run fact factory if asked to
        create_facts( stationName, year)
    else:  #checking to see if required fact data files exist
        glob_string= "../data/facts/"+stationName+"/"+year+"/*/*.json"
        fact_files_list= glob.glob(glob_string)
        if not(fact_files_list): 
            #if the directory supposed to be containing fact files is empty rerun parser and ff
            create_facts( stationName, year)

##########STOPPING POINT OF EDITING?REWRITING#########################
    if (lookUpDate == 'year'):
        year= factfilename[-4:]
        factdatefiles = [
                f for f in os.listdir("../data/facts/"+stationName+'/'+year)
                if os.path.isdir(os.path.join("../data/facts/"+stationName+'/'+year, f))]
    elif (not isinstance(lookUpDate, list)):
        print("Please input list of strings MM_DD_YYYY for 3rd function argument.
                Alternatively input a string YYYY to run a coral bleaching
                forecast on the entire year\n")
        return
    else:
        year= lookUpDate[0][-4:]
        factdatefiles = lookUpDate

    SRI = {}
    dateI = "01_01_"+year
    yearF = int(year) +1
    dateF = "01_01_"+str(yearF)
    dateStart = datetime.datetime.strptime(dateI, '%m_%d_%Y')
    dateFin = datetime.datetime.strptime(dateF, '%m_%d_%Y')
    step = datetime.timedelta(days=1)
    while dateStart < dateFin:
        SRI[dateStart.strftime('%m_%d_%Y')] = 0
        dateStart += step

    factdatefiles= sorted(factdatefiles)

    for date_iterator in factdatefiles:
        #put fact files into single fact list
        factlist= []
        alertDict = {}
        try:
            with open("../data/facts/"+stationName+'/'+year+'/'+date_iterator+"/tide1m.json", 'r') as fin:
                factlist= factlist + json.load( fin, object_hook= fact.tide1m_decoder)
        except:
            pass
        try:
            with open("../data/facts/"+stationName+'/'+year+'/'+date_iterator+"/windsp3day.json", 'r') as fin:
                factlist= factlist + json.load( fin, object_hook= fact.windsp3day_decoder)
        except:
            pass #print('windsp3day data does not exist for: '+ date_iterator)
        try:
            with open("../data/facts/"+stationName+'/'+year+'/'+date_iterator+"/seandbc.json", 'r') as fin:
                factlist= factlist + json.load( fin, object_hook= fact.seandbc_decoder)
        except:
            pass #print('seandbc data does not exist for: '+ date_iterator)
        try:
            with open("../data/facts/"+stationName+'/'+year+'/'+date_iterator+"/seandbcM.json", 'r') as fin:
                factlist= factlist + json.load( fin, object_hook= fact.seandbcM_decoder)
        except:
            pass #print('seandbcM data does not exist for: '+ date_iterator)
        try:
            with open("../data/facts/"+stationName+'/'+year+'/'+date_iterator+"/windsp.json", 'r') as fin:
                factlist= factlist + json.load( fin, object_hook= fact.windsp_decoder)
        except:
            pass #print('windsp data does not exist for: '+ date_iterator)

        #call knowledge engine to process analyze facts
        alertDict['sName'] = stationName
        currentDT = datetime.datetime.now()
        alertDict['runDate'] = currentDT.strftime( '%m_%d_%Y')
        alertDict['alertDate'] = date_iterator
        alertDict['forecastType'] = "MassCoralBleaching"
        #alertDict['alerts'] = ke.knowledge_engine( factlist)
        SRI[date_iterator] = ke.knowledge_engine( factlist)

    if not os.path.exists(os.path.dirname('../data/SRI/'+stationName+'/')):
        os.makedirs(os.path.dirname('../data/SRI/'+stationName+'/'))

    with open('../data/SRI/'+stationName+"/"+year+'.csv', mode='w') as sri_file:
        sri_writer = csv.writer(sri_file, delimiter=',')
        for date_iterator in factdatefiles:
            sri_writer.writerow([date_iterator, SRI[date_iterator]])
