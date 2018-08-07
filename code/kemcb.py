#!/usr/bin/env python3

###mcb Ecoforecast prototype goal is to implement rules base from http://ecoforecast.coral.noaa.gov/index/0/MLRF1/model-detail&name=MASS-CORAL-BLEACHING and 'print' a forecast###

__author__= "Madison Soden"
__date__= "Tue Aug 07, 2018  03:03PM"
__license__= "NA?"
__email__= "madison.soden@gmail.com"
__status__= "Production"


############################################################################################???????????????????????????? rule 18 verse rule 20 supposed to call different facts???????????????????????

import pyknow as pk
from IPython import embed
import fact

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
    # 'pre-sunset' - 'psun' - 1800 to 21:00
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
    return pk.P(lambda y: y in values)


class MCB( pk.KnowledgeEngine):

    def retract(self, idx_or_declared_fact):
        """
        Retracts a specific fact, using its index
        .. note::
            This updates the agenda
        """
        self.facts.retract(idx_or_declared_fact)

        #if not self.running:
        added, removed = self.get_activations()
        self.strategy.update_agenda(self.agenda, added, removed)


#initial instruction output
    def display(self): 
        print('\n',
            '----------------------------------------------------------------------\n',
            'To declare Knowledge Engine:\n',
            '>> e = mcb.MCB()\n',
            '>> e.reset()\n',
            '\n\n',
            'To add facts to fact list call:\n',
            '>> e.declare_facts()\n',
            '>> e.declare_facts(\'factname\', \'fuzzyI\', \'fuzzyTod\', \'date\', \'locus\')\n',
            '\n\n',
            'To import a fact csv call:\n',
            '>> e.import_facts(\'./test_suite/fact_CSVs/testX.csv\')\n',
            '\n\n',
            'To view current rule base call:\n',
            '>> e.get_rules()\n',
            '\n\n',
            'To view rule nomenclature reference call:\n',
            '>> mcb.printRuleRef()\n',
            '\n\n',
            'To view current fact base call:\n',
            '>> e.facts\n',
            '\n\n',
            'To run Knowledge Engine call:\n',
            '>> e.run()\n',
            '----------------------------------------------------------------------\n',
            '\n  \n \n\n')

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
    @pk.Rule(pk.OR(fact.sst(fuzzyI='uLow'), fact.sst(fuzzyI='uHigh')))
    def u_fI_sst(self):
        print("sst values in unbelievable range")

    @pk.Rule(pk.OR(fact.windsp(fuzzyI='uLow'), fact.windsp(fuzzyI='uHigh')))
    def u_fI_windsp(self):
        print("wind scalar values in unbelievable range")

    @pk.Rule(pk.OR(fact.seandbc(fuzzyI='uLow'), fact.seandbc(fuzzyI='uHigh')))
    def u_fI_seandbc(self):
        print("seandbc values in unbelievable range")

    @pk.Rule(pk.OR(fact.parsurf(fuzzyI='uLow'), fact.parsurf(fuzzyI='uHigh')))
    def u_fI_parsurf(self):
        print("parsurf values in unbelievable range")

    @pk.Rule(pk.OR(fact.tide1m(fuzzyI='uLow'), fact.tide1m(fuzzyI='uHigh')))
    def u_fI_tide1m(self):
        print("tide1m values in unbelievable range")

    @pk.Rule(pk.OR(fact.sea1m(fuzzyI='uLow'), fact.sea1m(fuzzyI='uHigh')))
    def u_fI_sea1m(self):
        print("sea1m values in unbelievable range")

    @pk.Rule(pk.OR(fact.seandbcM(fuzzyI='uLow'), fact.seandbcM(fuzzyI='uHigh')))
    def u_fI_seandbcM(self):
        print("seandbcM values in unbelievable range")

    @pk.Rule(pk.OR(fact.windsp3day(fuzzyI='uLow'), fact.windsp3day(fuzzyI='uHigh')))
    def u_fI_windsp3day(self):
        print("windsp3day values in unbelievable range")

    @pk.Rule(pk.OR(fact.sea1mM(fuzzyI='uLow'), fact.sea1mM(fuzzyI='uHigh')))
    def u_fI_sea1mM(self):
        print("sea1mM values in unbelievable range")

    @pk.Rule(pk.OR(fact.curveB(fuzzyI='uLow'), fact.curveB(fuzzyI='uHigh')))
    def u_fI_curveB(self):
        print("curveB values in unbelievable range")

