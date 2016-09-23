"""
Connects to HR PeopleDB database (same data the PEOPLE REST SERVICE)
"""
from AbstractDB import AbstractDB, SQLRec, fuzzyTerm

class PeopleDBRec (SQLRec):
	"""
	assign an attribute for each record field
	"""
	
	def __init__ (self, data):
		SQLRec.__init__ (self, data)
		if self.schema:
			for field in self.schema:
				setattr (self, field, self[field])

class OrganizationRec (PeopleDBRec):	
	def __repr__ (self):
		return "%s (%s)" % (self.full_name, self.acronym)
				
class PersonRec (PeopleDBRec):
	"""
	A Person Record from the People DataBase
	exposes attributes:
		'upid', 'name_last', 'name_first', 'name_middle', 'name_suffix', 
		'nickname', 'name_last_alt', 'email', 'phone', 'phone_alt', 'active'
	"""

	
	def __repr__ (self):
		baseName = "%s %s, %s " % (self.upid, self.name_last, self.name_first)
		if (self.name_middle):
			baseName = "%s %s." % (baseName, self.name_middle)
		return baseName

class PeopleDB (AbstractDB):
	
	host = "merapisql.ucar.edu"
	user = "ostwald"
	password = "Jbjbjatw2009"
	db = "people"
	
	def __init__ (self, host=None, user=None, password=None, db=None):
		
		"""
		establishes connection with PUBs DB and initializes schemas for each of the
		tables that will be accessed
		"""
		AbstractDB.__init__ (self)
		PersonRec.schema = self.getSchema ("person")
		OrganizationRec.schema = self.getSchema ("organization")
		
	def getPeople (self, start=0, end=30000, where=None):
		"""
		returns list of PersonRecs corresponding to specified
		- rows of the database (start, end), and 
		- where clause, e.g., "pubstatus = 'published' AND class = 'refereed'"
		"""
		rows = self.getRows ("person", start, end, where)
		return map (PersonRec, rows)
		
	def getPerson (self, upid):
		"""
		return PersonRec for specified pub_id
		"""
		data = self.getRecordFromKey ('upid', upid, 'person')
		if data:
			return PersonRec (data)

	def getOrganizations (self, start=0, end=30000, where=None):
		"""
		returns list of OrganizationRecs corresponding to specified
		- rows of the database (start, end), and 
		- where clause, e.g., "pubstatus = 'published' AND class = 'refereed'"
		"""
		rows = self.getRows ("organization", start, end, where)
		return map (OrganizationRec, rows)
			
	def getUpid (self, upid):
		"""
		obtain the upid for this person
		"""
		person = self.getPerson (upid)
		if person:
			return person.upid
			
	def fuzzySearch (self, name_last=None, name_first=None, name_middle=None):
		where = ""
		if name_last is not None:
			where = where + " `name_last` LIKE '%s'" % fuzzyTerm(name_last)
			conjunction = " and"
		if name_first is not None:
			where = where + "%s `name_first` LIKE '%s'" % (conjunction, fuzzyTerm(name_first))
			conjunction = " and "
		if name_middle is not None:
			where = where + "%s `name_middle` LIKE '%s'" % (conjunction, fuzzyTerm(name_middle))
		# print "where: ", where
		return self.getPeople (where = where)

	def pubsSearch (self, name_last=None, name_first=None, name_middle=None):
		where = ""
		if name_last is not None:
			where = where + " `name_last` = '%s'" % name_last
			conjunction = " and"
		if name_first is not None:
			where = where + "%s `name_first` LIKE '%s'" % (conjunction, name_first+"%")
			conjunction = " and "
		if name_middle is not None:
			where = where + "%s `name_middle` LIKE '%s'" % (conjunction, name_middle+'%')
		# print "where: ", where
		return self.getPeople (where = where)
		
	def search (self, name_last=None, name_first=None, name_middle=None):
		where = ""
		conjunction = ""
		if name_last is not None:
			where = where + " `name_last` = '%s'" % (name_last)
			conjunction = " and"
		if name_first is not None:
			where = where + "%s `name_first` = '%s'" % (conjunction, name_first)
			conjunction = " and "
		if name_middle is not None:
			where = where + "%s `name_middle` = '%s'" % (conjunction, name_middle)
		# print "where: ", where
		return self.getPeople (where = where)		
			
def doCountTester ():		
	db = PeopleDB()
	query = "FROM publication WHERE pubstatus = 'published' AND class = 'refereed'"
	n = db.doCount (query)
	print 'there are %d records' % n
	
def batchTester ():
	db = PeopleDB()
	people = db.getPeople(0,20)
	people.sort()
	print 'there are %d people' % len(people)
	for person in people:
		print person

def whereTester ():
	db = PeopleDB()
	where = "pubstatus = 'published'"
	people = db.getPeople(where=where)
	print 'there are %d people' % len(people)

		
def recordTester ():
	db = PeopleDB() 
	upid = '8888' # '103397'
	person = db.getPerson (upid)
	if person:
		print person
	else:
		print "nothing found for upid = '%s'" % upid	
		
def searchTester ():
	db = PeopleDB()
	name_last = "Randall" # "ostwald"
	name_first =  'D' # "jonathan"
	name_middle = 'A' # "l"
	print "\nsearching for name_last: '%s', name_first: '%s', name_middle: '%s'\n" % \
		(name_last, name_first, name_middle)
	people = db.pubsSearch (name_last=name_last, name_first=name_first, name_middle=name_middle)
	for person in people:
		print person
		
if __name__ == "__main__":
	# batchTester()
	recordTester()
	# whereTester()
	# doCountTester()
	# searchTester()


		
