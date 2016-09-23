## from xml.dom.minidom import parse, parseString
## from xml.parsers.expat import ExpatError
import string
from JloXml import XmlRecord

xml = """<record>
  <description parseType="Literal" lang="en-US">In grades K-4,
  what students know and are able to do includes<ul>
<li>asking questions and stating predictions (hypotheses) that can be addressed
through scientific investigation;</li>
</ul>
</description></record>"""

class myXmlRecord (XmlRecord):
	def __init__ (self, xml):
		XmlRecord.__init__ (self)
		self.setRecordXml (xml)

	def getText(self, element):
		print "getText\n-----------"
		rc = ""

		parseLiteral =  element.getAttribute ("parseType") == "Literal"
		
		for node in element.childNodes:
			print "nodetype: %d" % node.nodeType
			if node.nodeType == node.TEXT_NODE:
				print "\t%s" % node.data
				rc = rc + node.data
			elif node.nodeType == node.ELEMENT_NODE and parseLiteral:
				rc = rc + node.toxml()
			else:
				print "skipped"
		print "-----------\n"
		return string.strip(rc)

rec = myXmlRecord(xml)

text = rec.getTextAtPath("record:description")
print text
