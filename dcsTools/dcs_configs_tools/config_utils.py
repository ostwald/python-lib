import sys, os, string
"""
Class for collecting and traversing the files in a config directory
"""

from dcs_conf_globals import *
from JloXml import CollectionConfigRecord
from UserDict import UserDict

def fix_namespace (config, nameSpace, schemaURI):

	rootElement = config.doc
	noNameSpace = "xsi:noNamespaceSchemaLocation"
	if rootElement.hasAttribute (noNameSpace):
		# print rootElement.getAttribute (noNameSpace)
		rootElement.removeAttribute (noNameSpace);
	
	rootElement.setAttribute ("xmlns", nameSpace)
	rootElement.setAttribute ("xsi:schemaLocation", nameSpace + " " + schemaURI)


class ConfigDir (UserDict):
	"""
	manages dict of config records, keyed by collection id
	"""
	
	configClass = CollectionConfigRecord
	
	def __init__ (self, configDir, recurse=None):
		self.configDir = configDir
		self.recurse = recurse
		UserDict.__init__ (self, None);
		self.read (self.configDir)
		
	def read (self, dir):
		
		for filename in os.listdir (dir):
			path = os.path.join (dir, filename)
			if os.path.isdir (path) and self.recurse:
				self.read (path)
			else:
				key, ext = os.path.splitext (filename)
				if not ext == ".xml":
					# print "rejecting %s" % filename
					continue
				rec = self.configClass (path=path)
				key = self.getKey (rec)
				self[key] = rec
				
	def getFiles (self):
		return self.values()
			
	def __getitem__ (self, key):
		if not self.data.has_key (key):
			print "config not found for %s .. skipping" % key
			return None
		return UserDict.__getitem__ (self, key)
			
	def getKey (self, rec):
		"""
		return a key (e.g., xmlFormat) identifying this particular record
		"""
		raise "Abstract Method"
		
	def write (self):
		print "writing"
		for config in self.values():
			config.write()
			print "\t", config.path
			
	def report (self):
		for key in self.keys():
			print "\nid: %s\n%s" % (key, self[key])
		

if __name__ == "__main__":

	configDir = "C:/Documents and Settings/ostwald/devel/projects/schemedit-project/web/WEB-INF/collection-config"
	configDir = "/dls/devel/ostwald/tomcat/tomcat/dcs_conf/framework_config"
	ConfigDir(configDir)
