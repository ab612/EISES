###mcb Ecoforecast prototype goal is to implement rules base from http://ecoforecast.coral.noaa.gov/index/0/MLRF1/model-detail&name=MASS-CORAL-BLEACHING and 'print' a forecast###

__author__= "Madison Soden"
__date__= "Tue Jul 24, 2018  01:48PM"
__license__= "NA?"
__email__= "madison.soden@gmail.com"
__status__= "Production"


############################################################################################???????????????????????????? rule 18 verse rule 20 supposed to call different facts???????????????????????

from pyknow import *
import texttable as tt
from IPython import embed

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

def RuleRef( index):
    ruleDict = {
        'p': '    p    -    parsurf\n',
        's': '    s    -    sst\n',
        'w': '    w    -    windsp\n',
        't': '    t    -    tide1m\n',
        'a': '    a    -    seandbc\n',
        'e': '    e    -    sea1m\n',
        'b': '    b    -    curveB\n',
        'eM': '    eM    -    sea1mM\n',
        'aM': '    aM    -    seandbcM\n',
        'w3': '    w3    -    windsp3day\n'}
    return ruleDict.get( index, "incorrect input\n")

###Helper functions###
def anyof(*values):
    return P(lambda y: y in values)

###FACT DECLARATIONS###
class parsurf(Fact):
    #photosynthetically active radiation at ocean surface
    pass

class sst(Fact):
    #Remss 'misst' Blended Microwave/infrared sst (surface sea temperature)
    pass

class windsp(Fact):
    #hourly average wind speed
    pass

class tide1m(Fact):
    #tide level at ~1m depth
    pass

class seandbc(Fact):
    #depth-averaged sea temperature
    pass

class sea1m(Fact):
    #sea temperature at ~1m depth
    pass

class curveB(Fact):
    #Berkelmans Temperature-Duration Bleaching Curve
    pass

class sea1mM(Fact):
    #Monthly mean sea temperature at ~1m depth
    pass

class seandbcM(Fact):
    #Monthly Mean Depth-Averaged Sea Temperature
    pass

class windsp3day(Fact):
    #3-day average wind speed
    pass


class MCB(KnowledgeEngine):

#initial instruction output
#    print("""\n
#        ----------------------------------------------------------------------
#        To declare Knowledge Engine:
#        >> e = mcb.MCB()
#        >> e.reset()
#        \n
#        To add facts to fact list call:
#        >> e.declare_facts()
#        >> e.declare_facts('factname', 'fuzzyI', 'fuzzyTod', 'date', 'locus')
#        \n
#        To import a fact csv call:
#        >> e.import_facts('./test_suite/fact_CSVs/testX.csv')
#        \n
#        To view current rule base call:
#        >> e.get_rules()
#        \n
#        To view rule nomenclature reference call:
#        >> mcb.printRuleRef()
#        \n
#        To view current fact base call:
#        >> e.print_facts()
#        \n
#        To run Knowledge Engine call:
#        >> e.run()
#        ----------------------------------------------------------------------
#         \n  \n \n""")

#function to pipe pyknow e.fact output into something legible
    
    def print_facts(self):
    ## messy parsing of giantstring'
        giantstring = self.facts.__str__()
        giantstring = giantstring.strip('<f-')
        giantstring = giantstring.rstrip(')')
        factlines =giantstring.split(")\n<f-")
        printlist = []
        while factlines:
            factstring = factlines.pop(0)
            factstring = factstring.split(',', 1)
            key = factstring[0]
            factstring = factstring[1]
            factstring = factstring[4:]
            factstring = factstring.split('(', 1)
            factname = factstring[0]
            if len(factstring[1]) > 4:
                factstring = factstring[1]
                factstring = factstring[8:]
                factstring = factstring.split('\'', 1)
                rRangeAtt = factstring[0]
                factstring = factstring[1]
                factstring = factstring[12:]
                factstring = factstring.split('\'', 1)
                todAtt = factstring[0]
                factstring = factstring[1]
                factstring = factstring[8:]
                factstring = factstring.split('\'', 1)
                dateAtt = factstring[0]
                factstring = factstring[1]
                factstring = factstring[9:]
                factstring = factstring.split('\'', 1)
                locusAtt = factstring[0]
            else :
                rRangeAtt, todAtt, dateAtt, locusAtt = ' ', ' ', ' ', ' '
            factlist = [key, factname, rRangeAtt, todAtt, dateAtt, locusAtt]
            printlist.append(factlist)

    ##formatting printlist using Texttable library
        table = tt.Texttable()
        headings = ['Key', 'Fact', 'fuzzyI', 'fuzzyTod', 'Date', 'Locus']
        table.header(headings)
        for x in printlist:
            table.add_row(x)
        s = table.draw()
        print(s)

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

