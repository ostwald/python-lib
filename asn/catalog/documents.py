"""
ASN Documents - this module encapsulates the Documents API
see - http://asn.jesandco.org/content/asn-web-services-overview

e.g., 
`	- http://asn.jesandco.org/api/1/documents

Fragment of webservice response:
	
<asnDocuments>
   <Document xml:id="10420">
     <DocumentID type="asnUri">http://asn.jesandco.org/resources/D100019A</DocumentID>
     <DocumentID type="asnPurl">http://purl.org/ASN/resources/D100019A</DocumentID>
     <DocumentTitle xml:lang="en"><![CDATA[Social Studies Curriculum Frameworks Revised 2000]]></DocumentTitle>
     <DocumentSubject href="http://purl.org/ASN/scheme/ASNTopic/behavioralStudies">Behavioral Studies</DocumentSubject>
     <DocumentJurisdiction href="http://purl.org/ASN/scheme/ASNJurisdiction/AR">AR</DocumentJurisdiction>

     <LocalAdoptionDate>2000</LocalAdoptionDate>
     <PublicationStatus href="http://purl.org/ASN/scheme/ASNPublicationStatus/Deprecated">Deprecated</PublicationStatus>
     <DocumentRdf type="xml">http://asn.jesandco.org/resources/D100019A_full.xml</DocumentRdf>
     <DocumentRdf type="json">http://asn.jesandco.org/resources/D100019A_full.json</DocumentRdf>
     <DocumentRdf type="turtle">http://asn.jesandco.org/resources/D100019A_full.ttl</DocumentRdf>
     <DocumentRdf type="notation3">http://asn.jesandco.org/resources/D100019A_full.n3</DocumentRdf>

     <DocumentHtml>http://asn.jesandco.org/resources/D100019A</DocumentHtml>
   </Document>
<asnDocuments>


"""
import os, sys
from serviceclient import SimpleClient
from UserDict import UserDict
from JloXml import XmlRecord, XmlUtils

class Document:
	"""
	exposes:
		
	"""
		
	def __init__ (self, element):
		# print element.toxml()
		self.element = element
		self.id = element.getAttribute ("xml:id")
		self.asnUri = self.getChildByTypeAttr('DocumentID', 'asnUri')
		self.asnPurl = self.getChildByTypeAttr('DocumentID', 'asnPurl')
		self.title = XmlUtils.getChildText (self.element, 'DocumentTitle')
		self.uid = os.path.basename(self.asnUri)
		self.author = XmlUtils.getChildText (self.element, 'DocumentJurisdiction')
		self.topic = XmlUtils.getChildText (self.element, 'DocumentSubject')
		self.created = XmlUtils.getChildText (self.element, 'LocalAdoptionDate')
		self.status = XmlUtils.getChildText (self.element, 'PublicationStatus')

		
	def getChildByTypeAttr (self, tag, typeAttr):
		for child in XmlUtils.getChildElements(self.element, tag):
			if child.getAttribute("type") == typeAttr:
				return XmlUtils.getText(child)
			
	def getKey (self):
		"""
		doc.getAuthor(), doc.getTopic(), doc.getCreated(), doc.getUid());
		"""
		for attr in ['author', 'topic', 'created', 'uid']:
			print "%s: %s" % (attr, getattr(self, attr))
		return self.author + "." + self.topic + "." + self.created + "." + self.uid;
		
	def report(self):
		for attr in ['title', 'asnUri', 'topic', 'created', 'id', 'uid', 'status']:
			print '- %s: %s' % (attr, getattr(self, attr))
			
	def asCatalogElement(self):
		element = XmlUtils.createElement ('asnDocument')
		element.setAttribute ("id", self.asnUri)
		for attr in ['title', 'topic', 'author', 'created',  'status']:
			child = XmlUtils.createElement(attr)
			val = getattr(self, attr) or ''
			## print "val: %s (%s)" % (val, type(val))
			XmlUtils.setText (child, val)
			element.appendChild(child)
		return element
				
class AsnDocuments(UserDict):
	baseUrl = "http://asn.jesandco.org/api/1/documents"
	
	def __init__ (self, params):
		self.data = {}
		client = SimpleClient (self.baseUrl)
		client.verbose = 0
		rec = client.getResponseDoc(params=params)
		# print rec
		docNodes = rec.selectNodes(rec.dom, 'asnDocuments:Document')
		# print "%d docs found" % len(docNodes)
		for element in docNodes:
			doc = Document(element)
			# if not doc.asnPurl:
				# # raise KeyError, "asnPurl not found \n%s" % element.toxml()
				# print "asnPurl not found"
				# continue
			self[doc.asnUri] = doc
				
class CatalogDocument (AsnDocuments):
	"""
	collect information about documents associated with a PARTICULAR JURISDICTION,
	and puts together (see "asCatalogDoc") as an XML Document that can be read by the AsnCatalog
	java Class.
	"""
	
	def __init__ (self, jurisdiction, baseDir):
		"""
		jurisdiction uses the abbrev (e.g., "CO") or "organizationJurisdiction" field of the 
		ASN jurisdiction web service request
		"""
		self.baseDir = baseDir
		self.jurisdiction = jurisdiction
		AsnDocuments.__init__(self, {'jurisdiction' : jurisdiction})
	
	def asCatalogDoc (self):
		rec = XmlRecord(xml='<AsnDocuments/>')
		root = rec.doc
		root.setAttribute ("jurisdiction", self.jurisdiction)
		for asnDoc in self.values():
			root.appendChild (asnDoc.asCatalogElement())
		return rec
		
	def write (self):
		if not os.path.exists(self.baseDir):
			raise IOError, "basedir does not exist at %s" % self.baseDir
		path = os.path.join (self.baseDir, self.jurisdiction+".xml")
		self.asCatalogDoc().write(path)
		print 'wrote to', path
		
def tester():
	params = {'jurisdiction' : 'CO'}
	documents = AsnDocuments(params)
	for key in documents.keys():
		# print '%s: %s' % (documents[key].getKey(), key)
		documents[key].report()
		print ''
		
def findErrorJurisdictions():
	from jurisdictions import AsnJurisdictions
	juris = AsnJurisdictions()
	for key in juris.keys():
		# print key
		try:
			cat = CatalogDocument (key, None)
			print "%s - OKAY" % key
		except Exception, e:
			print "%s - %s" % (key, e)
		
if __name__ == '__main__':
	if 0:
		author = 'CO'
		cachedir = "/home/ostwald/Documents/ASN/ASN_v3.1.0-cache"
		cat = CatalogDocument (author, cachedir)
		print cat.asCatalogDoc()
		# cat.write ()
	else:
		# findErrorJurisdictions()
		tester()

