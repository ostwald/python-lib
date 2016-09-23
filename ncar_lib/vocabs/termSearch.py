import os, sys
from UserList import UserList
from ncar_lib.repository import RepositorySearcher, SearchResult
from serviceclient import ServiceClient
from ncar_lib.osm import OsmRecord
from JloXml import XmlRecord, XmlUtils
	
class TermSearcher (RepositorySearcher):
	
	baseUrl = "http://nldr.library.ucar.edu/schemedit/services/ddsws1-1"
	verbose = False
	dowrite = 0
	
	def __init__ (self, term, searchFields):
		"""
		searchFields can be a list of fields. In this case, the query ORs together the
		fields, each clause with the same term value
		"""
		self.term = term
		if type(searchFields) == type(""):
			self.searchFields = [searchFields]
		else:
			self.searchFields = searchFields
		RepositorySearcher.__init__(self, self.baseUrl)
		
	def get_params (self, collection, xmlFormat):
		"""
		searchFields can be a list of fields. In this case, the query ORs together the
		fields, each clause with the same term value
		"""
		q = ' OR '.join (map (lambda x:'%s:"%s"' % (x, self.term), self.searchFields))
		# print q
		
		return {
			"verb": "Search",
			'q': q,
			"xmlFormat": 'osm'
		}
		
	def report (self):
		s=[];add = s.append
		add (self.term)
		for result in self:
			add (result.recId)
		return '\n - '.join(s)

class TermCounter (TermSearcher):
	
	def __init__ (self, term, searchFields):
		UserList.__init__ (self)
		self.term = term
		if type(searchFields) == type(""):
			self.searchFields = [searchFields]
		else:
			self.searchFields = searchFields
		
		self.params = self.get_params(None, None)
		self.service_client = ServiceClient (self.baseUrl)
		self.numRecords = self._get_num_records()
		if self.verbose:
			print "%d total records" % self.numRecords

		
if __name__ == '__main__':
	if 0:
		term = 'Communications in Asteroseismology'
		searchField = '/key//record/general/pubName'
	
	else:
		term = 'National Center for Atmospheric Research (NCAR)'
		searchField1 = [
			'/key//record/contributors/organization/affiliation/instName',
			'/key//record/contributors/person/affiliation/instName'
		]
		searchField2 = '/key//record/contributors/organization/affiliation/instName'
		searchField3 = '/key//record/contributors/person/affiliation/instName'
	
	# numresults = len(TermSearcher(term, searchField))
	numresults = TermCounter(term, searchField3).numRecords
	print "%d results found for %s" % (numresults, term)
	


