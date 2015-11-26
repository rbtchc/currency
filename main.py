import sys
sys.path.insert(0, 'libs')

import datetime
import webapp2

from google.appengine.api import datastore_types
from google.appengine.ext import ndb
from models import XchgRecord
from helper import GenericBank
from twbank import TWBank
from webapp2_extras import jinja2


class BaseHandler(webapp2.RequestHandler):

    @webapp2.cached_property
    def jinja2(self):
        """ Returns a Jinja2 renderer cached in the app registry. """
        return jinja2.get_jinja2(app=self.app)

    def render_response(self, _template, **context):
        """ Renders a template and writes the result to the response. """
        rv = self.jinja2.render_template(_template, **context)
        self.response.write(rv)

    def write(self, *a, **kw):
        self.response.write(*a, **kw)

class MainHandler(BaseHandler):

    def get(self):
        self.render_response('main.html')

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

APPLICATION = webapp2.WSGIApplication([
        ('/', MainHandler),
        ], debug=True)

