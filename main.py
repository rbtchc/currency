import banks
import datetime
import logging
import webapp2

from google.appengine.api import datastore_types
from google.appengine.api import users
from google.appengine.ext import ndb

from models import XchgRecord
from helper import GenericBank
from twbank import TWBank
from webapp2_extras import jinja2

# Import the Flask Framework
from flask import Flask, request, jsonify
from flask import render_template
from flask_restful import abort, reqparse
from flask_restful import Resource, Api

app = Flask(__name__)
app.config["ERROR_404_HELP"] = False

# Note: We don't need to call run() since our application is embedded within
# the App Engine WSGI application server.
api = Api(app)

@app.route('/')
def landing_page():
    u = users.get_current_user()
    logging.info("user = %s" % u)
    return render_template('main.html', user=u)

def daterange(start_date, end_date):
    for n in range(int ((end_date - start_date).days)):
        yield start_date + datetime.timedelta(n)

class Rate(Resource):
    '''
    '''
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('start_date', type=str, required=True)
        self.parser.add_argument('end_date',   type=str, required=True)
        self.parser.add_argument('currency',   type=str, required=True)

        super(Rate, self).__init__()


    def get(self, bank_id):

        args = self.parser.parse_args(strict=True)

        bank = banks.get_bank(bank_id)
        if not bank:
            abort(404, message="Not found. Supported banks = %s" % ','.join(banks.get_bank_ids()))
        try:
            start_date = datetime.datetime.strptime(args['start_date'], '%Y%m%d')
            # until the end of the day
            end_date = datetime.datetime.strptime(args['end_date'], '%Y%m%d') + datetime.timedelta(days=1)
        except:
            abort(400, message="Unable to parse start/end date")

        ancestor_key = ndb.Key('Bank', bank.name())
        data = {'quotes':[]}
        if (end_date - start_date) > datetime.timedelta(days=1):
            # FIXME we need to generate a different table for this instead of query ndb day by day
            for sd in daterange(start_date, end_date):
                ed = sd + datetime.timedelta(days=1)
                x = XchgRecord.get_latest_quotes(ancestor_key).filter(XchgRecord.base_currency == args['currency'])\
                        .filter(XchgRecord.quote_date <= ed).filter(XchgRecord.quote_date >= sd).get()
                if x:
                    x.quote_date -= datetime.timedelta(hours=8) # FIXME: ndb records are stored as GMT +8
                    data['quotes'].append([x.quote_date.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
                    x.cash_buy, x.cash_sell, x.spot_buy, x.spot_sell])
        else:
            for x in XchgRecord.get_latest_quotes(ancestor_key).filter(XchgRecord.base_currency == args['currency'])\
                    .filter(XchgRecord.quote_date <= end_date).filter(XchgRecord.quote_date >= start_date).fetch():
                x.quote_date -= datetime.timedelta(hours=8) # FIXME: ndb records are stored as GMT +8
                data['quotes'].append([x.quote_date.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
                    x.cash_buy, x.cash_sell, x.spot_buy, x.spot_sell])
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

