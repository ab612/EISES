#!/usr/bin/env python3
### main function to call knowledge engine based ecoforecast pipeline

__author__= "Madison.Soden"
__date__= "Thu Jul 26, 2018  12:46PM"
__license__= "NA?"
__email__= "madison.soden@gmail.com"
__status__= "Production"

import pyknow as pk
import ffmcb as ff
import kemcb as ke
import json
from os import listdir
from os.path import isfile, join
from  parsers import insitu_to_json
from IPython import embed
import fact


def main( factfilename, stationname, date=''): 
    #parse insitu txt file and save as json file
    insitu_to_json.main(factfilename)

    #call fact factory to generate facts
    ff.factfactory( factfilename, stationname)
    
    if (date ==''):
        #get list of all files in directory ../data/fffacts (dates of the form MM_DD_YY)
        factdatefiles = [f for f in listdir("../data/fffacts/"+factfilename) if isfile(join("../data/fffacts/"+factfilename, f))]

        for date in factdatefiles:
            #put fact files into single fact list
            factlist= []
            with open("../data/fffacts/"+factfilename+'/'+date+"/airt.json", 'r') as fin:
                factlist.append(json.load( fin, object_hook= airt_decoder))
            with open("../data/fffacts/"+factfilename+'/'+date+"/barom.json", 'r') as fin:
                factlist.append(json.load( fin, object_hook= barom_decoder))
            with open("../data/fffacts/"+factfilename+'/'+date+"/seandbc.json", 'r') as fin:
                factlist.append(json.load( fin, object_hook= seandbc_decoder))
            with open("../data/fffacts/"+factfilename+'/'+date+"/winddir.json", 'r') as fin:
                factlist.append(json.load( fin, object_hook= winddir_decoder))
            with open("../data/fffacts/"+factfilename+'/'+date+"/windgu.json", 'r') as fin:
                factlist.append(json.load( fin, object_hook= windgu_decoder))
            with open("../data/fffacts/"+factfilename+'/'+date+"/windsp.json", 'r') as fin:
                factlist.append(json.load( fin, object_hook= windsp_decoder))
            #call knowledge engine to process analyze facts
            ke.knowledge_engine( factlist)
            return
    else: 
        #put fact files into single fact list
        factlist= []
        with open("../data/fffacts/"+factfilename+'/'+date+"/airt.json", 'r') as fin:
            factlist= factlist + json.load( fin, object_hook= fact.airt_decoder)
        with open("../data/fffacts/"+factfilename+'/'+date+"/barom.json", 'r') as fin:
            factlist= factlist + json.load( fin, object_hook= fact.barom_decoder)
        with open("../data/fffacts/"+factfilename+'/'+date+"/seandbc.json", 'r') as fin:
            factlist= factlist + json.load( fin, object_hook= fact.seandbc_decoder)
        with open("../data/fffacts/"+factfilename+'/'+date+"/winddir.json", 'r') as fin:
            factlist= factlist + json.load( fin, object_hook= fact.winddir_decoder)
        with open("../data/fffacts/"+factfilename+'/'+date+"/windgu.json", 'r') as fin:
            factlist= factlist + json.load( fin, object_hook= fact.windgu_decoder)
        with open("../data/fffacts/"+factfilename+'/'+date+"/windsp.json", 'r') as fin:
            factlist= factlist + json.load( fin, object_hook= fact.windsp_decoder)
        
        #call knowledge engine to process analyze facts
        e = ke.MCB()
        e.reset()
        embed()
        for f in factlist:
            e.declare(f)

        embed()
        e.run()
        return 
