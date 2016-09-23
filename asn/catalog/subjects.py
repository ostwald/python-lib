"""
ASN Subjects - this module encapsulates the Subjects API
see - http://asn.jesandco.org/content/asn-web-services-overview

e.g., 
`	- http://asn.jesandco.org/api/1/subjects

Fragment of webservice response:
	
<asnSubjects>
   <Subject xml:id="85">
     <Subject>Science</Subject>
     <SubjectIdentifier>http://purl.org/ASN/scheme/ASNTopic/science</SubjectIdentifier>
     <DocumentCount>1906</DocumentCount>
   </Subject>
</asnSubjects>


"""

from serviceclient import SimpleClient
from UserDict import UserDict
from JloXml import XmlRecord, XmlUtils

class Subject:
	"""
	exposes:
		id (e.g., 85")
		Subject (e.g., 'Science')
		SubjectIdentifier (e.g., 'http://purl.org/ASN/scheme/ASNTopic/science')
		DocumentCount (e.g., '1906')
	"""
		
	def __init__ (self, element):
		self.id = element.getAttribute ("xml:id")
		for child in XmlUtils.getChildElements (element):
			setattr (self, child.tagName, XmlUtils.getText(child))
		
class AsnSubjects(UserDict):
	baseUrl = "http://asn.jesandco.org/api/1/subjects"
	
	def __init__ (self):
		self.data = {}
		client = SimpleClient (self.baseUrl)
		rec = client.getResponseDoc()
	
		for element in rec.selectNodes(rec.dom, 'asnSubjects:Subject'):
			subj = Subject(element)
			self[subj.Subject] = subj
		
if __name__ == '__main__':
	subjects = AsnSubjects()
	for key in subjects.keys():
		print '\n%s' % key
		for attr in ['id', 'Subject', 'SubjectIdentifier', 'DocumentCount']:
			print '- %s: %s' % (attr, getattr(subjects[key], attr))
