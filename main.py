import banks
import datetime
import logging
import webapp2

from google.appengine.api import datastore_types
from google.appengine.ext import ndb
from models import XchgRecord
from helper import GenericBank
from twbank import TWBank
from webapp2_extras import jinja2

# Import the Flask Framework
from flask import Flask, request, jsonify
from flask_restful import abort, reqparse
from flask_restful import Resource, Api

app = Flask(__name__)
app.config["ERROR_404_HELP"] = False

# Note: We don't need to call run() since our application is embedded within
# the App Engine WSGI application server.
api = Api(app)

class LandingPage(Resource):
    def get(self):
        return {'hi': 'there'}
api.add_resource(LandingPage, '/')

class Rate(Resource):

    def get(self, bank_id):
        bank = banks.get_bank(bank_id)
        if not bank:
            abort(404,
                  message="Not found. Supported banks = %s"
                          % ','.join(banks.get_bank_ids()))

        ancestor_key = ndb.Key('Bank', bank.name())
        data = {}
        for x in XchgRecord.get_latest_quotes(ancestor_key).fetch(19):
            logging.info(x)
            data[x.base_currency] = [x.cash_buy, x.cash_sell, x.spot_buy, x.spot_sell]
        return jsonify(data)
api.add_resource(Rate, '/rate/v1.0/<string:bank_id>')


class TaskQuote(Resource):
    '''
    Task queue handlers for polling quotes from banks periodically
    '''

    def get(self, bank_id):
        bank = banks.get_bank(bank_id)
        if not bank:
            abort(404,
                  message="Not found. Supported banks = %s"
                          % ','.join(banks.get_bank_ids()))

        data = bank.quote()
        quote_date = datetime.datetime.fromtimestamp(data['date']) if 'date' in data else None
        ancestor_key = ndb.Key('Bank', bank.name())
        # sanity check if quotes are already stored
        if quote_date:
            qry = XchgRecord.query(XchgRecord.quote_date == quote_date, ancestor=ancestor_key)
            if qry.get(keys_only=True):
                return '', 204

        for c, r in data['data'].iteritems():
            rec = XchgRecord(parent=ancestor_key)
            rec.base_currency = c
            rec.to_currency = 'TWD'
            rec.cash_buy =  r[0]
            rec.cash_sell = r[1]
            rec.spot_buy =  r[2]
            rec.spot_sell = r[3]
            if quote_date: rec.quote_date = quote_date
            #TODO: put quote records at once
            rec.put()
        return '', 201
api.add_resource(TaskQuote, '/tasks/quote/v1.0/<string:bank_id>', endpoint='task_quote')

