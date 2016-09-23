import sys, os, string, shutil
from UserDict import UserDict
from JloXml import DleseCollectRecord, IdPrefixesRecord
"""
we can't just copy records blindly, because the collection records
will have name collisions. also, there is a chance that we could have
collection key collisions ...
"""

external_instance_names = [
	"agi",
	"argonne",
	"cipe",
	"evalcoreservices",
	"k-12community",
	"mynasadata",
	"noaa",
	"pri",
	"swi",
	"tapestry",
	"unavco",
	"utig",
	]

dpc_instance_names = [
	"dcc",
	"dpc",
	"news",
]

instance_names = external_instance_names + dpc_instance_names
	
tomcatBaseDir = "/dpc/services/dcs/dcs.dlese.org/tomcat"
instanceDir = "/dpc/metadata/cataloging"

# gatherDir = "/dpc/services/dcs/dcs.dlese.org/tmp/Gathered"
gatherDir = "/home/ostwald/tmp/GatheredRecords"

item_formats = ['adn', 'news_opps', 'dlese_anno']
skip_formats = ['trash', 'dlese_collect', 'dcs_data']

class Instance:
	def __init__ (self, name):
		self.verbose = 0
		self.name = name
		self.path = os.path.join (instanceDir, self.name)
		
		collectionRecords = CollectionRecords (self)
		
		self.formats = self._getFormats()
		self.collections = self._getCollections(collectionRecords)
		self.tomcatPath = os.path.join (tomcatBaseDir, name)
		self.prefixMap = self._getPrefixMap ()
		self.collectionConfigs = self._getCollectionConfigs()
						
	def _getFormats (self):
		"""
		a list of item-level formats for this instance
		"""
		formats = []
		for format in os.listdir (self.path):
			if format in item_formats:
				formats.append (format)
		return formats
		
	def _getCollections (self, collectionRecords):
		"""
		return a list of item-record Collection instances.
		
		Note: collectionRecords is a map {collectionKey, collectionRecord} of collectionRecords
			  for this instance.
		
		Build the collections list by traversing the item-level record directories (named by collection key)
		skipping the following:
			- directories that do not have a corresponding collectionRecord
			- collections whose shortTitles begin with "test"
		"""
		collections = []
		for format in self.formats:
			formatPath = os.path.join (self.path, format)
			for key in os.listdir (formatPath):
				try:
					rec = collectionRecords[key]
				except KeyError:
					if self.verbose:
						print 'WARNING: "%s" ... skipping ...' % sys.exc_info()[1]
					continue
				shortTitle = rec.getShortTitle()
				if shortTitle.lower().startswith ("test"):
					if self.verbose:
						print 'skipping test collection "%s" in instance "%s"' % (shortTitle, self.name)
					continue
				collections.append (Collection (key, format, rec, self))
		return collections
	
	def _getCollectionConfigs(self):
		configs=[]
		configDir = os.path.join (self.tomcatPath, "dcs_conf/collection_config")
		for key in map (lambda c: c.getKey(), self.collections):
			configPath = os.path.join (configDir, key+".xml")
			if os.path.exists (configPath):
				configs.append (configPath)
		return configs
		
	def _getPrefixMap (self):
		prefixesPath = os.path.join (self.tomcatPath, "vocab-ui-project/collection", "idPrefixes.xml");
		rec = IdPrefixesRecord (prefixesPath)
		key_filter = map (lambda m: m.getKey(), self.collections)
		return rec.getPrefixMap (key_filter)
		
class CollectionRecords (UserDict):
	"""
		dict = {key:collectionRecord)
	"""
	def __init__ (self, instance):
		UserDict.__init__ (self);
		self.instance = instance
		self.collectPath = os.path.join (instance.path, "dlese_collect", "collect")
		
		for filename in os.listdir (self.collectPath):
			if not filename.lower().endswith (".xml"): continue
			rec = DleseCollectRecord (path=os.path.join (self.collectPath, filename))
			self[rec.getKey()] = rec
			
	def __getitem__ (self, key):
		if not self.has_key(key):
			msg = '%s does not exist in "%s" instance' % (key, self.instance.name)
			raise KeyError, msg
		else:
			return self.data[key]
			
	def report (self):
		print "%s collection records" % self.instance.name
		for key in self.keys():
			rec = self[key]
			print "\tkey: %s  id: %s" % (key, rec.getId())
			
	# def moveAndRename (self, dst
			
		
class Collection:
	def __init__ (self, key, format, rec, instance):
		self.key = key
		self.format = format
		self.instance = instance
		self.rec = rec
		
	def getKey (self):
		return self.key
		
	def getShortTitle (self):
		return self.rec.getShortTitle()
		
	def __repr__ (self):
		return "%s (%s) prefix: %s format: %s" % (self.getShortTitle(),
												  self.getKey(),
												  self.instance.prefixMap[self.getKey()],
												  self.format)
												  

