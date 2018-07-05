#!/Users/soden/ python

"""mcb0_6 Ecoforecast prototype goal is to implement rules base from http://ecoforecast.coral.noaa.gov/index/0/MLRF1/model-detail&name=MASS-CORAL-BLEACHING and 'print' a forecast"""

from pyknow import *
import numpy as np

__author__ = "Madison Soden"
__date__ = "Thur Dec 21 11:23:58 2017"
__license__ = "NA?"
__version__ = "mcb0_6"
__email__ = "madison.soden@gmail.com"
__status__ = "Production"

"""Fact Definition Documentation"""
    #rRange is a string containing a fuzzy (i.e. proxy) values for sst
    #key = 'rRange' / 0
    #fuzzy values can be 'uLow', 'dLow', 'vLow', 'Low', 'sLow', 'average', 'sHigh',
    # 'High', 'vHigh', 'dHigh', 'uHigh'
"""REWRITE TOD DOCUMENTATION"""
    #tod is a tuple of boolean values indicating a fuzzy time of day values for the- 
    # time rRange was recorded. Taken in eight 3 hour, then four 6 hour, then
    # two 12 hour , and one 24 hour time increments. TRUE indicates rRange was
    # recorded at that time. The 24 hour bool cannot be TRUE unless all
    # contained time increments are true. 
        #EG: tod=(0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0) to initialize
        #    tod[3] to access 4th item in array
        #    or tod.item[2][3] to access item row 3 column 4
    #key = 'tod' and/or 1
    #fuzzy values can be 'predawn'(12AM-2:59AM) tod[0],
    # 'dawn'(3AM-5:59AM) tod[1], 'morning'(6AM-8:59AM) tod[2], 
    # 'midday'(9AM-11:59AM) tod[3], 'evening'(12PM-2:59PM) tod[4],
    # 'presunset'(3PM-5:59PM) tod[5],'sunset'(6PM-8:59PM) tod[6],
    # 'midnight'(9PM-11:59PM) tod[7], 'early morning'(12AM-5:59AM)
    #  tod[8], 'late morning'(6AM-11:59AM) tod[9], 'early
    #  afternoon'(12PM-5:59PM) tod[10], 'late afternoon'(6PM-11:59PM)
    #  tod[11], 'early day'(12AM-11:59AM) tod[12], 'late
    #  day'(12PM-11:59PM) tod[13], and 'whole day'(12AM-11:59PM)
    #  tod[14]

    #date is a string containing the date that rRange was calculated on in DDMMYYYY
    #key = 'dateR' and/or 4


"""Fact declarations"""
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
#Mass Coral Bleaching Forecast

#initial instruction output
    print("""\n
        ----------------------------------------------------------------------
        To declare Knowledge Engine: 
        >> e = mcb0_1.GCoralBleaching() 
        >> e.reset() 
        \n
        To use test cases call: 
        >> e.likely_facts() 
        >> e.unlikely_facts() 
        >> e.verylikely_facts() 
        >> e.misinformed_facts()
        >> e.missing_facts()
        \n
        To manually insert facts into knowledge engine call:
        >> yield sst(rRange = 'value') 
        or 
        >> yield windsp(rRange = 'value') 
        rRange values are 'uLow', 'dLow', 'vLow', 'Low', 'sLow', 'average', 'sHigh',
        'High', 'vHigh', 'dHigh', and 'uHigh'
        \n
        To view current rule base call: 
        >> e.get_rules() 
        \n 
        To view current fact base call: 
        >> e.fact
        \n
        To run Knowledge Engine call: 
        >> e.run() 
        ----------------------------------------------------------------------
        \n \n \n""")

