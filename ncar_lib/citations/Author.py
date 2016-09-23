class Author:
	"""
	A Citation author that can represent itself as an Element for inclusion in a Citation record
	"""
	def __init__ (self, lastname, firstname=None, middlename=None, suffix=None, 
				  authororder=None, person_id=None, upid=None):
		self.lastName = lastname
		self.firstName = firstname or ""
		self.middleName = middlename or ""
		self.suffix = suffix or ""
		self.authororder = authororder or ""
		self.person_id = person_id or ""
		self.upid = upid or ""
		
	def __repr__ (self):
		s = self.lastName
		if self.firstName or self.middleName:
			s = s + ","
		if self.firstName:
			s = "%s %s." % (s, self.firstName)
		if self.middleName:
			s = "%s %s." % (s, self.middleName)
		if self.authororder:
			s = "%s (%d)" % (s, self.authororder)
		return s
		
class AuthorList:
	"""
	generate a list of Author recs for the given record
	"""
	
	pass
		
class WOSAuthor (Author):
	
	def __init__ (self, lastname=None, firstname=None, middlename=None, authororder=None):
		Author.__init__ (self, lastname=lastname, firstname=firstname, middlename=middlename, suffix=None, 
						 authororder=authororder, person_id=None, upid=None)
	