#Missing info rules
    @pk.Rule( fact.sst(fuzzyI=~anyof('uLow', 'dLow', 'vLow', 'Low', 'sLow', 'average', 'sHigh', 'High', 'vHigh', 'dHigh', 'uHigh')))
    def m_fI_sst(self):
        print("missing or unreadable value for sst fuzzyI")

    @pk.Rule( fact.seandbc(fuzzyI=~anyof('uLow', 'dLow', 'vLow', 'Low', 'sLow', 'average', 'sHigh', 'High', 'vHigh', 'dHigh', 'uHigh')))
    def m_fI_seandbc(self):
        print("missing or unreadable value for seandbc fuzzyI")

    @pk.Rule( fact.parsurf(fuzzyI=~anyof('uLow', 'dLow', 'vLow', 'Low', 'sLow', 'average', 'sHigh', 'High', 'vHigh', 'dHigh', 'uHigh')))
    def m_fI_parsurf(self):
        print("missing or unreadable value for parsurf fuzzyI")

    @pk.Rule(fact.windsp( fuzzyI=~anyof('uLow', 'dLow', 'vLow', 'Low', 'sLow', 'average', 'sHigh', 'High', 'vHigh', 'dHigh', 'uHigh')))
    def m_fI_windsp(self):
        print("missing or unreadable value for windsp fuzzyI")

    @pk.Rule(fact.tide1m(fuzzyI=~anyof('uLow', 'dLow', 'vLow', 'Low', 'sLow', 'average', 'sHigh', 'High', 'vHigh', 'dHigh', 'uHigh')))
    def m_fI_tide1m(self):
        print("missing or unreadable value for tide1m fuzzyI")

    @pk.Rule(fact.sea1m(fuzzyI=~anyof('uLow', 'dLow', 'vLow', 'Low', 'sLow', 'average', 'sHigh', 'High', 'vHigh', 'dHigh', 'uHigh')))
    def m_fI_sea1m(self):
        print("missing or unreadable value for sea1m fuzzyI")

    @pk.Rule(fact.seandbcM(fuzzyI=~anyof('uLow', 'dLow', 'vLow', 'Low', 'sLow', 'average', 'sHigh', 'High', 'vHigh', 'dHigh', 'uHigh')))
    def m_fI_seandbcM(self):
        print("missing or unreadable value for seandbcM fuzzyI")

    @pk.Rule(fact.curveB(fuzzyI=~anyof('uLow', 'dLow','vLow', 'Low', 'sLow', 'average', 'sHigh', 'High', 'vHigh' ,'dHigh', 'uHigh')))
    def m_fI_curveB(self):
        print("missing or unreadable value for curveB fuzzyI")

    @pk.Rule( fact.sea1mM(fuzzyI=~anyof('uLow', 'dLow', 'vLow', 'Low', 'sLow', 'average', 'sHigh', 'High', 'vHigh', 'dHigh', 'uHigh')))
    def m_fI_sea1mM(self):
        print("missing or unreadable value for sea1mM fuzzyI")


#MCB MASS-CORAL-BLEACHING implementation (forecast model has 24 rules)
#Description: Mass bleaching of hard corals

