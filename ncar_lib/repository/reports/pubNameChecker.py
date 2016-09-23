"""
Compile a list of all osgc records with either no pubName or illegal pubName and produce
a tab-delimited report
"""

import codecs
from ncar_lib.repository import RepositorySearcher, OsmSearchResult
from ncar_lib.osm import OsmRecord
from ncar_lib.osm.vocabs.pub_name.pubNameXSD import PubNameXSD

baseUrl = "http://nldr.library.ucar.edu/schemedit/services/ddsws1-1"
default_baseUrl = "http://nldr.library.ucar.edu/schemedit/services/ddsws1-1"


def getTermList ():
	xsd = PubNameXSD("../../osm/vocabs/pub_name/pubName.xsd")
	
	sortedTerms = xsd.getSortedTerms()
	print "%d terms read from pubName.xsd" % len (sortedTerms)
	return sortedTerms

	
class PubNameChecker (RepositorySearcher):
	"""
	after getting all results from dds search, report on results that
	have bad pubnames
	"""
	numToFetch = 2000
	batchSize = 200
	searchResult_constructor = OsmSearchResult
	dowrite = 1
	
	def __init__ (self, collection=None, xmlFormat=None, baseUrl=default_baseUrl):
		self.termList = getTermList()
		self.badRecs = []
		RepositorySearcher.__init__ (self, collection, xmlFormat, baseUrl)
		
	def get_params (self, collection, xmlFormat):
		"""
		define the params used to query the search service
		"""
		return {
			"verb": "Search",
			"xmlFormat": xmlFormat,
			"ky": collection,
			"storedContent":['dcsstatus', 'dcsstatusNote', 'dcsisValid']
			}
		
	def processResults (self):
		"""
		collect results having illegal pubName as "badRecs", and display or write to file
		depending on value of dowrite
		"""
		for result in self:
			myId = result.recId
			if not result.pubName in self.termList:
				
				# result fields to put in report
				fields = ['recId', 'pubName', 'dcsstatus', 'dcsstatusNote', 'dcsisValid']
				
				values = map (lambda x:getattr(result, x), fields)
				#print "values: %s" % values
				
				self.badRecs.append ('\t'.join (values))
								
		if self.dowrite:
			outpath = "output/badPubNames.txt"	
			fp = codecs.open (outpath, 'w', 'utf8')
			content = '\n'.join (self.badRecs)
			fp.write (unicode(content))
			# fp.write (content.encode('utf-8'))
			fp.close()
			print ("wrote to ", outpath)
		else:
			self.report()
			
	def report (self):
		print '\n'.join (self.badRecs)
			
if __name__ == '__main__':
	xmlFormat = 'osm'
	collection = 'osgc'
	PubNameChecker(collection, xmlFormat)