#test functions to initialize specific combinations of facts

    def test_tuple(self):
        self.declare(sst(rRange='High', tod=(1,0,0,1,1,0,1,0,1,0,1,0,0,0,1,0),
             numd=5, offset=0))

    def likely_facts(self):
        self.declare(sst(rRange='High', tod=(0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0), date='29112017'))
        self.declare(windsp(rRange='Low', tod=(0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0), date='29112017'))

    def unlikely_facts(self):
        self.declare(sst(rRange='average',  tod=(0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0), date='29112017'))
        self.declare(windsp(rRange='average', tod=(0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0), date='29112017')) 

    def verylikely_facts(self):
        self.declare(sst(rRange='vHigh', tod=(0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0), date='29112017'))
        self.declare(windsp(rRange='sLow', tod=(0, 0, 0, 1, 1, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0), date='29112017'))

    def misinformed_facts(self):
        self.declare(sst(rRange='uLow', tod=(0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0), date='29112017'))
        self.declare(windsp(rRange='uHigh', tod=(0, 0, 0, 1, 1, 0, 0, 0, 0, 0
            ,0, 0, 0, 0, 0, 0), date='29992017'))

    def missing_facts(self):
        self.declare(sst(rRange='sLow', tod='', date='29112017'))
        self.declare(windsp(rRange='', tod=(0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0), date=''))


#Rule production & alert printing

#example/reference rules
""" @Rule(sst(rRange='dLow'))
    def sst0(self):
        print("sst is drastically Low")

    @Rule(sst(rRange='High'), salience=1)
    def sst6(self):
        print("sst is high")

    @Rule(sst(rRange='High'), windsp(rRange='Low'))
    def c1(self):
        print(" Coral bleaching is likely")
"""

#other cases
    @Rule(OR(sst(rRange='uLow'), sst(rRange='uHigh')))
    def u1(self):
        print("sst values in unbelievable range")

    @Rule(OR(windsp(rRange='uLow'), windsp(rRange='uHigh')))
    def u2(self):
        print("wind scalar values in unbelievable range")

    @Rule(NOT(sst(rRange= L('uLow') | L('dLow') | L('vLow') | L('Low') | L('sLow') |
        L('average') | L('sHigh') | L('High') | L('vHigh') | L('dHigh') |
        ('uHigh'))))
    def m1(self):
        print("missing or unreadable value for sst rRange")

    @Rule(NOT(windsp(rRange= L('uLow') | L('dLow') | L('vLow') | L('Low') | L('sLow') |
        L('average') | L('sHigh') | L('High') | L('vHigh') | L('dHigh') |
        L('uHigh'))))
    def m2(self):
        print("missing or unreadable value for windsp rRange")

#MCB MASS-CORAL-BLEACHING implementation
#Description: Mass bleaching of hard corals
#forecast has 24 distinct rules

#Ecoforecast Rule #1: Coral-Bleaching-Itlwt
#Description: Mass coral bleaching (high in-situ sea temperature + high light + low wind + low tide)
    @Rule(foo)
    def mcb1(self):
        print("Coral-Bleaching-Itlwt fired")

#Ecoforecast Rule #2: Coral-Bleaching-Stlwt
#Description: Mass coral bleaching (high 'shallow' sea temperature + high light + low wind + low tide)
    @Rule(foo)
    def mcb2(self):
        print("Coral-Bleaching-Stlwt fired")

#Ecoforecast Rule #3: Coral-Bleaching-Tlwt
#Description: Mass coral bleaching (high SST + high light + low wind + low tide)
    @Rule(foo)
    def mcb3(self):
        print("Coral-Bleaching-Tlwt fired")

#Ecoforecast Rule #4: Coral-Bleaching-Itlw
# Description: Mass coral bleaching (high in-situ sea temperature + high light + low wind)
    @Rule(foo)
    def mcb4(self):
        print("Coral-Bleaching-Itlw fired")

#Ecoforecast Rule #5: Coral-Bleaching-Itwt
#Description: Mass coral bleaching (high in-situ sea temperature + low wind + low tide)
    @Rule(foo)
    def mcb5(self):
        print("Coral-Bleaching-Itwt")

#Ecoforecast Rule #6: Coral-Bleaching-Stlw
#Description: Mass coral bleaching (high 'shallow' sea temperature + high light + low wind)
    @Rule(foo)
    def mcb6(self):
        print("Coral-Bleaching-Stlw fired")

#Ecoforecast Rule #7: Coral-Bleaching-Stwt
#Description: Mass coral bleaching (high 'shallow' sea temperature + low wind + low tide)
    @Rule(foo)
    def mcb7(self):
        print("Coral-Bleaching-Stwt fired")


#Ecoforecast Rule #8: Coral-Bleaching-Tlw
#Description: Mass coral bleaching (high SST + high light + low wind)
    @Rule(foo)
    def mcb8(self):
        print("Coral-Bleaching-Stwt fired")

