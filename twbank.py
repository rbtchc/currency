#!/usr/bin/env python

import calendar
import logging
import json
import re
import time

from bs4 import BeautifulSoup
from helper import fetch_url
from helper import GenericBank

currency_table = {
    u'\xa0Australian Dollar (AUD)':  'AUD',
    u'\xa0Canadian Dollar (CAD)':    'CAD',
    u'\xa0Swiss Franc (CHF)':        'CHF',
    u'\xa0China Yen (CNY)':          'CNY',
    u'\xa0Euro (EUR)':               'EUR',
    u'\xa0British Pound (GBP)':      'GBP',
    u'\xa0Hong Kong Dollar (HKD)':   'HKD',
    u'\xa0Indonesian Rupiah (IDR)':  'IDR',
    u'\xa0Japanese Yen (JPY)':       'JPY',
    u'\xa0Korean Won (KRW)':         'KRW',
    u'\xa0Malaysian Ringgit (MYR)':  'MYR',
    u'\xa0New Zealand Dollar (NZD)': 'NZD',
    u'\xa0Philippine Peso (PHP)':    'PHP',
    u'\xa0Swedish Krona (SEK)':      'SEK',
    u'\xa0Singapore Dollar (SGD)':   'SGD',
    u'\xa0Thai Baht (THB)':          'THB',
    u'\xa0American Dollar (USD)':    'USD',
    u'\xa0Vietnam Dong (VND)':       'VND',
    u'\xa0South African Rand (ZAR)': 'ZAR',
}

content = fetch_url("http://rate.bot.com.tw/Pages/Static/UIP003.en-US.htm")
soup = BeautifulSoup(content, "lxml")
tables = soup.find_all('table')

quote_date_str = re.findall(ur'Quoted Date[\uff1a][\xa0](.*)\r', tables[4].find_all('td')[:][-1].text)
if not quote_date_str:
    logging.error("Unable to parse quoted date from html!")
# Hardcoded as GMT+8 (CST)
quote_date = calendar.timegm(time.strptime(quote_date_str[0]+' CST', "%m/%d/%Y %H:%M %Z"))

data = {}
# extract currency exchange data from sixth table
for tr in tables[6].find_all('tr'):
    tds = [td.text for td in tr.find_all('td')]
    if not tds:
        continue
    data[currency_table[tds[0]]] = [float(x) if x != '-' else None for x in tds[1:5]]
data = {"date": quote_date, "data": data}

GenericBank.dump_data(data)
