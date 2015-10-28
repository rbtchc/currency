#!/usr/bin/env python

import logging
from bs4 import BeautifulSoup

USE_GAE = False

def fetch_url(url):
    if not USE_GAE:
        import urllib2
        try:
            response = urllib2.urlopen(url)
            return response.read()
        except urllib2.URLError, e:
            logging.error(e)
    else:
        from urllib2 import urlopen as urlfetch
        #logging.warning("start fetching....")
        response = urlfetch.fetch(url=url,
                                  payload=None,
                                  method=urlfetch.GET,
                                  headers=HEADERS,
                                  allow_truncated=False,
                                  follow_redirects=False,
                                  deadline=DEADLINE)
    #logging.warning("eof fetching....")
    return response.content

currency_table = {
    u'\u745e\u58eb\u6cd5\u90ce\uff08CHF\uff09': 'chf',
    u'\u7d10\u5e63\uff08NZD\uff09': 'nzd',
    u'\u6b50\u5143\uff08EUR\uff09': 'eur',
    u'\u7f8e\u5143\uff08USD\uff09': 'usd',
    u'\u6fb3\u5e63\uff08AUD\uff09': 'aud',
    u'\u52a0\u62ff\u5927\u5e63\uff08CAD\uff09': 'cad',
    u'\u6cf0\u5e63\uff08THB\uff09': 'thb',
    u'\u5357\u975e\u5e63\uff08ZAR\uff09': 'zar',
    u'\u65e5\u5713\uff08JPY\uff09': 'jpy',
    u'\u65b0\u52a0\u5761\uff08SGD\uff09': 'sgd',
    u'\u82f1\u938a\uff08GBP\uff09': 'gbp',
    u'\u6e2f\u5e63\uff08HKD\uff09': 'hkd',
    u'\u745e\u5178\u514b\u6717\u5e63 (SEK)': 'sek',
    u'\u4eba\u6c11\u5e63\uff08CNY\uff09': 'cny'
}

data = {}
content = fetch_url("http://www.standardchartered.com.tw/check/inquiry-rate-foreign-exchange.asp")
soup = BeautifulSoup(content, "lxml")
for tr in soup.table.find_all(['tr'])[1:]:
    key = currency_table.get(tr.th.getText(), None)
    value = [None if x.getText() == '-' else float(x.getText()) for x in tr.find_all(['td'])]
    data[key] = value

import json
print json.dumps(data)
