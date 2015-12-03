import calendar
import datetime
import time

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

class GenericBank(object):

    supported_currencies = \
        {
            'AUD': 'Australian Dollar',
            'CAD': 'Canadian Dollar',
            'CHF': 'Swiss Franc',
            'CNY': 'Chinese Yuan',
            'EUR': 'Euro',
            'GBP': 'British Pound',
            'HKD': 'Hong Kong Dolloar',
            'IDR': 'Indonesian Rupiah',
            'JPY': 'Japanese Yen',
            'KRW': 'South Korean Won',
            'MYR': 'Malaysian Ringgit',
            'NZD': 'New Zealand Dollar',
            'PHP': 'Philippine Peso',
            'SEK': 'Swedish Krona',
            'SGD': 'Singapore Dollar',
            'THB': 'Thai Baht',
            'TWD': 'Taiwan New Dollar',
            'USD': 'US Dollar',
            'VND': 'Vietnamese Dong',
            'ZAR': 'South African Rand'
        }
    bank_name = None

    @staticmethod
    def get_epoch():
        return calendar.timegm(time.gmtime())

    @staticmethod
    def dump_data(data):
        """
        Dump currency data
        """
        if 'date' in data:
            print "Quote date:", datetime.datetime.utcfromtimestamp(data['date']).strftime('%Y-%m-%dT%H:%M:%SZ')
        print "Currency Cash_buy Cash_sell Spot_buy Spot_sell"
        print '-' * 48
        for cur, rates in data['data'].iteritems():
            print '%-08s %-08s %-09s %-08s %-09s' % (cur,
                    rates[0] if rates[0] else '-', rates[1] if rates[1] else '-',
                    rates[2] if rates[2] else '-', rates[3] if rates[3] else '-')

    def quote(self):
        """
        Returns current quoted currency exchange data in format
        {
          "date": epoch time (type: int)
          "data": {
              "currency 1": [cash buy, cash sell, spot buy, spot sell],
              "currency 2": [cash buy, cash sell, spot buy, spot sell],
              ...
          }
          where
           - "currency 1" is listed in GenericBank.supported_currencies (type: string)
           - exchange rates in float
        """
        raise

    def name(self):
        """
        Return name of the bank which gives the quote
        """
        return self.bank_name

