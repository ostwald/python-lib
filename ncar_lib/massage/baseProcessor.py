"""

Make file containing mappings from library_dc records to webcat records, including accessionNums

- Walk a collection directory. For each library_dc record:
-- getID, derive accessionNum from url
-- get corresponding webcat record. from webcat record, 
--- getID, accessionNum

if accession nums don't match - throw exception

"""

import os, sys
from ncar_lib.lib import globals, webcatUtils
from ncar_lib.lib.frameworks import LibraryDCRec, WebcatRec

class InvalidRecord (Exception):
	pass

class RecordProcessor:
	"""
	first, test for correspondence between id numbers of library_dc and webcat_dc recs
	
	NOTE: an error will be raised if any library_dc records do not have corresponding webcat records
	
	"""
	def __init__ (self, library_dc_path):
		self.lib_dc_rec = LibraryDCRec (library_dc_path)
		self.recId = self.lib_dc_rec.getId()
		self.collection = os.path.basename (os.path.dirname (library_dc_path))
		self.webcat_rec = self._getWebcatRec (self.recId)
		self.accessionNum = self.webcat_rec.accessionNum
		self.ncar_rec = self._getNCARLibraryDCRec (self.recId)
		
	def _getNCARLibraryDCRec (self, recId):
		"""
		get ncar library record with id=recId
		"""
		# path = os.path.join (globals.metadata, "ncar_library_dc", self.collection, recId+'.xml')
		path = webcatUtils.getRecordPath (recId, "ncar_library_dc")
		return LibraryDCRec (path)
		
	def _getWebcatRec (self, recId):
		"""
		get webcat record with id=recId
		"""
		# path = os.path.join (globals.metadata, "webcat", self.collection, recId+'.xml')
		path = webcatUtils.getRecordPath (recId, "webcat")
		return WebcatRec (path=path)
			
class CollectionProcessor:
	
	rpClass = RecordProcessor
	
	def __init__ (self, collection):
		self.dir = os.path.join (globals.metadata, "library_dc", collection)
		files = os.listdir (self.dir)
		files.sort()
		for filename in files:
			if not filename.endswith (".xml"): continue
			path = os.path.join (self.dir, filename)
			rp = self.rpClass (path)
			self.process (rp)
			
	def process (self, rp):
		print rp.recId
				
class MetadataProcessor:
	
	cpClass = CollectionProcessor
	
	def __init__ (self):
		baseDir = os.path.join (globals.metadata, "library_dc")
		for collection in os.listdir (baseDir):
			if collection == ".DS_Store": continue
			self.cpClass (collection)
			
class SimpleIdListProcessor:
	rpClass = RecordProcessor
	
	def __init__ (self, idList):
		self.idList = idList
		self.idList.sort()
		for id in self.idList:
			path = webcatUtils.getRecordPath(id)
			rp = self.rpClass (path)
			self.process (rp)
			
	def process (self, rp):
		print rp.recId	
		
	# def getPath (self, id, set="library_dc"):
		# prefix = id[:id.index ("-000")]
		# collection = globals.prefixMap[prefix]
		# return os.path.join (globals.metadata, set, collection, id+'.xml')
	
def recordProcessorTester ():
	id = "TECH-NOTE-000-000-000-006"
	path = webcatUtils.getRecordPath (id)
	# path = os.path.join (globals.metadata, "library_dc/technotes", "TECH-NOTE-000-000-000-006.xml")
	rp = RecordProcessor (path)
	print rp.recId
	
def collectionProcessorTester():
	CollectionProcessor ("technotes")
	
if __name__ == "__main__":
	recordProcessorTester ()
	collectionProcessorTester()
	# MetadataProcessor()
	
	# print globals.getRecordPath ("TECH-NOTE-000-000-000-826")
	# SimpleIdListProcessor (["TECH-NOTE-000-000-000-003"])
