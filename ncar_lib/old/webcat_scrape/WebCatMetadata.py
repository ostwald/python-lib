"""
WebCatMetadata
"""
from JloXml import XmlRecord, XmlUtils
import os, sys, re
import urllib

def makeId (accessionNum, prefix):
	try:
		idNum = int (accessionNum[2:])
	except:
		msg = "illegal accession #: '%s'" % accessionNum
		raise Exception, msg
	thousands = idNum / 1000
	## print "thousands: %d" % thousands
	ones = idNum % 1000
	## print "ones: %d" % ones
	id = "%s-000-000-%03d-%03d" % (prefix, thousands, ones)
	return id


class WebCatMetadata (XmlRecord):
	"""
	we treate the Metadata Information table as an xml record...
	"""
	
	default_prefix = "TECH-NOTE"
	
	def __init__ (self, url, prefix=None):
		
		## print "reading from: '%s'" % url
		self.url = url
		self.prefix = prefix or self.default_prefix
		pagedata = urllib.urlopen(url)
		content = pagedata.read()
		
		XmlRecord.__init__ (self, xml="<record/>")
		
		
		marker = content.find ("<H3>Metadata Information</H3>")
		if marker < 0:
			raise Exception, "metadata marker not found"
		
		tablePat = re.compile ("<TABLE[^>]*?>(.*?)</TABLE>", re.S)
		m = tablePat.search (content[marker:])
		if not m:
			raise Exception, "metadata TABLE not found"
		## print m.group()
		self.populateXml(m.group())
		self.finalizeXml ()
		
	def finalizeXml (self):
		self.doc.setAttribute ("xmlns:"+self.schema_instance_namespace, \
								self.SCHEMA_INSTANCE_URI)
		self.setNoNamespaceSchemaLocation ( \
			"http://www.dls.ucar.edu/people/ostwald/Metadata/webcat/webcat-record.xsd")
		
		accessionNum = self.getAccessionNum ()
		
		url = "http://www.library.ucar.edu/uhtbin/hyperion-image/" + accessionNum
		urlElement = self.dom.createElement ("url")
		XmlUtils.setText(urlElement, url)
		
		id = makeId (accessionNum, self.prefix)
		idElement = self.dom.createElement ("recordID")
		XmlUtils.setText(idElement, id)
		
		children = XmlUtils.getChildElements (self.doc)
		self.doc.insertBefore (urlElement, children[0])
		self.doc.insertBefore (idElement, urlElement)

	def populateXml (self, xmlData):
		dataRec = XmlRecord (xml=xmlData)
		dataElements = dataRec.getElements (dataRec.doc)
		for dataElement in dataElements:
			cells = XmlUtils.getChildElements (dataElement, "TD")
			name = XmlUtils.getText (cells[0]).strip()
			if name[-1] == ":": name = name[:-1]
			value = XmlUtils.getText (XmlUtils.getChild ("B", cells[1])).strip()
			
			XmlUtils.addChild (self.dom, self.normalizeTagName(name), value)
	
	def getAccessionNum (self):
		"""
		this method cannot be called until the record has been populated
		(AccessionNum is a derived element name)
		"""
		return XmlUtils.getChildText (self.doc, "accessionNum")
	
	def getId (self):
		"""
		this method cannot be called until after finalizeXml has executed
		"""
		return XmlUtils.getChildText (self.doc, "recordID")
		
	def normalizeTagName (self, tag):
		"""
		convert webCat field names so they are acceptable for xml
		"""
		splits = tag.split(" ")
		capitalize = lambda a: a[0].upper() + a[1:]
		capSplits = ""
		if len(splits) > 1:
			capSplits = "".join (map (capitalize, splits[1:]))
		norm = splits[0].lower() + capSplits
		norm = norm.replace ("#", "Num")
		return norm
	
	def write (self, dir="."):
		id = self.getId()
		if not id:
			raise Exception, "Could not write record: id not found"
		path = os.path.join (dir, id + ".xml")
		if os.path.exists (path):
			msg = "Could not write: File already exists for %s" % path
			raise Exception,  msg
		# fp = open (path, 'w')
		# fp.write (self.doc.toprettyxml ("  ","\n"))
		# fp.close()
		XmlRecord.write(self, path)
	
def makeMetadata (urls, prefix):
	if type (urls) == type (""):
		urls = [urls]
	for url in urls:
		md = WebCatMetadata(url, prefix)
		# print md
		md.write("scraped")	
	print "%d metadata records written" % len(urls)
		
if __name__ == "__main__":
	# path = "techNoteIssue.html"
	# content = open (path).read()
	urls = [ 
		"http://library.ucar.edu/uhtbin/cgisirsi/xdH61zWSOX/SIRSI/44010022/511/8635",
		"http://library.ucar.edu/uhtbin/cgisirsi/xdH61zWSOX/SIRSI/44010022/511/8784" 
		]
	prefix = "THESES"
	makeMetadata (urls, prefix)

	
