from xls import XslWorksheet, WorksheetEntry

from UserDict import UserDict
from UserList import UserList

path = 'EsslPeopleDBdump.txt'

class EsslPeopleSpreadsheet (XslWorksheet):

	linesep = "\n"
	
	def __init__ (self, path):
		XslWorksheet.__init__ (self, entry_class=EsslPersonEntry)
		self.read (path)
			
class EsslPersonEntry (WorksheetEntry):
	"""
	all schema fields are exposed as attributes:
		person_id, lastname, firstname, middlename, nickname, prefix, title, suffix, upid
	"""
		
	def __init__ (self, data, schema):
		WorksheetEntry.__init__ (self, data, schema)
		for field in self.schema:
			setattr (self, field, self[field])

	def getFullName(self):
		"""
		contruct a full name (for display, not comparison)
		"""
		name = self.lastname
		if self.firstname or self.middlename:
			name = name + ", "
			if self.firstname:
				name = name + self.firstname
				if len(self.firstname) == 1:
					name = name + '.'
				if self.middlename:
					name = name + " " + self.middlename
					if len(self.middlename) == 1:
						name = name  + "."
		return name
	
	def __repr__ (self):
		return '%s - %s (%s)' % (self.person_id, self.getFullName(), self.upid)
			
if __name__ == '__main__':
	people = EsslPeopleSpreadsheet (path)
	print 'schema: %s' % people.schema
	print "%d recs read" % len(people)
	for rec in people.data[0:50]:
		print rec
	
		
