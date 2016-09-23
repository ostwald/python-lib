import sys, os, string
"""
extracts the prefixes from all collection_config files in given directory
and writes collection key -> prefix mappings as xml
"""

from JloXml import XmlRecord, XmlUtils, CollectionConfigRecord
from collection_configurator import CollectionConfigs
from UserDict import UserDict
from time import asctime, localtime

class PrefixExtractor (CollectionConfigs):
	
	record_template = "<?xml version=\"1.0\" encoding=\"UTF-8\" ?>\n" + \
							"<collectionPrefixes/>\n"
	record_source = "/dls/devel/common/records"
							
	def makeRecord (self):
		rec = XmlRecord(xml=self.record_template)
		XmlUtils.addChild (rec.dom, "date", asctime (localtime()))
		XmlUtils.addChild (rec.dom, "recordSource", self.record_source)
		collections = XmlUtils.addElement (rec.dom, rec.doc, "collections")
		for key in self.keys():
			collection = XmlUtils.addElement (rec.dom, collections, "collection")
			collection.setAttribute ("key", key)
			collection.setAttribute ("prefix", self[key].getIdPrefix())
		return rec

if __name__ == "__main__":
	configDir = "/dls/devel/ostwald/tomcat/tomcat/dcs_conf/collection_config"
	# p = Prefixer (configDir, idPrefixesPath).update()
	
			
	
	pe = PrefixExtractor (configDir)
	print pe.makeRecord()

