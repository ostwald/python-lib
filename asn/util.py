from UserList import UserList
from JloXml import XmlRecord
from UserDict import UserDict

from asnUriService.asnHelper import AsnHelper
from asnUriService.offlineAsnHelper import OffLineAsnHelper

# asnHelper = AsnHelper()
# asnHelper = OffLineAsnHelper()

def getAsnHelper ():
	offline = False
	if offline:
		return OffLineAsnHelper()
	else:
		return AsnHelper()

class SortedDict (UserDict):
	
	def keys (self):
		sorted = self.data.keys()
		sorted.sort()
		return sorted

def beautify (path, out=None):
	out = out or path
	rec = XmlRecord (path=path)
	s = rec.doc.toprettyxml()
	fp = open (out,'w')
	fp.write (s)
	fp.close()

def makeKey (doc):
	""" doc is a StdDocumentHtml instance """
	##return "%s.%s.%s" % (doc.author, doc.topic, doc.created)
	asnHelper = getAsnHelper()
	return "%s.%s.%s.%s" % (asnHelper.getAuthor(doc.author), asnHelper.getTopic(doc.topic), 
							doc.created, doc.docId)

def getNumId (id):
	pat = "http://purl.org/ASN/resources/"
	return id[len(pat):]
	
def makeFullId (idNum):
	return "http://purl.org/ASN/resources/%s" % idNum
	
def gradeRangeCmp (gr1, gr2):
	c = cmp (gr1._lowerInt(), gr2._lowerInt())
	if c == 0:
		return cmp (gr1._upperInt(), gr2._upperInt())
	else:
		return c
	
class GradeRange (UserList):
	def __init__ (self, nodeList):
		UserList.__init__ (self, [])
		if nodeList:
			for n in nodeList:
				self.append (n.getAttribute("rdf:resource").split("/")[-1])
		self.sort (self._gradeCmp)
		
	def _grade2int (self, gr):
		if gr.lower() == "k":
			return 0
		if gr.lower() == "pre-k":
			return -1
		try:
			return int (gr)
		except:
			raise "UnknownGradeRange", gr
				
	def _gradeCmp (self, grade1, grade2):
		return cmp(self._grade2int(grade1), self._grade2int(grade2))
		
	def _lowerInt (self):
		if len(self) == 0:
			return -2
		return self._grade2int (self[0])
	
	def _upperInt (self):
		if len(self) == 0:
			return -2
		return self._grade2int (self[-1])
		
				
	def __repr__ (self):
		if len(self) == 0:
			return "[]"
		if len(self) == 1:
			return "[%s]" % self[0]
		# return "[%s &mdash; %s]" % (self[0], self[-1])
		# return "[%s&mdash;%s]" % (self[0], self[-1])
		return "[%s - %s]" % (self[0], self[-1])