##Ecoforecast Rule #1: Coral-Bleaching-PtwA
##Description: Mass coral bleaching (high in-situ sea temperature + high light + low wind + low tide)
    @pk.Rule(fact.parsurf( fuzzyI=anyof('High', 'vHigh', 'dHigh'), fuzzyTod=anyof('midd', 'psun', 'dayl', 'aftn', 'all'), I = pk.MATCH.parsurfI),
            fact.tide1m( fuzzyI=anyof('dLow', 'vLow', 'Low'), fuzzyTod=anyof('morn', 'midd', 'psun', 'dayl', 'dayb', 'aftn', 'all'), I = pk.MATCH.tide1mI),
            fact.windsp( fuzzyI=anyof('dLow', 'vLow', 'Low'), fuzzyTod=anyof('morn', 'midd', 'psun', 'dayl', 'dayb', 'aftn', 'all'), I= pk.MATCH.windspI),
            fact.seandbc( fuzzyI=anyof('High', 'vHigh', 'dHigh'), fuzzyTod=pk.W(), I= pk.MATCH.seandbcI))
    def mcb_PtwA(self, parsurfI, tide1mI, windspI, seandbcI):
        print("- Coral-Bleaching-PtwA fired")
        print(' ', RuleRef('p')+'intensity= '+parsurfI,\
                RuleRef('t')+'intensity= '+tide1mI,\
                RuleRef('w')+'intensity= '+windspI,\
                RuleRef('a')+'intensity= '+seandbcI)

##Ecoforecast Rule #2: Coral-Bleaching-PtwE
##Description: Mass coral bleaching (high 'shallow' sea temperature + high light + low wind + low tide)
    @pk.Rule(fact.parsurf( fuzzyI=anyof('High', 'vHigh', 'dHigh'), fuzzyTod=anyof('midd', 'dayl', 'all'), I= pk.MATCH.parsurfI),
            fact.tide1m( fuzzyI=anyof('dLow', 'vLow', 'Low'), fuzzyTod=anyof('morn', 'midd', 'psun', 'dayl', 'dayb', 'aftn', 'all'), I= pk.MATCH.tide1mI),
            fact.windsp( fuzzyI=anyof('dLow', 'vLow', 'Low'), fuzzyTod=anyof('morn', 'midd', 'psun', 'dayl', 'dayb', 'aftn', 'all'), I= pk.MATCH.windspI),
            fact.sea1m( fuzzyI=anyof('High', 'vHigh', 'dHigh'), fuzzyTod=pk.W(), I = pk.MATCH.sea1mI))
    def mcb_PtwE(self, parsurfI, tide1mI, windspI, sea1mI):
        print("- Coral-Bleaching-PtwE fired")
        print(' ', RuleRef('p') +' intensity= '+parsurfI,\
                RuleRef('t')+ 'intensity= '+ tide1mI,\
                RuleRef('w')+ 'intensity= '+ windspI,\
                RuleRef('e')+ 'intensity= '+ sea1mI)

##Ecoforecast Rule #3: Coral-Bleaching-PtwS
##Description: Mass coral bleaching (high SST + high light + low wind + low tide)
    @pk.Rule(fact.parsurf(fuzzyI=anyof('High', 'vHigh', 'dHigh'), fuzzyTod=anyof('midd', 'dayl', 'all'), I= pk.MATCH.parsurfI),
            fact.tide1m( fuzzyI=anyof('dLow', 'vLow', 'Low'), fuzzyTod=anyof('morn', 'midd', 'psun', 'dayl', 'dayb', 'aftn', 'all'), I= pk.MATCH.tide1mI),
            fact.windsp( fuzzyI=anyof('dLow', 'vLow', 'Low'), fuzzyTod=anyof('morn', 'midd', 'psun', 'dayl', 'dayb', 'aftn', 'aftn', 'all'), I= pk.MATCH.windspI),
            fact.sst( fuzzyI=anyof('High', 'vHigh', 'dHigh'), fuzzyTod=pk.W(), I= pk.MATCH.sstI))
    def mcb_PtwS(self, parsurfI, tide1mI, windspI, sstI):
        print("- Coral-Bleaching-Tlwt fired")
        print(' ', RuleRef('t'), RuleRef('l'), RuleRef('w'),
                RuleRef('t'))

