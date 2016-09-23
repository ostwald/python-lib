import sys, codecs
from UserList import UserList
from JloXml import XmlUtils
from ncar_lib.repository import RepositorySearcher, OsmSearchResult
from dds_title_search import TitleSearcher
baseUrl = "http://nldr.library.ucar.edu/schemedit/services/ddsws1-1"


"""
Use search service to retrieve a batch of osm records and check for records with duplicate titles
"""

default_baseUrl = "http://nldr.library.ucar.edu/schemedit/services/ddsws1-1"

class UniqueTitleGetter (RepositorySearcher):

	"""
	optimize RepositorySearcher to collect only RecordIds from search results
	"""
	
	numToFetch = 2000
	batchSize = 200
	verbose = True
	title_path = 'DDSWebService:Search:results:record:metadata:record:general:title'
	
	def __init__ (self, collection=None, xmlFormat=None, baseUrl=default_baseUrl):
		unique_titles = []
		RepositorySearcher.__init__ (self, collection, xmlFormat, baseUrl)
	
	def get_result_batch (self, start, num):
		responseDoc = self.get_response_doc (start, num)
		responseDoc.xpath_delimiter = ":"
		titleNodes = responseDoc.selectNodes (responseDoc.dom, self.title_path)
		return map (lambda x:XmlUtils.getText(x), titleNodes)
		
	def processResults (self):
		unique_titles = []
		print "%d titles BEFORE filtering" % len (self)
		for title in self:
			if not title:
				continue
			if not title in unique_titles:
				unique_titles.append (title)
			else:
				# print title
				pass
			

		print "%d titles AFTER filtering" % len (unique_titles)
		self.unique_titles=unique_titles

class DupTitleChecker (UserList):
	"""
	after getting records from dds search, they are stored in self.recs
	"""

	dowrite = 1
	
	def __init__ (self, collection=None, xmlFormat=None, baseUrl=default_baseUrl):
		UserList.__init__ (self)

		self.titles = getUniqueTitles()
		
		print "processing %d unique titles" % len (self.titles)
		
		cnt = 0
		for title in self.titles:
			# sys.stdout.write('.')
			cnt += 1
			if cnt % 50 == 0:
				print "%d/%d" % (cnt, len(self.titles))
			dups = TitleSearcher (title, collection, xmlFormat).dups
			if dups:
				self.append (dups)

		if self.dowrite:
			self.write()
		else:
			self.report()
		
	def report (self):
		print "\nDup Title Checker Results"
		for dups in self:
			print "\n%s" % dups.title
			for result in dups.results:
				print " - %s | %25s | %s" % (result.recId, result.dcsstatus, result.dcsstatusNote)
				
	def toTabDelimited (self):
		s=[];add=s.append
		for dups in self:
			for result in dups.results:
				add ("%s\t%s\t%s\t%s" % (dups.title, result.recId, result.dcsstatus, result.dcsstatusNote))
		return '\n'.join(s)
				
	def toTabDelimited1 (self):
		s=[];add=s.append
		for dups in self:
			add ("%s\t%s\t%s" % (dups.title, "", ""))
			for result in dups.results:
				add ("%s\t%s\t%s" % (result.recId, result.dcsstatus, result.dcsstatusNote))
		return '\n'.join(s)
		
	def write (self):
		outpath = 'output/dupTitlesReport.txt'
		fp = codecs.open (outpath, 'w', 'utf-8')
		fp.write (self.toTabDelimited())
		fp.close()
		print "wrote to %s" % outpath
		
def getUniqueTitles():
	xmlFormat = 'osm'
	collection = 'osgc'
	titles = UniqueTitleGetter(collection, xmlFormat).unique_titles
	titles.sort()
	
	print "getUniqueTitles returning %d titles" % len(titles)
	
	return titles
	# for title in titles:
		# print title.encode('utf-8')	
		
if __name__ == '__main__':
	
	xmlFormat = 'osm'
	collection = 'osgc'
	checker = DupTitleChecker(collection, xmlFormat)

	




