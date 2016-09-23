"""
URL Save records are metadata records that contain a copy of a record that has been saved in the CCS.
The classes here are able to update the URLs found in the different formats of saved records

"""
import os, sys, re, shutil
from JloXml import XmlRecord, MetaDataRecord, XmlUtils, AdnRecord
from bscs.protected import base_protected_url, isProtectedUrl, \
		getAssetPath, getReorgProtectedDir, getReorgUserContentRepo
from bscs.bscs_merge_workflow import systemGeneratedKeysMap

class UserSaveURLRewritingRecord (XmlRecord):
	"""
	MetaDataRecord that gets and sets the URL field(s)
	- collection attribute has key of this record's collection
	"""
	url_path = None
	xpath_delimiter = '/'
	verbose = 0
	
	def __init__ (self, xml):
		# MetaDataRecord.__init__ (self, xml=xml)
		XmlRecord.__init__ (self, xml=xml)
		
		self.savedXmlFormat = self.getTextAtPath('savedResource/savedXmlFormat')
		self.id = self.getTextAtPath('savedResource/id')
		self.collection = self.getTextAtPath('savedResource/ddsRepoInfo/collectionKey')
	
	# def getUrl(self):
		# return self.getTextAtPath (self.url_path) 
		# 
	# def setUrl(self, url):
		# self.setTextAtPath (self.url_path, url)
		
	def getUrlNodes(self):
		return self.selectNodes(self.dom, self.url_path);
		
	def getProtectedUrls(self):
		return map (lambda x:XmlUtils.getText(x), self.getProtectedUrlNodes())
		
	def getProtectedUrlNodes (self):
		return filter (lambda x: isProtectedUrl(XmlUtils.getText(x)),
					   self.getUrlNodes())
		
	def hasProtectedUrl(self):
		return len (self.getProtectedUrlNodes()) > 0
		
	def getId(self):
		return self.id
		
	def rewriteProtectedUrls (self):
		"""
		rewrite each protectected Url in this record with a new_url:
		  - base_protected_url + self.collection + protectedAssetFileName
		  
		returns True if a change was made, False otherwise
		  
		 """
		recordChanged = False
		for urlNode in self.getProtectedUrlNodes():
			url = XmlUtils.getText(urlNode)
			
			assetPath = getAssetPath (url)
			fileName = os.path.basename(url)
			
			collection = systemGeneratedKeysMap.has_key(self.collection) and \
							systemGeneratedKeysMap[self.collection]['key'] or \
							self.collection
			
			newAssetPath = os.path.join (getReorgProtectedDir(), collection, fileName)
			newProtectedUrl = os.path.join (base_protected_url, collection, fileName)

			if self.verbose:
				print '\n- assetPath:', assetPath
				print '- newAssetPath:', newAssetPath
				print '- oldUrl:', url
				print '- newProtectedUrl:', newProtectedUrl
				print '- self.collection: ' + self.collection
				sys.exit()
			if url != newProtectedUrl:
				XmlUtils.setText(urlNode, newProtectedUrl)
				recordChanged = True
				
		return recordChanged
		
	def verifyAssets (self):
		errors = []
		for urlNode in self.getProtectedUrlNodes():
			url = XmlUtils.getText(urlNode)
			
			assetPath = getAssetPath (url)
			if not os.path.exists(assetPath):
				errors.append (assetPath)
				
		if errors:
			errMsg = 'assets not found\n- %s' % '\n- '.join(errors)
			raise Exception (errMsg)


class AdnUrlRewriter (UserSaveURLRewritingRecord):
	url_path = "itemRecord/technical/online/primaryURL"
	
class AssessmentsUrlRewriter (UserSaveURLRewritingRecord):
	url_path_1 = "savedResource/record/assessment/question/outline/@url"
	url_path_2 = "savedResource/record/assessment/answer/outline/@url"
	
	def getUrlNodes(self):
		return filter(None, self.selectNodes(self.dom, self.url_path_1) + \
			   				self.selectNodes(self.dom, self.url_path_2))			
	
class DleseAnnoUrlRewriter (UserSaveURLRewritingRecord):
	url_path = "savedResource/record/annotationRecord/annotation/content/url"
	
class NsdlDcUrlRewriter (UserSaveURLRewritingRecord):
	url_path = "savedResource/record/nsdl_dc:nsdl_dc/dc:identifier"
	
savedResourceUrlRewritingClasses = {
	'adn' : AdnUrlRewriter,
	'assessments' : AssessmentsUrlRewriter,
	'dlese_anno' : DleseAnnoUrlRewriter,
	'nsdl_dc' : NsdlDcUrlRewriter 
}

if __name__ == '__main__':
	# for testing, create paths to metadata files. in the real thing we us
	# search results
	if 0:
		id = 'CCS-SAVED-DL-RESOURCE-KH-ASSESS-000-000-000-082' # assessment
	elif 1:
		id = 'CCS-SAVED-DL-RESOURCE-TASK-000-000-000-046' # nsdl_dc
	elif 1:
		id = 'CCS-SAVED-DL-RESOURCE-KH-TIPS-000-000-000-452' # dlese_anno
			
	path = os.path.join (getReorgUserContentRepo(), \
						 'ccs_saved_resource/ccsselecteddlresources', \
						 id+'.xml')
			
	tmpRec = XmlRecord(path=path)
	savedXmlFormat = tmpRec.getTextAtPath('savedResource:savedXmlFormat')
	# recordXml = unicode (str(result.payload).decode('utf-8'))
	rec = savedRecordClasses[savedXmlFormat](xml=str(tmpRec))
	
	nodes = rec.getUrlNodes()
	print '%d nodes found' % len(nodes)
	# print rec
	protectedFound = rec.hasProtectedUrl()
	print 'hasProtected: %s' % protectedFound
	protectedNodes = rec.getProtectedUrlNodes()
	print 'found %d protected nodes' % len (protectedNodes)
	rec.rewriteProtectedUrls ()
	print rec
