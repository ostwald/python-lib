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
from par_globals import *
from parResult import ParResult, recordSchema, personSchema


class ParReport (RepositorySearcher):
	"""
	for each submitter, display the # of sumissions between 2010-8-16 and 2010-10-31
	
	List API to search hits (instances of specified searchResult_constructor)
	
	The following lists are of instances created by self.parResult_class
	- self.results = []  # all search hits
	- self.upid_matches = [] # upid matches are pretty sure:-)
	- self.name_matches = []  # match as far as we can tell (but should be verified checked)
	- self.lastName_matches = [] # match only on last name, so they probably aren't matches
	"""

	numToFetch = 2000
	batchSize = 200
	searchResult_constructor = SearchResult
	# filter_predicate = self.parAuthorFilter
	verbose = True
	parResult_class = None
	
	def __init__ (self, parAuthor, baseUrl=default_baseUrl):
		self.parAuthor = parAuthor
		self.results = []  # all search hits
		self.upid_matches = [] # upid matches are pretty sure:-)
		self.name_matches = []  # match as far as we can tell (but should be verified checked)
		self.lastName_matches = [] # match only on last name, so they probably aren't matches
		RepositorySearcher.__init__(self,  baseUrl)
			
	def get_params (self, collection, xmlFormat):
		"""
		define the params used to query the search service
		"""
		raise Exception, "get_params is not instantiated"
	
	def processResults (self):
		"""
		populate self.results with list of ParResult instances (self.parResult_class)
		
		we want to find the "matching person" from each osmRecord and associate them with
		one of the lists (upid_matches, name_matches, lastName_matches)
		"""
		print "\nprocessResults"
		print "there were %d records found" % len (self)
		for result in self:
			parResult = self.parResult_class (result, self.parAuthor)
			
			# print 'target: %s . bestMatch: %s' % (self.parAuthor.upid, parResult.matchingPerson.upid)
			
			if parResult.matchingPerson.upid and self.parAuthor.upid:
				# print 'matching person upid: %s' % parResult.matchingPerson.upid
				if self.parAuthor.upid == parResult.matchingPerson.upid:
					self.upid_matches.append (parResult)
					# print '  upid_matches: %s' % result.recId
				else:
					# eliminate mis-matched upids from report
					# print 'eliminated %s for upid mismatch (%s)' % (result.recId, parResult.matchingPerson.upid)
					continue
				
			elif self.parAuthor.matchesPersonName (parResult.matchingPerson):
				self.name_matches.append (parResult)
				# print '  name_matches: %s' % result.recId
			else:
				self.lastName_matches.append (parResult)
				# print '  lastName_matches: %s' % result.recId
				
			self.results.append(parResult)
				
	def summarize (self):
		print "\nReporting for %s" % self.parAuthor
		print "%d upid matches (sure match)" % len(self.upid_matches)
		print "%d name matches (to verify)" % len(self.name_matches)
		print "%d last name matches (low probalilty)" % len(self.lastName_matches)
		#for parResult in self.results:
			# print parResult.recId
			# print parResult.matchingPerson.upid
			# mp = parResult.matchingPerson
			# print "%s, %s, %s (%s)" % (mp.firstName, mp.middleName, mp.lastName, mp.upid)
			
	def writeTabDelimited (self, records, outpath=None):
		s = [];add=s.append
		# header
		add ('\t'.join (recordSchema + personSchema))
		
		for result in (records):
			add (result.asTabDelimited())
			
		tabDelimited = '\n'.join (s)
		if outpath is None:
			outpath = 'reports/' + self.parAuthor.lastname+'.txt'
		## fp = open (outpath, 'w')
		fp = codecs.open(outpath, 'w', "utf-8")
		fp.write (tabDelimited)
		fp.close()
		
		print 'wrote tab-delimited to ', outpath

	def writeReports (self):
		# high confidence
		name = self.parAuthor.lastname+'.txt'
		records = self.upid_matches + self.name_matches
		self.writeTabDelimited (records, os.path.join ('reports', name))
		
		# other
		name = self.parAuthor.lastname+'_other.txt'
		records = self.lastName_matches
		self.writeTabDelimited (records, os.path.join ('reports', name))
		



