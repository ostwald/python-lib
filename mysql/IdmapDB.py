
import MySQLdb

class IdmapDB:
	
	def __init__ (self, host=None, user=None, password=None, db=None):
		
		self.host = host or self.host
		self.user = user or self.user
		self.password = password or self.password
		self.db = db or self.db
		
		self.connection = MySQLdb.connect( host=host, user=user, passwd=password, db=db)
		
	def getCursor (self):
		return self.connection.cursor()
		
	def getSchema (self, table):
		cursor = self.getCursor()
		# table = "idmapCollection"
		query = "DESCRIBE %s" % table
		schema = []
		cursor.execute (query)
		for row in cursor.fetchall():
			schema.append( row[0] )
		return schema
		
	def doSelect (self, query):
		cursor = self.getCursor()
		cursor.execute (query)
		# for row in cursor.fetchall():
		#	print row
		return cursor.fetchall()
	
	def doCount (self, query):
		query = "from idmapMmd where primaryContent is NULL and collKey = 'dcc'"
		cursor = self.getCursor()
		cursor.execute ("select count(*) %s" % query)
		row = cursor.fetchone()
		if row:
			return int(row[0])

	def findDups (self, collKey, id):
		# get the idmapMmd rec for this record
		queryStr = "SELECT primaryUrl, primaryChecksum FROM idmapMmd " \
			  + " WHERE collKey = '%s' " \
			  + " AND id = '%s'"
		query = queryStr % (collKey, id)
		dbmat = self.doSelect (query)

		primaryUrl = None
		checksum = 0
		
		if len(dbmat) == 1:
			primaryUrl = dbmat[0][0]
			checksum = dbmat[0][1] or 0

		## must have both a primaryUrl and a checksum ...
		if not (primaryUrl and checksum):
			return []
		

		# find other recs with same checksum and primaryUrl
		queryStr = "SELECT collKey, id, primaryUrl, primaryChecksum FROM idmapMmd" \
				+ " WHERE ( primaryChecksum = '%d'" \
				+ " OR primaryUrl = '%s' )"
		query = queryStr % (checksum, primaryUrl)
		dbmat = self.doSelect (query)
		# print "%d records found" % len (dbmat)

		dups = []
		for rec in dbmat:
			if rec[1] != id:
				dups.append(Dup (rec))
		return dups

class Dup:

	def __init__ (self, tuple):
		self.collKey = tuple[0]
		self.id = tuple[1]
		self.primaryUrl = tuple[2]
		self.primaryChecksum = tuple[3]


def getRecs (db, collKey):
	queryStr = "SELECT id, primaryUrl FROM idmapMmd WHERE collKey='%s'" % collKey
	queryStr = queryStr + " LIMIT 1, 30"

	rows = db.doSelect (queryStr)
	# for row in rows:
		# print row[0], row[1]
	return rows
	
			
class WebTestDB (IdmapDB):
	host = "tmysql.ucar.edu"
	user = "idmap"
	password = "lhasa31"
	db = "IdMap"
	name = "WebTest"
	
	def __init__ (self):
		IdmapDB.__init__ (self, host=self.host, user=self.user, password=self.password, db=self.db)

class WebPubDB (IdmapDB):
	host = "mysql.ucar.edu"
	user = "idmap"
	password = "lhasa31"
	db = "IdMap"
	name = "WebPub"	
	
	def __init__ (self):
		IdmapDB.__init__ (self, host=self.host, user=self.user, password=self.password, db=self.db)
		
class BolideDB (IdmapDB):
	host = "lahar.dpc.ucar.edu"
	user = "idmap"
	password = "lhasa31"
	db = "IdMap_Live"
	name = "Bolide"	
	
	
	def __init__ (self):
		IdmapDB.__init__ (self, host=self.host, user=self.user, password=self.password, db=self.db)

def getDB (db):
	if db == 'bolide': return BolideDB()
	if db == 'webpub': return WebPubDB()
	if db == 'webtest': return WebTestDB()
		
def getDBs ():
	dbs = []
	dbclasses = ['webtest', 'webpub','bolide', ]
	for c in dbclasses:
		try:
			dbs.append (getDB (c))
		except:
			print "WARNING: unable to instantiate database (%s)" % c
	return dbs
		
if __name__ == "__main__":
	# print WebTestDB().doCount(None)
	id = "DLESE-000-000-001-001"
	db = BolideDB()
	collKey = "dcc"
	# db.findDups(collKey, id)
	recs = getRecs (db, collKey)
	for rec in recs:
		id = rec[0]
		dups = db.findDups (collKey, id)
		if (dups):
			print id
			for dup in dups:
				print "\t%s: %s (%s)" % (dup.id, dup.primaryUrl, dup.primaryChecksum)