#function to automate declaring facts: has a function call mode w/ attributes
##or an interactive mode for terminal
    def declare_facts(self, x='na', y='na', z='na'):
        if x!='na':
            print("""
                'windsp3day', 'seandbcM', 'sea1mM', 'curveB','sea1m','seandbc', 'tide1m', 'windsp', 'sst', or 'parsurf'
                'uLow', 'dLow', 'vLow', 'Low', 'sLow','average', 'sHigh','High', 'vHigh','dHigh', or 'uHigh'
                'even'(00-03), 'midn'(03-06), 'pdaw'(06-09), 'dawn'(09-12),'morn'(12-15), 'midd'(15-18), 'psun'(18-21), 'suns'(21-24), 'nite'(00-09), 'dayb'(09-15), 'aftn'(18-24), 'dayl'(09-24), 'all'(03-03)
                """)
            exec("self.declare(%s(fuzzyI=y, fuzzyTod=z))" % (x))
        else:
            done='n'
            while(done=='n'):
                print("""Which fact would you like to declare?('windsp3day', 'seandbcM', 'sea1mM', 'curveB', 'sea1m', 'seandbc', 'tide1m', 'windsp', 'sst', or 'parsurf').""")
                x = input('  ')
                print("""What is the fuzzyI?('uLow', 'dLow', 'vLow', 'Low', 'sLow','average', 'sHigh', 'High', 'vHigh', 'dHigh', or 'uHigh').""")
                y = input('  ')
                print("""What is the fuzzyTod?( 'even'(00-03), 'midn'(03-06), 'pdaw'(06-09), 'dawn'(09-12), 'morn'(12-15), 'midd'(15-18), 'psun'(21-24), 'suns'(21-24), 'nite'(00-09), 'dayb'(09-15), 'aftn'(18-24), 'dayl'(09-24), 'all'(03-03).""")
                z = input('  ')
                exec("self.declare(%s(fuzzyI=y, fuzzyTod=z))" % (x))
                print("""Are you finished declaring facts? (y/n)""")
                done = input('  ')

###RULE DECLARATIONS###
#Unbelievable value Rules
    @Rule(OR(sst(fuzzyI='uLow'), sst(fuzzyI='uHigh')))
    def u_fI_sst(self):
        print("sst values in unbelievable range")

    @Rule(OR(windsp(fuzzyI='uLow'), windsp(fuzzyI='uHigh')))
    def u_fI_windsp(self):
        print("wind scalar values in unbelievable range")

    @Rule(OR(seandbc(fuzzyI='uLow'), seandbc(fuzzyI='uHigh')))
    def u_fI_seandbc(self):
        print("seandbc values in unbelievable range")

    @Rule(OR(parsurf(fuzzyI='uLow'), parsurf(fuzzyI='uHigh')))
    def u_fI_parsurf(self):
        print("parsurf values in unbelievable range")

    @Rule(OR(tide1m(fuzzyI='uLow'), tide1m(fuzzyI='uHigh')))
    def u_fI_tide1m(self):
        print("tide1m values in unbelievable range")

    @Rule(OR(sea1m(fuzzyI='uLow'), sea1m(fuzzyI='uHigh')))
    def u_fI_sea1m(self):
        print("sea1m values in unbelievable range")

    @Rule(OR(seandbcM(fuzzyI='uLow'), seandbcM(fuzzyI='uHigh')))
    def u_fI_seandbcM(self):
        print("seandbcM values in unbelievable range")

    @Rule(OR(windsp3day(fuzzyI='uLow'), windsp3day(fuzzyI='uHigh')))
    def u_fI_windsp3day(self):
        print("windsp3day values in unbelievable range")

    @Rule(OR(sea1mM(fuzzyI='uLow'), sea1mM(fuzzyI='uHigh')))
    def u_fI_sea1mM(self):
        print("sea1mM values in unbelievable range")

    @Rule(OR(curveB(fuzzyI='uLow'), curveB(fuzzyI='uHigh')))
    def u_fI_curveB(self):
        print("curveB values in unbelievable range")

