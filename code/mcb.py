### main function to call knowledge engine based ecoforecast pipeline

__author__= "Madison.Soden"
__date__= "Tue Jul 24, 2018  12:53PM"
__license__= "NA?"
__email__= "madison.soden@gmail.com"
__status__= "Production"

import pyknow as pk
import ffmcb as ff
import kemcb as ke
import json
from os import listdir
from os.path import isfile, join

class airt( pk.Fact):
    pass
class barom( pk.Fact):
    pass
class seandbc( pk.Fact):
    pass
class winddir( pk.Fact):
    pass
class windgu( pk.Fact):
    pass
class windsp( pk.Fact):
    pass


def airt_decoder( obj):
    return airt(fuzzyI= obj['fuzzyI'], fuzzyT= obj['fuzzyTod'], date= obj['date'], locus= obj['locus'])
def barom_decoder( obj):
    return barom(fuzzyI= obj['fuzzyI'], fuzzyT= obj['fuzzyTod'], date= obj['date'], locus= obj['locus'])
def seandbc_decoder( obj):
    return seandbc(fuzzyI= obj['fuzzyI'], fuzzyT= obj['fuzzyTod'], date= obj['date'], locus= obj['locus'])
def winddir_decoder( obj):
    return winddir(fuzzyI= obj['fuzzyI'], fuzzyT= obj['fuzzyTod'], date= obj['date'], locus= obj['locus'])
def windgu_decoder( obj):
    return windgu(fuzzyI= obj['fuzzyI'], fuzzyT= obj['fuzzyTod'], date= obj['date'], locus= obj['locus'])
def windsp_decoder( obj):
    return windsp(fuzzyI= obj['fuzzyI'], fuzzyT= obj['fuzzyTod'], date= obj['date'], locus= obj['locus'])


def main( factfilename, stationname, date=''): 
    #call fact factory to generate facts
    #ff.factfactory( factfilename, stationname)
    
    if (date ==''):
        #get list of all files in directory ../data/fffacts (dates of the formMM_DD_YYYY)
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


