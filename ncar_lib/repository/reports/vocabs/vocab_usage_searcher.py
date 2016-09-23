"""
instName_searcher - find occurances of a given value for instaName by searching all osm
records in the following fields:
	/key//record/contributors/person/affiliation/instName
	/key//record/contributors/organization/affiliation/instName
"""
import os, sys
from ncar_lib.repository import RepositorySearcher, OsmSearchResult
from JloXml import XmlRecord
import vocab_data

XmlRecord.debug = 1

default_baseUrl = "http://nldr.library.ucar.edu/schemedit/services/ddsws1-1"

class VocabUsageSearcher (RepositorySearcher):
	"""
	find records that contain a given vocab term (in a particular for this vocabType)
	results are exposed via UserList API
	"""
	numToFetch = 200
	batchSize = 200
	searchResult_constructor = OsmSearchResult
	verbose = True
	
	def __init__ (self, term, indexField, baseUrl=default_baseUrl):
		self.term = term
		self.indexField = indexField
		self.results = []  # all search hits
		RepositorySearcher.__init__(self,  baseUrl)
	
	def get_params (self, collection, format):
		
		# collections_q = 'allrecords:true NOT (%s)' % ' OR '.join(map (lambda x:"key:"+x, vocab_data.test_collections))
		collections_q = '%s' % ' OR '.join(map (lambda x:"key:"+x, vocab_data.test_collections))
		
		maketerm = lambda field:'%s:"%s"' % (field, self.term)
		if type(self.indexField) == type(""):
			q = maketerm (self.indexField)
		elif type(self.indexField) == type([]):
			q = ' OR '.join (map (maketerm, self.indexField))
		else:
			raise Exception, 'could not process self.indexField of type: %s' % type(self.indexField)
			
		q = '%s NOT (%s)' % (q, collections_q)
			
		params = {
			'verb' : 'Search',
			'xmlFormat' : 'osm',
			'q' : q,
			# 'dcsStatus' : 'Done',
			'storedContent':[
				'dcsstatus', 
				'dcsstatusNote', 
				'dcsisValid'
				]
			}
		return params
		
if __name__ == '__main__':
	# term = "IDAEA, Consejo Superior de Investigaciones Cientificas"
	term = "University of Graz"
	# term = "great event"
	# index_fields = '/key//record/general/eventName'
	index_fields = [
				'/key//record/contributors/person/affiliation/instName',
				'/key//record/contributors/organization/affiliation/instName'
			]
	searcher = VocabUsageSearcher (term, index_fields)
	# searcher = VocabUsageSearcher ()
	print "%d results found for '%s'" % (len (searcher), searcher.term)
	
	for result in searcher.data:
		print result.recId
	
	if 0:
		recordCreatedDates = map (lambda x:x.payload.getRecordDate(), searcher.data)
		recordCreatedDates.sort()
		for recordCreated in recordCreatedDates:
			print recordCreated

