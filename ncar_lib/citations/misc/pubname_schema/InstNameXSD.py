import os, sys
from JloXml import XmlRecord, XmlUtils

class InstNameXSD (XmlRecord):
	xpath_delimiter = "/"

	def getInstNames (self):
		xpath = "xs:schema/xs:simpleType/xs:restriction/xs:enumeration"
		# xpath = "xs:schema/xs:simpleType/xs:restriction/xs:enumeration"
		nodes = self.getElementsByXpath (self.dom, xpath)
		# print "%d nodes found" % len(nodes)
		values = []
		for node in nodes:
			values.append (node.getAttribute("value"))
		return values
		
	def setInstNames (self, instNames):
		# <xs:enumeration value="Abstracts of Papers of the American Chemical Society"/>
		xpath = "xs:schema/xs:simpleType/xs:restriction"
		parent = self.selectSingleNode (self.dom, xpath)
		if not parent:
			raise Exception, "instName parent not found"
		for child in self.getElements(parent):
			# self.clearElement (child)
			parent.removeChild (child)
			child.unlink()
			
		
		for pn in instNames:
			child = self.addElement (parent, "xs:enumeration")
			child.setAttribute ("value", pn)
			
		
		
def getInstNames (path, verbose=0):
	rec = InstNameXSD (path=path)
	instNames = rec.getInstNames()
	if verbose:
		print '%d instNames found' % len(instNames)
		for pn in instNames:
			print pn
	return instNames
	
def setInstNames (path, instNames):
	rec = InstNameXSD (path=path)
	rec.setInstNames (instNames)
	return rec
	
if __name__ == "__main__":
	schemadir = "/home/ostwald/Documents/NCAR Library/Citations project/schemaBlending"
	# filename = 'instName-from-libraryDC.xsd'
	# filename = 'instName-from-PUBS-publisher.xsd'
	filename = 'unionInstNames.xsd'
	path = os.path.join (schemadir, filename)
	instNames = ["fee", "foo"]
	## rec = setInstNames (path, instNames)
	## print rec
	getInstNames (path, 1)
