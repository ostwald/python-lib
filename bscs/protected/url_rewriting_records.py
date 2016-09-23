"""
URL records are metadata records that 
- know how to update their protected URls, and
- can move the protected asset to it's proper place in protected directory.

"""
import os, sys, re, shutil
from JloXml import XmlRecord, MetaDataRecord, XmlUtils, AdnRecord
from bscs.protected import base_protected_url, isProtectedUrl, isBscsProtectedUrl, \
						   getAssetPath, getReorgProtectedDir, isCcsProtectedUrl, \
						   isAnyProtectedUrl

class AssetNotFoundException (Exception):
	pass

def urlRewritingRecordFromSearchResult (result):
	xmlFormat = result.xmlFormat
	if not urlRewritingRecordClasses.has_key(xmlFormat):
		raise Exception, "urlReadingRecord not found for xmlFormat: '%s'" % xmlFormat
	recordXml = unicode (str(result.payload).decode('utf-8'))
	return urlRewritingRecordClasses[xmlFormat](xml=recordXml)
	

class URLRewritingRecord (MetaDataRecord):
	"""
	MetaDataRecord that gets and sets the URL field
	- collection attribute has key of this record's collection
	"""
	url_path = None
	xpath_delimiter = '/'
	verbose = 1
	dowrites = 1
	
	def __init__ (self, path=None, xml=None, collection=None):
		self.collection = collection
		MetaDataRecord.__init__ (self, xml=xml, path=path)
		
		# if xml:
			# MetaDataRecord.__init__ (self, xml=xml)
		# else:
			# MetaDataRecord.__init__ (self, path=path)
	
	def getUrl(self):
		"""
		returns FRIRST url found
		"""
		return self.getTextAtPath (self.url_path) 
		
	def setUrl(self, url):
		"""
		sets FIRST url
		"""
		self.setTextAtPath (self.url_path, url)
		
	def getUrlNodes(self):
		return self.selectNodes(self.dom, self.url_path);
		
	def getBSCSUrlNodes (self):
		"""
		return url nodes that contain 'bscs.dls.ucar.edu'
		"""		
		def filterFn (node):
			url = XmlUtils.getText(node)
			return url.find('bscs.dls.ucar.edu') != -1
					
		return filter (filterFn, self.getUrlNodes())
		
	def getBSCSUrls(self):
		"""
		return urls found at url nodes that contain
		'bscs.dls.ucar.edu'
		"""
		return map (lambda x:XmlUtils.getText(x), self.getBSCSUrlNodes())
		
	def getProtectedUrls(self):
		return map (lambda x:XmlUtils.getText(x), self.getProtectedUrlNodes())
		
	def getProtectedUrlNodes (self):
		"""
		returns url nodes that have either a protected ccs or
		bscs url as content
		"""
		def filterFn (node):
			url = XmlUtils.getText(node)
			# return isCcsProtectedUrl(url) or isBscsProtectedUrl(url) or isDpsProtectedUrl(url)
			return isAnyProtectedUrl(url)
					
		return filter (filterFn, self.getUrlNodes())
		
	def hasProtectedUrl(self):
		"""
		returns True if this record has at least one protectedUrl
		"""
		return len (self.getProtectedUrlNodes()) > 0
		
	def getId(self):
		"""
		returns record ID - Derived from file path
		"""
		filename = os.path.basename(self.path)
		root, ext = os.path.splitext(filename)
		return root
		
	def rewriteUrls(self, selectFn, urlTestFn, rewriteFn):
		"""
		NOT TESTED!
		for each node selected by selectFn (e.g., getBSCSUrlNodes)
		- if url at that node passes 
		rewrite each Url that matches testFn with a falue that
		is computed by writeFn:
		  - base_protected_url + self.collection + protectedAssetFileName
		  
		returns True if a change was made, False otherwise
		  
		 """
		recordChanged = False
		for urlNode in selectFn(self):
			url = XmlUtils.getText(urlNode)
			
			assetPath = getAssetPath (url)
	
			newProtectedCollPath = os.path.join (getReorgProtectedDir(), self.collection)
			newAssetPath = os.path.join (newProtectedCollPath, os.path.basename(assetPath))
			newProtectedUrl = os.path.join (base_protected_url, self.collection, os.path.basename(assetPath))

			if self.verbose:
				print '\n- assetPath:', assetPath
				print '- newAssetPath:', newAssetPath
				print '- oldUrl:', url
				print '- newProtectedUrl:', newProtectedUrl
				
			if urlTestFn(self, url):
				new_url = writeFn (self, url)
				XmlUtils.setText(urlNode, new_url)
				recordChanged = True
				
		return recordChanged	

class MultiPathMixin:
	"""
	supply custom getUrlNodes that collects nodes selected from mulitiple paths
	"""
	def getUrlNodes(self):
		selected = []
		for xpath in self.url_paths:
			selected = selected + self.selectNodes(self.dom, xpath)
		return selected

class AdnURLRewritingRecord (MultiPathMixin, URLRewritingRecord):
	"""
	A URLRewritingRecord for adn format
	"""
	url_paths = [
		"itemRecord/technical/online/primaryURL",
		"itemRecord/relations/relation/urlEntry/@url",
		"itemRecord/relations/relation/urlEntry"
		]
	
class AssessmentsURLRewritingRecord (MultiPathMixin, URLRewritingRecord):
	url_paths = [
		"assessment/question/outline/@url",
		"assessment/question/outline/outline/@url",
		"assessment/question/outline/outline/outline/@url",
		
		"assessment/answer/outline/@url",
		"assessment/answer/outline/outline/@url",
		"assessment/answer/outline/outline/outline/@url"
	]
		
class DleseAnnoURLRewritingRecord (URLRewritingRecord):
	url_path = "annotationRecord/annotation/content/url"
	
class NcsItemURLRewritingRecord (URLRewritingRecord):
	url_path = "record/general/url"
	
class CommAnnoURLRewritingRecord (MultiPathMixin, URLRewritingRecord):
	url_paths = [
		"comm_anno/standardURL",
		"comm_anno/url"
	]
	
class ConceptURLRewritingRecord (URLRewritingRecord):
	url_path = "concept/contents/content/url"
	
urlRewritingRecordClasses = {
	'adn' : AdnURLRewritingRecord,
	'assessments' : AssessmentsURLRewritingRecord,
	'dlese_anno' : DleseAnnoURLRewritingRecord,
	'ncs_item' : NcsItemURLRewritingRecord,
	'comm_anno' : CommAnnoURLRewritingRecord,             
	'concepts' : ConceptURLRewritingRecord             
}

if __name__ == '__main__':
	if 1:
		path = '/Users/ostwald/devel/dcs-repos/reorg-workspace/dcs-reorg/records/assessments/assess_bscs/ASSESS-BSCS-000-000-000-001.xml'
		rec = AssessmentsURLRewritingRecord(path, collection=None)
	else:
		path = '/Users/ostwald/devel/dcs-repos/reorg-workspace/dcs-reorg/records/adn/act-stv/STV-ACT-000-000-000-001.xml'
		rec = AdnURLRewritingRecord(path=path)
	
	nodes = rec.getUrlNodes()
	print '%d nodes found' % len(nodes)
	print rec
	protectedFound = rec.hasProtectedUrl()
	print 'hasProtected: %s' % protectedFound
	protectedNodes = rec.getProtectedUrlNodes()
	print 'found %d protected nodes' % len (protectedNodes)
	rec.update ('COLL')
	print rec