def copyDir (src, dst):
	if not os.path.exists (src): return
	
	for filename in os.listdir(src):
		srcPath = os.path.join (src, filename)
		dstPath = os.path.join (dst, filename)
		# directory
		if os.path.isdir (srcPath):
			if not os.path.exists(dstPath):
				os.mkdir (dstPath)
			copyDir (srcPath, dstPath)
		else:  # file
			if os.path.exists (dstPath):
				raise "FileExists", dstPath
			shutil.copy2 (srcPath, dstPath)

class Gatherer:
	"""

		- no duplicate collection record ids
	"""
	
	
	def __init__ (self, basePath):
		self.basePath = basePath
		self.recordsPath = os.path.join (basePath, "records")
		self.collectionConfigPath = os.path.join (basePath, "collection_config")
		self.instances = []
		for name in instance_names:
			i = Instance (name)
			self.instances.append (i)

		self.collectDir = os.path.join (self.recordsPath, "dlese_collect", "collect")
		self.prefixMap = self._buildPrefixMap() # throws error if key or prefix duplications
		
		print "\nInstantiated Gatherer (baseDir: %s)\n" % self.basePath
		
	def _buildPrefixMap (self):
		"""
			sanity checks:
				- no duplicate collection keys
				- no duplicate collection prefixes
		"""
		uniquePrefixes = []
		uniqueKeys = []
		globalPrefixMap = {}
		for instance in self.instances:
			prefixMap = instance.prefixMap
			for key in prefixMap.keys():
				if key in uniqueKeys:
					raise "DuplicateCollectionKey", key
				uniqueKeys.append (key)
				
				prefix = prefixMap[key]
				if prefix in uniquePrefixes:
					raise "DuplicateCollectionPrefix", prefix					
				uniquePrefixes.append (prefix)
				
				globalPrefixMap[key] = prefix
		return globalPrefixMap

		
	def getNextCollectionId  (self):
		maxNum = 1 # 1 is reserved for master collection record
		for filename in os.listdir (self.collectDir):
			root, ext = os.path.splitext(filename)
			n = int(root[-3:])
			maxNum = max (maxNum, n)
		if maxNum < 999:
			baseName = "DCS-COLLECTION-000-000-000-"
			return baseName + "%03d" % (maxNum + 1)

	def moveItemRecords (self):
		print "moving Item Records ... "
		for i in self.instances:
			print "\t", i.name
			for format in i.formats:
				# print format
				src = os.path.join (i.path, format)
				dst = os.path.join (self.recordsPath, format)
				if not os.path.exists (dst):
					os.makedirs (dst)
				copyDir (src, dst)
				
				src = os.path.join (i.path, "dcs_data", format)
				dst = os.path.join (self.recordsPath, "dcs_data", format)
				if not os.path.exists (dst):
					os.makedirs (dst)
				copyDir (src, dst)
		print " ... finished writing item Records"

	def handleMasterCollectRecord (self, rec):
		masterId = "DCS-COLLECTION-000-000-000-001"
		masterPath = os.path.join (self.collectDir, masterId+".xml")
		if not os.path.exists (masterPath):
			rec.setId (masterId)
			rec.write (masterPath)
				
	def moveCollectionRecords (self):
		print "moveCollectionRecords"
		if not os.path.exists (self.collectDir):
			os.makedirs(self.collectDir)
		for instance in self.instances:
			# for key in instance.collectionRecords.keys():
				# rec = instance.collectionRecords[key]
			for collection in instance.collections:
				rec = collection.rec
				key = collection.key
				
				# print "\nkey: " + key
				if key == "collect":
					self.handleMasterCollectRecord (rec)
					continue
					
				recId = rec.getId();
				newId = self.getNextCollectionId();
				# print "\toldId: %s  --> newId: %s" % (recId, newId)
				rec.setId (newId)
				rec.write (os.path.join (self.collectDir, newId + ".xml"))
		print "move Collection Records"
			
	def writePrefixMap (self):
		xml = """<prefixes>
					<prefix>
						<prefix-key>collect</prefix-key>
						<prefix-value>DCS-COLLECTION</prefix-value>
					</prefix>
				</prefixes>"""
		rec = IdPrefixesRecord (xml=xml)
		for key in self.prefixMap.keys():
			rec.addPrefix (key, self.prefixMap[key])
		rec.write (os.path.join (self.basePath, "idPrefixes.xml"))
		print "wrote prefixMap configs"
			
	def moveCollectionConfigRecords (self):
		if not os.path.exists (self.collectionConfigPath):
			os.makedirs (self.collectionConfigPath)
		for instance in self.instances:
			for srcPath in instance.collectionConfigs:
				dstPath = os.path.join (self.collectionConfigPath, os.path.basename (srcPath))
				## print "%s\n\t%s" % (srcPath, dstPath)
				shutil.copy2 (srcPath, dstPath)
		print "Wrote collection configs"
				
def doGather ():

	g = Gatherer(gatherDir)
	g.moveItemRecords()
	g.writePrefixMap()
	g.moveCollectionRecords()	
	g.moveCollectionConfigRecords()
		
if __name__ == "__main__":
	doGather()
	


		
