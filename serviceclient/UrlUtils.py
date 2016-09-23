
import urllib
from urlparse import urlsplit, urljoin
from cgi import parse_qs
from ServiceClient import ServiceRequest
from CATGlobals import baseUrl, suggest_standards_params, more_like_these_params
from URL import URL
from urls import *

class UrlComparator:
	def __init__ (self, url1, url2):
		self.ut1 = URL(url1)
		self.ut2 = URL (url2)
		self.params = self._allparams()

	def _allparams(self):
		all = [];add=all.append
		for ut in [self.ut1, self.ut2]:
			for p in ut.getParamNames():
				if not p in all:
					add(p)
		return all

	def diff (self):
		msg = [];add=msg.append
		if self.ut1.getBaseUrl() != self.ut2.getBaseUrl():
			add ("baseUrls are different")
		p1 = self.ut1.getParamMap()
		p2 = self.ut2.getParamMap()

		for p in self._allparams():
			if not p1.has_key(p):
				add ("'%s' is not defined in 1" % p)
			elif not p2.has_key(p):
				add ("'%s' is not defined in 2" % p)
			elif p1[p] != p2[p]:
				add ("different values for '%s'" % p)
				add ("\t1 - %s\n\t2 - %s" % (p1[p], p2[p]))
		if not msg:
			return "no diff"
		else:
			return '\n'.join (msg)

def cmpUrls (url1, url2):
	ct = UrlComparator (url1, url2)
	ct.ut1.report("URL 1")
	ct.ut2.report("URL 2")
	print "\nDiff:"
	print ct.diff()

if __name__ == "__main__":
	ut = URL (ssDoc)
	print ut.getTuple()
	
