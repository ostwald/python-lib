"""
pubs_probe - tools for looking at specific records in specific PUBs databases
"""

from mysql import PubsDB

def getProductionDB ():
	host = "merapisql.ucar.edu"
	user = "ostwald"
	password = "Jbjbjatw2009"
	db = "essl_publications"
	
	return PubsDB (host, user, password, db)
	
def getHoldingDB ():
	host = "merapisql.ucar.edu"
	user = "rduser"
	password = "rd.user"
	db = "h_essl_publications"
	
	return PubsDB (host, user, password, db)
	
def getOldDB ():
	host = "sql.ucar.edu"
	user = "rduser"
	password = "rd.user"
	db = "essl_publications"
	
	return PubsDB (host, user, password, db)
	
class PubsProbe:
	
	dbs = ["PROD", "HOLDING", "OLD"]
	default_fields = ['pub_id', 'type', 'timestamp']

	def __init__ (self, db='PROD'):
		self.db = self.getPubsDB (db)
		
	def getPubsDB (self, db):
		if not db in self.dbs:
			raise KeyError, "Unrecognized Pubs database: '%s'" % db
		if db == 'PROD':
			return getProductionDB()
		elif db == 'HOLDING':
			return getHoldingDB()
		elif db == 'OLD':
			return getOldDB()
	
	def showRecord (self, rec, fields):
		s=[];add=s.append
		for field in fields:
			if field == 'pubname':
				add (self.db.getPubname (rec['pubname_id']))
			else:
				add (str(rec[field]))
		return ', '.join (s)
	
	def report (self, ids, fields=None):
		print "host: %s  database: %s\n" % (self.db.host, self.db.db)
		fields = fields or self.default_fields
		for id in ids:
			rec = self.db.getPub (id)
			if rec:
				print self.showRecord(rec, fields)
			else:
				print "%s - record not found" % id
		
def verifyPubTypes ():
	"""
	check the records for given ids - the types should all be 'journal'
	"""
	ids = [
		200217, 
		200877, 
		105081, 
		104509, 
		200878,
		103756, 
		100487,
		201237,
		201236,
		201218,
		201199,
		201186,
		200711,
		200614,
		104510,
		]
	for db in PubsProbe.dbs:
		probe = PubsProbe (db)
		print '\n%s' % db
		probe.report (ids)
	
def verifyPubName ():
	"""
	check the record - pubname should be 'Biogeochemistry'
	"""
	ids = ['103756']
	fields = ['pub_id', 'pubname', 'timestamp']
	
	for db in PubsProbe.dbs:
		probe = PubsProbe (db)
		print '\n%s' % db
		probe.report (ids, fields)
		
def verifyUrls ():
	"""
	check the record - pubname should be 'Biogeochemistry'
	"""
	ids = ['201111', '106652', '106468']
	fields = ['pub_id', 'url', 'timestamp']
	
	for db in PubsProbe.dbs:
		probe = PubsProbe (db)
		print '\n%s' % db
		probe.report (ids, fields)
		
if __name__ == "__main__":	
	verifyPubTypes()
	# verifyPubName()
	# verifyUrls ()
