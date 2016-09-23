"""
BackPackModelObject -
	collects information about a curricular object
	- metadata record
	- type
	- collection
	- xmlFormat
"""
import os, sys
from JloXml import XmlRecord, XmlUtils
from UserDict import UserDict

class BackPackModelObject:
	"""
	A node in the data model, able to create an Xml record
	"""
	
	xmlRecord_constructor = None
	def __init__(self, parent=None):
		"""
		parent is a BackPackModelObject instance
		
		"""
		self.parent = parent
		self.record = None
		self._id = None
		self._children = None # a mapping from childID to childData

	def getId(self):
		return self.getRecord().getId()
		
	def getChildren(self):
		raise Exception, 'getChildren is not implemented in %s' % self.__class__.__name__
		
	def write (self, write_children=0):
		# print 'write: ', self.getRecord().getId()
		self.getRecord().write()
		for childObject in self.getChildren().values():
			childObject.write(write_children)
		
	def getRecord (self):
		"""
		children are instantiated, and records obtained so that
		the relations fields of self record can be populated with the
		ids of the children
		"""
		if not self.record:
			self.record = self.xmlRecord_constructor ()
		return self.record

class SortedValuesDict (UserDict):
	"""
	tries to sort it's values. used for ordering relations, etc
	"""
	
	def values(self):
		values = self.data.values()
		values.sort()
		return values
		
	def keys(self):
		sorted = self.data.keys()
		sorted.sort()
		return sorted
		
if __name__ == '__main__':
	path = '/Documents/Work/NSDL/BackPack/curricul-data-working/Physics 2.6.0 Part 1.txt'
	# chapter = Chapter (path)
	# print chapter.getRecord()
