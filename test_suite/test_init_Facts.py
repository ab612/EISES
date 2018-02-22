#test_init_Facts.py
#tests fact initialization

import sys
sys.path.append('../')
import mcb
import pytest

@pytest.fixture(scope="session", autouse=True)
def declared_engine():
    """Returns knowledge engine that has been initially reset"""
    print('\n    declared_engine(): ')
    e = mcb.MCB()
    yield e
    print('\n    tear down engine')

@pytest.fixture(scope="class")
def reset_engine(declared_engine, request):
    """Resets knowledge engine once per declared scope"""
    print('\n    reset_engine(declared_engine): ')
    declared_engine.reset()
#    return request.param

@pytest.fixture(scope = 'class')
def psetup(request):
    """Passes parameters into test classes"""
    print('\n    passing parameters')
    
    #initializing
    test1names = ('sst', 'seandbc', 'parsurf', 'windsp', 'tide1m', 'sea1m',
        'seandbcM', 'windsp3day', 'sea1mM', 'curveB')
    test2names = ('parsurf', 'windsp', 'sst', 'tide1m', 'seandbc', 'sea1m',
        'seandbc', 'sea1m', 'seandbcM', 'windsp3day', 'curveB', 'sea1mM')
    parameterdata = [
        ("./fact_CSVs/test1.csv", test1names),
        ("./fact_CSVs/test2.csv", test2names),
            ]

#create everything for instance

    #inject class variables
    request.cls.parameterdata = parameterdata
    yield

#delete everything for instance



@pytest.mark.usefixtures( 'declared_engine', 'psetup')
#@pytest.mark.parametrize("filename, factnames", [ ("./fact_CSVs/test1.csv"),
#    ("./fact_CSVs/test2.csv") ] )
class Test1:

    def test_fact_init_order( self, declared_engine, psetup):
        print('\n    test_fact_init_order(declared_engine): ')
        declared_engine.import_facts( self.parameterdata[0][0])
        assert  (declared_engine.facts[0].__class__ == mcb.fact.InitialFact) and\
                (declared_engine.facts[1].__class__.__name__ == self.parameterdata[0][1][0]) and\
                (declared_engine.facts[2].__class__.__name__ == 'seandbc') and\
                (declared_engine.facts[3].__class__.__name__ == 'parsurf') and\
                (declared_engine.facts[4].__class__.__name__ == 'windsp') and\
                (declared_engine.facts[5].__class__.__name__ == 'tide1m') and\
                (declared_engine.facts[6].__class__.__name__ == 'sea1m') and\
                (declared_engine.facts[7].__class__.__name__ == 'seandbcM') and\
                (declared_engine.facts[8].__class__.__name__ == 'windsp3day') and\
                (declared_engine.facts[9].__class__.__name__ == 'sea1mM') and\
                (declared_engine.facts[10].__class__.__name__ == 'curveB') and\
                (declared_engine.facts.last_index == 11)

    def test_function_output(self, declared_engine):
        print('\n    test1_function_output(): ')
        # a = self.agenda.activations
        # len(a)
        # a[0].rule.__name_
        assert 1 == 1

