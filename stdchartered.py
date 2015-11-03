#!/usr/bin/env python

import logging
import json

from bs4 import BeautifulSoup
from helper import fetch_url

currency_table = {
    u'\u6fb3\u5e63\uff08AUD\uff09':             'AUD',
    u'\u52a0\u62ff\u5927\u5e63\uff08CAD\uff09': 'CAD',
    u'\u745e\u58eb\u6cd5\u90ce\uff08CHF\uff09': 'CHF',
    u'\u4eba\u6c11\u5e63\uff08CNY\uff09':       'CNY',
    u'\u6b50\u5143\uff08EUR\uff09':             'EUR',
    u'\u82f1\u938a\uff08GBP\uff09':             'GBP',
    u'\u65e5\u5713\uff08JPY\uff09':             'JPY',
    u'\u7d10\u5e63\uff08NZD\uff09':             'NZD',
    u'\u745e\u5178\u514b\u6717\u5e63 (SEK)':    'SEK',
    u'\u65b0\u52a0\u5761\uff08SGD\uff09':       'SGD',
    u'\u6cf0\u5e63\uff08THB\uff09':             'THB',
    u'\u6e2f\u5e63\uff08HKD\uff09':             'HKD',
    u'\u7f8e\u5143\uff08USD\uff09':             'USD',
    u'\u5357\u975e\u5e63\uff08ZAR\uff09':       'ZAR',
}

data = {}
content = fetch_url("http://www.standardchartered.com.tw/check/inquiry-rate-foreign-exchange.asp")
soup = BeautifulSoup(content, "lxml")
for tr in soup.table.find_all(['tr'])[1:]:
    key = currency_table.get(tr.th.getText(), None)
    value = [None if x.getText() == '-' else float(x.getText()) for x in tr.find_all(['td'])]
    data[key] = value

print json.dumps(data)
