"""
nsdl_updater.py

task1 - 

"""
import sys, os, re
from JloXml import MetaDataRecord, XmlUtils
from ncar_lib.repository.updater import FormatUpdater, CollectionUpdater, ObjectUpdater, Collection, Format, Task

import nsdl_task_1	

tasks = [nsdl_task_1]

nsdl_tasks = map (Task, tasks)


class NsdlCollection (Collection):

	itemClass = MetaDataRecord

class NsdlFormat (Format):

	itemClass = NsdlCollection
	
	def instantiateItemClass (self, path):
		return self.itemClass(path=path)
	
class NsdlCollectionUpdater (NsdlCollection):

	def __init__ (self, baseDir, itemTasks=None, format=None):
		self.itemTasks = itemTasks
		print "NsdlCollectionUpdater constructor"
		NsdlCollection.__init__ (self, baseDir, format)
		
	def instantiateItemClass (self, path, tasks, format):
		print 'instantiating item (%s)' % self.itemClass.__name__
		return self.itemClass(path=path)
		
	def update (self):
		print '\n-----------------------------'
		print 'updating Collection: %s' % self.key
		print '      there are %d items' % len(self)
		
		objectUpater = ObjectUpdater (self.itemTasks)

		for item in self:
			objectUpater.update(item)
			
class NsdlFormatUpdater (FormatUpdater):
	
	itemClass = NsdlCollectionUpdater
	
	def __init__ (self, baseDir, tasks):
		FormatUpdater.__init__ (self, baseDir, tasks)
		


if __name__ == '__main__':
	repoPath = '/Users/ostwald/devel/python/python-lib/nsdl/updates/repo'
	msp2Path = os.path.join (repoPath, 'msp2')
	
	msp2FormatUpdater = NsdlFormatUpdater(msp2Path, nsdl_tasks)
	collectionUpdater = msp2FormatUpdater.getCollection ('1235694767688')
	
	print 'collectionUpdater class: %s' % collectionUpdater.__class__.__name__
	
	collectionUpdater.update ()
