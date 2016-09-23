"""
Record Manager -

provides access to metadata records in the repository
- remotely - via webservices
- locally - via files cached on disk

getRecord - tries local cache first, and if no record is found obtains from webservice

putRecord - can put either to local cache or to repository via webservice

at this point we are handling OSM metadata (just osm, no dcs_data) records

"""
import os, sys, re, time, shutil
from UserDict import UserDict
from ncar_lib import OsmRecord
from JloXml import XmlUtils
from put_record import PutRecordClient, ttambora_putBaseUrl
from get_record import GetRecord

nldr_searchBaseUrl = "http://nldr.library.ucar.edu/schemedit/services/ddsws1-1"
ttambora_searchBaseUrl = "http://ttambora.ucar.edu:10160/schemedit/services/ddsws1-1"


default_searchBaseUrl = ttambora_searchBaseUrl
default_putBaseUrl = ttambora_putBaseUrl
default_baseCachePath = "cache"

class PrefixMap (UserDict):
	"""
	create a prefix map (Prefix -> collectionKey) from the file structure of
	the provided CachingRecordManager instance
	"""
	verbose = False
	
	def __init__ (self, mgr):
		self.data = {}
		for key in os.listdir(mgr.baseCachePath):
			if key[0] =='.': continue # whatch out for svn and osx files
			collectiondir = os.path.join (mgr.baseCachePath, key)
			if not os.path.isdir(collectiondir):
				print 'Prefix map skipping ', key
				continue
				
			# grab record to us
			mdfilename = None
			for filename in os.listdir(collectiondir):
				if filename[0] not in ['.', '#']:
					mdfilename = filename
					break
				
			prefix = mgr.getPrefix(mdfilename)
			self[prefix] = key
			if self.verbose:
				print "prefix %s --> %s" % (prefix, key)

	def report (self):
		print "\nPrefixMap"
		for key in self.keys():
			print "- %s -> %s" % (key, self[key])
				
class CachedRecordError (Exception):
	pass

