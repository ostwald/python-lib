"""

How to search for all records for a given fiscal year?
- determine the endpoints. E.b., FY2010 begins 9/30/09 and ends 10/1/10 ??
(see utils for FiscalYear class)

- work out query to search (again, hasn't this been done?)

custom field: osmDateFiscal

date range query params:    
	
	{
		dateField : osmDateFiscal,
		fromDate : fy2010.start,
		endDate : fy2010.end
	}
	
* dateField - an optional argument that indicates which index date field to
search in. If supplied, one or both of either the fromDate or toDate arguments
must be supplied.

* fromDate - an optional argument that indicates a date range to search from. If
supplied, the dateField argument must also be supplied.

* toDate - an optional argument that indicates a date range to search to. If
supplied, the dateField argument must also be supplied.

Don't know what role *Authors* will have but should think about it:
	Apply the PAR search:
		if upid match: 100% confidence
		if name match (last name, first name, and middle): high confidence
		else (only last name match): low confidence

use case:
	find fy10 records written by Greg Holland:
		Author represented by a AuthorEntry supporting a dict interface with
		keys specified by mmm_author.author_fields.
		
		- lastName - /record/authors/author/firstName
		- nickName - /record/authors/author/firstName  !! there is no middle name. here we might sub nickname for first??
		- upid - /record/contributors/person/@UCARid
		
"""

import os, sys
from author_xls import AuthorWorksheet
from ncar_lib.repository import SummarySearcher, SearchResult, OsmSearchResult

class FiscalYearReporter (SummarySearcher):
	"""
	we want to search for Done records within Fy2010 that were written by either one or more authors
	"""
	default_baseUrl = "http://nldr.library.ucar.edu/schemedit/services/ddsws1-1"

	verbose = False
	
	default_collection = 'osgc'
	
	def __init__ (self, year=None, collection=None, xmlFormat=None, baseUrl=None):
		baseUrl = baseUrl or self.default_baseUrl
		collection = collection or self.default_collection
		self.year = year
				
		self.base_params = {
			'verb' : 'Search',
			# 'dcsStatus' : 'Done',
			'ky' : collection,
			'xmlFormat' : xmlFormat,
			'storedContent':[
				'dcsstatus', 
				'dcsstatusNote', 
				'dcsisValid',
				'dcsosmFiscalYear',
				'dcsosmFlattenedTitle'
				]
			}
		
		
		SummarySearcher.__init__ (self, collection, xmlFormat, baseUrl)

		
	def get_params_simple (self, collection, xmlFormat):
		"""
		just match osmDateFiscal date ...
		"""
		
		self.base_params.update ({
			'q' : 'dcsosmFiscalYear:%s' % self.year,
		})
		
		return self.base_params

	def get_params_multi (self, collection, xmlFormat):
		"""
		just match osmDateFiscal date ...
		"""
		
		self.base_params.update ({
			'q' : 'dcsosmFiscalYear:2008 OR dcsosmFiscalYear:2009'
			})
			
		return self.base_params
			
	def get_params_range (self, collection, xmlFormat):
		"""
		bummer: i don't think this works ....
		"""
		
		print 'fromDate: %s. endDate: %s' % (fromDate, endDate)
		
		self.base_params.update ({
			'dateField' : "dcsosmFiscalYear",
			'fromDate' : '2008',
			'endDate' : '2009',
			})
			
		return self.base_params
			

	get_params = get_params_simple
			
def reportByFiscalYear (collection):
	years = range(2011, 1950, -1)
	for year in years:
		s = FiscalYearReporter (year=year, collection=collection)
		print '%d - %d' % (year, s.numRecords)
				
if __name__ == '__main__':
	print '\n----------------------------'
	reportByFiscalYear ('not-fy10')
	# dateRangeTester()
	#searcher = 	s = FiscalYearReporter (year=2010)
	# print 'searcher got %d results' % len(searcher)
