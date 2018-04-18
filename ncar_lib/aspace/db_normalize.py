# -*- coding: utf-8 -*-

from mysql import GenericDB, TableRow
import MySQLdb
from UserDict import UserDict
import codecs

class ArchivesSpaceDB (GenericDB):
	
	host = "aspace.ucar.edu"
	user = "archivesspace"
	password = "ecapssevihcra"
	db = "archivesspace"
	
	def __init__ (self, host=None, user=None, password=None, db=None):
		# GenericDB.__init__ (self, host=self.host, user=self.user, password=self.password, db=self.db)
		GenericDB.__init__ (self)
		
	def getConnection (self):
		return MySQLdb.connect(host=self.host, user=self.user, passwd=self.password, db=self.db)
		
normalize_mappings = [
	# ['\xe2\x80\x9a\xc3\x84\xc3\xba','\xe2\x80\x9c'],  # left-double quotes
	# ['\xe2\x80\x9a\xc3\x84\xc3\xb9','\xe2\x80\x9d'],   # right-double quotes
	
	# ["'",u"\u2019".encode('utf8')],
	# ['\xe2\x80\x9a\xc3\x84\xc3\xb4',u"\u2019".encode('utf8')]
	
	['\xe2\x80\x9a\xc3\x84\xc3\xba','"'],  	 # left-double quotes -> straight
	['\xe2\x80\x9a\xc3\x84\xc3\xb9','"'],    # right-double quotes -> straight
	[' \xe2\x80\x9a\xc3\x84\xc3\xac',':'],   # – - was a dash, turn into colon!
	["'", "\\'"],
	['\xe2\x80\x9a\xc3\x84\xc3\xb4',"\\'"],  # apos (’s)
	['\xe2\x80\x9a\xc3\x84\xc2\xb6', ''],    # unknown: … - only 3 of these. eliminate them
	# ['\xe2\x80\x9a', ''],					 # non-displaying junk - eliminate
]
		
class DigitalObjects (UserDict):
	"""
	wrapper for table
	"""
	table = 'archival_object'
	schema = ["id", "title", "display_string"]
		   
	def __init__ (self, db):
		self.data = {}
		self.db = db
		self.table_schema = self.db.getSchema(self.table)
	
	def get_results (self, query):
		return self.db.doSelect (query)
	
	def show_results(self, rows):
		print len(rows), " found"
		for row in rows:
			print row
	
	def to_table_row (self, record, schema=None):
		"""
		convert raw data in to TableRow instance
		"""
		if schema is None:
			schema = self.table_schema
		return TableRow(record, schema)
	
	def normalize_record (self, id):
		"""
		fix the title and the xxx fields
		"""
		title = self.get_record_title (id)
		
		normalized_title = normalize_str(title)
		
		print 'NORM: {}'.format(normalized_title)
		
		update_title_query = """UPDATE archivesspace.%s SET display_string='%s' 
		  WHERE id=%s""" % (self.table, normalized_title, id)
		  
		print update_title_query
		return
		
		self.db.doUpdate(update_title_query)
	
	def get_record(self, id):
		query = """SELECT %s
		   FROM %s
		   WHERE id=%s""" % (','.join (self.schema), self.table, id)
		results = self.get_results(query)
		if len(results) > 1:
			raise Exception, 'Get record (%s) got too many results (%d)' % (id, len(results))
		if len(results) == 0:
			return None
		return results[0]
			
	def search (self, search_str, match="anywhere"):
		if match == 'anywhere':
			search_str = '%'+search_str+'%'
		elif match == 'start':
			search_str = search_str+'%'
		elif match == 'end':
			search_str = '%'+search_str
		elif match == 'exact':
			pass
		query = """SELECT %s
	           FROM %s
			   WHERE title LIKE '%s'""" % (','.join (self.schema), self.table, search_str)		
		return self.get_results(query)
		
		
	def get_record_title (self, id):
		record = self.get_record(id)
		if record is not None:
			return record[self.schema.index('title')]
		else:
			print 'Record NOT FOUND for %s' % id
		
	def make_normalize_script (self, record):
		query = "UPDATE archivesspace.%s SET title = '%s' WHERE id=%s;" %  \
			(self.table, normalize_str(record['title']), record['id'])
		query += "\nUPDATE archivesspace.%s SET display_string = '%s' WHERE id=%s;" %  \
			(self.table, normalize_str(record['display_string']), record['id'])
		return query
		
def normalize_str (str):
	for mapping in normalize_mappings:
		str = str.replace(mapping[0], mapping[1])
	return str.strip()
		
def make_update_script (table):
	dowrites = 1
	
	# search_str = '\xe2\x80\x9a\xc3\x84\xc3\xb4' # apos (’s)
	# search_str = '\xe2\x80\x9a\xc3\x84\xc3\xac' # – - converted to colon
	
	# search_str ='\xe2\x80\x9a\xc3\x84\xc3\xba' # 135 done
	
	search_str = '\xe2\x80\x9a' # 210
	
	# search_str = '\xe2\x80\x9a\xc3\x84\xc2\xb6' # unknown: … there are 3 of these and it looks like they
												# should simply be eliminated ....
	
	results = table.search(search_str)
	# print results[0]   # see raw sample
	# table.show_results (results)
	records = map (lambda x: table.to_table_row (x, table.schema), results)
	print '{} records found'.format(len(records))
	sql_lines = [];add = sql_lines.append
	for rec in records:
		# print rec['id'], rec['display_string']
		# print table.make_normalize_script(rec)
		add (table.make_normalize_script(rec))
		# break
	sql = '\n'.join (sql_lines)
	print sql
	
	if dowrites:
		sql_path = '/Users/ostwald/Documents/Archivesspace_migration/data_cleanup_9-2017/normalize.sql'
		if 0:
			fp = codecs.open(sql_path, 'w', 'utf-8')
			fp.write(sql.decode('utf-8'))
		if 1:
			fp = open(sql_path, 'w')
			fp.write(sql)
		fp.close
		print 'wrote to ', sql_path
		
if __name__ == "__main__":
	# print WebTestDB().doCount(None)
	db = ArchivesSpaceDB()
	objs = DigitalObjects (db)
	
	# objs.normalize_record(3266)
	
	make_update_script (objs)
	
	if 0:
		results = objs.search ('\xe2\x80\x9a\xc3\x84\xc3\xba') # 140
		# results = table.search ('\xe2\x80\x9a') # 210
		# table.show_results (results)
		for result in results:
			print result[0], result[1]
			print '   ', result

	
	if 1:
		# id = 12446 # …  
		id = 3047
		rec = objs.get_record(id)
		print rec
		title = objs.get_record_title(id)
		print 'title: {}'.format(title)
		print 'NORMALIZED: {}'.format(normalize_str(title))
		# print 'table schema: {}'.format(objs.table_schema)
	


