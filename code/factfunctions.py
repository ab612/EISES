###mcb Ecoforecast prototype goal is to implement rules base from http://ecoforecast.coral.noaa.gov/index/0/MLRF1/model-detail&name=MASS-CORAL-BLEACHING and 'print' a forecast###
__author__ = "Madison Soden"
__date__ = "Tue Feb 27 11:34:48 2018"
__license__ = "NA?"
__version__ = "mcb"
__email__ = "madison.soden@gmail.com"
__status__ = "Production"


############################################################################################???????????????????????????? rule 18 verse rule 20 supposed to call different facts???????????????????????

from pyknow import *

###Fact Definition Documentation### 
    #fact names are declared as 'parsurf', 'sst', 'windsp', 'tide1m',
    #'seandbc', 'sea1m', 'curveB', 'sea1mM', 'seandbcM', 'windsp3day'

    #fuzzyI is a string containing a fuzzy (i.e. proxy) values for sst 
    #key = 'fuzzyI' / 0
    #fuzzy values can be 'uLow', 'dLow', 'vLow', 'Low', 'sLow', 'average', 'sHigh',
    # 'High', 'vHigh', 'dHigh', 'uHigh'
    #fuzzyTod is a string indicating a fuzzy time of day values for the-
    # time fuzzyI was recorded. Taken in eight 3 hour, then four 6 hour, then
    # two 12 hour , and one 24 hour time increments
    #key = 'fuzzyTod' and/or 1
    #fuzzy values can be 
    # 'evening' - 'even' - 0000 to 0300
    # 'midnight' - 'midn' - 0300 to 0600
    # 'pre-dawn' - 'pdaw' - 0600 to 0900
    # 'dawn' - 'dawn' - 0900 to 1200
    # 'morning' - 'morn' - 1200 to 1500
    # 'mid-day' - 'midd' - 1500 to 1800
    # 'pre-sunset' - 'psun' - 2100 to 2400
    # 'sunset' - 'suns' - 2100 to 2400
    # 
    # 'night-hours' - 'nite' - 0000 to 0900
    # 'dawn-morning' - 'dayb' - 0900 to 1500
    # 'afternoon' - 'aftn' - 1800 to 2400
    # 'daylight-hours' - 'dayl' - 0900 to 2400
    # 'all-day' - 'all' - 0300 to 0300
    
    #date is a string containing the date that fuzzyI was calculated on in DDMMYYYY
    #key = 'date' and/or 2 
    
    #locus is an string containing the abbreviated geographic location that
    #fuzzyI, fuzzyTod and date apply to.
    #key = 'locus' and/or 3

###Helper functions###
def anyof(*values):
    return P(lambda y: y in values)

def makefact( factName, factFuzzyI, fuzzyTod, factDate, factLocus)

#test functions to initialize specific combinations of facts
    def import_facts(self, filename='1'):
#       filename = './test_suite/fact_CSVs/test' + filenum +'.csv'
        factlines= [x.rstrip('\n') for x in open(filename)]
        while factlines:
            factString = factlines.pop(0)
            factName, factFuzzyI, factFuzzyTod, factDate, factLocus = factString.split(",")
           # print("DECLARED: ", factName, " ", factFuzzyI, " ", factFuzzyTod, " ",
           #         factDate, " ", factLocus, "\n")
            exec("self.declare(%s(fuzzyI=factFuzzyI, fuzzyTod=factFuzzyTod, date=factDate, locus=factLocus))" % (factName))

