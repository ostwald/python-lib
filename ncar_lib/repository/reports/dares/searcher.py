"""
Dares Searcher
- what are the specs for our search?

Author - provided DaresAuthor
Collections - All
Format - osm
Years - any

Report:
	record number, collection, status
Metdata:
	assign upid and affiliation in metadata record (these could only be osm)

"""


import os, sys, codecs
import authors
from ncar_lib.repository.author_search import Author, OsmAuthorSearcher, \
			ReporterMixin, OsmAuthorSearchResult, personSchema

class DaresAuthorSearchResult (OsmAuthorSearchResult):
	"""
	Extend OsmAuthorSearchResult to expose attribute relevant to dares author reports and processing 
	- collection
	- status
	- recID
	- strength of match
	"""
	
	record_fields = ['recId', 'collection', 'status', 'matchStrength', 'publishedDate', 'recordDate']
	
	def __init__ (self, searchResult, Author):
		OsmAuthorSearchResult.__init__ (self, searchResult, Author)
		
	def asTabDelimited (self):
		s=[];add=s.append
		for field in self.record_fields:
			if field == 'matchStrength':
				add (self.getMatchStrength())
			else:
				add (str (getattr(self, field)))
		matchingAuthor = self.getMatchingPerson()
		for field in personSchema:
			add (getattr(matchingAuthor, field) or "")
		return '\t'.join (s)
		## return '\t'.join (map (lambda x:str(getattr(self, x)), self.report_fields))
		
	def __repr__ (self):
		return "%s - %s - %s - (%s)" % (self.recId, self.collection, self.status, self.getMatchStrength())


class DaresAuthorSearcher (OsmAuthorSearcher):
	"""
	Extend OsmAuthorSearcher, which returns a list of SearchResults
	for a given Author instance
	"""

	authorSearchResult_class = DaresAuthorSearchResult
	verbose = True
			

	def __init__ (self, author, baseUrl=None):
		OsmAuthorSearcher.__init__ (self, author, baseUrl)
	
	def get_params (self, collection, xmlFormat):
		"""
		define the params used to query the search service
		"""
		return {
			"verb": "Search",
			"ky": ['ams-pubs', 'osgc', 'not-fy10'],
			"storedContent":['dcsstatus', 'dcsstatusNote', 'dcsisValid'],
			'q': '/key//record/contributors/person/lastName:"%s"' % self.author.lastname
			}

# class DaresReporter (DaresAuthorSearcher, ReporterMixin):
class DaresReporter (DaresAuthorSearcher):
	"""
	we need to create reports listing the following for each result:
		collection, recordID, status, match_strength
	"""

	def summarize(self):
		DaresAuthorSearcher.summarize (self)
		for result in self.results:
			print result
			
	def writeTabDelimited (self, outpath=None, records=None):
		s = [];add=s.append
		
		records = records or self.results
		records.sort()
		
		# make header
		hdr = u'\t'.join (self.authorSearchResult_class.record_fields + personSchema)
		print 
		add (hdr)
		
		# print 'getting as tab delimited'
		for result in (records):
			# print ' adding a row'
			add (result.asTabDelimited())
			#print result.asTabDelimited()
		tabDelimited = '\n'.join (s)
		if outpath is None:
			reportName = str(self.author).replace(' ', '_')
			outpath = 'reports/' + reportName +'.txt'
		## fp = open (outpath, 'w')
		fp = codecs.open(outpath, 'w', "utf-8")
		fp.write (tabDelimited)
		fp.close()
		
		print 'wrote tab-delimited to ', outpath
		

def processDaresAuthor (name):
	print ("processDaresAuthor (%s)" % name)
	author = authors.getAuthor (name)
	print '\nprocessing %s ...' % author.lastname
	print "\n\n--------"
	if 0:
		searcher = DaresAuthorSearcher(author)
		searcher.summarize()
	else:
		reporter = DaresReporter(author)
		reporter.summarize()
		reporter.writeTabDelimited ()
	
def processDaresAuthors():
	for author in authors.getAllAuthors():
		processDaresAuthor (author)
		
if __name__ == '__main__':

	# processDaresAuthor ('Glen Romine')
	processDaresAuthors ()