#Missing info rules
    @Rule(NOT(sst(fuzzyI= anyof('uLow', 'dLow', 'vLow', 'Low', 'sLow',
        'average', 'sHigh', 'High', 'vHigh', 'dHigh', 'uHigh'))))
    def m_fI_sst(self):
        print("missing or unreadable value for sst fuzzyI")

    @Rule(NOT(seandbc(fuzzyI= anyof('uLow', 'dLow', 'vLow', 'Low', 'sLow',
        'average', 'sHigh', 'High', 'vHigh', 'dHigh', 'uHigh'))))
    def m_fI_seandbc(self):
        print("missing or unreadable value for seandbc fuzzyI")

    @Rule(NOT(parsurf(fuzzyI= anyof('uLow', 'dLow', 'vLow', 'Low', 'sLow',
        'average', 'sHigh', 'High', 'vHigh', 'dHigh', 'uHigh'))))
    def m_fI_parsurf(self):
        print("missing or unreadable value for parsurf fuzzyI")

    @Rule(NOT(windsp(fuzzyI= anyof('uLow', 'dLow', 'vLow', 'Low', 'sLow',
        'average', 'sHigh', 'High', 'vHigh', 'dHigh', 'uHigh'))))
    def m_fI_windsp(self):
        print("missing or unreadable value for windsp fuzzyI")

    @Rule(NOT(tide1m(fuzzyI= anyof('uLow', 'dLow', 'vLow', 'Low', 'sLow',
        'average', 'sHigh', 'High', 'vHigh', 'dHigh', 'uHigh'))))
    def m_fI_tide1m(self):
        print("missing or unreadable value for tide1m fuzzyI")

    @Rule(NOT(sea1m(fuzzyI= anyof('uLow', 'dLow', 'vLow', 'Low', 'sLow',
        'average', 'sHigh', 'High', 'vHigh', 'dHigh', 'uHigh'))))
    def m_fI_sea1m(self):
        print("missing or unreadable value for sea1m fuzzyI")

    @Rule(NOT(seandbcM(fuzzyI= anyof('uLow', 'dLow', 'vLow', 'Low', 'sLow',
        'average', 'sHigh', 'High', 'vHigh', 'dHigh', 'uHigh'))))
    def m_fI_seandbcM(self):
        print("missing or unreadable value for seandbcM fuzzyI")

    @Rule(NOT(curveB(fuzzyI= anyof('uLow', 'dLow','vLow', 'Low', 'sLow',
        'average', 'sHigh', 'High', 'vHigh' ,'dHigh', 'uHigh'))))
    def m_fI_curveB(self):
        print("missing or unreadable value for curveB fuzzyI")

    @Rule(NOT(sea1mM(fuzzyI= anyof('uLow', 'dLow', 'vLow', 'Low', 'sLow',
        'average', 'sHigh', 'High', 'vHigh', 'dHigh', 'uHigh'))))
    def m_fI_sea1mM(self):
        print("missing or unreadable value for sea1mM fuzzyI")


#MCB MASS-CORAL-BLEACHING implementation (forecast model has 24 rules)
#Description: Mass bleaching of hard corals

