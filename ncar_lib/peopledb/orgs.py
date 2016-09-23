"""
* Get all orgs by doing a search with no params (which returns all)
doc - https://wiki.ucar.edu/display/peopledb/Search+Organizations
e.g., https://people.api.ucar.edu/orgs/

Orgs produces a UserDict of all orgs (mapped to their acronym)
"""

import os, sys, urllib, urllib2, demjson, time, re
# from client import PeopleDBClient
from UserDict import UserDict
# from ncar_lib import unionDateToSecs
from organization import Organization
from ncar_lib.osm.vocabs import VocabXSD

class Orgs (UserDict):

	baseUrl = "https://people.api.ucar.edu/orgs/"
	
	def __init__ (self):
		"""
		"""
		self.data = {}
		resp = self.getResponse()
		
		for item in resp:
			org = Organization (item)
			self.data[org.acronym] = org
		
	def getResponse(self):
		url = self.baseUrl
		req = urllib2.Request(url)
		try:
			response = urllib2.urlopen(req)
		except urllib2.URLError, e:
			if hasattr(e, 'reason'):
				print 'we failed to reach the server.'
				print 'Reason:', e.reason
			elif hasattr (e, 'code'):
				print 'the server couldn\'t fulfill the request (%s)' % url
				print 'Error code:', e.code
			# print e.reason
			return
		return demjson.decode (response.read())

class InstDivXSD (VocabXSD):
	"""
	- reads in an instDiv.xsd template file
	"""
	xsd_path = '/Users/ostwald/tmp/instDivision.xsd'
	acronymPat = re.compile ('.*\((.*)\)')

	def __init__ (self):
		"""
		as an XSD we have access to the vocab values in the source xsd
		"""
		VocabXSD.__init__ (self, path=self.xsd_path)
		print self
		self.typeName = "instDivisionCurrentType"
		self.instDiv = self.getEnumerationType(self.typeName)
		assert self.instDiv is not None
			
	def getValues (self):
		"""
		gets the values of the instDiv vocab
		"""
		return self.getEnumerationValues(self.typeName)
		
	def getLeafAcronyms(self):
		ret=[]
		for val in self.getValues():
			last = val.split(':')[-1]
			m = self.acronymPat.match (last)
			if m:
				ret.append(m.group(1))
			else:
				print "ACRONYM NOT FOUND FOR %s" % val
		return ret

def main():
	orgs = Orgs ()
	xsd = InstDivXSD()
	for val in xsd.getLeafAcronyms():
		if not val in orgs.keys():
			print val, "NOT FOUND"
			if val[:-1] in orgs.keys():
				print ' ... %s found' % val[:-1] 

		
if __name__ == '__main__':
	main()
