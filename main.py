import banks
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
from flask_restful import abort, reqparse
from flask_restful import Resource, Api

app = Flask(__name__)
app.config["ERROR_404_HELP"] = False

# Note: We don't need to call run() since our application is embedded within
# the App Engine WSGI application server.
api = Api(app)

#@app.route('/')
#def landing_page():
#    """Return a friendly HTTP greeting."""
#    return 'Hi there!'

class LandingPage(Resource):
    def get(self):
        return {'hi': 'there'}
api.add_resource(LandingPage, '/')


class Quote(Resource):

    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('bank', type=str, required=True)
        args = parser.parse_args(strict=True)
        bank = banks.get_bank(args['bank'])
        if not bank:
            abort(404, message="Requested bank is not supported")

        data = bank.quote()
        quote_date = datetime.datetime.fromtimestamp(data['date']) if 'date' in data else None
        for c, r in data['data'].iteritems():
            rec = XchgRecord()
            rec.bank = bank.name()
            rec.base_currency = c
            rec.to_currency = 'TWD'
            rec.cash_buy =  r[0]
            rec.cash_sell = r[1]
            rec.spot_buy =  r[2]
            rec.spot_sell = r[3]
            if quote_date: rec.quote_date = quote_date
            rec.put()
        return data
api.add_resource(Quote, '/quote')

