"""
BackPackMetadataMixin - behaviours that all curriculum XML records inherit, such as
- instantiation by means of a template record, which is then filled in
- assigning appropriate ID,
- writing to correct location in file structure
"""
import os, sys
from backpack import ConceptsRecord
import bp_share

class BackPackMetadataMixin:
	
	repository = bp_share.repository
	templateDir = bp_share.templateDir
	dowrites = 1
	
	id_prefix = None
	xmlFormat = None
	collection = None
	xmlTemplate = None
	xmlRecordClass = None
	
	def __init__ (self):
		template = os.path.join( self.templateDir, self.xmlTemplate)
		self.xmlRecordClass.__init__(self, path=template)
		# print self
		recNum = self.assignId()
	
	def assignId (self):
		"""
		assign id based on the records already present, and then write
		the record so that the next record's id will be incremented
		"""
		dirpath = os.path.join (self.repository, self.xmlFormat, self.collection)
		recNum = bp_share.getNextIdNum (dirpath)
		self.setId (self.makeRecordId (self.id_prefix, recNum))
		self.write ()
		
	
	def write (self, path=None):
		"""
		if no path is provided, we write to the repository to a path
		determined by format, collection and id
		"""
		if path is None:
			path = os.path.join (self.repository, 
								 self.xmlFormat, 
								 self.collection, 
								 self.getId() + '.xml')
		if self.dowrites:
			self.xmlRecordClass.write(self, path)
			print 'wrote to', path
		else:
			print 'WOULDVE written to', path
		
if __name__ == '__main__':
	rec = BackPackMetadataMixin()
