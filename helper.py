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


