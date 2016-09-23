import sys, os
from JloXml import XmlRecord, XmlUtils
from UserDict import UserDict

class EadStructuralUnit:
	"""
	the major structural components of an EAD document, namely
	archDesc and Containers
	"""
	title = "Unknown"
	
	def __init__ (self, element, parent):
		self.element = element
		self.parent = parent
		did_element = XmlUtils.selectSingleNode (element, 'did')
		if not did_element:
			raise Exception, "did not found"
		self.did = EadDID (did_element)
		self.title = self.did.unittitle or self.title
		self.level = element.getAttribute('level')
		
	def report (self):
		header = "%s report" % self.__class__.__name__.split('.')[-1]
		print "\n%s\n%s" % (header, '-'*len(header))
		print "title: " + self.title
		print "level: " + self.level	
		
class ArchDesc (EadStructuralUnit):
	"""
	encapsulates the 'archdesc' element, which 'describes Collection-Level 
	information in the EAD framework 
	(see http://www.loc.gov/ead/ag/agcre2.html#sec1a
	"""
	title = "unknown"
	
	def __init__ (self, element, parent):
		EadStructuralUnit.__init__ (self, element, parent)
		self.ead = self.parent
		self.id = self.did.unitid

class EadComponent (EadStructuralUnit):
	def __init__ (self, element, parent):
		EadStructuralUnit.__init__ (self, element, parent)
		self.id = element.getAttribute('id')
		
class Container (UserDict):
	"""
	items are lists or ??
	"""
	def keys (self):
		sorted = self.data.keys()
		sorted.sort()
		return sorted
		
	def __getitem__ (self, key):
		if self.data.has_key (key):
			return self.data[key]
		else:
			None
		
	def values(self):
		return self.data.values() or []
		
	def addItem (self, item):
		raise Exception, "addItem is not defined"
		
		
class Box (Container):
	"""
	boxes are made up of folders
	"""
	
	def addItem (self, item):
		"""
		add to appropriate folder
		"""
		key = item.folder
		folder = self.getFolder (key)
		folder.addItem (item)
		self[key] = folder
	
	# def __setitem__(self, key, item): 
	#	self.data[key] = item
	
	def getFolders (self):
		return self.values()
		
	def getFolder (self, id):
		return self[id] or Folder()
		# if self.data.has_key(id):
			# return self[id]
		# else:
			# return Folder()
		
class Folder (Container):
	
	def cmpItems (self, x, y):
		i1 = int (x.id[3:])
		i2 = int (y.id[3:])
		return cmp(i1, i2)
	
	def getItems (self):
		values = self.values()
		# values.sort (lambda x, y: cmp (x.id, y.id))
		values.sort (self.cmpItems)
		return values
		
	def getItem (self, id):
		return self[id]
		
	def addItem (self, item):
		self[item.id] = item

class EadDID:
	"""
	the 'Descriptive Identification' for a given body(unit) of materials
	see http://www.loc.gov/ead/ag/agcre2.html#sec1aa
	"""
	
	unittitle = None
	
	def __init__ (self, did_element):
		if not did_element:
			raise Exception, "did_element is NONE"
		self.element = did_element
		self.unittitle = XmlUtils.getTextAtPath (did_element, "unittitle/title")
		self.unitid = XmlUtils.getTextAtPath (did_element, "unitid")
		self.containerElements = XmlUtils.selectNodes (self.element, "container")
		self.physdescElements = XmlUtils.selectNodes (self.element, "physdesc")
		
def getEadRecord ():
	from EadRecord import EadRecord
	path = "Final Washington EAD.xml"
	return EadRecord (path=path)
			

