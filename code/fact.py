#!/usr/bin/env python3

### main function to creat facts

__author__= "Madison.Soden"
__date__= "Thu Jul 26, 2018  12:46PM"
__license__= "NA?"
__email__= "madison.soden@gmail.com"
__status__= "Production"

import pyknow as pk
from IPython import embed

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
    return airt(fuzzyI= obj['fuzzyI'], fuzzyTod= obj['fuzzyTod'], date= obj['date'], locus= obj['locus'])
def barom_decoder( obj):
    return barom(fuzzyI= obj['fuzzyI'], fuzzyTod= obj['fuzzyTod'], date= obj['date'], locus= obj['locus'])
def seandbc_decoder( obj):
    return seandbc(fuzzyI= obj['fuzzyI'], fuzzyTod= obj['fuzzyTod'], date= obj['date'], locus= obj['locus'])
def winddir_decoder( obj):
    return winddir(fuzzyI= obj['fuzzyI'], fuzzyTod= obj['fuzzyTod'], date= obj['date'], locus= obj['locus'])
def windgu_decoder( obj):
    return windgu(fuzzyI= obj['fuzzyI'], fuzzyTod= obj['fuzzyTod'], date= obj['date'], locus= obj['locus'])
def windsp_decoder( obj):
    return windsp(fuzzyI= obj['fuzzyI'], fuzzyTod= obj['fuzzyTod'], date= obj['date'], locus= obj['locus'])

