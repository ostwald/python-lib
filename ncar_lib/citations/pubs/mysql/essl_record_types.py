"""
classes to handle records from various tables of the PUBs data base
"""

from AbstractDB import SQLRec

class PubnameRec (SQLRec):
	pass
	
class PublisherRec (SQLRec):
	pass
	
class AuthorRec (SQLRec):
	"""
	exports: 'lastname', 'firstname', 'middlename', 'person_id', 'authororder', 'upid', 'pub_id'
	"""
	def __init__ (self, data):
		SQLRec.__init__ (self, data)
		for attr in ['lastname', 'firstname', 'middlename', 'person_id', 'authororder', 'upid', 'pub_id']:
			setattr (self, attr, self[attr] or "")
			
	def getFullName (self):
		fullname = self.lastname
		if self.firstname:
			fullname = "%s, %s" % (fullname, self.firstname)
		if self.middlename:
			fullname = "%s %s" % (fullname, self.middlename)
		return fullname
			
	def __cmp__ (self, other):
		return cmp(self.getFullName(), other.getFullName())
	
class PublicationRec (SQLRec):
	pass
	
class PersonRec (SQLRec):
	"""
	Record from the essl_person.person table.
	exports: 'lastname', 'firstname', 'middlename', 'suffix', 'person_id', 'upid'
	"""
	def __init__ (self, data):
		SQLRec.__init__ (self, data)
		for attr in ['lastname', 'firstname', 'middlename', 'suffix', 'person_id', 'upid']:
			setattr (self, attr, self[attr] or "")
			
	def __repr__ (self):
		return "%s -- %s, %s (upid: %s)" % (self.person_id, self.lastname, self.firstname, self.upid)
		
	def __cmp__ (self, other):
		return cmp (self.person_id, other.person_id)
