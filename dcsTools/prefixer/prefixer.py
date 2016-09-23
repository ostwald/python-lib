import sys, os, string

from JloXml import IdPrefixesRecord, CollectionConfigRecord
from UserDict import UserDict

config = "collection-config.xml"

class CollectionConfigs (UserDict):
	"""
	manages dict of config records, keyed by collection id
	"""
	
	def __init__ (self, configDir):
		self.configDir = configDir
		UserDict.__init__ (self, None);
		
		for filename in os.listdir (configDir):
			key, ext = os.path.splitext (filename)
			if not ext == ".xml" or key == "default":
				# print "rejecting %s" % filename
				continue
			path = os.path.join (configDir, filename)
			rec = CollectionConfigRecord (path=path)
			key = rec.getId()
			self[key] = rec
			
	def __getitem__ (self, key):
		if not self.data.has_key (key):
			print "config not found for %s .. skipping" % key
			return None
		return UserDict.__getitem__ (self, key)
			
	def write (self):
		print "writing"
		for config in self.values():
			config.write()
			print "\t", config.path
		
	def report (self):
		for key in self.keys():
			print "id: %s, prefix: %s" % (key, self[key].getIdPrefix())
			

class Prefixer:
	
	def __init__ (self, configDir, idPrefixesPath):
		self.configs = CollectionConfigs (configDir)
		self.prefixMap = IdPrefixesRecord (path=idPrefixesPath).getPrefixMap()
		
		for key, value in self.prefixMap.items ():
			config = self.configs[key]
			if config:
				config.setIdPrefix (value)
			else:
				print "no config found for %s" % key
		# self.configs.report()
		
	def update (self):
		self.configs.write()
		
def configTester ():
	configDir = "collection_config"
	configs = CollectionConfigs (configDir)
	configs.report()

if __name__ == "__main__":
	idPrefixesPath = "idPrefixes.xml"
	configDir = "collection_config"
	# p = Prefixer (configDir, idPrefixesPath).update()
	
	configTester()
