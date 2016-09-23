import time
import MySQLdb
from UserDict import UserDict

class TableRow (UserDict):

	"""
	Provide field-addressible wrapper for table row (search result)
		e.g., result['Title']
	
	"""

	def __init__ (self, row_data, schema):
		self.schema = schema
		UserDict.__init__ (self,{})

		for index in range(len(self.schema)):
			self[self.schema[index]] = row_data[index]


class GenericDB:
	
	def __init__ (self, host=None, user=None, password=None, db=None):
		
		self.host = host or self.host
		self.user = user or self.user
		self.password = password or self.password
		self.db = db or self.db
		
		self.connection = self.getConnection()
		
	def getConnection (self):
		return MySQLdb.connect(host=self.host, user=self.user, passwd=self.password, db=self.db)
		
	def getCursor (self):
		return self.connection.cursor()
		
	def doEmptyTable (self, table):
		"""
		TRUNCATE TABLE `table_name`  
		"""
		cursor = self.getCursor()
		query = "TRUNCATE TABLE `%s`" % table
		cursor.execute (query)
		
	def getSchema (self, table):
		"""
		returns a list of fieldnames
		"""
		cursor = self.getCursor()
		# table = "idmapCollection"
		query = "DESCRIBE %s" % table
		schema = []
		cursor.execute (query)
		for row in cursor.fetchall():
			schema.append( row[0] )
		return schema
		
	def doSelect (self, query):
		"""
		example query:
			SELECT 
		returns a list of results (the fields specified in SELECT) that match query
		"""
		cursor = self.getCursor()
		cursor.execute (query)
		# for row in cursor.fetchall():
		#	print row
		return cursor.fetchall()
		
	def doInsert (self, query):
		cursor = self.getCursor()
		cursor.execute(query)

		
if __name__ == "__main__":
	# print WebTestDB().doCount(None)
	db = HrsDB()
	for field in db.getSchema():
		print field