##Ecoforecast Rule #1: Coral-Bleaching-PtwA
##Description: Mass coral bleaching (high in-situ sea temperature + high light + low wind + low tide)
    @Rule(parsurf(fuzzyI=anyof('High', 'vHigh', 'dHigh')),
            parsurf(fuzzyTod=anyof('midd', 'psun', 'dayl', 'aftn', 'all')),
            tide1m(fuzzyI=anyof('dLow', 'vLow', 'Low')),
            tide1m(fuzzyTod=anyof('morn', 'midd', 'psun', 'dayl', 'dayb',
                'aftn', 'all')),
            windsp(fuzzyI=anyof('dLow', 'vLow', 'Low')),
            windsp(fuzzyTod=anyof('morn', 'midd', 'psun', 'dayl', 'dayb',
                'aftn', 'all')),
            seandbc(fuzzyI=anyof('High', 'vHigh', 'dHigh')),
            seandbc(fuzzyTod=W()))
    def mcb_PtwA(self):
        print("- Coral-Bleaching-PtwA fired")
        print(' ', RuleRef('p'), RuleRef('t'), RuleRef('w'),
                RuleRef('a'))

##Ecoforecast Rule #2: Coral-Bleaching-PtwE
##Description: Mass coral bleaching (high 'shallow' sea temperature + high light + low wind + low tide)
    @Rule(parsurf(fuzzyI=anyof('High', 'vHigh', 'dHigh')), 
            parsurf(fuzzyTod=anyof('midd', 'dayl', 'all')),
            tide1m(fuzzyI=anyof('dLow', 'vLow', 'Low')),
            tide1m(fuzzyTod=anyof('morn', 'midd', 'psun', 'dayl', 'dayb',
                'aftn', 'all')),
            windsp(fuzzyI=anyof('dLow', 'vLow', 'Low')),
            windsp(fuzzyTod=anyof('morn', 'midd', 'psun', 'dayl', 'dayb',
                'aftn', 'all')),
            sea1m(fuzzyI=anyof('High', 'vHigh', 'dHigh')),
            sea1m(fuzzyTod=W()))
    def mcb_PtwE(self):
        print("- Coral-Bleaching-PtwE fired")
        print(' ', RuleRef('p'),  RuleRef('t'), RuleRef('w'),
                RuleRef('e'))

##Ecoforecast Rule #3: Coral-Bleaching-PtwS
##Description: Mass coral bleaching (high SST + high light + low wind + low tide)
    @Rule(parsurf(fuzzyI=anyof('High', 'vHigh', 'dHigh')),
            parsurf(fuzzyTod=anyof('midd', 'dayl', 'all')),
            tide1m(fuzzyI=anyof('dLow', 'vLow', 'Low')),
            tide1m(fuzzyTod=anyof('morn', 'midd', 'psun', 'dayl', 'dayb', 'aftn', 'all')),
            windsp(fuzzyI=anyof('dLow', 'vLow', 'Low')),
            windsp(fuzzyTod=anyof('morn', 'midd', 'psun', 'dayl', 'dayb', 'aftn', 'aftn', 'all')),
            sst(fuzzyI=anyof('High', 'vHigh', 'dHigh')),
            sst(fuzzyTod=W()))
    def mcb_PtwS(self):
        print("- Coral-Bleaching-Tlwt fired")
        print(' ', RuleRef('t'), RuleRef('l'), RuleRef('w'),
                RuleRef('t'))

##Ecoforecast Rule #4: Coral-Bleaching-PwA
## Description: Mass coral bleaching (high in-situ sea temperature + high light + low wind)
    @Rule(parsurf(fuzzyI=anyof('High', 'vHigh', 'dHigh')),
            parsurf(fuzzyTod=anyof('midd', 'psun', 'dayl', 'aftn', 'all')),
            windsp(fuzzyI=anyof('dLow', 'vLow', 'Low')),
            windsp(fuzzyTod=anyof('morn', 'midd', 'psun', 'dayl', 'dayb', 'aftn', 'all')),
            seandbc(fuzzyI=anyof('High', 'vHigh', 'dHigh')),
            seandbc(fuzzyTod=W()))
    def mcb_PwA(self):
        print("- Coral-Bleaching-PwA fired")
        print(' ', RuleRef('p'), RuleRef('w'), RuleRef('a'))

