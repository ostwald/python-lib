"""
Get the term values across all osm collections (except the test collections) using a
faceted search (i.e., the facets are term values and their counts).
"""

import os, sys
from ncar_lib.repository import SummarySearcher, SearchResult, OsmSearchResult, FacetedField
from ncar_lib.repository import SearchResult, OsmSearchResult
# from ncar_lib.repository.search_summary_nldr import SummarySearcher, FacetedField

import vocab_data

class FacetedSearcher (SummarySearcher):
	"""
	Searches Production NCS by default
	"""
	default_baseUrl = "http://nldr.library.ucar.edu/schemedit/services/ddsws1-1"

	verbose = True
	
	xmlFormat = 'osm'
	
	def __init__ (self, facetXpath, baseUrl=None):
		"""
		facetXpath can be a single path or a list of paths
		e.g., [
				'/key//record/contributors/person/affiliation/instName',
				'/key//record/contributors/organization/affiliation/instName'
		   	  ]
		"""
		self.facetXpath = facetXpath
		baseUrl = baseUrl or self.default_baseUrl
		SummarySearcher.__init__ (self, baseUrl=baseUrl)
		
		print 'FacetedSearcher instantiated'
		
		
	def get_params (self, collection, xmlFormat):
		
		q = 'allrecords:true NOT (%s)' % ' OR '.join(map (lambda x:"key:"+x, vocab_data.test_collections))
		
		params = self.base_params = {
			'q' : q,
			'verb' : 'Search',
			'xmlFormat' : 'osm',
			'facet' : 'on',
			'facet.field' : self.facetXpath,
			# 'facet.category' : 'UCARDivision',
			# 'dcsStatus' : 'Done',
			'storedContent':[
				'dcsstatus', 
				'dcsstatusNote', 
				'dcsisValid'
				]
			}
		return params
			
def getFacetedField (index_field):
	"""
	creates and populates a FacetedField instance, which holds Facets (term, count).
	accomodates case where a there are more than one index path at which
	a vocab can occur (e.g. //org/affiliation/instName, //person/affiliation/instName)
	"""
	searcher = FacetedSearcher(index_field)
	summary = searcher.summary
	norm = FacetedField ()
	norm.name = "Normalized Faceted Field for %s" % index_field
	reject_count = 0
	# get unique keys across facets (if more than one facetXpath is used, there may
	# dup values ...
	unique_keys = []
	if not summary.faceted_fields:
		print "no faceted fields found!!"
		return
		
	for field in summary.faceted_fields:
		for key in field.keys():
			if key not in unique_keys:
				unique_keys.append(key)
			else:
				# print 'rejected %s' % key
				reject_count += 1
			
	print "%d terms were rejected as dups" % reject_count
				
	# for key in unique_keys[:100]:
		# print key
		
	# now march through the facets normalizing values (sum up the counts
	# across possibly mulitple faceted fields
	for key in unique_keys:
		total_count = 0
		for field in summary.faceted_fields:
			if field.has_key(key):
				total_count = total_count + field[key]
		norm.add (key, total_count)
		
	return norm
	
		
def reportTester (index_field):
	reporter = FacetedSearcher(index_field)
	summary = reporter.summary
	
	if 0:
		facetedField = getFacetedField(xpath)
		if facetedField.facets is None:
			print "facetedField.facets is None for %s" % xpath
			continue
		for i, facet in enumerate(facetedField.facets):
			self.add (facet.term, facet.count)
			if i % 100 == 0:
				print "added %d/%d" % (i, len(facetedField.facets))

	print '%d faceted_fields found' % len(summary.faceted_fields)
	for field in summary.faceted_fields:  # field is a FacetedField instance
		print '%s (%d)' % (field.name, len(field))
		for term in field.getTerms():
			print " - %s (%s)" % (term, field.getCount(term))
				
def anotherTester ():
	instName_facetXpaths = [
		'/key//record/contributors/person/affiliation/instName',
		'/key//record/contributors/organization/affiliation/instName'
	]
	pubName_facetXpath = '/key//record/general/pubName'
	facetedField = getFacetedField(instName_facetXpaths)
	## facetedField.report(verbose=1)
	term = 'University of Graz'
	print '%s: %d' % (term, facetedField.getCount(term))
	
if __name__ == '__main__':
	print '\n----------------------------'
	# print reporter.service_client.request.getUrl()
	reportTester('/key//record/contributors/person/affiliation/instName')

