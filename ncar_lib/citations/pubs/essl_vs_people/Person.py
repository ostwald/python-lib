from ncar_lib.citations.pubs.mysql import PeopleDB, PersonRec

class Person:
	"""
	A Citation author that can represent itself as an Element for inclusion in a Citation record
	"""
	
	attrs = ['lastname', 'firstname', 'middlename', 'suffix', 'person_id', 'upid']
	
	def __init__ (self, **args):
		for attr in self.attrs:
			setattr (self, attr, "")
			
		for key in args:
			if not hasattr (self, key):
				raise KeyError, "Unexpected parameter: %s" % key
			setattr (self, key, args[key])

	def __repr__ (self):
		s = self.lastname
		if self.firstname or self.middlename:
			s = s + ","
		if self.firstname:
			s = "%s %s." % (s, self.firstname)
		if self.middlename:
			s = "%s %s." % (s, self.middlename)
		if self.suffix:
			s = "%s (%d)" % (s, self.suffix)
		return s
	
	
		
	def compare (self):
		if not self.upid:
			raise KeyError, "upid not defined"
		other = PeoplePerson(self.upid)
		return self.compare_fn(other)
		
	def compare_lastnames(self, other):
		return self.doCompare (other, ['lastname', 'firstname'])
		
	def doCompare (self, other, fields=None):
		diff = []
		fields = fields or ['lastname']
		for field in fields:
			myval = getattr(self, field)
			otherval = getattr (other, field)
			if myval != otherval:
				diff.append ((field, myval, otherval))
		return diff
		
	compare_fn = compare_lastnames
		
class EsslPerson (Person):
		
	"""
	Uses data from EsslPersonEntry to instantiate
	"""
	def __init__ (self, esslPersonEntry):
		Person.__init__ (self, lastname = esslPersonEntry.lastname,
							   firstname = esslPersonEntry.firstname,
							   middlename = esslPersonEntry.middlename,
							   suffix = esslPersonEntry.suffix,
							   upid = esslPersonEntry.upid,
							   person_id = esslPersonEntry.person_id)	
	
class PeoplePerson (Person):
	"""
	Retrieves data from PeopleDB for record associated with upid
	"""
	def __init__ (self, upid):
		peopleDBRec = PeopleDB().getPerson (upid)
		if not peopleDBRec:
			raise KeyError, "PeopleDB entry not found for %s" % upid
		Person.__init__ (self, lastname = peopleDBRec.name_last,
							   firstname = peopleDBRec.name_first,
							   middlename = peopleDBRec.name_middle,
							   suffix = peopleDBRec.name_suffix,
							   upid = peopleDBRec.upid)			   
		
if __name__ == '__main__':
	print PeoplePerson('10')
	