##Ecoforecast Rule #4: Coral-Bleaching-PwA
## Description: Mass coral bleaching (high in-situ sea temperature + high light + low wind)
    @pk.Rule(fact.parsurf( fuzzyI=anyof('High', 'vHigh', 'dHigh'), fuzzyTod=anyof('midd', 'psun', 'dayl', 'aftn', 'all'), I= pk.MATCH.parsurfI),
            fact.windsp( fuzzyI=anyof('dLow', 'vLow', 'Low'), fuzzyTod=anyof('morn', 'midd', 'psun', 'dayl', 'dayb', 'aftn', 'all'), I= pk.MATCH.windspI),
            fact.seandbc( fuzzyI=anyof('High', 'vHigh', 'dHigh'), fuzzyTod=pk.W(), I= pk.MATCH.seandbcI))
    def mcb_PwA(self, parsurfI, windspI, seandbcI):
        print("- Coral-Bleaching-PwA fired")
        print(' ', RuleRef('p'), RuleRef('w'), RuleRef('a'))

##Ecoforecast Rule #5: Coral-Bleaching-twA
##Description: Mass coral bleaching (high in-situ sea temperature + low wind + low tide)
    @pk.Rule(fact.tide1m( fuzzyI=anyof('dLow', 'vLow', 'low'), fuzzyTod=anyof('morn', 'midd', 'psun', 'dayl', 'dayb', 'aftn', 'all'), I= pk.MATCH.tide1mI),
            fact.windsp( fuzzyI=anyof('dLow', 'vLow', 'Low'), fuzzyTod=anyof('morn', 'midd', 'psun', 'day', 'dayb', 'aftn', 'all'),  I= pk.MATCH.windspI),
            fact.seandbc( fuzzyI=anyof('High', 'vHigh', 'dHigh'), fuzzyTod=pk.W(), I= pk.MATCH.seandbcI))
    def mcb_twA(self, tide1mI, windspI, seandbcI):
        print("- Coral-Bleaching-twA")
        print(' ', RuleRef('t'), RuleRef('w'), RuleRef('a'))

##Ecoforecast Rule #6: Coral-Bleaching-PwE
##Description: Mass coral bleaching (high 'shallow' sea temperature + high light + low wind)
    @pk.Rule(fact.parsurf( fuzzyI=anyof('High', 'vHigh', 'dHigh'), fuzzyTod=anyof('midd', 'dayl', 'all'), I= pk.MATCH.parsurfI),
            fact.windsp( fuzzyI=anyof('dLow', 'vLow', 'Low'), fuzzyTod=anyof('morn', 'midd', 'psun', 'dayl', 'dayb', 'aftn', 'all'), I= pk.MATCH.windspI),
            fact.sea1m( fuzzyI=anyof('High', 'vHigh', 'dHigh'), fuzzyTod=pk.W(), I= pk.MATCH.sea1mI))
    def mcb_PwE(self, parsurfI, windspI, sea1mI):
        print("- Coral-Bleaching-PwE fired")
        print(' ', RuleRef('p'), RuleRef('w'), RuleRef('e'))

##Ecoforecast Rule #7: Coral-Bleaching-twE
##Description: Mass coral bleaching (high 'shallow' sea temperature + low wind + low tide)
    @pk.Rule(fact.tide1m( fuzzyI=anyof('dLow', 'vLow', 'Low'), fuzzyTod=anyof('morn', 'midd', 'psun', 'dayl', 'dayb', 'aftn', 'all'), I= pk.MATCH.tide1mI),
            fact.windsp( fuzzyI=anyof('dLow', 'vLow', 'Low'), fuzzyTod=anyof('morn', 'midd', 'psun', 'dayl', 'dayb', 'aftn', 'all'), I= pk.MATCH.windspI),
            fact.sea1m( fuzzyI=anyof('High', 'vHigh', 'dHigh'), fuzzyTod=pk.W(), I= pk.MATCH.sea1mI))
    def mcb_twE(self, tide1mI, windspI, sea1mI):
        print("- Coral-Bleaching-twE fired")
        print(' ', RuleRef('t'), RuleRef('w'), RuleRef('e'))


