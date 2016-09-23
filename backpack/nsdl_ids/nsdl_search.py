import os, sys, urlparse
from UserDict import UserDict
from ncar_lib.repository import RepositorySearcher, SearchResult
from JloXml import XmlRecord, XmlUtils

default_baseUrl = "http://nsdl.org/nsdl_dds/services/ddsws1-1"

idCacheFile = None

if 0:# taos
	pass
else:
	idCacheFile = '/home/ostwald/python-lib/backpack/nsdl_ids/id_cache.xml'

class NsdlIDNotFoundError (Exception):
	pass
	
class CachingNsdlIdService (UserDict):
	
	verbose = 1
	
	def __init__ (self):
		self.data = {}
		NsdlSearcher.verbose = False
		if os.path.exists(idCacheFile):
			rec = XmlRecord(path=idCacheFile)
		else:
			rec = self.getBlankRec()
			
		for node in rec.selectNodes(rec.dom, 'idCache:entry'):
			url = node.getAttribute('url')
			nsdlId = node.getAttribute('id')
			self[url] = nsdlId
			
	def resolveId (self,url):
		"""
		this url wasn't found as is, so try permutations
		if resolved, return tuple: [id, url]
		"""
		nsdlId = self._getNsdlId(url)
		if nsdlId:
			return nsdlId, url
		parsed = urlparse.urlparse (url)
		if parsed[4]: # query
			print '  found query'
			return None
		if parsed[2]: # path
			root, ext = os.path.splitext(parsed[2])
			if ext:
				print "  found ext: ", ext
				return None
		
		if url[-1] == '/':
			# try without
			print '  stripping trailing /'
			nsdlId = self._getNsdlId(url[:-1])
			if nsdlId:
				return nsdlId
		else:
			print '  adding trailing / to normalize'
			url = url + '/'
		# print '  normalized as:', url
		nsdlId = self._getNsdlId(url)
		if nsdlId:
			return nsdlId, url		
		
		# if there is a trailing slash, try the old standards
		old_standards = ['index.html','index.htm', 'index.jsp', 'index.php']
		for filename in old_standards:
			tryUrl = url + filename
			nsdlId = self._getNsdlId(tryUrl)
			if nsdlId:
				return nsdlId, tryUrl
			
	def _getNsdlId (self, url):
		print "  _getNsdlId - %s" % url
		results = NsdlSearcher (url)
		# print "  # %d results found" % len(results)
		if results:
			return results[0].recId
		
	def getId (self, url):
		if not self.has_key(url):
			if self.verbose:
				print "fetching url via webservice"
			nsdlId = self._getNsdlId(url)
			self[url] = nsdlId or "NSDL id not found for %s" % url
			self.write()
		return self[url]
		
	def getId_with_resolution (self, url):
		if not self.has_key(url):
			if self.verbose:
				print "fetching url via webservice"
			resovedNsdlId = self.resolveId(url)
			self[url] = resovedNsdlId[0] or "NSDL id not found for %s" % url
			self.write()
		return self[url]
		
	def getBlankRec (self):
		rec = XmlRecord(xml='<idCache/>')
		rec.path = idCacheFile
		return rec
		
	def clear (self):
		self.data = {}
		self.write()
		
	def write(self):
		rec = self.getBlankRec()
		for url in self.keys():
			node = XmlUtils.addElement(rec.dom, rec.doc, 'entry')
			node.setAttribute ('url', url)
			node.setAttribute ('id', self[url])
		rec.write()
	
class NsdlSearcher (RepositorySearcher):
	
	verbose = False
	
	def __init__ (self, url):
		self.url = url
		RepositorySearcher.__init__(self,  baseUrl=default_baseUrl)
		# print self.service_client.request.getUrl()
	
	def get_params (self, collection, xmlFormat):
		urlParam = 'url:"%s"' % self.url
		return {
			'q' : urlParam,
			"verb": "Search"
		}
		
if __name__ == '__main__':
	# url = 'http://mathdl.maa.org/mathDL/46/?pa=content&sa=viewDocument&nodeId=3362'
	url = 'http://www.csus.edu/indiv/s/slaymaker/Archives/Geophysics.htm'
	nsdlId = CachingNsdlIdService().getId (url)
	print nsdlId
	resolved = CachingNsdlIdService().resolveId (url)
	if resolved:
		print "resolved: " + resolved[0]
