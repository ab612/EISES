#!/Users/soden/ python

"""mcb0_2 Ecoforecast prototype goal is to implement rules base from http://ecoforecast.coral.noaa.gov/index/0/MLRF1/model-detail&name=MASS-CORAL-BLEACHING and 'print' a forecast"""

from pyknow import *
import numpy as np

__author__ = "Madison Soden"
__date__ = "Sun Dec 17 15:03:46 2017"
__license__ = "NA?"
__version__ = "mcb0_2"
__email__ = "madison.soden@gmail.com"
__status__ = "Production"

"""Fact Definition Documentation""" 
    #rRange is a string containing a fuzzy (i.e. proxy) values for sst
    #key = 'rRange' / 0
    #fuzzy values can be 'uLow', 'dLow', 'vLow', 'Low', 'sLow', 'average', 'sHigh',
    # 'High', 'vHigh', 'dHigh', 'uHigh'
"""REWRITE TOD DOCUMENTATION"""
    #tod is an array of boolean values indicating a fuzzy time of day values for the- 
    # time rRange was recorded. Taken in eight 3 hour, then four 6 hour, then
    # two 12 hour , and one 24 hour time increments. TRUE indicates rRange was
    # recorded at that time. The 24 hour bool cannot be TRUE unless all
    # contained time increments are true. 
        #EG: tod=np.zeros((1,16), dtype=bool) to initialize
        #    tod.item(3) to access 4th item in array
        #    or tod.item((2,3)) to access item row 3 column 4
    #key = 'tod' and/or 1
    #fuzzy values can be 'predawn'(12AM-2:59AM) tod.item(0),
    # 'dawn'(3AM-5:59AM) tod.item(1), 'morning'(6AM-8:59AM) tod.item(2), 
    # 'midday'(9AM-11:59AM) tod.item(3), 'evening'(12PM-2:59PM) tod.item(4),
    # 'presunset'(3PM-5:59PM) tod.item(5),'sunset'(6PM-8:59PM) tod.item(6),
    # 'midnight'(9PM-11:59PM) tod.item(7), 'early morning'(12AM-5:59AM)
    #  tod.item(8), 'late morning'(6AM-11:59AM) tod.item(9), 'early
    #  afternoon'(12PM-5:59PM) tod.item(10), 'late afternoon'(6PM-11:59PM)
    #  tod.item(11), 'early day'(12AM-11:59AM) tod.item(12), 'late
    #  day'(12PM-11:59PM) tod.item(13), and 'whole day'(12AM-11:59PM)
    #  tod.item(14)

    #numd is a int representing the number of consecutive days tod and rRange
    # apply to. For example, numd=7 for rRange data that is a weekly average.
    # numd must always be a whole number
    #key = 'numd' and/or 2

    #offset is the number of days from the current day that tod and numd end at
    # For example, last weeks' weekly average has an offset of 0. Last, last
    # weeks' weekly average has an offset of 7. offset is recorded as a
    # positive integer for the past and a negative integer for the future. 
    #key = 'offset' and/or 3

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
        pass

    def likely_facts(self):
        self.declare(sst(rRange='High', tod='midday', date='29112017'))
        self.declare(windsp(rRange='Low', tod='midday', date='29112017'))
        pass

    def unlikely_facts(self):
        self.declare(sst(rRange='average', tod='midday', date='29112017'))
        self.declare(windsp(rRange='average', tod='midday', date='29112017')) 

    def verylikely_facts(self):
        self.declare(sst(rRange='vHigh', tod='midday', date='29112017'))
        self.declare(windsp(rRange='sLow', tod='midday', date='29112017'))

    def misinformed_facts(self):
        self.declare(sst(rRange='uLow', tod='midday', date='29112017'))
        self.declare(windsp(rRange='uHigh', tod='midday', date='29992017'))

    def missing_facts(self):
        self.declare(sst(rRange='sLow', tod='', date='29112017'))
        self.declare(windsp(rRange='', tod='midday', date=''))


