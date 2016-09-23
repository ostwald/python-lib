class Author:
	"""
	Represntation of the person we are looking for as we search OpenSky
	exposes:
		firstname
		middlename
		lastname
		first (initial)
		middle (initial)
		upid
	"""
	
	verbose = 0
	
	def __init__ (self, lastname, firstname, middlename=None, upid=None):
		self.firstname = firstname
		self.middlename = middlename
		self.lastname = lastname
		self.upid = upid
		self.first = self.firstname[0]
		self.middle = self.middlename and self.middlename[0] or None
		
	def matchesPersonName (self, person):
		"""
		person is a MetadataAuthor instance (first and last are initials)
		returns true if all data commonly available in provided osmAthor and this author match
		-	e.g., if osmAuthor doesn't have middleName, we don't compare on this field
		
		"""
		self.log ("\nAuthor.matchesPersonName() - comparing Author: %s with person: %s" % (self, person))
		if self.lastname != person.last: 
			self.log ('  last name mismatch')
			return 0
		if person.first and self.first and self.first[0] != person.first:
			self.log ('  first name mismatch')
			return 0
		if person.middle and self.middle and self.middle[0] != person.middle:
			self.log ('  middle name mismatch' )
			return 0
		self.log( '  match')
		return 1
		
	def log (self, s):
		if self.verbose:
			print s
		
	def __repr__ (self):
		s = u""
		if self.firstname:
			s = self.firstname
		if self.middlename:
			s += " " + self.middlename
		return s +  " " + self.lastname

