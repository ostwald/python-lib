"""
ASN Catalog - now that the ASN no longer supports the soap-based acsr service (and good riddance),
we need a new way of cataloging the standards docs that are available

services: see http://asn.jesandco.org/content/asn-web-services-overview

- Request a listing of all jurisdictions in the ASN:
http://asn.jesandco.org/api/1/jurisdictions

- Request a listing of all subjects in the ASN:
http://asn.jesandco.org/api/1/subjects

- Request all ASN Standards Documents from Arkansas using the human readable jurisdiction parameter:
http://asn.jesandco.org/api/1/documents?jurisdiction=ar

- Request all Arkansas, Math, Published ASN Standards Documents:
http://asn.jesandco.org/api/1/documents?jurisdiction=ar&subject=math&status=published

"""
import os, sys
from UserDict import UserDict
from JloXml import XmlRecord, XmlUtils

from jurisdictions import Jurisdiction, AsnJurisdictions
from documents import AsnDocuments, CatalogDocument

def showJurisdictions (juris):
	for key in juris.keys():
		print '\n%s' % key
		for attr in ['id', 'organizationName', 'organizationAlias', 'organizationJurisdiction', 'organizationClass', 'DocumentCount']:
			print '- %s: %s' % (attr, getattr(juris[key], attr))
		
def cacheDocsPerJurisdiction ():
	"""
	first step in making catalog - download info about all asnDocs
	by Jurisdiction and then write to disk
	
	the result is a directory ("cashdir") of xml files, each containing
	information about all the asnDocs for a particular jurisdiction
	"""
	cachedir = "/home/ostwald/Documents/ASN/ASN_v3.1.0-cache"
	
	if not os.path.exists(cachedir):
		os.mkdir (cachedir)
		
	juris = AsnJurisdictions()
	print 'downloading from %d jurisdictions' % len(juris)
	
	for j in juris.values():
		author = j.organizationJurisdiction
		try:
			cat = CatalogDocument(author, cachedir)
		except Exception, e:
			print 'unable to create catalogDocument for %s: %s' % (author, e)
			continue
		cat.write ()
			
class AsnInfo:
	"""
	<asnDocument id="http://asn.jesandco.org/resources/D100019C">
		<title>Mathematics Grade-Level Expectations</title>
		<topic>Math</topic>
		<author>LA</author>
		<created>2004</created>
		<status>Published</status>
	</asnDocument>
	"""
	def __init__ (self, element):
		self.element = element
		self.id = element.getAttribute('id')
		for child in XmlUtils.getChildElements(element):
			attr = child.tagName
			val = XmlUtils.getText(child)
			setattr(self, attr, val)
		
class TopicCatalog (UserDict):
	"""
	maps topic to asnDocs from various jurisdictions for that topic
	"""
	cacheBase = "/home/ostwald/Documents/ASN/ASN_v3.1.0-cache"
	
	def __init__ (self):
		self.data = {}
		self.jurisCache = os.path.join(self.cacheBase, 'jurisdictions')
		self.topicCache = os.path.join(self.cacheBase, 'topics')
		
		jurisFiles = filter (lambda x:x.endswith('.xml'), os.listdir(self.jurisCache))
		for j in jurisFiles:
			# print 'processing %s' % j
			path = os.path.join (self.jurisCache, j)
			rec = XmlRecord(path=path)
			asnDocs = map (AsnInfo, rec.selectNodes (rec.dom, 'AsnDocuments:asnDocument'))
			# print ' ... %d docs found' % len(asnDocs)
			for asnInfo in asnDocs:
				topic = asnInfo.topic
				vals = []
				if self.has_key(topic):
					vals = self[topic]
				vals.append(asnInfo.element.cloneNode(True))
				self[topic] = vals
				
	def keys(self):
		sorted = self.data.keys()
		sorted.sort()
		return sorted
				
	def report (self):
		for topic in self.keys():
			print "%s - %d" % (topic, len(self[topic]))
			
	def writeTopicRecords (self):
		for topic in self.keys():
			print "%s - %d" % (topic, len(self[topic]))
			rec = XmlRecord(xml="<AsnDocuments/>")
			root = rec.doc
			root.setAttribute ("topic", topic)
			for asnInfo in self[topic]:
				root.appendChild (asnInfo)
			path = os.path.join(self.topicCache, topic+'.xml')
			rec.write(path)
			print 'wrote to', path

		
def tester ():
	juris = AsnJurisdictions()
	print 'there are %d jurisdictions' % len(juris)
	
	for j in juris.values():
		org = j.organizationJurisdiction
		print '** %s **' % org
		try:
			docs = AsnDocuments({'jurisdiction':org})
			print '%d found for %s (should have been %s)' % (len(docs), j.organizationName, j.DocumentCount)
		except Exception, e:
			print 'could not get AsnDocuments for %s: %s' % (org, e)
		
if __name__ == '__main__':
	# cacheDocsPerJurisdiction()
	cat = TopicCatalog()
	cat.writeTopicRecords()