##Ecoforecast Rule #5: Coral-Bleaching-twA
##Description: Mass coral bleaching (high in-situ sea temperature + low wind + low tide)
    @Rule(tide1m(fuzzyI=anyof('dLow', 'vLow', 'low')),
            tide1m(fuzzyTod=anyof('morn', 'midd', 'psun', 'dayl', 'dayb', 'aftn', 'all')),
            windsp(fuzzyI=anyof('dLow', 'vLow', 'Low')),
            windsp(fuzzyTod=anyof('morn', 'midd', 'psun', 'day', 'dayb', 'aftn', 'all')),
            seandbc(fuzzyI=anyof('High', 'vHigh', 'dHigh')),
            seandbc(fuzzyTod=W()))
    def mcb_twA(self):
        print("- Coral-Bleaching-twA")
        print(' ', RuleRef('t'), RuleRef('w'), RuleRef('a'))

##Ecoforecast Rule #6: Coral-Bleaching-PwE
##Description: Mass coral bleaching (high 'shallow' sea temperature + high light + low wind)
    @Rule(parsurf(fuzzyI=anyof('High', 'vHigh', 'dHigh')),
            parsurf(fuzzyTod=anyof('midd', 'dayl', 'all')),
            windsp(fuzzyI=anyof('dLow', 'vLow', 'Low')),
            windsp(fuzzyTod=anyof('morn', 'midd', 'psun', 'dayl', 'dayb', 'aftn', 'all')),
            sea1m(fuzzyI=anyof('High', 'vHigh', 'dHigh')),
            sea1m(fuzzyTod=W()))
    def mcb_PwE(self):
        print("- Coral-Bleaching-PwE fired")
        print(' ', RuleRef('p'), RuleRef('w'), RuleRef('e'))

##Ecoforecast Rule #7: Coral-Bleaching-twE
##Description: Mass coral bleaching (high 'shallow' sea temperature + low wind + low tide)
    @Rule(tide1m(fuzzyI=anyof('dLow', 'vLow', 'Low')),
            tide1m(fuzzyTod=anyof('morn', 'midd', 'psun', 'dayl', 'dayb', 'aftn', 'all')),
            windsp(fuzzyI=anyof('dLow', 'vLow', 'Low')),
            windsp(fuzzyTod=anyof('morn', 'midd', 'psun', 'dayl', 'dayb', 'aftn', 'all')),
            sea1m(fuzzyI=anyof('High', 'vHigh', 'dHigh')),
            sea1m(fuzzyTod=W()))
    def mcb_twE(self):
        print("- Coral-Bleaching-twE fired")
        print(' ', RuleRef('t'), RuleRef('w'), RuleRef('e'))


##Ecoforecast Rule #8: Coral-Bleaching-PwS
##Description: Mass coral bleaching (high SST + high light + low wind)
    @Rule(parsurf(fuzzyI=anyof('High', 'vHigh', 'dHigh')),
            parsurf(fuzzyTod=anyof('midd', 'dayl', 'all')),
            windsp(fuzzyI=anyof('dLow', 'vLow', 'Low')),
            windsp(fuzzyTod=anyof('morn', 'midd', 'psun', 'dayl', 'dayb', 'aftn', 'all')),
            sst(fuzzyI=anyof('High', 'vHigh', 'dHigh')),
            sst(fuzzyTod=W()))
    def mcb_PwS(self):
        print("- Coral-Bleaching-PwS fired")
        print(' ', RuleRef('p'), RuleRef('w'), RuleRef('s'))

##Ecoforecast Rule #9: Coral-Bleaching-twS
##Description: Mass coral bleaching (high SST + low wind + low tide)
    @Rule(tide1m(fuzzyI=anyof('dLow', 'vLow', 'Low')),
            tide1m(fuzzyTod=anyof('morn', 'midd', 'psun', 'dayl', 'dayb', 'aftn', 'all')),
            windsp(fuzzyI=anyof('dLow', 'vLow', 'Low')),
            windsp(fuzzyTod=anyof('morn', 'midd', 'psun', 'dayl', 'dayb', 'aftn', 'all')),
            sst(fuzzyI=anyof('High', 'vHigh', 'dHigh')),
            sst(fuzzyTod=W()))
    def mcb_twS(self):
        print("- Coral-Bleaching-twS fired")
        print(' ', RuleRef('t'), RuleRef('w'), RuleRef('s'))

