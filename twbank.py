#!/usr/bin/env python

import csv
import logging
import json

from helper import fetch_url

data = {}
#content = fetch_url("http://rate.bot.com.tw/Pages/UIP003/Download.ashx?lang=en-US&fileType=1&date=2015-11-02T11:00:52")
content = fetch_url("http://rate.bot.com.tw/Pages/UIP003/Download.ashx?lang=en-US&fileType=1")

fields = ['Currency', 'Rate', 'Cash', 'Spot', 'Forward-10Days',
          'Forward-30Days', 'Forward-60Days', 'Forward-90Days', 'Forward-120Days', 'Forward-150Days',
          'Forward-180Days' 'Rate', 'Cash' 'Spot', 'Forward-10Days',
          'Forward-30Days', 'Forward-60Days', 'Forward-90Days', 'Forward-120Days', 'Forward-150Days',
          'Forward-180Days']

table = {}
for l in content.split('\r\n')[1:]:
    if not l.strip(): continue
    columns = [x.strip() for x in l.strip().split(',')]
    table[columns[0]] = [float(x) for x in columns[2:4] + columns[12:14]]

print json.dumps(table)
