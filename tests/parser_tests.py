import pytest
from collections import defaultdict
from xml.etree import ElementTree
from gamerank.parser import *

@pytest.mark.parametrize(('test', 'exp_id', 'exp_name', 'exp_votes', 
                          'exp_bayes'), [
    (ElementTree.parse('ex1.xml').getroot(), '175914', 'Food Chain Magnate', 
     '0', '7'), 
    (ElementTree.parse('ex2.xml').getroot(), '999999', 'Food Chain Magnate2', 
     '10', '6.99568'), 
    (ElementTree.parse('ex3.xml').getroot(), '1422', 'Food Chain Magnate3', 
     '2', '6.09568') 
])
def test_loop_through_xml_tree(test, exp_id, exp_name, exp_votes, exp_bayes):
    test_case = loop_through_xml_tree(test, defaultdict(list))
    
    assert test_case['item_id'] == [exp_id]
    assert test_case['name_value'] == [exp_name]
    assert test_case['result_numvotes'] == [exp_votes]
    assert test_case['rank_bayesaverage'] == [exp_bayes]
    # TODO: fix failing test on result_numvotes -- need to change key somehow