###mcb Ecoforecast prototype goal is to implement rules base from http://ecoforecast.coral.noaa.gov/index/0/MLRF1/model-detail&name=MASS-CORAL-BLEACHING and 'print' a forecast###
__author__ = "Madison Soden"
__date__ = "Thu Jan 18 15:28:22 2018"
__license__ = "NA?"
__version__ = "mcb"
__email__ = "madison.soden@gmail.com"
__status__ = "Production"



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
    print("""\n
        ----------------------------------------------------------------------
        To declare Knowledge Engine:
        >> e = mcb.MCB()
        >> e.reset()
        \n
        To add facts to fact list call:
        >> e.declare_facts()
        \n
        To view current rule base call:
        >> e.get_rules()
        \n
        To view current fact base call:
        >> e.facts
        \n
        To run Knowledge Engine call:
        >> e.run()
        ----------------------------------------------------------------------
         \n \n \n""")

#function to pipe pyknow e.fact output into something legible
    def print_facts(self):
        giantstring = e.fact
        giantstring = giantstring.strip('FactList([')
        giantstring = giantstring.strip(]))
        giantstringlines = giantstring.split("), (")
        while giantstringlines:
            factstring = giantstringlines.pop(0)
            print(factstring, "\n")

#test functions to initialize specific combinations of facts
    def import_facts(self, filename='./test_suite/fact_CSVs/test1.csv'):
        factlines= [x.rstrip('\n') for x in open(filename)]
        while factlines:
            factString = factlines.pop(0)
            factName, factFuzzyI, factFuzzyTod, factDate, factLocus = factString.split(",")
            print("DECLARED: ", factName, " ", factFuzzyI, " ", factFuzzyTod, " ",
                    factDate, " ", factLocus, "\n")
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
#Unbelievable or missing info Rules
    @Rule(OR(sst(fuzzyI='uLow'), sst(fuzzyI='uHigh')))
    def u1(self):
        print("sst values in unbelievable range")

    @Rule(OR(windsp(fuzzyI='uLow'), windsp(fuzzyI='uHigh')))
    def u2(self):
        print("wind scalar values in unbelievable range")

    @Rule(NOT(sst(fuzzyI= L('uLow') | L('dLow') | L('vLow') | L('Low') | L('sLow') |
        L('average') | L('sHigh') | L('High') | L('vHigh') | L('dHigh') |
        ('uHigh'))))
    def m1(self):
        print("missing or unreadable value for sst fuzzyI")

    @Rule(NOT(windsp(fuzzyI= L('uLow') | L('dLow') | L('vLow') | L('Low') | L('sLow') |
        L('average') | L('sHigh') | L('High') | L('vHigh') | L('dHigh') |
        L('uHigh'))))
    def m2(self):
        print("missing or unreadable value for windsp fuzzyI")

#MCB MASS-CORAL-BLEACHING implementation (forecast model has 24 rules)
#Description: Mass bleaching of hard corals

##Ecoforecast Rule #1: Coral-Bleaching-Itlwt
##Description: Mass coral bleaching (high in-situ sea temperature + high light + low wind + low tide)
    @Rule(parsurf(fuzzyI=L('High') | L('vHigh') | L('dHigh')),
            parsurf(fuzzyTod=L('midd') | L('psun') | L('dayl') | L('aftn') | L('all')),
            tide1m(fuzzyI=L('dLow') | L('vLow') | L('Low')),
            tide1m(fuzzyTod=L('morn') | L('midd') | L('psun') | L('dayl') |
                L('dayb') | L('aftn') | L('all')),
            windsp(fuzzyI=L('dLow') | L('vLow') | L('Low')),
            windsp(fuzzyTod=L('morn') | L('midd') | L('psun') | L('dayl') |
                L('dayb') | L('aftn') | L('all')),
            seandbc(fuzzyI=L('High') | L('vHigh') | L('dHigh')),
            seandbc(fuzzyTod=W()))
    def mcb1(self):
        print("Coral-Bleaching-Itlwt fired")