##Ecoforecast Rule #8: Coral-Bleaching-PwS
##Description: Mass coral bleaching (high SST + high light + low wind)
    @pk.Rule(fact.parsurf( fuzzyI=anyof('High', 'vHigh', 'dHigh'), fuzzyTod=anyof('midd', 'dayl', 'all'), I= pk.MATCH.parsurfI),
            fact.windsp( fuzzyI=anyof('dLow', 'vLow', 'Low'), fuzzyTod=anyof('morn', 'midd', 'psun', 'dayl', 'dayb', 'aftn', 'all'),  I= pk.MATCH.windspI),
            fact.sst( fuzzyI=anyof('High', 'vHigh', 'dHigh'), fuzzyTod=pk.W(), I= pk.MATCH.sstI))
    def mcb_PwS(self, parsurfI, windspI, sstI):
        print("- Coral-Bleaching-PwS fired")
        print(' ', RuleRef('p'), RuleRef('w'), RuleRef('s'))

##Ecoforecast Rule #9: Coral-Bleaching-twS
##Description: Mass coral bleaching (high SST + low wind + low tide)
    @pk.Rule(fact.tide1m( fuzzyI=anyof('dLow', 'vLow', 'Low'), fuzzyTod=anyof('morn', 'midd', 'psun', 'dayl', 'dayb', 'aftn', 'all'), I= pk.MATCH.tide1mI),
            fact.windsp( fuzzyI=anyof('dLow', 'vLow', 'Low'), fuzzyTod=anyof('morn', 'midd', 'psun', 'dayl', 'dayb', 'aftn', 'all'), I= pk.MATCH.windspI),
            fact.sst( fuzzyI=anyof('High', 'vHigh', 'dHigh'), fuzzyTod=pk.W(), I= pk.MATCH.sstI))
    def mcb_twS(self, tide1mI, windspI, sstI):
        print("- Coral-Bleaching-twS fired")
        print(' ', RuleRef('t'), RuleRef('w'), RuleRef('s'))

##Ecoforecast Rule #10: Coral-Bleaching-w3A
##Description: Mass coral bleaching (high in-situ sea temperature + doldrums)
    @pk.Rule(fact.windsp3day( fuzzyI=anyof('dLow', 'vLow', 'Low'), fuzzyTod=pk.W(), I= pk.MATCH.windsp3dayI),
            fact.seandbc( fuzzyI=anyof('High', 'vHigh', 'dHigh'), fuzzyTod=pk.W(), I= pk.MATCH.seandbcI))
    def mcb_w3A(self, windsp3dayI, seandbcI):
        print("- Coral-Bleaching-w3A fired")
        print(' ', RuleRef('w3'), RuleRef('a'))

##Ecoforecast Rule #11: Coral-Bleaching-PA
##Description: Mass coral bleaching (very high in-situ sea temperature + very high light)
    @pk.Rule(fact.parsurf(fuzzyI=anyof('vHigh', 'dHigh'), fuzzyTod=anyof('midd', 'psun', 'dayl', 'aftn', 'all'), I= pk.MATCH.parsurfI),
            fact.seandbc(fuzzyI=anyof('vHigh', 'dHigh'), fuzzyTod=pk.W(), I= pk.MATCH.seandbcI))
    def mcb_PA(self, parsurfI, seandbcI):
        print("- Coral-Bleaching-PA fired")
        print(' ', RuleRef('p'), RuleRef('a'))