##Ecoforecast Rule #10: Coral-Bleaching-w3A
##Description: Mass coral bleaching (high in-situ sea temperature + doldrums)
    @Rule(windsp3day(fuzzyI=anyof('dLow', 'vLow', 'Low')),
            windsp3day(fuzzyTod=W()),
            seandbc(fuzzyI=anyof('High', 'vHigh', 'dHigh')),
            seandbc(fuzzyTod=W()))
    def mcb_w3A(self):
        print("- Coral-Bleaching-w3A fired")
        print(' ', RuleRef('w3'), RuleRef('a'))

##Ecoforecast Rule #11: Coral-Bleaching-PA
##Description: Mass coral bleaching (very high in-situ sea temperature + very high light)
    @Rule(parsurf(fuzzyI=anyof('vHigh', 'dHigh')),
            parsurf(fuzzyTod=anyof('midd', 'psun', 'dayl', 'aftn', 'all')),
            seandbc(fuzzyI=anyof('vHigh', 'dHigh')),
            seandbc(fuzzyTod=W()))
    def mcb_PA(self):
        print("- Coral-Bleaching-PA fired")
        print(' ', RuleRef('p'), RuleRef('a'))

##Ecoforecast Rule #12: Coral-Bleaching-wA
##Description: Mass coral bleaching (very high in-situ sea temperature + very low wind)
    @Rule(windsp(fuzzyI=anyof('dLow', 'vLow')),
            windsp(fuzzyTod=anyof('morn', 'midd', 'psun', 'dayl', 'dayb', 'aftn', 'all')),
            seandbc(fuzzyI=anyof('vHigh', 'dHigh')),
            seandbc(fuzzyTod=W()))
    def mcb_wA(self):
        print("- Coral-Bleaching-wA fired")
        print( ' ',RuleRef('w'), RuleRef('a'))

##Ecoforecast Rule #13: Coral-Bleaching-w3E
##Description: Mass coral bleaching (high 'shallow' sea temperature + doldrums)
    @Rule(windsp3day(fuzzyI=anyof('dLow', 'vLow', 'Low')),
            windsp3day(fuzzyTod=W()),
            sea1m(fuzzyI=anyof('High', 'dHigh', 'vHigh')),
            sea1m(fuzzyTod=W()))
    def mcb_w3E(self):
        print("- Coral-Bleaching-w3E fired")
        print(' ', RuleRef('w3'), RuleRef('e'))

##Ecoforecast Rule #14: Coral-Bleaching-PE
##Description: Mass coral bleaching (very high 'shallow' sea temperature + very high light)
    @Rule(parsurf(fuzzyI=anyof('vHigh', 'dHigh')),
            parsurf(fuzzyTod=anyof('midd', 'dayl', 'all')),
            sea1m(fuzzyI=anyof('vHigh', 'dHigh')),
            sea1m(fuzzyTod=W()))
    def mcb_PE(self):
        print("- Coral-Bleaching-PE fired")
        print(' ', RuleRef('p'), RuleRef('e'))

##Ecoforecast Rule #15: Coral-Bleaching-wE
##Description: Mass coral bleaching (very high 'shallow' sea temperature + very low wind)
    @Rule(windsp(fuzzyI=anyof('dLow', 'vLow')),
            windsp(fuzzyTod=anyof('morn', 'midd', 'psun', 'dayl', 'dayb', 'aftn', 'all')),
            sea1m(fuzzyI=anyof('vHigh', 'dHigh')),
            sea1m(fuzzyTod=W()))
    def mcb_wE(self):
        print("- Coral-Bleaching-wE fired")
        print(' ', RuleRef('w'), RuleRef('e'))