#Ecoforecast Rule #9: Coral-Bleaching-Twt
# Description: Mass coral bleaching (high SST + low wind + low tide)
    @Rule(foo)
    def mcb9(self):
        print("Coral-Bleaching-Stwt fired")

#Ecoforecast Rule #10: Coral-Bleaching-Itd
#Description: Mass coral bleaching (high in-situ sea temperature + doldrums)
    @Rule(foo)
    def mcb10(self):
        print("Coral-Bleaching-Stwt fired")

#Ecoforecast Rule #11: Coral-Bleaching-Itl
#Description: Mass coral bleaching (very high in-situ sea temperature + very high light)
    @Rule(foo)
    def mcb11(self):
        print("Coral-Bleaching-Stwt fired")

#Ecoforecast Rule #12: Coral-Bleaching-Itw
#Description: Mass coral bleaching (very high in-situ sea temperature + very low wind)
    @Rule(foo)
    def mcb12(self):
        print("Coral-Bleaching-Stwt fired")

#Ecoforecast Rule #13: Coral-Bleaching-Std
#Description: Mass coral bleaching (high 'shallow' sea temperature + doldrums)
    @Rule(foo)
    def mcb13(self):
        print("Coral-Bleaching-Stwt fired")

#Ecoforecast Rule #14: Coral-Bleaching-Stl
#Description: Mass coral bleaching (very high 'shallow' sea temperature + very high light)
    @Rule(foo)
    def mcb14(self):
        print("Coral-Bleaching-Stwt fired")

#Ecoforecast Rule #15: Coral-Bleaching-Stw
#Description: Mass coral bleaching (very high 'shallow' sea temperature + very low wind)
    @Rule(foo)
    def mcb15(self):
        print("Coral-Bleaching-Stwt fired")

#Ecoforecast Rule #16: Coral-Bleaching-Tl
#Description: Mass coral bleaching (very high SST + very high light)
    @Rule(foo)
    def mcb16(self):
        print("Coral-Bleaching-Stwt fired")

#Ecoforecast Rule #17: Coral-Bleaching-Tw    
#Description: Mass coral bleaching (very high SST + very low wind)
    @Rule(foo)
    def mcb17(self):
        print("Coral-Bleaching-Stwt fired")

#Ecoforecast Rule #18: Coral-Bleaching-B    
#Description: Mass coral bleaching (Berkelmans bleaching curve)    
    @Rule(foo)
    def mcb18(self):
        print("Coral-Bleaching-Stwt fired")

#Ecoforecast Rule #19: Coral-Bleaching-It    
#Description: Mass coral bleaching (drastic high in-situ sea temperature)
    @Rule(foo)
    def mcb19(self):
        print("Coral-Bleaching-Stwt fired")

#Ecoforecast Rule #20: Coral-Bleaching-Mort    
#Description: Mass coral mortality (>50%) for local sensitive species (Berkelmans)
    @Rule(foo)
    def mcb20(self):
        print("Coral-Bleaching-Stwt fired")

#Ecoforecast Rule #21: Coral-Bleaching-Mst 
#Description: Mass coral bleaching (high monthly mean 'shallow' sea temperature)
    @Rule(foo)
    def mcb21(self):
        print("Coral-Bleaching-Stwt fired")

#Ecoforecast Rule #22: Coral-Bleaching-Mwt
#Description: Mass coral bleaching (high monthly mean in situ sea temperature)
    @Rule(foo)
    def mcb22(self):
        print("Coral-Bleaching-Stwt fired")

#Ecoforecast Rule #23: Coral-Bleaching-St
#Description: Mass coral bleaching (drastic high 'shallow' sea temperature)
    @Rule(foo)
    def mcb23(self):
        print("Coral-Bleaching-Stwt fired")

#Ecoforecast Rule #24: Coral-Bleaching-T
#Description: Mass coral bleaching (drastic high SST)
    @Rule(foo)
    def mcb24(self):
        print("Coral-Bleaching-Stwt fired")



#import mcb0_6 as a
#e = a.MCB()
#e.reset()
#e.missing_facts()
#e.facts() """displays current fact list in working memory"""
#e.run()
#"""expected output: 'sst is Some what Low'"""

