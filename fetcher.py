import os
import requests
import re
import time
import pandas as pd
import numpy as np
from xml.etree import ElementTree
from collections import defaultdict
from gamerank.parser import *

wd = os.getcwd()

if not os.path.isfile('hotness.csv'):
    try:
        hot = get_hotness_data('boardgame')
    except:
        print 'Error getting BoardGameGeek hotness data.'
    hotd = xml_to_df(hot)
    hotd.write_csv('hotness.csv', columns=[''], index=False)