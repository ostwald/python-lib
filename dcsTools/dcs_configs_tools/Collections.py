from config_utils import *

class Collections (ConfigDir):
	configClass = CollectionConfigRecord
	
	configDirNotFoundList = []
	specialCaseList = []
	
	def getKey (self, rec):
		return rec.getId()
		
	def visit (self):
		for rec in self.values():
			try :
				recFixer ( rec )
			except ConfigDirNotFoundException, e:
				## print "SpecialCaseException: ", e.value
				self.configDirNotFoundList.append (e.value)
				continue
			except SpecialCaseException, e:
				## print "SpecialCaseException: ", e.value
				self.specialCaseList.append (e)
				continue
			print "writing to ", rec.path
			rec.write()

def recFixer (rec):

	# fix_namespace(rec, collection_config_namespace, collection_config_schemaURI)
	fix_exportDir(rec)

def makeNewExportDir (exportDir, id):
	"""
	oldExportDir is in the form format/version/collection
	newExportDir is format/collection
	
	returns None for special cases:
		- collectionID and collectionDir aren't the same 
			(e.g., 'dcr' -> dlese_collect/1.0.00/collect)
	"""
	if exportDir is None:
		return None
		
	try:
		splits = exportDir.split("/")
		collectionName = splits[2]
		format = splits[0]
	except:
		return None
	
	# don't operate on special cases!
	if collectionName != id:
		return None
	else:
		return format + "/" + collectionName
		
def fix_exportDir (configRecord):
	""" 
	develop in collection_config.py and move to config_utils when stable
	"""
	id = configRecord.getId()
	exportDir = configRecord.getExportDir()
	if (exportDir):
		newExportDir = makeNewExportDir(exportDir, id)
		if newExportDir is None:
			raise SpecialCaseException (id, exportDir)
		print "\n%s\n\t%s\n\t%s" % (id, exportDir, newExportDir)
	else:
		raise ConfigDirNotFoundException (configRecord.path)
		
	configRecord.setExportDir (newExportDir)
	print "exportDir set to ", configRecord.getExportDir()
		
class SpecialCaseException (Exception):
	def __init__ (self, collection, exportPath):
		self.collection = collection
		self.exportPath = exportPath
	def __str__ (self):
		return "%s: %s" % (self.collection, self.exportPath)
	
class ConfigDirNotFoundException (Exception):
	def __init__ (self, value):
		self.value = value
	def __str__ (self):
		return repr (self.value)
		
if __name__ == "__main__":
	# path = "/dls/devel/ostwald/tomcat/tomcat/dcs_conf/collection_config"
	# path = "/home/ostwald/tmp/queen-collections"
	path = "C:/Documents and Settings/ostwald/devel/tmp/dcs_conf/collections"
	fcd = Collections (path)
	fcd.visit()
	
	# report specialCaseList
	print "configDirNotFoundList"
	for path in fcd.configDirNotFoundList:
		print "\t%s" % path
		
	# report specialCaseList
	print "specialCaseList"
	for path in fcd.specialCaseList:
		print "\t%s" % path
	
	# for format in ["collection_config", "framework_config", "dcs_data"]:
		# fixer = RecFixer ( fcd[format] )
		# fixer.fix_namespace()
	# fcd.report()
