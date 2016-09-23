"""
dataset refers to the collection of Ids that have been downloaded 
from a repository and cached on disk as files containing Ids, one
per line.

The items of a DataSet are ids

"""
import os, sys
from bscs import *

class DataSet:
	"""
	The DataSet is a directory holding files named for collections
	in the repository. The files contain the ids of the item level metadata
	for the collections.

	"""

	def __init__ (self, base_dir):
		"""
		base_dir - the DataSet directory path
		name - used to identify the subdirectory of id_cache for this DataSet
		   typically 'BSCS' or 'CCS'
		"""
		# self.base_dir = os.path.join (id_cache, self.name)
		self.base_dir = base_dir
		self.name = os.path.basename(base_dir)

	def getMergedItems(self, filenames):
		"""
		returns all the items in all the files for this DataSet,
		which ammounts to all the Ids in the repository
		"""
		items = []
		for filename in filenames:
			items += self.getItems(filename)
		return items
	
	def getItems(self, filename):
		"""
		utility to read a file and return a list of stripped
		strings, one per non-empty and non-commented lines
		"""
		path = self.getPath(filename)
		lines = open(path, 'r').read().split('\n')
		lines = filter(lambda x:x != '' and x[0] != '#', map (lambda x:x.strip(), lines))
		print '%d items - %s' % (len(lines), filename)	
		return lines
		
	def getRandomIdFileNames (self):
		"""
		gets the ids from all files exept those specied in "skipnames"
		
		skip names : emailIds.txt, userInfo.txt
		"""
		skipnames = ['emailIds.txt', 'userInfo.txt']
		
		return filter (lambda x:x not in skipnames, self.getAllFilenames())
	
	def getPath(self, filename):
		# print 'getPath(): ',filename
		return os.path.join (self.base_dir, filename)
		
	def getAllFilenames (self):
		"""
		return list of filenames that contain Ids
		
		"""
		def accept(filename):
			if filename.startswith('TEST'): return 0
			if not filename.endswith('.txt'): return 0
			if os.path.isdir(self.getPath(filename)) : return 0
			return 1
		
		return filter (accept, os.listdir(self.base_dir))
		
def getDataSet (name):
	"""
	convenience function for BSCS merge, so we can work with CCS and BSCS
	DataSets.
	"""
	
	id_cache = os.path.join (os.path.dirname(bscs.__file__), 'id_cache')
	print 'id_cache:', id_cache
	return DataSet (os.path.join (id_cache, name))
	
		
if __name__ == '__main__':
	id_cache = '/Users/ostwald/devel/python/python-lib/bscs/id_cache'
	
	if 0:
		path = '/Users/ostwald/devel/python/python-lib/bscs/id_cache/CCS/TEST_DATA.txt'
		items = getItems(path)
		print '%d items returned' % len (items)
		for item in items:
			print '- "%s"' % item
			
	dataset = DataSet (os.path.join(id_cache, 'CCS'))
	# paths = getAllFilenames()
	paths = dataset.getRandomIdFileNames()
	print 'PATHS'
	for p in paths:
		print ' - ',p
		
	items = dataset.getMergedItems (paths)
	print '%d items read' % len(items)
