"""
reader for an EAD record as produced by AT.
items all exist at a particular path
"""
import sys, os
from JloXml import XmlRecord, XmlUtils
from UserDict import UserDict
from EadFoundation import ArchDesc
from EadCollection import EadCollection

class EadRecord (XmlRecord):
	itemPath = "ead/archdesc/dsc/c01/c02/c03"
	xpath_delimiter = "/"
	
	def __init__ (self, path):
		XmlRecord.__init__ (self, path=path)
		archdescElement = self.selectSingleNode (self.dom, 'ead/archdesc')
		self.archdesc = ArchDesc (archdescElement, self)
		self.collections = self._get_collections()
		self.itemMap = UserDict()
		for col in self.collections:
			for item in col.getItems():
				self.itemMap[item.id] = item
				
	def getItem (self, id):
		if id in self.itemMap:
			return self.itemMap[id]
		else:
			return None
	
	def _get_collections (self):
		# collections = self.selectNodes (self.dom, 'ead/archdesc/dsc/c01/c02')
		collections = []
		for node in self.selectNodes (self.dom, 'ead/archdesc/dsc/c01/c02'):
			collections.append (EadCollection (node, self))
		return collections
	
	def getCollection (self, id):
		for c in self.collections:
			if c.id == id:
				return c
		return None

if __name__ == "__main__":
	path = "Final Washington EAD.xml"
	ead = EadRecord (path=path)


