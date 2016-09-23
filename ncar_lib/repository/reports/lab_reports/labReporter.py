"""
Make a report for all pubs by a group of authors

from jamaica:
	So, here's the first list (from MMM).  We're expecting similar lists from ACD and CGD.  
	We want to search over all DONE records with a fiscal year of 2010.  
	Output should be in excel, and should include the following fields:

   * Authors
   * Title
   * pubName
   * Volume, issue, page numbers (as available)
   * doi (as available)
   * Classification
   * Status (published, in press, etc)
   * DCS record number
   
author information is stored in 'data/mmm_authors.txt' (tab-delimited),and accessed using mmm_authors.AuthorWorksheet
- find upid #s for those that couldn't be found
- ask J how the authors are used? (do we want individual reports?)

- NO! we put them all together as one, right Jamaica?

Search the NCS:
	- DONE records
	- fiscal year = 2010
	
Collect Info specified above from results:
	for Authors I guess I make a list or something
	
Extend OsmAuthorSearcher

-------------------------
NOTES

* Searching for Fiscal Year *
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

* What do to with authors?? *
Don't know what role *Authors* will have but should think about it:
	Apply the PAR search:
		if upid match: 100% confidence
		if name match (last name, first name, and middle): high confidence
		else (only last name match): low confidence

use case
	find fy10 records written by Greg Holland:
		Author represented by a AuthorEntry supporting a dict interface with
		keys specified by mmm_author.author_fields.
		
		- lastName - /record/authors/author/firstName
		- nickName - /record/authors/author/firstName  !! there is no middle name. here we might sub nickname for first??
		- upid - /record/contributors/person/@UCARid
"""
import os, sys, codecs
import utils
from author_xls import get_MMM_authors, get_ACD_authors, get_GCD_authors
from ncar_lib.repository.author_search import OsmAuthorSearcher, OsmAuthorSearchResult, Author
from ncar_lib.repository import OsmSearchResult
from labReportResult import LabReportResult
from UserList import UserList

class LabReporter (OsmAuthorSearcher):
	"""
	
	LabReporter searches over 'osgc' and 'not-fy10' collections
	for a specific AUTHOR and generates a report
	
	extends OsmAuthorSearcher - creates three lists whose members are matches (written by author) of
	varying degree of confidence.
	- self.results - all results
	- self.upid_matches - certain confidence
	- self.name_matches = high confidence
	- self.lastName_matches = low confidence
	
	Searches over Fy10, for status=Done for a specified author
	"""
		
	numToFetch = 200
	searchResult_constructor = OsmSearchResult
	authorSearchResult_class = LabReportResult
	verbose = 0
	
	collection = ['osgc', 'not-fy10']
	default_fiscal_year = 2010
	report_dir = None
	
	def __init__ (self, author, fiscalYear=None):
		self.fiscalYear = fiscalYear or self.default_fiscal_year
		OsmAuthorSearcher.__init__ (self, author)
	
	def get_params (self, collection, xmlFormat):
		base_params = OsmAuthorSearcher.get_params(self, collection, xmlFormat)
		authorQuery = base_params['q']
		fiscalQuery = fiscalQuery = 'osmDateFiscal:%s' % self.fiscalYear
		base_params.update ({
			'dcsStatus' : 'Done',
			'ky' : self.collection,			
			'q': "%s AND %s" % (authorQuery, fiscalQuery)
		})
		return base_params
		
	def log (self, s):
		if self.verbose:
			print s
		
			
	def writeTabDelimited (self, outpath=None, records=None):
		s = [];add=s.append
		
		records = records or self.results
		
		# make header
		hdr = '\t'.join (self.authorSearchResult_class.report_fields)
		add (hdr)
		
		for result in (records):
			add (result.asTabDelimited())
			
		tabDelimited = '\n'.join (s)
		if outpath is None:
			if self.report_dir is None:
				raise Exception, 'report_dir is not initialized for this lab reporter'
			if not os.path.exists(self.report_dir):
				os.mkdir (self.report_dir)
			#reportName = str(self.author).replace(' ', '_')
			reportName = '%s_%s' % (self.author.lastname, self.author.firstname)
			outpath = os.path.join(self.report_dir, reportName +'.txt')
		## fp = open (outpath, 'w')
		fp = codecs.open(outpath, 'w', "utf-8")
		fp.write (tabDelimited)
		fp.close()
		
		print 'wrote tab-delimited to ', outpath
		
class BatchReporter(UserList):
	
	default_authors = None
	lab_reporter_class = None
	
	def __init__ (self, authors):
		# self.authors = get_MMM_Authors()
		self.authors = authors or self.default_authors
		print '\nReporting over %d authors' % len (self.authors)
		for author in self.authors:
			print author
			self.reportAuthor(author)
	
	def reportAuthor(self, author):
		reporter = self.lab_reporter_class(author)
		# reporter.showParams()
		reporter.summarize()
		reporter.writeTabDelimited ()
		
class ACDReporter (LabReporter):
	
	report_dir = 'ACD-report'
	
class ACDBatchReporter (BatchReporter):
	
	default_authors = get_ACD_authors()
	lab_reporter_class = ACDReporter
	
class GCDReporter (LabReporter):
	
	report_dir = 'GCD-report'
	
class GCDBatchReporter (BatchReporter):
	
	default_authors = get_GCD_authors()
	lab_reporter_class = GCDReporter
	
if __name__ == '__main__':
	if 0:
		authors = get_GCD_authors()
		print "%d authors read" % len(authors)
		for a in authors:
			print a.lastname
	else:
		authors = get_GCD_authors()[:1]
		authors = [Author ('Li', 'Z', upid='2390')]
		GCDBatchReporter (None)
	