class CachingRecordManager:
	"""
	"""
	# prefixMap = {
		# 'PUBS-NOT-FY2010' : 'not-fy10',
		# 'OSGC' : 'osgc',
		# 'PUBS' : 'pubs-ref',
		# 'AMS-PUBS' : 'ams-pubs',
		# 'NAB' : 'ncar-books',
		# 'TESTO' : 'testosm'
		# }
	
	prefixPat = re.compile ('(.*?)-000.*')
	
	allow_remote_put = 1
	
	def __init__ (self, searchBaseUrl=None, putBaseUrl=None, baseCachePath=None):
		self.searchBaseUrl = searchBaseUrl or default_searchBaseUrl
		self.putBaseUrl = putBaseUrl or default_putBaseUrl
		self.baseCachePath = baseCachePath or default_baseCachePath
		self.baseUrl = putBaseUrl
		self.statusNote = None
		
		self.prefixMap = self.getPrefixMap()

	def getPrefixMap(self):
		"""
		can be overridden to chage or add mappings
		"""
		return PrefixMap(self)
		
	def getPrefix (self, recId):
		"""
		return prefix portion of provided record ID
		"""
		m = self.prefixPat.match (recId)
		if not m:
			raise Exception, 'prefix not found (%s)' % recId
		return m.group(1)
		
	def getCollectionKey (self, recId):
		"""
		from the provided recId, first obtain the prefix and using the prefix get the collectionKey
		"""
		prefix = self.getPrefix(recId)
		if not self.prefixMap.has_key(prefix):
			raise KeyError, "prefix not found for provided id (%s)" % recId
		return self.prefixMap[prefix]
		
	def getCachedRecordIds (self, collection):
		"""
		"""
		path = os.path.join (self.baseCachePath, collection)
		try:
			return map (lambda x:x[:-4], filter (lambda x:x.endswith('.xml'), os.listdir(path)))
		except:
			raise Exception, "asked for a non-existing collection (%s)" % collection
			
	def getCachedCollectionIds (self):
		"""
		"""
		return filter (lambda x:x[0] != '.', os.listdir (self.baseCachePath))
		
	def getTimeStamp(self, timeStr):
		"""
		return time in seconds for provided timeStr (e.g., 2010-09-20T14:44:13Z)
		"""
	
		format = '%Y-%m-%dT%H:%M:%SZ'
		tple = time.strptime(timeStr, format)
		return time.mktime(tple)
		
	def getPrettyTimeStr (timeStr):
		"""
		return time in seconds for provided timeStr (e.g., 2010-09-20T14:44:13Z)
		"""
	
		uglyformat = '%Y-%m-%dT%H:%M:%SZ'
		tple = time.strptime(timeStr, uglyformat)
		prettyformat = "%m/%d/%Y %H:%M"
		return time.strftime(prettyformat, tple)
		
	def getCachePath (self, recId):
		"""
		get the path to the cached record for provided recId 
		"""
		return os.path.join (self.baseCachePath, self.getCollectionKey(recId), recId+'.xml')		
		
	def getRecord(self, recId):
		"""
		gets cached record (OsmRecord by default) instance for provided recId, 
		looking first in the cache. To get a different class of record, override
		"getCachedRecord"
		and if not found there, getting record via Web Service.
		"""
		try:
			rec = self.getCachedRecord (recId)
			print "obtained rec from cache"
			return rec
		except CachedRecordError, msg:
			# print msg
			return self.getRemoteRecord(recId)
		
	def getCachedRecord (self, recId, record_class=OsmRecord):
		"""
		gets osmRecord record instance for provided recId.
		raises Exception if no record is found
		"""
		path = self.getCachePath(recId)
		if not os.path.exists(path):
			raise CachedRecordError, "cached record does not exist at %s" % path
		return record_class(path=path)
		
	def emptyCache(self):
		"""
		utility to remove all the files from the cache
		"""
		for filename in os.listdir (self.baseCachePath):
			shutil.rmtree (os.path.join (self.baseCachePath, filename))
		
	def cacheRecord (self, rec):
		"""
		write provided record to the cache
		"""
		recId = rec.getId()
		path = self.getCachePath (recId)
		if not os.path.exists(os.path.dirname(path)):
			os.makedirs (os.path.dirname(path))
		rec.write (path)
		print 'wrote to ', path
		
	def writeCacheToRemote (self, baseDir=None):
		"""
		writes the entire cache to remote DCS repository
		"""
		if baseDir is None:
			baseDir = self.baseCachePath
		for filename in os.listdir(baseDir):
			path = os.path.join (baseDir, filename)
			root, ext = os.path.splitext(filename)
			if ext == '.xml':
				rec = self.getCachedRecord(root)
				self.putRemoteRecord (rec)
			if os.path.isdir (path):
				self.writeCacheToRemote (path)
				
		
	def getRemoteResult (self, recId):
		"""
		returns entire search result, including header, record and storedContent
		"""
		return GetRecord (recId, self.searchBaseUrl).response
		
	def getRemoteRecord (self, recId):
		"""
		fetch metadata record for specified recId from searchService
		"""
		result = self.getRemoteResult (recId)
		if not result:
			raise Exception, "could not find %s" % recId
		return result.payload
		
	def putRemoteRecord (self, rec):
		"""
		writes the provided osmRecord to the remote DCS via put service
		"""
		recId = rec.getId()
		collection = self.getCollectionKey(recId)
		params = {
			'collection' : collection,
			'xmlFormat' : 'osm',
			'id' : recId,
			'recordXml' : rec.doc.toxml()
		}
		
		if self.statusNote:
			params['dcsStatusNote'] = self.statusNote
		
		if not self.allow_remote_put:
			print "WOULD HAVE put record: %s" % recId
			return
		putRecord = PutRecordClient (params, self.putBaseUrl)
		if not putRecord.id:
			raise Exception, "Put record failed for %s" % recId
		print "put %s" % recId
			
		
def putRecordTester (id):
	mgr = CachingRecordManager()
	rec = mgr.getCachedRecord (id)
	statusNote = "this is but a test"
	mgr.putRemoteRecord (rec, statusNote)
		
		
if __name__ == '__main__':
	id = 'TESTO-000-000-000-019'

	if 0:
		mgr = CachingRecordManager()
		rec = mgr.getRecord (id)
		mgr.cacheRecord(rec)
		# print rec
	elif 0:
		putRecordTester (id)
	else:
		mgr = CachingRecordManager()
		mgr.statusNote = "i am a status note"
		mgr.writeCacheToRemote()


	