##Ecoforecast Rule #2: Coral-Bleaching-Stlwt
##Description: Mass coral bleaching (high 'shallow' sea temperature + high light + low wind + low tide)
    @Rule(parsurf(fuzzyI=L('High') | L('vHigh') | L('dHigh')), 
            parsurf(fuzzyTod=L('midd') | L('dayl') | L('all')),
            tide1m(fuzzyI=L('dLow') | L('vLow') | L('Low')),
            tide1m(fuzzyTod=L('morn') | L('midd') | L('psun') | L('dayl') |
                L('dayb') | L('aftn') | L('all')),
            windsp(fuzzyI=L('dLow') | L('vLow') | L('Low')),
            windsp(fuzzyTod=L('morn') | L('midd') | L ('psun') | L('dayl') |
                L('dayb') | L('aftn') | L('all')),
            sea1m(fuzzyI=L('High') | L('vHigh') | L('dHigh')),
            sea1m(fuzzyTod=W()))
    def mcb2(self):
        print("Coral-Bleaching-Stlwt fired")

##Ecoforecast Rule #3: Coral-Bleaching-Tlwt
##Description: Mass coral bleaching (high SST + high light + low wind + low tide)
    @Rule(parsurf(fuzzyI=L('High') | L('vHigh') | L('dHigh')),
            parsurf(fuzzyTod=L('midd') | L('dayl') | L('all')),
            tide1m(fuzzyI=L('dLow') | L('vLow') | L('Low')),
            tide1m(fuzzyTod=L('morn') | L('midd') | L('psun') | L('dayl') |
                L('dayb') | L('aftn') | L('all')),
            windsp(fuzzyI=L('dLow') | L('vLow') | L('Low')),
            windsp(fuzzyTod=L('morn') | L('midd') | L('psun') | L('dayl') |
                L('dayb') | L('aftn') | L('aftn') | L('all')),
            sst(fuzzyI=L('High') | L('vHigh') | L('dHigh')),
            sst(fuzzyTod=W()))
    def mcb3(self):
        print("Coral-Bleaching-Tlwt fired")

##Ecoforecast Rule #4: Coral-Bleaching-Itlw
## Description: Mass coral bleaching (high in-situ sea temperature + high light + low wind)
    @Rule(parsurf(fuzzyI=L('High') | L('vHigh') | L('dHigh')),
            parsurf(fuzzyTod=L('midd') | L('psun') | L('dayl') | L('aftn') |
                L('all')),
            windsp(fuzzyI=L('dLow') | L('vLow') | L('Low')),
            windsp(fuzzyTod=L('morn') | L('midd') | L('psun') | L('dayl') |
                L('dayb') | L('aftn') | L('all')),
            seandbc(fuzzyI=L('High') | L('vHigh') | L('dHigh')),
            seandbc(fuzzyTod=W()))
    def mcb4(self):
        print("Coral-Bleaching-Itlw fired")

##Ecoforecast Rule #5: Coral-Bleaching-Itwt
##Description: Mass coral bleaching (high in-situ sea temperature + low wind + low tide)
    @Rule(tide1m(fuzzyI=L('dLow') | L('vLow') | L('low')),
            tide1m(fuzzyTod=L('morn') | L('midd') | L('psun') | L('dayl') |
                L('dayb') | L('aftn') | L('all')),
            windsp(fuzzyI=L('dLow') | L('vLow') | L('Low')),
            windsp(fuzzyTod=L('morn') | L('midd') | L('psun') | L('day') | L('dayb')
                | L('aftn') | L('all')),
            seandbc(fuzzyI=L('High') | L('vHigh') | L('dHigh')),
            seandbc(fuzzyTod=W()))
    def mcb5(self):
        print("Coral-Bleaching-Itwt")

##Ecoforecast Rule #6: Coral-Bleaching-Stlw
##Description: Mass coral bleaching (high 'shallow' sea temperature + high light + low wind)
    @Rule(parsurf(fuzzyI=L('High') | L('vHigh') | L('dHigh')),
            parsurf(fuzzyTod=L('midd') | L('dayl') | L('all')),
            windsp(fuzzyI=L('dLow') | L('vLow') | L('Low')),
            windsp(fuzzyTod=L('morn') | L('midd') | L('psun') | L('dayl') |
                L('dayb') | L('aftn') | L('all')),
            sea1m(fuzzyI=L('High') | L('vHigh') | L('dHigh')),
            sea1m(fuzzyTod=W()))
    def mcb6(self):
        print("Coral-Bleaching-Stlw fired")

