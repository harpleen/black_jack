from lib.basic_strategy import *

'''
If given a hard total 
Returns the correct action according to basic strategy
'''

def test_hard_totals_8(): 
    basic_strategy = BasicStrategy(8, False, '2')
    assert basic_strategy.get_action() == 'HIT'

def test_hard_totals_12_4():
    basic_strategy = BasicStrategy(12, False, '4')
    assert basic_strategy.get_action() == 'STAND'

def test_hard_totals_16_10():
    basic_strategy = BasicStrategy(16, False, '10')
    assert basic_strategy.get_action() == 'HIT'

def test_hard_totals_20_6():
    basic_strategy = BasicStrategy(20, False, '6')
    assert basic_strategy.get_action() == 'STAND'

'''
If given a soft total 
Returns the correct action according to basic strategy
'''
def test_soft_totals_13_5():
    basic_strategy = BasicStrategy(13, True, '5')
    assert basic_strategy.get_action() == 'DOUBLE DOWN'

def test_soft_totals_17_3():
    basic_strategy = BasicStrategy(17, True, '3')
    assert basic_strategy.get_action() == 'DOUBLE DOWN'

def test_soft_totals_18_9():
    basic_strategy = BasicStrategy(18, True, '9')
    assert basic_strategy.get_action() == 'HIT'

def test_soft_totals_19_6():
    basic_strategy = BasicStrategy(19, True, '6')
    assert basic_strategy.get_action() == 'DOUBLE DOWN'

'''
If given a pair
Returns the correct action according to basic strategy
'''
def test_pair_splitting_2s_3():
    basic_strategy = BasicStrategy(2, False, '3', is_pair=True)
    assert basic_strategy.get_action() == 'SPLIT'

def test_pair_splitting_6s_7():
    basic_strategy = BasicStrategy(6, False, '7', is_pair=True)
    assert basic_strategy.get_action() == 'HIT'

def test_pair_splitting_9s_10():
    basic_strategy = BasicStrategy(8, False, '10', is_pair=True)
    assert basic_strategy.get_action() == 'SPLIT'

def test_pair_splitting_As_5():
    basic_strategy = BasicStrategy(11, False, '5', is_pair=True)
    assert basic_strategy.get_action() == 'SPLIT'