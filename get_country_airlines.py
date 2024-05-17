import requests
from bs4 import BeautifulSoup

import re
from datetime import datetime

import pandas as pd
import json
from jsonfinder import jsonfinder

import pickle

def getRatingRecords(letra):
    data = []

    allarticles = soup.findAll('script')[0].string

    for _, __, obj in jsonfinder(allarticles, json_only=True):
        if (obj and
            isinstance(obj, list) and
            isinstance(obj[0], dict) and
            {'rank'}.issubset(obj[0])
            ):
            break
    
    for x in obj['site']['profileSearch'][letra]:
        if x['type']['name']  == "Airline":
            record = {}
            record['name'] = x['name']       
            record['icao'] = x['icao']       
            record['country'] = x['country']['name']
            record['country_code'] = x['country']['code']
    
            data.append(record)

    return data


Bdata = []

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

print(datetime.now())

for x in range(ord('a'), ord('z')+1):
    cur_url = 'https://centreforaviation.com/data/profiles/airlines?start='+ chr(x)

    response = requests.get(cur_url, headers=headers)

    soup = BeautifulSoup(response.text, "html.parser")
    Bdata=Bdata + getRatingRecords(chr(x))

    print(len(Bdata))

print(datetime.now())

with open(r'c:\tmp\airlines_countries.out', 'wb') as fp:
    pickle.dump(Bdata, fp)

