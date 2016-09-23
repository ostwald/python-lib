#!/usr/bin/env python
"""
  goal - an automated script of requests to DCS with measured response times

http://dcs.dlese.org/tapestry/adn/adn.do?command=edit&recId=TEST-000-000-000-006

  
"""
import sys, os, site, re
import string
import urllib
import MyURLopener

instances = (
	('mgr' 				, 'http://ncs.nsdl.org/mgr'),
	('' 				, ''),
	('ccs-cataloging' 	, 'http://acorn.dls.ucar.edu:27248/dcs'),
	('ccs-devel' 		, 'http://acorn.dls.ucar.edu:17248/dcs'),
	('ccs-live' 		, 'http://acorn.dls.ucar.edu:7248/dcs'),
	('' 				, ''),
	('dls-sanluis' 		, 'http://dls-sanluis.dls.ucar.edu/schemedit'),
	('' 				, ''),
	('mast' 			, 'http://meta.usu.edu:8080/mast'),
	('' 				, ''),
	('dlese' 			, 'http://dcs.dlese.org/schemedit'),
	('dlese-test' 		, 'http://ttambora.ucar.edu:10110/schemedit'),
	('' 				, ''),
	('ncar lib' 		, 'http://nldr.library.ucar.edu/schemedit'),
	('ncar lib-test' 	, 'http://ttambora.ucar.edu:10160/schemedit')
	)

class Requestor:
	"""
	tests the availability of instances on lahar
	"""

	## url_opener = urllib.URLopener()	# create URLopener
	url_opener = MyURLopener.MyURLopener ("jonathan", "mypass")	# create URLopener

	def __init__ (self, base_url):
		self.base_url = base_url
	
	def make_url (self, instance, frag):
		if instance == 'news&opps':
			url = self.base_url + "schemedit"
		else:
			url = self.base_url + instance
		url = url + "/" + frag
		print "url:", url
		return url
		
	def getVersion (self):
		url = os.path.join (self.base_url, 'about.jsp')
		try :
			self.url_opener.tries = 0
			data = self.url_opener.open(url)   # open file by url
			html = data.read()

		except IOError, error_code :		# catch the error
			if error_code[0] == "http error" :
				# print "error: ", error_code[1]
				raise IOError, "http error: %s" % error_code[1]
			else:
				raise IOError, "%s" % sys.exc_info()[1]
			
			
		pat = re.compile ("<p>Version (.*?)</p>")
		m = pat.search (html)
		if m:
			# print "Version: %s" % m.group(1)
			return m.group(1)
		else:
			raise Exception, "Version not found"


def testOne ():
	url = "http://ncs.nsdl.org/mgr"
	r = Requestor(url)
	## r.foo ("http://www.google.com")
	r.getVersion ()	

def testAll ():
	for instance in instances:
		name = instance[0]
		url = instance[1]
		if not name:
			print ''
			continue
		r = Requestor(url)
		try:
			version = r.getVersion ()
		except:
			version = "Error: %s" % sys.exc_info()[1]
		print "%20s: %s" % (name, version)
	
if __name__ == "__main__":
	testAll()




