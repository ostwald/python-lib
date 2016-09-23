"""
ASN Jurisdictions - this module encapsulates the Jursidiction API
see - http://asn.jesandco.org/content/asn-web-services-overview

e.g., 
`	- http://asn.jesandco.org/api/1/jurisdictions
	- http://asn.jesandco.org/api/1/jurisdictions?class=Organization
	- http://asn.jesandco.org/api/1/jurisdictions?class=U.S.%20States%20and%20Territories

Fragment of webservice response:
	
<?xml version="1.0" encoding="utf-8" ?>
<asnJurisdictions>
	...
   <Jurisdiction xml:id="162">
     <organizationName>American Association for the Advancement of Science</organizationName>
     <organizationAlias>http://purl.org/ASN/scheme/ASNJurisdiction/AAAS</organizationAlias>
     <organizationJurisdiction>AAAS</organizationJurisdiction>
     <organizationClass>Organization</organizationClass>
     <DocumentCount>3</DocumentCount>
   </Jurisdiction>
   ...
</asnJurisdictions>


"""

from serviceclient import SimpleClient
from UserDict import UserDict
from JloXml import XmlRecord, XmlUtils

class Jurisdiction:
	"""
	exposes:
		id (e.g., 162")
		organizationName (e.g., 'American Association for the Advancement of Science')
		organizationAlias (e.g., 'http://purl.org/ASN/scheme/ASNJurisdiction/AAAS')
		organizationJurisdiction (e.g., 'AAAS')
		organizationClass (e.g., Organization)
		DocumentCount (e.g., '3')
	"""
		
	def __init__ (self, element):
		self.id = element.getAttribute ("xml:id")
		for child in XmlUtils.getChildElements (element):
			setattr (self, child.tagName, XmlUtils.getText(child))
		
class AsnJurisdictions(UserDict):
	baseUrl = "http://asn.jesandco.org/api/1/jurisdictions"
	
	def __init__ (self):
		self.data = {}
		client = SimpleClient (self.baseUrl)
		client.verbose = 0
		rec = client.getResponseDoc()
	
		for element in rec.selectNodes(rec.dom, 'asnJurisdictions:Jurisdiction'):
			j = Jurisdiction(element)
			self[j.organizationJurisdiction] = j
			
	def keys(self):
		sorted = self.data.keys()
		sorted.sort()
		return sorted
		
if __name__ == '__main__':
	juris = AsnJurisdictions()
	for key in juris.keys():
		print '\n%s' % key
		for attr in ['id', 'organizationName', 'organizationAlias', 'organizationJurisdiction', 'organizationClass', 'DocumentCount']:
			print '- %s: %s' % (attr, getattr(juris[key], attr))
