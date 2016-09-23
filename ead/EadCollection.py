import sys, os
from EadFoundation import EadComponent, Box, getEadRecord
from JloXml import XmlUtils
from UserDict import UserDict
from EadItem import EadItem

class EadCollection (EadComponent):
	"""
	collection elements correspond to the "c02" level of the EAD document
	"""
	def __init__ (self, element, parent):
		EadComponent.__init__ (self, element, parent)
		self._items = UserDict()
		self.boxes = UserDict()
		for node in XmlUtils.selectNodes (element, "c03"):
			self.add (EadItem (node, self))
		
	def getItems (self):
		return self._items.values()
		
	def getBox (self, key):
		if not self.boxes.has_key (key):
			self.boxes[key] = Box()
		return self.boxes[key]
			
	def getFolder (self, box_key, folder_key):
		if not self.boxes.has_key (box_key):
			raise Exception, "box not found for %s" % box_key
		box = self.boxes[box_key]
		
		if not box.has_key (folder_key):
			raise Exception, "folder not found in box %s for %s" % (box_key, folder_key)
		return box.getFolder (folder_key)
		
	def add (self, item):
		self._items[item.id] = item
		box = self.getBox (item.box)
		box.addItem (item)
	
	def report (self):
		EadComponent.report (self)
		print "id: %s" % self.id
		print "items: %d" % len(self._items)

def digitalObjectReport (ead):
	ead.archdesc.report()
	for col in ead.collections:
		col.report()
		for item in col.getItems():
			if item.hasDigitalObject():
				print "\n---------------------------\n%s" % item.dao
				
def reportCollections (ead):
	ead = getEadRecord()
	ead.archdesc.report()
	for col in ead.collections:
		col.report()				

def getBestCollection ():
	ead = getEadRecord()
	return ead.collections[0]
		
def foo(ead):
	for col in ead.collections:
		col.report()
		for item in col.getItems():
			item.did._get_containerInfo()
			
if __name__ == "__main__":
	best = getBestCollection()
	best.report()