##Ecoforecast Rule #7: Coral-Bleaching-Stwt
##Description: Mass coral bleaching (high 'shallow' sea temperature + low wind + low tide)
    @Rule(tide1m(fuzzyI=L('dLow') | L('vLow') | L('Low')),
            tide1m(fuzzyTod=L('morn') | L('midd') | L('psun') | L('dayl') |
                L('dayb') | L('aftn') | L('all')),
            windsp(fuzzyI=L('dLow') | L('vLow') | L('Low')),
            windsp(fuzzyTod=L('morn') | L('midd') | L('psun') | L('dayl') |
                L('dayb') | L('aftn') | L('all')),
            sea1m(fuzzyI=L('High') | L('vHigh') | L('dHigh')),
            sea1m(fuzzyTod=W()))
    def mcb7(self):
        print("Coral-Bleaching-Stwt fired")


##Ecoforecast Rule #8: Coral-Bleaching-Tlw
##Description: Mass coral bleaching (high SST + high light + low wind)
    @Rule(parsurf(fuzzyI=L('High') | L('vHigh') | L('dHigh')),
            parsurf(fuzzyTod=L('midd') | L('dayl') | L('all')),
            windsp(fuzzyI=L('dLow') | L('vLow') | L('Low')),
            windsp(fuzzyI=L('morn') | L('midd') | L('psun') | L('dayl') |
                L('dayb') | L('aftn') | L('all')),
            sst(fuzzyI=L('High') | L('vHigh') | L('dHigh')),
            sst(fuzzyTod=W()))
    def mcb8(self):
        print("Coral-Bleaching-Tlw fired")

##Ecoforecast Rule #9: Coral-Bleaching-Twt
##Description: Mass coral bleaching (high SST + low wind + low tide)
    @Rule(tide1m(fuzzyI=L('dLow') | L('vLow') | L('Low')),
            tide1m(fuzzyTod=L('morn') | L('midd') | L('psun') | L('dayl') |
                L('dayb') | L('aftn') | L('all')),
            windsp(fuzzyI=L('dLow') | L('vLow') | L('Low')),
            windsp(fuzzyTod=L('morn') | L('midd') | L('psun') | L('dayl') |
                L('dayb') | L('aftn') | L('all')),
            sst(fuzzyI=L('High') | L('vHigh') | L('dHigh')),
            sst(fuzzyTod=W()))
    def mcb9(self):
        print("Coral-Bleaching-Twt fired")

##Ecoforecast Rule #10: Coral-Bleaching-Itd
##Description: Mass coral bleaching (high in-situ sea temperature + doldrums)
    @Rule(windsp3day(fuzzyI=L('dLow') | L('vLow') | L('Low')),
            windsp3day(fuzzyTod=W()),
            seandbc(fuzzyI=L('High') | L('vHigh') | L('dHigh')),
            seandbc(fuzzyTod=W()))
    def mcb10(self):
        print("Coral-Bleaching-Itd fired")

##Ecoforecast Rule #11: Coral-Bleaching-Itl
##Description: Mass coral bleaching (very high in-situ sea temperature + very high light)
    @Rule(parsurf(fuzzyI=L('vHigh') | L('dHigh')),
            parsurf(fuzzyTod=L('midd') | L('psun') | L('dayl') | L('aftn') |
                L('all')),
            seandbc(fuzzyI=L('vHigh') | L('dHigh')),
            seandbc(fuzzyTod=W()))
    def mcb11(self):
        print("Coral-Bleaching-Itl fired")

##Ecoforecast Rule #12: Coral-Bleaching-Itw
##Description: Mass coral bleaching (very high in-situ sea temperature + very low wind)
    @Rule(windsp(fuzzyI=L('dLow') | L('vLow')),
            windsp(fuzzyTod=L('morn') | L('midd') | L('psun') | L('dayl') |
                L('dayb') | L('aftn') | L('all')),
            seandbc(fuzzyI=L('vHigh') | L('dHigh')),
            seandbc(fuzzyTod=W()))
    def mcb12(self):
        print("Coral-Bleaching-Itw fired")

##Ecoforecast Rule #13: Coral-Bleaching-Std
##Description: Mass coral bleaching (high 'shallow' sea temperature + doldrums)
    @Rule(windsp3day(fuzzyI=L('dLow') | L('vLow') | L('Low')),
            windsp3day(fuzzyTod=W()),
            sea1m(fuzzyI=L('High') | L('dHigh') | L('vHigh')),
            sea1m(fuzzyTod=W()))
    def mcb13(self):
        print("Coral-Bleaching-Std fired")

