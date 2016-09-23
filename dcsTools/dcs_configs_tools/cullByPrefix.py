import sys, os, string
"""
Class for collecting and traversing the files in a config directory
"""

from dcs_conf_globals import *
from JloXml import CollectionConfigRecord
from config_utils import *

confDir = "C:/Program Files/Apache Software Foundation/Tomcat 5.5/var/dcs_conf"

class Configs (ConfigDir):
	configClass = CollectionConfigRecord
	
	def getKey (self, rec):
		return rec.getId()
		
	def report (self):
		for key in self.keys():
			configRec = self[key]
			print "\nid: %s\n%s\n%s" % (key,
										os.path.basename(configRec.path),
										configRec.getIdPrefix())

	def cull (self):
		for configRec in self.values():
			if not configRec.getIdPrefix():
				print "culling: %s" % os.path.basename(configRec.path)
				os.remove (configRec.path)

if __name__ == "__main__":
	path = os.path.join (confDir, "collections")
	configs = Configs (path)
	# configs.report()
	configs.cull()
	print "done"