##Ecoforecast Rule #12: Coral-Bleaching-wA
##Description: Mass coral bleaching (very high in-situ sea temperature + very low wind)
    @pk.Rule(fact.windsp( fuzzyI=anyof('dLow', 'vLow'), fuzzyTod=anyof('morn', 'midd', 'psun', 'dayl', 'dayb', 'aftn', 'all'), I= pk.MATCH.windspI),
            fact.seandbc( fuzzyI=anyof('vHigh', 'dHigh'), fuzzyTod=pk.W(), I= pk.MATCH.seandbcI))
    def mcb_wA(self, windspI, seandbcI):
        print("- Coral-Bleaching-wA fired")
        print( ' ',RuleRef('w'), RuleRef('a'))
        #self.halt()
        #embed()
        #for i in self.agenda.activations[0].facts:
        #    self.retract(i)
        #self.activation = None

##Ecoforecast Rule #13: Coral-Bleaching-w3E
##Description: Mass coral bleaching (high 'shallow' sea temperature + doldrums)
    @pk.Rule(fact.windsp3day(fuzzyI=anyof('dLow', 'vLow', 'Low'), fuzzyTod=pk.W(), I= pk.MATCH.windsp3dayI),
            fact.sea1m( fuzzyI=anyof('High', 'dHigh', 'vHigh'), fuzzyTod=pk.W(), I= pk.MATCH.sea1mI))
    def mcb_w3E(self, windsp3dayI, sea1mI):
        print("- Coral-Bleaching-w3E fired")
        print(' ', RuleRef('w3'), RuleRef('e'))

##Ecoforecast Rule #14: Coral-Bleaching-PE
##Description: Mass coral bleaching (very high 'shallow' sea temperature + very high light)
    @pk.Rule(fact.parsurf(fuzzyI=anyof('vHigh', 'dHigh'), fuzzyTod=anyof('midd', 'dayl', 'all'),  I= pk.MATCH.parsurfI),
            fact.sea1m( fuzzyI=anyof('vHigh', 'dHigh'), fuzzyTod=pk.W(), I= pk.MATCH.sea1mI))
    def mcb_PE(self, parsurfI, sea1mI):
        print("- Coral-Bleaching-PE fired")
        print(' ', RuleRef('p'), RuleRef('e'))

##Ecoforecast Rule #15: Coral-Bleaching-wE
##Description: Mass coral bleaching (very high 'shallow' sea temperature + very low wind)
    @pk.Rule(fact.windsp(fuzzyI=anyof('dLow', 'vLow'), fuzzyTod=anyof('morn', 'midd', 'psun', 'dayl', 'dayb', 'aftn', 'all'), I= pk.MATCH.windspI),
            fact.sea1m(fuzzyI=anyof('vHigh', 'dHigh'), fuzzyTod=pk.W(), I= pk.MATCH.sea1mI))
    def mcb_wE(self, windspI, sea1mI):
        print("- Coral-Bleaching-wE fired")
        print(' ', RuleRef('w'), RuleRef('e'))

##Ecoforecast Rule #16: Coral-Bleaching-PS
##Description: Mass coral bleaching (very high SST + very high light)
    @pk.Rule(fact.parsurf(fuzzyI=anyof('vHigh', 'dHigh'), fuzzyTod=anyof('midd', 'dayl', 'all'), I= pk.MATCH.parsurfI),
            fact.sst(fuzzyI=anyof('vHigh', 'dHigh'), fuzzyTod=pk.W(), I= pk.MATCH.sstI))
    def mcb_PS(self, parsurfI, sstI):
        print("- Coral-Bleaching-PS fired")
        print(' ', RuleRef('p'), RuleRef('s'))

