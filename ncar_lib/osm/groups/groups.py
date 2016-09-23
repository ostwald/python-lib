"""
class for creating groups file
"""
from JloXml import XmlRecord, XmlUtils

class GroupsFile (XmlRecord):
	
	def __init__ (self):
		XmlRecord.__init__ (self, xml="<opml></opml>")
		self.title = "Subject - Math"
		self.nameSpaceUri = "http://ns.nsdl.org/ncs/fields"
		self.schemaUri = "http://ns.nsdl.org/ncs/msp2/1.00/schemas/fields/mathSubject.xsd"
		self.version = "2.0"
		self.defaultNamespace = "http://ns.nsdl.org/ncs/fields"
		self.setSchemaLocation (self.schemaUri, self.nameSpaceUri)
		self.setSchemaNamespace ()
		self.doc.setAttribute ("xmlns:"+self.schema_instance_namespace, self.defaultNamespace)
		
		self.head = self.addElement (self.doc, "head")
		title = self.addElement (self.head, "title")
		self.setText (title, self.title)
		concept = self.addElement (self.head, "concept")
		concept.setAttribute ("language", "en-us")
		concept.setAttribute ("metaFormat", "osm")
		concept.setAttribute ("metaVersion", "1.0.0")
		concept.setAttribute ("text", "Mathematics Subject")
		concept.setAttribute ("audience", "cataloger")
		concept.setAttribute ("path", "/record/coverage/location/@state")
		concept.setAttribute ("deftn",  "mathematical topics the resource addresses")
		concept.setAttribute ("collapseExpand", "true")
		self.body = self.addElement (self.doc, "body")
		
		
if __name__ == '__main__':
	print GroupsFile()
		
