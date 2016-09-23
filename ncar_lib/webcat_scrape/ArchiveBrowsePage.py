"""
ArchiveBrowsePage
"""
from JloXml import XmlRecord, XmlUtils
import re
# import webcatUtils
from ncar_lib.lib import webcatUtils
import urllib

class ArchiveBrowsePage (XmlRecord):
	"""
	extract the browse hierarchy table as an xml record and deliver the
	nodes (table rows) to the caller (WebCat) ...
	"""
	
	def __init__ (self, url):
		# print "reading from: '%s'" % url
		self.url = url
		pagedata = urllib.urlopen(url)
		html = pagedata.read()
		marker = html.find ("<FONT SIZE=4 FACE=arial>Archive Browse</FONT>")
		if marker < 0:
			raise Exception, "browse html not found"
		
		tablePat = re.compile ("<TABLE[^>]*?>(.*?)</TABLE>", re.S)
		m = tablePat.search (html[marker:])
		if not m:
			raise Exception, "browse TABLE not found"
			
		## following are manipulations required to convert HTML into XML
		tableXml = webcatUtils.stripComments (m.group())
		tableXml = webcatUtils.fixAttributes (tableXml) # some attributes have no value or unquoted value
		tableXml = webcatUtils.removeBoldTags (tableXml) # bold tags are interleaved with "A" tags!
		tableXml = webcatUtils.removeFontTags (tableXml) # Font tags just make processing difficult
		
		if 0:
			fp = open ("tableXml.xml", 'w')
			fp.write (tableXml)
			fp.close()
		## print tableXml
		XmlRecord.__init__ (self, xml=tableXml)
		if 0:
			fp = open ("tableXml.xml", 'w')
			fp.write (self.__repr__())
			fp.close()
		self.nodeElements = self.getElements (self.doc)
		
	
if __name__ == "__main__":
	url = 'http://library.ucar.edu/uhtbin/cgisirsi/GSBdh1Jxl8/SIRSI/278850018/503/6934'
	page = ArchiveBrowsePage(url)
	print page


	
