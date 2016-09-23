from JloXml import XmlRecord, XmlUtils

class PubNameXSD (XmlRecord):
	xpath_delimiter = "/"

	def getPubNames (self):
		xpath = "xs:schema/xs:simpleType/xs:restriction/xs:enumeration"
		# xpath = "xs:schema/xs:simpleType/xs:restriction/xs:enumeration"
		nodes = self.getElementsByXpath (self.dom, xpath)
		# print "%d nodes found" % len(nodes)
		values = []
		for node in nodes:
			values.append (node.getAttribute("value"))
		return values
		
	def setPubNames (self, pubNames):
		# <xs:enumeration value="Abstracts of Papers of the American Chemical Society"/>
		xpath = "xs:schema/xs:simpleType/xs:restriction"
		parent = self.selectSingleNode (self.dom, xpath)
		if not parent:
			raise Exception, "pubName parent not found"
		for child in self.getElements(parent):
			# self.clearElement (child)
			parent.removeChild (child)
			child.unlink()
			
		
		for pn in pubNames:
			child = self.addElement (parent, "xs:enumeration")
			child.setAttribute ("value", pn)
			
def getPubNameSchema ():
	url = "http://nldr.library.ucar.edu/metadata/osm/1.0/schemas/vocabs/pubName.xsd"
	import urllib
	data = urllib.urlopen(url)
	# return PubNameXSD(xml=data.read().encode('utf-8'))
	return PubNameXSD(xml=data.read().decode ('utf-8'))
		
def getPubNames (verbose=0):
	rec = PubNameXSD (path="pubName.xsd")
	pubNames = rec.getPubNames()
	if verbose:
		print '%d pubNames found' % len(pubNames)
		for pn in pubNames:
			print pn
	return pubNames
	
def setPubNames (pubNames):
	rec = PubNameXSD (path="pubName.xsd")
	rec.setPubNames (pubNames)
	return rec
	
def setPubNamesTester ():
	pubNames = ["fee", "foo"]
	rec = setPubNames (pubNames)
	print rec
	
if __name__ == "__main__":
	rec = getPubNameSchema()
	print rec