##Ecoforecast Rule #17: Coral-Bleaching-wS
##Description: Mass coral bleaching (very high SST + very low wind)
    @pk.Rule(fact.windsp(fuzzyI=anyof('dLow', 'vLow'), fuzzyTod=anyof('morn', 'midd', 'psun', 'dayl', 'dayb', 'aftn', 'all'), I= pk.MATCH.windspI),
            fact.sst(fuzzyI=anyof('vHigh', 'dHigh'), fuzzyTod=pk.W(), I= pk.MATCH.sstI))
    def mcb_wS(self, windspI, sstI):
        print("- Coral-Bleaching-wS fired")
        print(' ', RuleRef('w'), RuleRef('s'))

##Ecoforecast Rule #18: Coral-Bleaching-B
##Description: Mass coral bleaching (Berkelmans bleaching curve)
    @pk.Rule(fact.curveB(fuzzyI=anyof('Conductive', 'vConductive'), fuzzyTod=pk.W(), I= pk.MATCH.curveBI))
    def mcb_B(self, curveBI):
        print("- Coral-Bleaching-B fired")
        print(' ', RuleRef('b'))

##Ecoforecast Rule #19: Coral-Bleaching-A
##Description: Mass coral bleaching (drastic high in-situ sea temperature)
    @pk.Rule(fact.seandbc( fuzzyI=anyof('dHigh'), fuzzyTod=pk.W(), I= pk.MATCH.seandbcI))
    def mcb_A(self, seandbcI):
        print("- Coral-Bleaching-A fired")
        print(' ', RuleRef('a'))

##Ecoforecast Rule #20: Coral-Bleaching-BB
##Description: Mass coral mortality (>50%) for local sensitive species (Berkelmans)
    @pk.Rule(fact.curveB(fuzzyI=anyof('Mortality', 'hMortality'), fuzzyTod=pk.W(), I= pk.MATCH.curveBI)) 
    def mcb_BB(self, curveBI):
        print("- Coral-Bleaching-BB fired")
        print(' ', RuleRef('b'))

##Ecoforecast Rule #21: Coral-Bleaching-EM
##Description: Mass coral bleaching (high monthly mean 'shallow' sea temperature)
    @pk.Rule(fact.sea1mM(fuzzyI=anyof('High', 'vHigh', 'dHigh'), fuzzyTod=pk.W(), I= pk.MATCH.sea1mMI))
    def mcb_EM(self, sea1mMI):
        print("- Coral-Bleaching-EM fired")
        print(' ', RuleRef('eM'))

##Ecoforecast Rule #22: Coral-Bleaching-AM
##Description: Mass coral bleaching (high monthly mean in situ sea temperature)
    @pk.Rule(fact.seandbcM(fuzzyI=anyof('High', 'vHigh', 'dHigh'), fuzzyTod=pk.W(), I= pk.MATCH.seandbcMI))
    def mcb_AM(self, seandbcMI):
        print("- Coral-Bleaching-AM fired")
        print(' ', RuleRef('aM'))

##Ecoforecast Rule #23: Coral-Bleaching-E
##Description: Mass coral bleaching (drastic high 'shallow' sea temperature)
    @pk.Rule(fact.sea1m(fuzzyI=pk.L('dHigh'), fuzzyTod=pk.W(), I= pk.MATCH.sea1mI))
    def mcb_E(self, sea1mI):
        print("- Coral-Bleaching-E fired")
        print( ' ',RuleRef('e'))

##Ecoforecast Rule #24: Coral-Bleaching-S
##Description: Mass coral bleaching (drastic high SST)
    @pk.Rule(fact.sst(fuzzyI=pk.L('dHigh'), fuzzyTod=pk.W(), I= pk.MATCH.sstI))
    def mcb_S(self, sstI):
        print("- Coral-Bleaching-S fired")
        print(' ', RuleRef('s'))
#        self.halt()
#        for i in self.agenda.activations[0].facts:
#            self.retract(i)




def knowledge_engine( factlist):
    e= MCB()
    e.reset()
    for f in factlist:
        e.declare( f)
    print('Call e.display() for help')
    embed()
    e.run()
