"""
Goal: find all refs in OpenSky (NCAR Library DCS) that a particular person (e.g., "Phil Judge") has contributed to

produce a report of the following fields: record #, title, collection, and status. 
sorted on title (but of course, this could be done in spreadsheet).

Challenge: we have to look across both 'osm' and 'citation' frameworks (any others?).

Approach: start with repository.
- search for all records with an author with same LASTNAME

categories of matches (in order of trustworthiness):
	- matching upid number
	- Matching lastname, firstinitial, lastinitial
	- matching lastname
"""


import codecs, os
from ncar_lib import RepositorySearcher, SearchResult
from author_search_globals import *
from authorSearchResult import AuthorSearchResult, recordSchema, personSchema


class AuthorSearcher (RepositorySearcher):
	"""
	for each submitter, display the # of sumissions between 2010-8-16 and 2010-10-31
	
	List API to search hits (instances of specified searchResult_constructor)
	
	The following lists are of instances created by self.authorSearchResult_class
	- self.results = []  # all search hits
	- self.upid_matches = [] # upid matches are pretty sure:-)
	- self.name_matches = []  # match as far as we can tell (but should be verified checked)
	- self.lastName_matches = [] # match only on last name, so they probably aren't matches
	"""

	numToFetch = 2000
	batchSize = 200
	searchResult_constructor = SearchResult
	# filter_predicate = self.authorFilter
	verbose = True
	authorSearchResult_class = None
	
	def __init__ (self, author, baseUrl=default_baseUrl):
		self.author = author
		self.results = []  # all search hits
		RepositorySearcher.__init__(self,  baseUrl)
			
	def get_params (self, collection, xmlFormat):
		"""
		define the params used to query the search service
		"""
		raise Exception, "get_params is not instantiated"
	
	def processResults (self):
		"""
		populate self.results with list of AuthorSearchResult instances (self.authorSearchResult_class)
		
		find the "best matching person" from each osmRecord and associate each with a
		"confidence" indicator based on whether they matched 
			upid (certian) full name (high), last name only (low)
		
		self.results will contain only those results with at least a low confidence 
		"""
		print "\nAuthorSearcher.processResults"
		print "there were %d records found" % len (self)
		for result in self:
			authorSearchResult = self.authorSearchResult_class (result, self.author)
			
			# print 'target: %s . bestMatch: %s' % (self.author.upid, authorSearchResult.matchingPerson.upid)
			
			if authorSearchResult.matchingPerson.upid and self.author.upid:
				# print 'matching person upid: %s' % authorSearchResult.matchingPerson.upid
				if self.author.upid == authorSearchResult.matchingPerson.upid:
					authorSearchResult.confidence = CERTAIN_CONFIDENCE
					
					#self.upid_matches.append (authorSearchResult)
					# print '  upid_matches: %s' % result.recId
				else:
					# eliminate mis-matched upids from report
					# print 'eliminated %s for upid mismatch (%s)' % (result.recId, authorSearchResult.matchingPerson.upid)
					continue
				
			elif self.author.matchesPersonName (authorSearchResult.matchingPerson):
				authorSearchResult.confidence = HIGH_CONFIDENCE
				# self.name_matches.append (authorSearchResult)
				# print '  name_matches: %s' % result.recId
			else:
				# self.lastName_matches.append (authorSearchResult)
				authorSearchResult.confidence = LOW_CONFIDENCE
				# print '  lastName_matches: %s' % result.recId
				
			if authorSearchResult.confidence:
				self.results.append(authorSearchResult)
				
	def summarize (self):
		upid_matches = filter (lambda x:x.confidence == CERTAIN_CONFIDENCE, self.results)
		name_matches = filter (lambda x:x.confidence == HIGH_CONFIDENCE, self.results)
		lastName_matches = filter (lambda x:x.confidence == LOW_CONFIDENCE, self.results)
		print "\nReporting for %s" % self.author
		print "%d upid matches (sure match)" % len(upid_matches)
		print "%d name matches (to verify)" % len(name_matches)
		print "%d last name matches (low probalilty)" % len(lastName_matches)
		#for authorSearchResult in self.results:
			# print authorSearchResult.recId
			# print authorSearchResult.matchingPerson.upid
			# mp = authorSearchResult.matchingPerson
			# print "%s, %s, %s (%s)" % (mp.firstName, mp.middleName, mp.lastName, mp.upid)
			
class ReporterMixin:
		
	def writeTabDelimited (self, records=None, outpath=None):
		records = records or self.results
		
		s = [];add=s.append
		# header
		add ('\t'.join (recordSchema + personSchema))
		
		for result in (records):
			add (result.asTabDelimited())
			
		tabDelimited = u'\n'.join (s)
		if outpath is None:
			outpath = 'reports/' + self.author.lastname+'.txt'
		## fp = open (outpath, 'w')
		fp = codecs.open(outpath, 'w', "utf-8")
		fp.write (tabDelimited)
		fp.close()
		
		print 'wrote tab-delimited to ', outpath

	def writeReports (self):
		# high confidence
		name = self.author.lastname+'.txt'
		records = self.upid_matches + self.name_matches
		self.writeTabDelimited (records, os.path.join ('reports', name))
		
		# other
		name = self.author.lastname+'_other.txt'
		records = self.lastName_matches
		self.writeTabDelimited (records, os.path.join ('reports', name))
			



