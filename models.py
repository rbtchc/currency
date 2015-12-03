from google.appengine.ext import ndb

"""
class Bank(ndb.Model):
    '''Info of bank which provides currency exchanges'''
    name          = ndb.StringProperty(required=True)
    created       = ndb.DateTimeProperty(auto_now_add=True)
    last_updated  = ndb.DateTimeProperty(auto_now=True)
"""

class XchgRecord(ndb.Model):
    '''Exchange rate record btw two currency'''
    bank          = ndb.StringProperty(required=True)
    base_currency = ndb.StringProperty(required=True)
    to_currency   = ndb.StringProperty(required=True)
    cash_buy      = ndb.FloatProperty()
    cash_sell     = ndb.FloatProperty()
    spot_buy      = ndb.FloatProperty()
    spot_sell     = ndb.FloatProperty()
    quote_date    = ndb.DateTimeProperty(required=True)
    created       = ndb.DateTimeProperty(auto_now_add=True)
    last_updated  = ndb.DateTimeProperty(auto_now=True)

