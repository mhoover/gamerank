import pytest
from collections import defaultdict
from xml.etree import ElementTree
from gamerank.parser import *


@pytest.mark.parametrize(('data', 'exp1', 'exp2', 'exp3'), [
    ('boardgame', 'tag', 'attrib', 'makeelement')
])
def test_get_hotness_data(data, exp1, exp2, exp3):
    url = 'http://www.boardgamegeek.com/xmlapi2'
    test_case = get_hotness_data(data)

    assert hasattr(test_case, exp1)
    assert hasattr(test_case, exp2)
    assert hasattr(test_case, exp3)


@pytest.mark.parametrize(('data_type', 'data_ids', 'data_stats', 'exp1', 
                         'exp2', 'exp3'), [
    ('boardgame', '38821', True, 'tag', 'attrib', 'makeelement'), 
    ('boardgame', '38821, 2651', True, 'tag', 'attrib', 'makeelement'), 
    ('boardgame', '38821, 2651', False, 'tag', 'attrib', 'makeelement')
])
def test_get_thing_data(data_type, data_ids, data_stats, exp1, exp2, exp3):
    url = 'http://www.boardgamegeek.com/xmlapi2'
    test_case = get_thing_data(data_type, data_ids, data_stats)

    assert hasattr(test_case, exp1)
    assert hasattr(test_case, exp2)
    assert hasattr(test_case, exp3)


@pytest.mark.parametrize(('test', 'exp_id', 'exp_name', 'exp_votes', 
                         'exp_votes2', 'exp_bayes'), [
    (ElementTree.parse('ex1.xml').getroot(), '175914', 'Food Chain Magnate', 
     '0', '1', '7'), 
    (ElementTree.parse('ex2.xml').getroot(), '999999', 'Food Chain Magnate2', 
     '10', '12', '6.99568'), 
    (ElementTree.parse('ex3.xml').getroot(), '1422', 'Food Chain Magnate3', 
     '2', '10', '6.09568') 
])
def test_loop_through_xml_tree(test, exp_id, exp_name, exp_votes, exp_votes2, 
                               exp_bayes):
    test_case = loop_through_xml_tree(test, defaultdict(list))
    
    assert test_case['item_id'] == [exp_id]
    assert test_case['name_value'] == [exp_name]
    assert test_case['result_numvotes'] == [exp_votes]
    assert test_case['result_numvotes1'] == [exp_votes2]
    assert test_case['rank_bayesaverage'] == [exp_bayes]
