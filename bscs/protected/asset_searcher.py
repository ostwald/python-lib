"""
finds metadata records that catalog an asset with given filename

pattern :h*/protected/*/filename

VERIFY: must file urls in the following formats:
- assessments (yes - it is found for BOTH xpaths - i.e., question and answer paths)
- ncs_item - yes
- adn - yes
- dlese_anno - yes
- comm_anno - yes

NOTE: we are NOT searching over the 'url' field, but rather using urlenc with the term
encoded with luceneEncodeToTerm 

xmlFormats = ['adn', 'nsdl_dc', 'dlese_anno', 'comm_anno']

"""
import os, sys, re, string
from repo import RepositorySearcher
from JloXml import XmlRecord, MetaDataRecord, XmlUtils, AdnRecord
from bscs.protected import base_protected_url, getAssetPath
from url_rewriting_records import urlRewritingRecordClasses

queryData = {
	'adn' : 'svunit0act3.pdf',
	# 'assessments' : 'svunit0act3_assess.pdf',
	'assessments' : 'fooberry.pdf',
	'ncs_item' : "TaskDA1.4_11.pdf",
	'dlese_anno' : "bscsSciExplanation.pdf",
	'comm_anno' : "esch1_standards.pdf" # note - i didn't find any comm_anno using url query ...
}

def luceneEncodeToTerm (s, encodeWildCards=True, encodeSpace=True):
	if s is None:
		return None;
	
	chars = s
	buf = ''
	for ch in chars:
		if ch in string.digits or ch in string.letters:
			buf += ch
		else:
			
			if encodeWildCards and ch == '*':
				buf += "*"
			elif not encodeSpace and ch == ' ':
				buf += ' '
			else:
				buf += 'x' + str(ord(ch));
	
	return buf.lower();


class AssetSearcher (RepositorySearcher):
	"""
	A searcher for records having a protected Url
	"""
	
	default_baseUrl = 'http://localhost:8070/curricula/services/ddsws1-1'
	numToFetch = 10
	batchSize = 200
	verbose = 0

	def __init__ (self, filename, collection=None, xmlFormat=None, baseUrl=None):
		self.formatTally = {}
		self.filename = filename
		RepositorySearcher.__init__(self, collection, xmlFormat, baseUrl)

	def get_params (self, collection, xmlFormat):
		"""
		define the params used to query the search service
		"""
		# query = 'url:h*\/protected\/*\/%s' % self.filename
		url = 'h*/protected/*/%s' % self.filename # works
		
		# url = 'http://ccs.dls.ucar.edu/home/protected/assess_dps/dps_u1introHelicopter.pdf'
		
		# print 'QUERY', query
		
		if 0: 
			query = "url:%s" % url
		else:
			query = "urlenc:%s" % luceneEncodeToTerm(url)
		
		return {
			"q":query,
			# "verb": "CheckUrl",
			"verb": "Search",
			# "xmlFormat": "assessments"
			# "ky" : collection
			}
			
	def processResults(self):
		print 'processResults ...'
		formats = {}
		for result in self:
			xmlFormat = result.xmlFormat
			num = formats.has_key(xmlFormat) and formats[xmlFormat] or 0
			formats[xmlFormat] = num + 1
		self.formatTally = formats
		
	def reportFormatTally(self):
		keys = self.formatTally.keys()
		keys.sort()
		for key in keys:
			print '- %s - %d' % (key, self.formatTally[key])

def testXmlFormat (filename, xmlFormat):
	searcher = AssetSearcher(filename, xmlFormat=xmlFormat)
	# searcher = AssetSearcher(filename)
	if searcher.data:
		print '\n* %s * - %d Records FOUND' % (xmlFormat, len(searcher.data))
		for result in searcher:
			print '- ', result.recId
	else:
		# print '* %s * - NO Records FOUND' %xmlFormat
		raise KeyError, '* %s * - NO Records FOUND' %xmlFormat

if __name__ == '__main__':

	
	if 1: # test all
		for xmlFormat in queryData.keys():
			filename = queryData[xmlFormat]
			if filename:
				testXmlFormat (filename, xmlFormat)
		
	if 0: # test one
		xmlFormat = 'dlese_anno'
		filename = queryData[xmlFormat]
		
		# override filename if desired
		# filename = 'fooberry'
		
		testXmlFormat (filename, xmlFormat)

