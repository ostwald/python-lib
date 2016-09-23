"""
field plucker

reads all metadata records in a directory

plucks desired field from each and returns in a list
"""
import os, sys, time
from nsdl import NCSCollectRecord
from UserList import UserList

class Plucker (UserList):

	def __init__ (self, field, masterDir, record_class):
		"""
		masterKey = collection of collections key
		"""
		self.masterDir = masterDir
		self.field = field
		self.record_class = record_class
		self.masterKey = os.path.basename(masterDir)
		self.data = []  # these will be record_class instances
		
	def getValues (self):
	
		# vals = filter (None, map (lambda x:x.get(self.field), self.getRecords()))
	
		vals = [];add=vals.append
		for record in self.getRecords():
			add (record.get(self.field))

		return filter (None, vals)
		
	def getRecords(self):
		
		if self.data == []:
			add = self.data.append
			for filename in os.listdir (self.masterDir):
				if not filename.endswith('.xml'):
					print 'skipping', filename
					continue
				path = os.path.join (self.masterDir, filename)
				add (self.record_class(path=path))

		return self.data
		
if __name__ == '__main__':
	master = '/Users/ostwald/Desktop/DLESE_MIGRATION/NSDL/records/ncs_collect/1201216476279'
	field = 'collSetSpec'
	plucker = Plucker(field, master, NCSCollectRecord)
	values = plucker.getValues()
	print '%d %s values found' % ( len(values), field)
	for key in values:
		print '-', key

