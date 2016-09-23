"""
idSet - holds IDs and compares with other idSets to find:

ids in common
differences in members, etc
"""
import os, sys
from dataset import DataSet, getDataSet
from UserList import UserList

class IdSet (UserList):
	"""
	Manages a list of IDs obtained from a single data file.
	
	compare - finds IDs in this idSet that are not in the other idSet
	
	incommon - finds IDs in this idSet that are also in the other idSet
	
	"""
	def __init__ (self, filename, dataSetName):
		dataset = getDataSet(dataSetName)
		self.filename = filename
		self.data = dataset.getItems(self.filename)
		
		# normalize userIds by removing 'DPS-' prefix
		if (0):
			def normalize (id):
				prefix = "DPS-"
				if id.startswith(prefix):
					return id[len(prefix):]
				return id
			
			self.data = map (normalize, self.data)
		
		self.title = '%s/%s' % (dataSetName, self.filename)
		print '%s idset has %s items' % (self.title, len(self))
		print ' - first: ', self[0]
		print ' - last: ', self[-1]
	
	def compare (self, other):
		missing = filter (lambda x:x not in other.data, self.data)
		print 'there are %d in %s that are NOT in %s' % (len(missing), self.title, other.title) 
	
	def inCommon (self, other):
		common = filter (lambda x:x in other.data, self.data)
		print 'there are %d that are in both idSets' % len(common) 
		return common
		
class RandomIdSet (IdSet):
	"""
	IdSet containing Ids from all the collections that have system-generated (random) ids
	"""
	def __init__ (self, dataSetName):
		dataset = getDataSet(dataSetName)
		self.filenames = dataset.getRandomIdFileNames()
		self.data = dataset.getMergedItems(dataset.getRandomIdFileNames())
		
		self.title = '%s/%s' % (dataSetName, ', '.join(self.filenames))
		print '%s idset has %s items' % (self.title, len(self))
		
class AllIdSet (IdSet):
	"""
	IdSet containing all the Ids defined in this dataSet
	"""
	def __init__ (self, dataSetName):
		dataset = getDataSet(dataSetName)
		self.filenames = dataset.getAllFilenames()
		self.data = dataset.getMergedItems(self.filenames)
		
		self.title = '%s/%s' % (dataSetName, ', '.join(self.filenames))
		print '%s idset has %s items' % (self.title, len(self))

def printlist(list, title=None):
	if title:
		print title
	for item in list:
		print '- ', item
		
def idSetTester():
	filename = 'userIds.txt'
	idset1 = IdSet(filename, 'BSCS')
	idset2 = IdSet(filename, 'CCS')
	common = idset1.inCommon(idset2)
	printlist(common)
	
	idset1.compare(idset2)
	idset2.compare(idset1)	
	
def randomIdSetTester():
	idset1 = RandomIdSet('BSCS')
	idset2 = RandomIdSet('CCS')
	common = idset1.inCommon(idset2)
	printlist(common)	
	
def compareAllIds ():
	"""
	find any Ids that are in both BSCS and CCS
	and report
	"""
	idset1 = AllIdSet('BSCS')
	idset2 = AllIdSet('CCS')
	common = idset1.inCommon(idset2)
	printlist(common)	
	
if __name__ == '__main__':
	compareAllIds()