##Ecoforecast Rule #14: Coral-Bleaching-Stl
##Description: Mass coral bleaching (very high 'shallow' sea temperature + very high light)
    @Rule(parsurf(fuzzyI=L('vHigh') | L('dHigh')),
            parsurf(fuzzyTod=L('midd') | L('dayl') | L('all')),
            sea1m(fuzzyI=L('vHigh') | L('dHigh')),
            sea1m(fuzzyTod=W()))
    def mcb14(self):
        print("Coral-Bleaching-Stl fired")

##Ecoforecast Rule #15: Coral-Bleaching-Stw
##Description: Mass coral bleaching (very high 'shallow' sea temperature + very low wind)
    @Rule(windsp(fuzzyI=L('dLow') | L('vLow')),
            windsp(fuzzyTod=L('morn') | L('midd') | L('psun') | L('dayl') |
                L('dayb') | L('aftn') | L('all')),
            sea1m(fuzzyI=L('vHigh') | L('dHigh')),
            sea1m(fuzzyTod=W()))
    def mcb15(self):
        print("Coral-Bleaching-Stw fired")

##Ecoforecast Rule #16: Coral-Bleaching-Tl
##Description: Mass coral bleaching (very high SST + very high light)
    @Rule(parsurf(fuzzyI=L('vHigh') | L('dHigh')),
            parsurf(fuzzyTod=L('midd') | L('dayl') | L('all')),
            sst(fuzzyI=L('vHigh') | L('dHigh')),
            sst(fuzzyTod=W()))
    def mcb16(self):
        print("Coral-Bleaching-Tl fired")

##Ecoforecast Rule #17: Coral-Bleaching-Tw
##Description: Mass coral bleaching (very high SST + very low wind)
    @Rule(windsp(fuzzyI=L('dLow') | L('vLow')),
            windsp(fuzzyTod=L('morn') | L('midd') | L('psun') | L('dayl') |
                L('dayb') | L('aftn') | L('all')),
            sst(fuzzyI=L('vHigh') | L('dHigh')),
            sst(fuzzyTod=W()))
    def mcb17(self):
        print("Coral-Bleaching-Tw fired")

##Ecoforecast Rule #18: Coral-Bleaching-B
##Description: Mass coral bleaching (Berkelmans bleaching curve)
    @Rule(curveB(fuzzyI=L('Conductive') | L('vConductive')),
            curveB(fuzzyTod=W()))
    def mcb18(self):
        print("Coral-Bleaching-B fired")

##Ecoforecast Rule #19: Coral-Bleaching-It
##Description: Mass coral bleaching (drastic high in-situ sea temperature)
    @Rule(seandbc(fuzzyI=L('dHigh')),
            seandbc(fuzzyTod=W()))
    def mcb19(self):
        print("Coral-Bleaching-It fired")

##Ecoforecast Rule #20: Coral-Bleaching-Mort
##Description: Mass coral mortality (>50%) for local sensitive species (Berkelmans)
    @Rule(curveB(fuzzyI=L('Mortality') | L('hMortality')),
            curveB(fuzzyTod=W()))
    def mcb20(self):
        print("Coral-Bleaching-Mort fired")

##Ecoforecast Rule #21: Coral-Bleaching-Mst
##Description: Mass coral bleaching (high monthly mean 'shallow' sea temperature)
    @Rule(sea1mM(fuzzyI=L('High') | L('vHigh') | L('dHigh')),
            sea1mM(fuzzyTod=W()))
    def mcb21(self):
        print("Coral-Bleaching-Mst fired")

##Ecoforecast Rule #22: Coral-Bleaching-Mwt
##Description: Mass coral bleaching (high monthly mean in situ sea temperature)
    @Rule(seandbcM(fuzzyI=L('High') | L('vHigh') | L('dHigh')),
            seandbcM(fuzzyTod=W()))
    def mcb22(self):
        print("Coral-Bleaching-Mwt fired")

##Ecoforecast Rule #23: Coral-Bleaching-St
##Description: Mass coral bleaching (drastic high 'shallow' sea temperature)
    @Rule(sea1m(fuzzyI=L('dHigh')),
            sea1m(fuzzyTod=W()))
    def mcb23(self):
        print("Coral-Bleaching-St fired")

##Ecoforecast Rule #24: Coral-Bleaching-T
##Description: Mass coral bleaching (drastic high SST)
    @Rule(sst(fuzzyI=L('dHigh')),
            sst(fuzzyTod=W()))
    def mcb24(self):
        print("Coral-Bleaching-T fired")


