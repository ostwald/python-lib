"""
Goal: find all refs in OpenSky (NCAR Library DCS) that a particular person (e.g., "Phil Judge") 
has contributed.

produce a report of the following fields: record #, title, collection, and status. 

sorted on title (but of course, this could be done in spreadsheet).

Challenge: we have to look across both 'osm' and 'citation' frameworks (any others?).


"""

# from UserList import UserList
# from UserDict import UserDict
# from serviceclient import ServiceClient, URL
# from JloXml import XmlRecord, XmlUtils
# from ncar_lib import RepositorySearcher, OsmSearchResult
# from ncar_lib.util import unionDateToSecs

import os, sys, codecs
from par_globals import *

from osmPar import OsmParReport
from citationPar import CitationParReport
from parResult import recordSchema, personSchema

"""
Use search service to retrieve a batch of records and then process them
"""

class ParReporter:
	
	def __init__ (self, parAuthor):
		self.parAuthor = parAuthor
		OsmParReport.verbose = CitationParReport.verbose = False
		self.osmPar = OsmParReport (parAuthor)
		self.citationPar = CitationParReport (parAuthor)
		
		self.results = self.osmPar.results + self.citationPar.results  # all search hits for lastName
		self.upid_matches = self.osmPar.upid_matches + self.citationPar.upid_matches
		self.name_matches = self.osmPar.name_matches + self.citationPar.name_matches
		self.lastName_matches = self.osmPar.lastName_matches + self.citationPar.lastName_matches
	
	def summarize (self):
		self.osmPar.summarize()
		self.citationPar.summarize()
		
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

def processParAuthor (parAuthor):
	print '\nprocessing %s ...' % parAuthor.lastname
	reporter = ParReporter(parAuthor)
	reporter.summarize()
	reporter.writeReports ()
	
def processParAuthors():
	for parAuthor in Authors_to_run:
		processParAuthor (parAuthor)
		
if __name__ == '__main__':
	from dares_authors import dares_authors
	processParAuthors()


