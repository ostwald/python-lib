
recordSchema = ['title', 'recId', 'collection', 'format', 'status', 'recordDate', 'publishedDate']

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

class ParResult:
	
	def __init__ (self, searchResult, parAuthor):
		self.searchResult = searchResult
		self.parAuthor = parAuthor
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
		
	def getMetadataAuthor (self):
		"""
		we are extracting fields from whatever getMatchingPerson returns
		"""
		raise Exception, 'getMetadataAuthor not yet implemented'
		
	def __repr__ (self):
		return "%s - collection: %s (%s)\n  %s" % (self.recId, self.collection, self.status, self.title)
		
	def asTabDelimited_simple (self):
		return '\t'.join (map (lambda x:getattr(self, x) or "", recordSchema))
		# return '\t'.join (self.recId, self.title, self.collection, self.status)

	def asTabDelimited (self):
		person = self.getMatchingPerson()
		schema = recordSchema + personSchema
		basefields = map (lambda x:getattr(self, x) or "", recordSchema)
		personfields = map (lambda x:getattr(person, x) or "", personSchema)
		return '\t'.join (basefields + personfields)
		

		


