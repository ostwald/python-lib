import sys, os, urllib2
from urlparse import urlparse, urlsplit, parse_qs

class ParseUrl:

    attrs = ['scheme', 'netloc', 'path', 'params', 'query', 'fragment']

    def __init__ (self, url):
        result = urlparse(url)
        for i, attr in enumerate (self.attrs):
            # print i, attr
            setattr(self, attr, urllib2.unquote(result[i]))
        

class SplitUrl:

    attrs = ['scheme', 'netloc', 'path', 'query', 'fragment']

    def __init__ (self, url):
        result = urlsplit(url)
        for i, attr in enumerate (self.attrs):
            # print i, attr
            setattr(self, attr, urllib2.unquote(result[i]))
        
def test ():
	pr = ParseUrl(url)
	# pr = SplitUrl(url)
	
	for attr in pr.attrs:
		print '- %s: %s' % (attr, getattr(pr, attr))

if __name__ == '__main__':
	url = 'http://nldr.library.ucar.edu/schemedit/services/ddsws1-1?q=%28xkcd+OR+xkcd%29+OR+%28%28title:%28xkcd%29^15+OR+title%28xkcd%29^10+OR+titlestems:%28xkcd%29^5%29+OR+titlestems:%28xkcd%29^3%29&verb=Search&s=0&n=10'
	print urllib2.unquote(url)
	
	parsed = ParseUrl(url)
	
	data = parse_qs(parsed.query)
	
	print '{'
	for key in data.keys():
		val = data[key]
		if type(val) == type([]) and len(val) == 1:
			val = val[0]
		print '  "%s": "%s",' % (key, val)
	print '}'
