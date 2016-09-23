import os, sys
from ncar_lib.repository import RepositorySearcher, SearchResult
from ncar_lib.osm import OsmRecord
from JloXml import XmlRecord, XmlUtils
	
class Dups:
	
	def __init__ (self, title, results):
		self.title = title
		self.results = results
		
	def size (self):
		return len(self.results)
	
class TitleSearcher (RepositorySearcher):
	
	# stop_collections = ["staffnotes"]
	# stop_collections = []
	baseUrl = "http://nldr.library.ucar.edu/schemedit/services/ddsws1-1"
	verbose = False
	dowrite = 0
	
	def __init__ (self, title, collection=None, xmlFormat='osm'):
		self.title = title
		self.dups = None
		RepositorySearcher.__init__(self, collection, xmlFormat)
		
	def get_params (self, collection, xmlFormat):
		return {
			"verb": "Search",
			'q':'/key//record/general/title:"%s"' % self.title,
			'storedContent':['dcsstatus','dcsstatusNote'],
			"xmlFormat": xmlFormat,
			"ky": collection,
			's': '0',
			'n': '100'
		}

	def processResults (self):
		if len(self) < 2: return
		self.dups = Dups(self.title, self.data)
		
	def report (self):
		s=[];add = s.append
		add (self.title)
		for result in self:
			# result fields to put in report
			fields = ['recId', 'dcsstatus', 'dcsstatusNote']
			values = map (lambda x:getattr(result, x), fields)
			add ('\t'.join (values))
		return '\n - '.join(s)
				
	def report1 (self):
		print "%d results found for %s" % (len (self), self.title)
		for result in self:
			result.report()
		
def getterTester(title):
	# asset = "asset-000-000-000-040"

	try:
		getter = TitleSearcher(title)
		# print getter.result
		# getter.result.report()	
	except:
		print sys.exc_info()[1]

			
if __name__ == '__main__':
	# title = 'Atmospheric chemistry of an Antarctic volcanic plume'
	# title = 'Climatological Validation of Microwave Lower Stratosphere Temperature using GPS RO Data'
	# title = 'Overview: Oxidant and particle photochemical processes above a south-east Asian tropical rainforest (the OP3 project): Introduction, rationale, location characteristics and tools'
	title = 'Forecasting skill of model averages'
	# getterTester (title)
	results = TitleSearcher(title)
	size = results.dups and results.dups.size() or 0
	print "%d results found (%d)" % (len(results), size)
	


