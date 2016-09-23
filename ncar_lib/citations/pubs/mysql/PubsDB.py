"""
Connects to essl_publications and extracts records from various Tables
"""
import sys
from AbstractDB import AbstractDB
from essl_record_types import PublicationRec, PubnameRec, PublisherRec, AuthorRec
from EsslPeopleDB import EsslPeopleDB
from PeopleDB import PeopleDB
from ncar_lib.citations.pubs.author_data import AuthorData

errors = []

class PubsDB (AbstractDB):
	"""
	Provides methods to extract records from the various tables in the
	PUBS database
	"""	
	
	# host = "mysql.ucar.edu"
	# user = "rduser"
	# password = "rd.user"
	# db = "essl_publications"
	
	host = "merapisql.ucar.edu"
	user = "ostwald"
	password = "Jbjbjatw2009"
	db = "essl_publications"
	
	def __init__ (self, host=None, user=None, password=None, db=None):
		
		"""
		establishes connection with PUBs DB and initializes schemas for each of the
		tables that will be accessed
		"""
		AbstractDB.__init__ (self, host, user, password, db)
		
		self.essl_peopleDB = EsslPeopleDB()
		self.peopleDB = PeopleDB()
		
		PublicationRec.schema = self.getSchema ("publication")
		PubnameRec.schema = self.getSchema ("pubname")
		PublisherRec.schema = self.getSchema ("publisher")
		AuthorRec.schema = self.getSchema ("author")
		
	def getPubs (self, start=None, end=None, where=None):
		"""
		returns list of PublicationRecs corresponding to specified
		- rows of the database (start, end), and 
		- where clause, e.g., "pubstatus = 'published' AND class = 'refereed'"
		"""
		rows = self.getRows ("publication", start, end, where)
		return map (PublicationRec, rows)
		
	def getPub (self, pub_id):
		"""
		return PublicationRec for specified pub_id
		"""
		data = self.getRecordFromKey ('pub_id', pub_id, 'publication')
		if data:
			return PublicationRec (data)
		
	def getPublisher (self, publisher_id):
		"""
		return name of publisher for specified publisher_id
		"""
		rec = self.getPublisherRec (publisher_id)
		if rec:
			return rec['publisher']
		
	def getPublisherRec (self, publisher_id):
		"""
		return PublisherRec for specified publisher_id
		"""
		data = self.getRecordFromKey ('publisher_id', publisher_id, 'publisher')
		if data:
			return PublisherRec (data)
		
	def getPubname (self, pubname_id):
		rec = self.getPubnameRec (pubname_id)
		if rec:
			return rec['pubname']
		
	def getPubnameRec (self, pubname_id):
		"""
		should be at most ONE record per pubname_id
		"""
		data = self.getRecordFromKey ('pubname_id', pubname_id, 'pubname')
		if data:
			return PubnameRec (data)
	
	def getAuthorRecs (self, pub_id):
		"""
		returns list of AuthorRecs for the authors associated with
		specified publication (pub_id)
		"""
		queryStr = "SELECT * FROM author WHERE pub_id='%s'" % pub_id
		return map (AuthorRec, self.doSelect (queryStr))
		
def fleshRecord (db, pub):
	"""
	debugging method to show all information associated with a given
	pub record by extracting information from appropriate PUBs DB tables
	"""
	
	import sys
	showpubfield = lambda a: sys.stdout.write ('%s: %s\n' % (a, pub[a]))
	
	print '\n'
	showpubfield("pub_id")
	showpubfield("title")
	showpubfield("year")
	showpubfield("editor")
	
	print 'pubname:', db.getPubname (pub['pubname_id'])
	print 'publisher:', db.getPublisher (pub['publisher_id'])
	
	showpubfield("volume")
	showpubfield("pages")
	showpubfield("doi")
	showpubfield("url")
	showpubfield("pubstatus")
	showpubfield("statusdate")
	showpubfield("meetstartdate")
	showpubfield("meetenddate")
	showpubfield("class")
	showpubfield("type")
	showpubfield("meetcity")
	showpubfield("meetstateprov")
	showpubfield("meetcountrycode")
	showpubfield("collaboration")
	showpubfield("meetdate")
	showAuthors (db, pub)
	
		
def showAuthors (db, pub):
	authorRecs = db.getAuthorRecs(pub['pub_id'])
	for authorRec in authorRecs:
		print AuthorData (db, authorRec)	
	
def doCountTester ():		
	db = PubsDB()
	# query = "FROM publication WHERE pubstatus = 'published' AND class = 'refereed'"
	
	# all records that didn't meet the published AND refereed test
	query = "FROM publication WHERE pubstatus != 'published' OR class != 'refereed'"
	n = db.doCount (query)
	print 'there are %d records' % n
	
def batchTester ():
	db = PubsDB()
	pubs = db.getPubs(0,200)
	print 'there are %d pubs' % len(pubs)
	for pub in pubs:
		# fleshRecord (db, pub)
		# print pub['pub_id'], pub['publisher_id']
		
		showAuthors (db, pub)

	if errors:
		print "\n ERRORS"
		for i in errors:
			print '- %s' % i

def whereTester ():
	db = PubsDB()
	where = "pubstatus = 'published'"
	pubs = db.getPubs(where=where)
	print 'there are %d pubs' % len(pubs)

		
def recordTester ():
	db = PubsDB() 
	pub_id = '200981' # '103397'
	pub = db.getPub (pub_id)
	if pub:
		fleshRecord (db, pub)
	else:
		print "nothing found for pub_id = '%s'" % pub_id	
		
if __name__ == "__main__":
	# batchTester()
	# recordTester()
	# whereTester()
	doCountTester()


		
