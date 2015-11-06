import json
import requests
import re
import pandas as pd
import numpy as np
from xml.etree import ElementTree
from collections import defaultdict

url = 'http://www.boardgamegeek.com/xmlapi2'

def get_hotness_data(type):
    """ Use BoardGameGeek API to get hotness rank for specified type. 
    Returns an XML object. """
    d = requests.get('{}/hot?type={}'.format(url, type))
    return ElementTree.fromstring(d.content)


def get_thing_data(type, ids, stats=True):
    """ Use BoardGameGeek API to get game statistics. Takes in ids of
    interest and parameter to identify if statistics are wanted and 
    returns an XML object with requested game information and 
    statistics.

    ids = individual id or list of ids
    type = boardgame, but could be something else supported by 
    BoardGameGeek, like boardgameexpansion, videogame, rpgitem, or 
    rpgissue """
    ids = re.sub('^0\s{1,}|\n[\w\s:,]{1,}', '', 
                 re.sub('\n[0-9]{1,}\s{1,}', ', ', ids))
    d = requests.get('{}/thing?type={}&id={}&stats={}'.format(url, type, 
                    ids, int(stats)))
    return ElementTree.fromstring(d.content)


def xml_to_df(xml):
    """ Formats XML output into a pandas dataframe """
    dict = defaultdict(list)
    for kid in xml:
        for key, val in kid.items():
            dict[key].append(val)
        for gkid in kid:
            for key, val in gkid.items():
                dict[gkid.tag].append(v)
    return pd.DataFrame(dict)
    