##Ecoforecast Rule #16: Coral-Bleaching-PS
##Description: Mass coral bleaching (very high SST + very high light)
    @Rule(parsurf(fuzzyI=anyof('vHigh', 'dHigh')),
            parsurf(fuzzyTod=anyof('midd', 'dayl', 'all')),
            sst(fuzzyI=anyof('vHigh', 'dHigh')),
            sst(fuzzyTod=W()))
    def mcb_PS(self):
        print("- Coral-Bleaching-PS fired")
        print(' ', RuleRef('p'), RuleRef('s'))

##Ecoforecast Rule #17: Coral-Bleaching-wS
##Description: Mass coral bleaching (very high SST + very low wind)
    @Rule(windsp(fuzzyI=anyof('dLow', 'vLow')),
            windsp(fuzzyTod=anyof('morn', 'midd', 'psun', 'dayl', 'dayb', 'aftn', 'all')),
            sst(fuzzyI=anyof('vHigh', 'dHigh')),
            sst(fuzzyTod=W()))
    def mcb_wS(self):
        print("- Coral-Bleaching-wS fired")
        print(' ', RuleRef('w'), RuleRef('s'))

##Ecoforecast Rule #18: Coral-Bleaching-B
##Description: Mass coral bleaching (Berkelmans bleaching curve)
    @Rule(curveB(fuzzyI=anyof('Conductive', 'vConductive')),
            curveB(fuzzyTod=W()))
    def mcb_B(self):
        print("- Coral-Bleaching-B fired")
        print(' ', RuleRef('b'))

##Ecoforecast Rule #19: Coral-Bleaching-A
##Description: Mass coral bleaching (drastic high in-situ sea temperature)
    @Rule(seandbc(fuzzyI=anyof('dHigh')),
            seandbc(fuzzyTod=W()))
    def mcb_A(self):
        print("- Coral-Bleaching-A fired")
        print(' ', RuleRef('a'))

##Ecoforecast Rule #20: Coral-Bleaching-BB
##Description: Mass coral mortality (>50%) for local sensitive species (Berkelmans)
    @Rule(curveB(fuzzyI=anyof('Mortality', 'hMortality')),
            curveB(fuzzyTod=W()))
    def mcb_BB(self):
        print("- Coral-Bleaching-BB fired")
        print(' ', RuleRef('b'))

##Ecoforecast Rule #21: Coral-Bleaching-EM
##Description: Mass coral bleaching (high monthly mean 'shallow' sea temperature)
    @Rule(sea1mM(fuzzyI=anyof('High', 'vHigh', 'dHigh')),
            sea1mM(fuzzyTod=W()))
    def mcb_EM(self):
        print("- Coral-Bleaching-EM fired")
        print(' ', RuleRef('eM'))

##Ecoforecast Rule #22: Coral-Bleaching-AM
##Description: Mass coral bleaching (high monthly mean in situ sea temperature)
    @Rule(seandbcM(fuzzyI=anyof('High', 'vHigh', 'dHigh')),
            seandbcM(fuzzyTod=W()))
    def mcb_AM(self):
        print("- Coral-Bleaching-AM fired")
        print(' ', RuleRef('aM'))

##Ecoforecast Rule #23: Coral-Bleaching-E
##Description: Mass coral bleaching (drastic high 'shallow' sea temperature)
    @Rule(sea1m(fuzzyI=L('dHigh')),
            sea1m(fuzzyTod=W()))
    def mcb_E(self):
        print("- Coral-Bleaching-E fired")
        print( ' ',RuleRef('e'))

##Ecoforecast Rule #24: Coral-Bleaching-S
##Description: Mass coral bleaching (drastic high SST)
    @Rule(sst(fuzzyI=L('dHigh')),
            sst(fuzzyTod=W()))
    def mcb_S(self):
        print("- Coral-Bleaching-S fired")
        print(' ', RuleRef('s'))




def knowledge_engine( factlist):
    e= MCB()
    e.reset()
    for f in factlist:
        e.declare( f)
    embed()
    e.run()
