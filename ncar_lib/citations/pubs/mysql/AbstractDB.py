"""
Connects to essl_publications and extracts records from various Tables
"""
import MySQLdb

INFINITY = 100000

class AbstractDB:
	
	host = ""
	user = ""
	password = ""
	db = ""
	
	def __init__ (self, host=None, user=None, password=None, db=None):
		
		"""
		establishes connection with PUBs DB and initializes schemas for each of the
		tables that will be accessed
		"""
		
		self.host = host or self.host
		self.user = user or self.user
		self.password = password or self.password
		self.db = db or self.db
		
		self.connection = MySQLdb.connect( host=self.host, user=self.user, passwd=self.password, db=self.db)
		
	def _getCursor (self):
		return self.connection.cursor()
		
	def getSchema (self, table):
		"""
		returns schema as a list of field names for specified table (e.g., "publication")
		"""
		cursor = self._getCursor()
		query = "DESCRIBE %s" % table
		schema = []
		cursor.execute (query)
		for row in cursor.fetchall():
			schema.append( row[0] )
		return schema
		
	def doSelect (self, query):
		"""
		returns result of specified select query as list of results
		"""
		# print "query", query
		cursor = self._getCursor()
		cursor.execute (query)
		return cursor.fetchall()
	
	def doCount (self, query):
		cursor = self._getCursor()
		cursor.execute ("select count(*) %s" % query)
		row = cursor.fetchone()
		if row:
			return int(row[0])

	def getRows (self, table, start=None, end=None, where=None):
		"""
		general purpose method to get specified rows from specified table
		"""
		end = end or INFINITY
		start = start or 0
		queryStr = queryStr = "SELECT * FROM %s" % table
		if where:
			queryStr = "%s WHERE %s" % (queryStr, where)
		queryStr = queryStr + " LIMIT %d, %d" % (start, end)
		return self.doSelect (queryStr)
			
	def getRecordFromKey (self, field, value, table):
		"""
		returns the data from the specifid table having specified value for specified field.
		- should be at most ONE record for this keyfield and keyvalue. an Exception is raised
		if there is more than one record found).
		"""
		queryStr = "SELECT * FROM %s WHERE %s='%s'" % (table, field, value)
		rows = self.doSelect (queryStr)
		if len(rows) > 1:
			raise Exception, "More than one rec found when only one was expeted"
		if len(rows) == 0:
			return None
		return rows[0]

class SQLRec:
	"""
	
	generic class representing a record from a database.
	provides mapping interface enabling access of field values by field name
	- schema - list of field names for the tables containing the different kind of records
	- data - list of field values in schema order
	
	NOTE: schema must be explicitly set PRIOR to accessing the contents via __getitem__.
	E.g., SQLRecClass.schema = dbInstance.getSchema (tablename)
	"""
	schema = None
	
	def __init__ (self, data):
		self.data = data
		
	def __repr__ (self):
		return str(self.data)
		
	def __getitem__ (self, attr):
		"""
		mapping interface enabling access of field values by field name.
		raises exception if attr is not contained in schema
		"""
		if attr in self.schema:
			return self.data[self.schema.index(attr)]
		raise KeyError, "field ('%s') is not defined for %s" % (attr, self.__class__.__name__)
	
def fuzzyTerm (term):
	"""
	wildcard provided to select on substring
	"""
	return '%' + term + '%'
