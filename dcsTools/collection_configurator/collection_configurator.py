import sys, os, string
"""
updates each collection_config file
- fixes namespace and schemaURI
"""

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
			

class NamespaceFixer:
	
	def __init__ (self, configDir):
		self.configs = CollectionConfigs (configDir)
		
		for key, value in self.configs.items ():
			config = self.configs[key]
			if config:
				## config.setIdPrefix (value)
				self.fix (config)
			else:
				print "no config found for %s" % key
		# self.configs.report()
		
	def fix (self, config):
		rootElement = config.doc
		noNameSpace = "xsi:noNamespaceSchemaLocation"
		print rootElement.getAttribute (noNameSpace)
		rootElement.removeAttribute (noNameSpace);
		
		nameSpace = "http://dcs.dlese.org/collection-config"
		schemaURI = "http://www.dlese.org/Metadata/dcs/collection-config/dcsCollectionConfig.xsd"
		
		rootElement.setAttribute ("xmlns", nameSpace)
		rootElement.setAttribute ("xsi:schemaLocation", nameSpace + " " + schemaURI)
		
		# print rootElement.getAttribute ("xsi:noNamespaceSchemaLocation")
		print config
		
		
	def update (self):
		self.configs.write()
		

if __name__ == "__main__":

	configDir = "C:/Documents and Settings/ostwald/devel/projects/schemedit-project/web/WEB-INF/collection-config"
	NamespaceFixer(configDir)
