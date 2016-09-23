from config_utils import *

class CollectionConfigDir (ConfigDir):
	configClass = CollectionConfigRecord
	
	def getKey (self, rec):
		return rec.getId()
		
	def fixall (self):
		for rec in self.values():
			recFixer ( rec )
			
		
def recFixer (rec):

	fix_namespace(rec, collection_config_namespace, collection_config_schemaURI)
		

		
if __name__ == "__main__":
	path = "/dls/devel/ostwald/tomcat/tomcat/dcs_conf/collection_config"
	fcd = CollectionConfigDir (path)
	fcd.fixall()
	# for format in ["collection_config", "framework_config", "dcs_data"]:
		# fixer = RecFixer ( fcd[format] )
		# fixer.fix_namespace()
	fcd.report()
