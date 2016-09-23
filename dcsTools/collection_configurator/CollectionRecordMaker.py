import sys, os
from JloXml import DleseCollectRecord

recs = "h:/Documents/NCAR Library/tmp/collect"
# recs = '""'
templatepath = os.path.join (recs, "NCAR-COLLECTION-template.xml")

# recname = 'DCS-COLLECTION-000-000-000-014.xml'

class RecordMaker:
	"""
	create a valid collection record by 
	- extracting certain fields from the provided (invalid) record
	- writing them into a valid, "template" record
	- changing ID and writing new recor to disk
	"""
	
	old_prefix = "DCS-COLLECTION"
	new_prefix = "NCAR-COLLECTION"
	
	def __init__ (self, path):
		"""
		path to invalide record
		"""
		print path
		self.path = path
		self.recname = os.path.basename (path)
		self.baseRec = DleseCollectRecord (path=os.path.join (recs, self.recname))
		self.fullTitle = self.baseRec.getFullTitle()
		self.shortTitle = self.baseRec.getShortTitle()
		self.description = self.baseRec.getDescription()
		self.key = self.baseRec.getKey()
		self.id = self.baseRec.getId()
		self.newId = self.getNewId (self.id)

		self.newRec = self._makeNewRec ()
		
	def report (self, rec):
		"""
		print out key fields of provided record
		"""
		print 'id: ', rec.getId()
		print 'key: ', rec.getKey()
		print 'fullTitle: ', rec.getFullTitle()
		print 'shortTitle: ', rec.getShortTitle()
		print 'description: ', rec.getDescription()

	def getNewId (self, id):
		return id.replace (self.old_prefix, self.new_prefix)
		
	def _makeNewRec (self):
		newRec = DleseCollectRecord (path=templatepath)
		newRec.setId(self.newId)
		newRec.setFullTitle (self.fullTitle)
		newRec.setShortTitle (self.shortTitle)
		newRec.setDescription ("NCAR Library " + self.shortTitle)
		newRec.setKey (self.key)
		return newRec

	def write (self, path=None):
		if path is None:
			path = os.path.join (os.path.dirname (self.path), self.newId+".xml")
		DleseCollectRecord.write (self.newRec, path)
		print "wrote to " + path
		
def makeCollectionRecords ():
	for filename in os.listdir (recs):
		if not filename.startswith (RecordMaker.old_prefix):
			continue
		path = os.path.join (recs, filename)
		RecordMaker(path).write()

def tester ():
	path = os.path.join (recs, recname)
	maker = RecordMaker (path)
	# maker.report (maker.baseRec)
	maker.write() 	
	
if __name__ == '__main__':
	makeCollectionRecords()
