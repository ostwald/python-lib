from author_search_globals import CERTAIN_CONFIDENCE, HIGH_CONFIDENCE, LOW_CONFIDENCE, NO_CONFIDENCE, strength_of_matches


recordSchema = ['title', 'recId', 'collection','confidence', 'format', 'status', 'recordDate', 'publishedDate']

# schema of a MetadataAuthor 
personSchema = ['upid', 'lastName', 'firstName', 'middleName']

		
class MetadataAuthor:
	"""
	holds information about a "matching author" from the metadata record
	- last
	- first (initial)
	- middle (initial)
	- upid
	"""
	def __init__ (self, last, first, middle, upid=None):
		self.last = last
		self.first = self.getInitial(first)
		self.middle = self.getInitial(middle)
		self.upid = upid
		
	def getInitial (self, s):
		if not s:
			return ""
		return s[0]
		
			
	def __repr__ (self):
		s = ""
		if self.first:
			s = '%s.' % self.first
		if self.middle:
			s = '%s %s.' % (s, self.middle)
		return s + ' ' + self.last

class AuthorSearchResult:
	"""
	pools information from a search result and a author and exposes:
		self.searchResult
		self.author
		self.recId
		self.format
		self.title
		self.collection
		self.status
		self.recordDate
		self.publishedDate
		self.matchingPerson
		
	match attribute indicates the strength of match for this result
	"""
	def __init__ (self, searchResult, author):
		self.searchResult = searchResult
		self.author = author
		self.confidence = NO_CONFIDENCE # int representation of confidence in match
		self.recId = searchResult.recId
		self.format = searchResult.xmlFormat
		self.title = searchResult.payload.getTitle()
		self.collection = searchResult.collection
		self.status = searchResult.dcsstatus
		self.recordDate = None  # payload dependent
		self.publishedDate = None # payload dependent
		self.matchingPerson = self.getMetadataAuthor()
		
	def getMatchingPerson (self):
		raise Exception, 'getMatchingPerson not yet implemented'
		
	def getMatchStrength (self):
		"""
		a string representation of confidence
		"""
		return strength_of_matches[self.confidence]
		
	def getMetadataAuthor (self):
		"""
		we are extracting fields from whatever getMatchingPerson returns
		"""
		raise Exception, 'getMetadataAuthor not yet implemented'
		
	def __repr__ (self):
		return "%s - collection: %s (%s)\n  %s" % (self.recId, self.collection, self.status, self.title)
		
	def getAttr (self, attr, baseObj=None):
		baseObj = baseObj or self
		# print ' @%s' % attr
		val = hasattr(baseObj, attr) and getattr(baseObj, attr) or ""
		return unicode(val)
	
		
	def asTabDelimited_simple (self):
		return '\t'.join (map (self.getAttr, recordSchema))
		# return '\t'.join (self.recId, self.title, self.collection, self.status)

	def asTabDelimited (self):
		person = self.getMatchingPerson()
		schema = recordSchema + personSchema
		basefields = map (self.getAttr, recordSchema)
		personfields = map (lambda x:self.getAttr(x, person), personSchema)
		return '\t'.join (basefields + personfields)
		

	def report (self):
		print "%s - %s" % (self.recId, self.author.lastname)
		


