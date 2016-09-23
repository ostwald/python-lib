import os, sys, re, codecs, string
from UserList import UserList

# path = 'C:/Documents and Settings/ostwald/devel/projects/frameworks-project/frameworks/osm/1.1/schemas/vocabs/pubName.xsd'

restriction_pat = re.compile ("<xs:restriction base=\"xs:string\">(.*)</xs:restriction>", re.DOTALL)

## <xs:enumeration value="AI Magazine"/><!--2010-08-31:correct name-->
enumeration_pat = re.compile ("<xs:enumeration value=\"(.*)\"/>")
comment_pat = re.compile("<!--(.*)-->")

sort_pat = re.compile("The|the|A|a|An|a ");

article_pat = re.compile("(The|the|A|a|An|a) ");

class VocabTerm:
	"""
	represents one controlled vocab term (a pubname) as well as an optional comment
	"""
	def __init__ (self, data=None, term=None, comment=None):
		# print "*%s*" % data
		self.term = term
		self.comment = comment
		if data:
			m = enumeration_pat.match (data)
			if not m:
				raise Exception, "enum not found in '%s'" % data
			self.term = m.group(1)
			remainder = data[m.end():].strip()
			self.comment = None
			m = remainder and comment_pat.match (remainder)
			self.comment = m and m.group(1).strip() or None
		
	def sortValue (self):
		"""
		implements custom search to ignore articles
		
		see "article_pat"
		"""
		m = article_pat.match (self.term)
		sortVal = self.term
		if m:
			sortVal = self.term[len(m.group(1)):].strip()
		return sortVal.lower()
		
	def __cmp__ (self, other):
		"""
		sort predicate for custom search
		"""
		try:
			return cmp(self.sortValue(), other.sortValue())
		except UnicodeDecodeError:
##			print 'couldnt compare: \n- %s\n- %s' % (self.term.encode('utf-8'), other.term.encode('utf-8'))
			toShow = type(self.sortValue()) == type("") and self.sortValue() or None
			if not toShow:
				toShow = type(other.sortValue()) == type("") and other.sortValue() or '??'
			
			print 'compare error: %s (%s <-> %s)' % (toShow, type(self.sortValue()), type(other.sortValue()))
			return 0		
		
	def __repr__ (self):
		s = "%s\n  %s" % (self.term, self.sortValue()) 
		# return s.encode('utf-8')
		return self.term.encode('utf-8')
		
	def toxml (self):
		"""
		the way it looks in the XSD file
		"""
		s = "<xs:enumeration value=\"%s\"/>" % self.term
		if self.comment:
			s += " <!-- %s -->" % self.comment
		return s
			
		
class TermList (UserList):
	
	def __init__ (self, xsdpath):
		UserList.__init__ (self)
		s = codecs.open(path, 'r', 'utf-8').read()
		## print s.encode('utf-8')
		m = restriction_pat.search (s)
		if not m:
			raise Exception, "restriction tag contents not found"
		lines = map (string.strip, m.group(1).split('\n'))
		lines = filter (lambda x: x, lines)
		
		self.data = map (VocabTerm, lines)
		self.sort()
		
	def addTerm (self, term, comment=None):
		self.append (VocabTerm (term=term, comment=comment))
		self.sort()

	
if __name__ == '__main__':
	path = "pubName.xsd"
	terms = TermList (path)
	terms.addTerm ("The aaa", "fake term")
	for term in terms.data[:800]:
		# print term.toxml().encode('utf-8')
		print term.toxml()
