import datetime
import webapp2

from google.appengine.api import datastore_types
from google.appengine.ext import ndb
from models import XchgRecord
from helper import GenericBank
from twbank import TWBank
from webapp2_extras import jinja2

# Import the Flask Framework
from flask import Flask
app = Flask(__name__)
# Note: We don't need to call run() since our application is embedded within
# the App Engine WSGI application server.

@app.route('/')
def hello():
    """Return a friendly HTTP greeting."""
    data = TWBank().quote_rate()
    quote_date = datetime.datetime.fromtimestamp(data['date']) if 'date' in data else None
    for c, r in data['data'].iteritems():
        rec = XchgRecord()
        rec.base_currency = c
        rec.to_currency = 'TWD'
        rec.cash_buy =  r[0]
        rec.cash_sell = r[1]
        rec.spot_buy =  r[2]
        rec.spot_sell = r[3]
        if quote_date: rec.quote_date = quote_date
        rec.put()
    return 'Hello World!'

