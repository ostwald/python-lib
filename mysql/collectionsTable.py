import string
import sys
import time
from UserDict import UserDict
from IdmapDB import getDBs
import datetime

class Collections (UserDict):

	"""
	wrapper for an idmapCollection table
	"""

	schema = ["collKey", "numResources", "numWarnings", "collCheckDate"]
	query = """SELECT %s
	           FROM idmapCollection
			   WHERE collActive=%d""" % (string.join (schema, ', '), 1)

	def __init__ (self, db):
		self.db = db
		rows = db.doSelect (self.query)
		UserDict.__init__ (self)
		# print len(rows), " found"

		for row in rows:
			rec = {}
			for index in range(len(self.schema)):
				rec[self.schema[index]] = row[index]
			self[rec["collKey"]] = rec

	def keys(self):
		keys = self.data.keys()
		keys.sort()
		return keys

	def getCollCheckDate (self, coll):
		return  self[coll]['collCheckDate']

def padString (s, length):
	out = str(s)
	if length > len(out):
		for i in range(length - len(out)):
			out = ' ' + out
	return out
		
class Report:
	
	field = "nofield"
	columnwidth = 10
	
	def __init__ (self, collList=None, dbs=None):
		
		self.dbs = dbs or getDBs()
		self.tables = map (Collections, self.dbs)
		
		self.collList = collList or (self.tables and self.tables[0].keys())
		if not self.collList:
			msg = "ERROR: collections could not be computed" + \
				  "\n- most likely this is because no databases could be instantiated"
			raise msg
			
		if type(self.collList) == type (""):
			self.collList = [self.collList]
			
		self.report()
	
	def report (self):
		print "%s report - %s\n" % (self.field, time.asctime())
	
		# make a list of Collections tables (one for each db)
		#print "%d tables" % len(tables)
		
		print "%-15s" % "Collection",
		for table in self.tables:
			# print "%(-vwidth)s" % table.db.name,
			print "%s" % self.padVal(table.db.name) ,
		print ""
		print "%s" % ('-')*(15 + 3 + (len(self.tables) * self.columnwidth))
	
		for key in self.collList:
			print "%-15s" % (key),
			for table in self.tables:
				try:
					value = self.getValue (table, key)
				except:
					# print sys.exc_info()[0], sys.exc_info()[1]
					# sys.exit()
					value = "??"
				print "%s" % self.padVal(value) ,
			print ""

	def getValue (self, table, coll):
		return table[coll][self.field]

	def padVal (self, s):
		out = str(s)
		if self.columnwidth > len(out):
			for i in range(self.columnwidth - len(out)):
				out = ' ' + out
		return out
		
class WarningsReport (Report):
	field = "numWarnings"
	
class ProgressReport (Report):
	field = "collCheckDate"
	columnwidth = 13

	def getValue (self, table, coll):
		val = Report.getValue(self, table, coll)
		# val is of type datetime.datetime (whatever that means)

		if val.date() == datetime.datetime.now().date():
			return "DONE"
		else:
			return val.date()
			# return " ... "
		
def tester ():
	c = Collections (db)
	print len (c), " collections read"
	for key in c.keys():
		print key, c[key]["numWarnings"]
		
if __name__ == "__main__":
	WarningsReport()
