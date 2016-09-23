"""
Connects to essl_People database (NOT to be confused with the PEOPLE REST SERVICE and extracts 
records from various Tables
"""
from AbstractDB import AbstractDB
from essl_record_types import PersonRec

class EsslPeopleDB (AbstractDB):
	
	host = "mysql.ucar.edu"
	user = "rduser"
	password = "rd.user"
	db = "essl_people"
	
	def __init__ (self, host=None, user=None, password=None, db=None):
		
		"""
		establishes connection with PUBs DB and initializes schemas for each of the
		tables that will be accessed
		"""
		AbstractDB.__init__ (self)
		PersonRec.schema = self.getSchema ("person")
		
	def getPeople (self, start=0, end=10000, where=None):
		"""
		returns list of PersonRecs corresponding to specified
		- rows of the database (start, end), and 
		- where clause, e.g., "pubstatus = 'published' AND class = 'refereed'"
		"""
		rows = self.getRows ("person", start, end, where)
		return map (PersonRec, rows)
		
	def getPerson (self, person_id):
		"""
		return PersonRec for specified pub_id
		"""
		data = self.getRecordFromKey ('person_id', person_id, 'person')
		if data:
			return PersonRec (data)

	def getUpid (self, person_id):
		"""
		obtain the upid for this person
		"""
		person = self.getPerson (person_id)
		if person:
			return person.upid
			
	def getPersonByUpid (self, upid):
		"""
		return PersonRec for specified pub_id
		"""
		if not upid:
			return None
		data = self.getRecordFromKey ('upid', upid, 'person')
		if data:
			if len(data) > 1:
				raise KeyError, "more than one person found for %s" % upid
			return PersonRec (data)
			
def doCountTester ():		
	db = EsslPeopleDB()
	query = "FROM publication WHERE pubstatus = 'published' AND class = 'refereed'"
	n = db.doCount (query)
	print 'there are %d records' % n
	
def batchTester ():
	db = EsslPeopleDB()
	people = db.getPeople(0,20)
	people.sort()
	print 'there are %d people' % len(people)
	for person in people:
		print person

def whereTester ():
	db = EsslPeopleDB()
	where = "pubstatus = 'published'"
	people = db.getPeople(where=where)
	print 'there are %d people' % len(people)

		
def recordTester ():
	db = EsslPeopleDB() 
	person_id = '100448' # '103397'
	person = db.getPerson (person_id)
	if person:
		print person
	else:
		print "nothing found for person_id = '%s'" % person_id	
		
def upidTester ():
	db = EsslPeopleDB() 
	upid = '8888' # '103397'
	person = db.getPersonByUpid (upid)
	if person:
		print person
	else:
		print "nothing found for upid = '%s'" % upid	
		
def getDump():
	"""
	download a tab-delimited dump of the EsslPeople table
	"""
	db = EsslPeopleDB()
	recs = db.getPeople ()
	data = [];add=data.append
	add ('\t'.join (recs[0].schema))
	for rec in recs:
		normalized = map (lambda x:x or "", rec.data)
		add ('\t'.join (map (str, normalized)))
	fp = open ("EsslPeopleDBdump2.txt", 'w')
	fp.write ('\n'.join (data))
	fp.close()	
	
if __name__ == "__main__":
	# batchTester()
	# recordTester()
	# whereTester()
	# doCountTester()
	# upidTester()
	getDump()



		
