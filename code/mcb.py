### main function to call knowledge engine based ecoforecast pipeline

__author__= "Madison.Soden"
__date__= "Mon Jul 23, 2018  01:42PM"
__license__= "NA?"
__email__= "madison.soden@gmail.com"
__status__= "Production"

import pyknow as pk
import ffmcb as ff
import kemcb as ke
import json

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


def main( factfilename, stationname): 
    #call fact factory to generate facts
    #ff.factfactory( factfilename, stationname)
    
    #split fact files into daily sections
    with open("../data/fffacts/"+factfilename+"/airt.json", 'r') as fin:
        airtfactlist= json.load( fin, object_hook= airt_decoder)
    with open("../data/fffacts/"+factfilename+"/barom.json", 'r') as fin:
        baromfactlist= json.load( fin, object_hook= barom_decoder)
    with open("../data/fffacts/"+factfilename+"/seandbc.json", 'r') as fin:
        seandbcfactlist= json.load( fin, object_hook= seandbc_decoder)
    with open("../data/fffacts/"+factfilename+"/winddir.json", 'r') as fin:
        winddirfactlist= json.load( fin, object_hook= winddir_decoder)
    with open("../data/fffacts/"+factfilename+"/windgu.json", 'r') as fin:
        windgufactlist= json.load( fin, object_hook= windgu_decoder)
    with open("../data/fffacts/"+factfilename+"/windsp.json", 'r') as fin:
        windspfactlist= json.load( fin, object_hook= windsp_decoder)




    #call knowledge engine to process analyze facts
    #ke.knowledge_engine( factlist)
    return


