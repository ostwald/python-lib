"""
nsdl_updater.py

task1 - 

"""
import sys, os, re
from JloXml import MetaDataRecord, XmlUtils
from ncar_lib.repository.updates import Repository, Collection, Format, Task
from nsdl.formats import Msp2Record, MathPathRecord, NcsItemRecord
import nsdl_task_1, nsdl_task_2, nsdl_task_3, nsdl_task_5

# tasks = [nsdl_task_1, nsdl_task_2, nsdl_task_3, nsdl_task_5]
tasks = [nsdl_task_5]

nsdl_tasks = map (Task, tasks)


class NsdlCollection (Collection):

	itemClass = MetaDataRecord
	
	def __init__ (self, baseDir, format=None, itemTasks=None):
		self.itemTasks = itemTasks
		Collection.__init__ (self, baseDir, format, tasks)
		
	def instantiateItemClass (self, path):
		"""
		Here's where we might instantate items based on format
		"""
		
		# print '   path: %s' % path
		
		if self.format == 'msp2':
			rec = Msp2Record (path=path)
		elif self.format == 'math_path':
			rec = MathPathRecord (path=path)
		elif self.format == 'ncs_item':
			rec = NcsItemRecord (path=path)
		else:
			raise KeyError, 'unrecognized format: %s' % self.format
		# print 'NsdlCollection: instantiated item (%s)' % rec.__class__.__name__
			
		return rec
		
			
class NsdlFormat (Format):
	
	itemClass = NsdlCollection
	
	def __init__ (self, baseDir, tasks):
		Format.__init__ (self, baseDir, tasks)
		
class NsdlRepository (Repository):
	
	itemClass = NsdlFormat

if __name__ == '__main__':
	repoPath = '/Users/ostwald/Documents/Work/NSDL/TNS Transition-Fall-2011/repo'
	
	repo = NsdlRepository (repoPath, nsdl_tasks)
	for format in repo.getFormats():
		if format.format == 'ncs_item':
			format.update()
