### ffmcb.py is a prototype fact factory implementation, meant to help provide an
#       example for a future, inherited fact factory implementation that would apply to
#       any ecoforecast. Not just MCB for MLRF1
__author__ = "Madison.Soden" 
__date__ = "Thu Apr 19 11:28:26 2018"
__license__ = "NA?"
__version__ = "mcb"
__email__ = "madison.soden@gmail.com"
__status__ = "Production"

import pyknow as pk

###Fact Definition Documentation###
#fact names are declared as 'parsurf', 'sst', 'windsp', 'tide1m',
#'seandbc', 'sea1m', 'curveB', 'sea1mM', 'seandbcM', 'windsp3day'

#fuzzyI is a string containing a fuzzy (i.e. proxy) values for sst
#key = 'fuzzyI' /
#fuzzy values can be 'uLow', 'dLow', 'vLow', 'Low', 'sLow', 'average', 'sHigh',
#'High', 'vHigh', 'dHigh', 'uHigh'$
#fuzzyTod is a string indicating a fuzzy time of day values for the-
#time fuzzyI was recorded Taken in eight 3 hour, then four 6 hour, then 
#two 12 hour , and one 24 hour time increments
#key = 'fuzzyTod' and/or 1
#fuzzy values can be
# 'evening' - 'even' - 0000 to 0300
#'midnight' - 'midn' - 0300 to 0600
#'pre-dawn' - 'pdaw' - 0600 to 0900
#'dawn' - 'dawn' - 0900 to 1200
# 'morning' - 'morn' - 1200 to 1500
#'mid-day' -'midd'-1500 to 1800
#'pre-sunset' - 'psun' - 2100 to 2400
#'sunset' - 'suns' - 2100 to 2400
#
# 'night-hours' - 'nite' - 0000 to 0900
# 'dawn-morning' - 'dayb' - 0900 to 1500
# 'afternoon' - 'aftn' - 1800 to 2400
# 'daylight-hours' - 'dayl' - 0900 to 2400
# 'all-day' - 'all' - 0300 to 0300

#date is a string containing the date that fuzzyI was calculated on in DDMMYYYY
#key = 'date' and/or 2

#locus is an string containing the abbreviated geographic location that
#fuzzyI, fuzzyTod and date apply to
#key = 'locus' and/or 3

class MyException(Exception):
    pass

class Factory( facttype, fuzzyRangedict=False, locus='MLRF1', date):
    """Factory Class"""
    def __init__ (self):
        if (type(date) is not type(0)):
            assert MyException("Date parameter not formatted correctly. Should\
                    be a 8 digit integer")
        if (type(facttype) is not type('string')):
            assert MyException("facttype parameter not of type string")
        if ((type(locus) is not type('string')) or (len(locus) is not 5)):
            assert MyException('locus parameter not formatted correctly. Should\
                    be a string of length 5')
        self.facttype = facttype
        self.ranges = fuzzyRangedict
        self.locus = locus
        self.date = date

#FUZZYRANDEDICT STRUCTURE
#rangeDict = {
#       ''
#
#
#
#           }

    def fuzzyI(self, data?):

