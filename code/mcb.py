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

def main(  factfilename, stationname, lookUpDate=None, run_ff=False):

    year = 0
    isRT= False
    if(factfilename[-2:]=='RT'):
        isRT = True

    fact_dir_name= factfilename[:5]
    fact_year_name= factfilename[-4:]
    glob_string= "../data/facts/"+fact_dir_name+"/"+fact_year_name+"/*/*.json"

    fact_files_list= glob.glob(glob_string)

    if not(fact_files_list) or run_ff or isRT:
        #parse insitu txt file and save as json file
        insitu_to_json.main( factfilename, isRT)
        #call fact factory to generate facts
        ff.factfactory( factfilename, stationname)


    if (lookUpDate == 'year'): #5isinstance(lookUpDate, str)):
        year= factfilename[-4:]
        factdatefiles = [f for f in
                os.listdir("../data/facts/"+fact_dir_name+'/'+year) if os.path.isdir(os.path.join("../data/facts/"+fact_dir_name+'/'+year, f))]
    elif (not isinstance(lookUpDate, list)):
        print("Please input list of strings for 3rd function\
                argument(MM_DD_YYYY). Alternatively input 'year' to run a coral forecast on the entire year\n")
        return
    else:
        year= lookUpDate[0][-2:]
        if(int(year)>50):
            year= '19'+year
        else:
            year= '20'+year
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
            with open("../data/facts/"+fact_dir_name+'/'+year+'/'+date_iterator+"/tide1m.json", 'r') as fin:
                factlist= factlist + json.load( fin, object_hook= fact.tide1m_decoder)
        except:
            pass
        try:
            with open("../data/facts/"+fact_dir_name+'/'+year+'/'+date_iterator+"/windsp3day.json", 'r') as fin:
                factlist= factlist + json.load( fin, object_hook= fact.windsp3day_decoder)
        except:
            pass #print('windsp3day data does not exist for: '+ date_iterator)
        try:
            with open("../data/facts/"+fact_dir_name+'/'+year+'/'+date_iterator+"/seandbc.json", 'r') as fin:
                factlist= factlist + json.load( fin, object_hook= fact.seandbc_decoder)
        except:
            pass #print('seandbc data does not exist for: '+ date_iterator)
        try:
            with open("../data/facts/"+fact_dir_name+'/'+year+'/'+date_iterator+"/seandbcM.json", 'r') as fin:
                factlist= factlist + json.load( fin, object_hook= fact.seandbcM_decoder)
        except:
            pass #print('seandbcM data does not exist for: '+ date_iterator)
        try:
            with open("../data/facts/"+fact_dir_name+'/'+year+'/'+date_iterator+"/windsp.json", 'r') as fin:
                factlist= factlist + json.load( fin, object_hook= fact.windsp_decoder)
        except:
            pass #print('windsp data does not exist for: '+ date_iterator)
        #call knowledge engine to process analyze facts
        currentDT = datetime.datetime.now()
        SRI[date_iterator] = ke.knowledge_engine( factlist)

    if not os.path.exists(os.path.dirname('../data/SRI/'+stationname+'/')):
        os.makedirs(os.path.dirname('../data/SRI/'+stationname+'/'))

    with open('../data/SRI/'+stationname+"/"+year+'.csv', mode='w') as sri_file:
        sri_writer = csv.writer(sri_file, delimiter=',')
        for date_iterator in factdatefiles:
            sri_writer.writerow([date_iterator, SRI[date_iterator]])
