import json
import requests
import re
import time
import pandas as pd
import numpy as np
from xml.etree import ElementTree
from collections import defaultdict

URL = 'http://www.boardgamegeek.com/xmlapi2'

def get_hotness_data(type):
    """ Use BoardGameGeek API to get hotness rank for specified type.
    Returns an XML object. """
    d = requests.get('{}/hot?type={}'.format(URL, type))
    return ElementTree.fromstring(d.content)


def get_thing_data(type, ids):
    """ Use BoardGameGeek API to get game statistics. Takes in ids of
    interest and parameter to identify if statistics are wanted and
    returns an XML object with requested game information and
    statistics.

    type = boardgame, but could be something else supported by
    BoardGameGeek, like boardgameexpansion, videogame, rpgitem, or
    rpgissue
    ids = individual id or list of ids; needs to be in the form
    '111' or '111, 112' -- can do this by wrapping a list in str()
    """
    ids = re.sub('^0\s{1,}|\n[\w\s:,]{1,}', '',
                 re.sub('\n[0-9]{1,}\s{1,}', ', ', ids))
    d = requests.get('{}/thing?type={}&id={}&stats=1'.format(URL, type,
                    ids))
    return ElementTree.fromstring(d.content)


def loop_through_xml_tree(parent, dict):
    for kid in parent:
        for key, val in kid.items():
            dict['{}_{}_{}'.format(parent.tag, kid.tag, key)].append(val)
        if len(kid)>=1:
            loop_through_xml_tree(kid, dict)
    return dict


def xml_to_df(xml, type='hotness'):
    """ Formats XML output into a pandas dataframe """
    d = loop_through_xml_tree(xml, defaultdict(list))
    if type=='hotness':
        df = pd.DataFrame(d)
    elif type=='thing':
        df = _construct_thing_df(d)
    else:
        raise Exception('Invalid \'type\'; try again.')

    df['date'] = time.strftime('%d-%b-%Y')
    return df


def _construct_thing_df(d):
    df = pd.DataFrame()
    df['id'] = d['items_item_id']
    df['type'] = d['items_item_type']
    df['name'] = ([name for name, conditional in zip(d['item_name_value'],
                  d['item_name_type']) if conditional=='primary'])
    df['published'] = d['item_yearpublished_value']
    df['playing_time'] = d['item_playingtime_value']
    df['nbr_ratings'] = d['ratings_usersrated_value']
    df['avg_score'] = d['ratings_average_value']
    df['bayes_score'] = d['ratings_bayesaverage_value']
    df['sd'] = d['ratings_stddev_value']
    df['category'] = ([name for name, conditional in
                      zip(d['ranks_rank_name'], d['ranks_rank_type']) if
                      conditional=='family'])
    df['category_rank'] = ([name for name, conditional in
                           zip(d['ranks_rank_value'], d['ranks_rank_type']) if
                           conditional=='family'])
    df['category_avg'] = ([name for name, conditional in
                          zip(d['ranks_rank_bayesaverage'],
                          d['ranks_rank_type']) if conditional=='family'])
    return df
