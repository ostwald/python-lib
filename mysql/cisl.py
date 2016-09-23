
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
		
	def doFind (self, query):
		cursor = self.getCursor()
		cursor.execute (query)
		for row in cursor.fetchall():
			print row
	
	def doCount (self, query):
		query = "from idmapMmd where primaryContent is NULL and collKey = 'dcc'"
		cursor = self.getCursor()
		cursor.execute ("select count(*) %s" % query)
		row = cursor.fetchone()
		if row:
			return int(row[0])
			
class WebTestDB (IdmapDB):
	host = "tmysql.ucar.edu"
	user = "idmap"
	password = "lhasa31"
	db = "IdMap"
	
	def __init__ (self):
		IdmapDB.__init__ (self, host=self.host, user=self.user, password=self.password, db=self.db)

class DLS (IdmapDB):
	host = "lahar.dpc.ucar.edu"
	user = "idmap"
	password = "lhasa31"
	db = "IdMap_Live"
	
	def __init__ (self):
		IdmapDB.__init__ (self, host=self.host, user=self.user, password=self.password, db=self.db)


if __name__ == "__main__":
	print WebTestDB().doCount(None)
