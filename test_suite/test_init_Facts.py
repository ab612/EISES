# test_init_Facts.py
#tests fact initialization

import sys
sys.path.append('../')
from mcb import *
import pytest

@pytest.fixture
def empty_engine():
    '''returns empty knowledge engine'''
    e = MCB()
    e.reset()
    return e

@pytest.fixture
def full_engine():
    '''returns knowledge engine with each fact declared once'''
    e = MCB()
    e.reset()
    e.declare_facts('parsurf', 'dummyI', 'dummyTOD')
    e.declare_facts('sst', 'dummyI', 'dummyTOD')
    e.declare_facts('windsp', 'dummyI', 'dummyTOD')
    e.declare_facts('tide1m', 'dummyI', 'dummyTOD')
    e.declare_facts('seandbc', 'dummyI', 'dummyTOD')
    e.declare_facts('sea1m', 'dummyI', 'dummyTOD')
    e.declare_facts('curveB', 'dummyI', 'dummyTOD')
    e.declare_facts('sea1mM', 'dummyI', 'dummyTOD')
    e.declare_facts('seandbcM', 'dummyI', 'dummyTOD')
    e.declare_facts('windsp3day', 'dummyI', 'dummyTOD')
    return e

def test_empty_engine(empty_engine):
    assert  (empty_engine.facts[0].__class__ == fact.InitialFact)and\
            (empty_engine.facts.last_index == 1)

def test_parsurf_declare(full_engine):
    assert  (full_engine.facts[0].__class__ == fact.InitialFact) and\
            (full_engine.facts[1].__class__ == parsurf) and\
            (full_engine.facts[2].__class__ == sst) and\
            (full_engine.facts[3].__class__ == windsp) and\
            (full_engine.facts[4].__class__ == tide1m) and\
            (full_engine.facts[5].__class__ == seandbc) and\
            (full_engine.facts[6].__class__ == sea1m) and\
            (full_engine.facts[7].__class__ == curveB) and\
            (full_engine.facts[8].__class__ == sea1mM) and\
            (full_engine.facts[9].__class__ == seandbcM) and\
            (full_engine.facts[10].__class__ == windsp3day) and\
            (full_engine.facts.last_index == 11)


