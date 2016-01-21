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
    base_currency = ndb.StringProperty(required=True,       indexed=True)
    to_currency   = ndb.StringProperty(required=True)
    cash_buy      = ndb.FloatProperty(indexed=False)
    cash_sell     = ndb.FloatProperty(indexed=False)
    spot_buy      = ndb.FloatProperty(indexed=False)
    spot_sell     = ndb.FloatProperty(indexed=False)
    quote_date    = ndb.DateTimeProperty(required=True,     indexed=True)
    created       = ndb.DateTimeProperty(auto_now_add=True, indexed=True)
    last_updated  = ndb.DateTimeProperty(auto_now=True,     indexed=True)

    @classmethod
    def get_latest_quotes(cls, ancestor_key):
        return cls.query(ancestor=ancestor_key).order(-cls.quote_date)

class User(ndb.Model):
  '''ndb model for saving user info and preferences'''
  nickname = ndb.StringProperty(required = True)
  email = ndb.StringProperty(required = True)
  created = ndb.DateTimeProperty(auto_now_add = True)
  isAdmin = ndb.BooleanProperty(required = True)


