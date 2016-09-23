import os, sys
from config import record_manager_config
from ncar_lib.repository import CachingRecordManager
from JloXml import XmlUtils

class MyRecordManager (CachingRecordManager):

	searchBaseUrl = "http://localhost:8080/schemedit/services/ddsws1-1"
	putBaseUrl = None # 'http://localhost:8080/schemedit/services/dcsws1-0'
	baseCachePath = "/Users/ostwald/tmp/updateCache"
	
	def __init__ (self, searchBaseUrl=None, 
						putBaseUrl=None, 
						baseCachePath=None):
							
		CachingRecordManager.__init__ (self, searchBaseUrl, putBaseUrl, baseCachePath)
		
		
class ConfiguredRecordManager (CachingRecordManager):
	
	def __init__ (self, config_name):
		self.config = record_manager_config[config_name]
		if not self.config:
			raise KeyError, "Could not resolve config for '%s'" % config_name
		
		CachingRecordManager.__init__ (self, searchBaseUrl=self.config['searchBaseUrl'],
											 putBaseUrl=self.config['putBaseUrl'], 
											 baseCachePath=self.config['baseCachePath'],)
		
if __name__ == '__main__':
	
	# mgr = MyRecordManager(searchBaseUrl=searchBaseUrl, putBaseUrl=putBaseUrl, baseCachePath=baseCachePath)
	mgr = MyRecordManager()
	
	osmRecord = mgr.getRemoteRecord ("OSGC-000-000-000-011");
	print osmRecord