#Rule production & alert printing
 
#only sst rules
    @Rule(sst(rRange='dLow'))
    def sst0(self):
        print("sst is drastically Low")
        pass

    @Rule(sst(rRange='vLow'))
    def sst1(self):
        print("sst is very low")
        pass

    @Rule(sst(rRange='Low'))
    def sst2(self):
        print("sst is low")
        pass
 
    @Rule(sst(rRange='sLow'))
    def sst3(self):
        print("sst is Some what Low")
        pass

    @Rule(sst(rRange='average'))
    def sst4(self):
        print("sst is average")
        pass

    @Rule(sst(rRange='sHigh'))
    def sst5(self):
        print("sst is somewhat high")
        pass

    @Rule(sst(rRange='High'),salience=1)
    def sst6(self):
        print("sst is high")
        pass

    @Rule(sst(rRange='vHigh'))
    def sst7(self):
        print("sst is very high")
        pass 

    @Rule(sst(rRange='dHigh'))
    def sst8(self):
        print("sst is drastically high")
        pass 


#only windsp rules
    @Rule(windsp(rRange='dLow'))
    def windsp0(self):
        print(" wind scalar is drastically Low")
        pass

    @Rule(windsp(rRange='vLow'))
    def windsp1(self):
        print("wind scalar is very low")
        pass

    @Rule(windsp(rRange='Low'))
    def windsp2(self):
        print("wind scalar is low")
        pass
 
    @Rule(windsp(rRange='sLow'))
    def windsp3(self):
        print("wind scalar is Some what Low")
        pass

    @Rule(windsp(rRange='average'))
    def windsp4(self):
        print("wind scalar is average")
        pass

    @Rule(windsp(rRange='sHigh'))
    def windsp5(self):
        print("wind scalar is somewhat high")
        pass

    @Rule(windsp(rRange='High'))
    def windsp6(self):
        print("wind scalar is high")
        pass

    @Rule(windsp(rRange='vHigh'))
    def windsp7(self):
        print("wind scalar is very high")
        pass 

    @Rule(windsp(rRange='dHigh'))
    def windsp8(self):
        print("wind scalar is drastically high")
        pass 


#combined sst and windsp rules
    @Rule(sst(rRange='High'),windsp(rRange='Low'))
    def c1(self):
        print(" Coral bleaching is likely")
        pass

    @Rule(sst(rRange='average'),windsp(rRange='average'))
    def c2(self):
        print("Coral bleaching is unlikely")
        pass

    @Rule(sst(rRange='vHigh'),windsp(rRange='sLow'))
    def c3(self):
        print("Coral bleaching is very likely")
        pass


#other cases
    @Rule(OR(sst(rRange='uLow'),sst(rRange='uHigh')))
    def u1(self):
        print("sst values in unbelievable range")
        pass

    @Rule(OR(windsp(rRange='uLow'),windsp(rRange='uHigh')))
    def u2(self):
        print("wind scalar values in unbelievable range")
        pass 

    @Rule(NOT(sst(rRange=L('uLow') | L('dLow') | L('vLow') | L('Low') | L('sLow') |
        L('average') | L('sHigh') | L('High') | L('vHigh') | L('dHigh') |
        ('uHigh'))))
    def m1(self):
        print("missing or unreadable value for sst rRange")
        pass 

    @Rule(NOT(windsp(rRange=L('uLow') | L('dLow') | L('vLow') | L('Low') | L('sLow') |
        L('average') | L('sHigh') | L('High') | L('vHigh') | L('dHigh') |
        L('uHigh'))))
    def m2(self):
        print("missing or unreadable value for windsp rRange")
        pass



#import eco0_0_3 as a
#e = a.GCoralBleaching()
#e.reset()
#e.missing_facts()
#e.facts() """displays current fact list in working memory"""
#e.run()
#"""expected output: 'sst is Some what Low'"""
