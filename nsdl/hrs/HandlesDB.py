"""
Performs select from 'reference' handle database that contains timestamp info for all handles
"""
import time
from mysql import GenericDB
import MySQLdb

class HandlesDB (GenericDB):
	
	host = "nsdl-rs1.nsdldev.org"
	user = "rsadmin"
	password = "dls*mysql4us"
	db = "handle_save"
	
	def __init__ (self, host=None, user=None, password=None, db=None):
		# GenericDB.__init__ (self, host=self.host, user=self.user, password=self.password, db=self.db)
		GenericDB.__init__ (self)
		
	def getConnection (self):
		return MySQLdb.connect(host=self.host, user=self.user, passwd=self.password, db=self.db)
		
	def getTimestamp (self, handle):
		"""
		should get 1 or 0 result records. 
		the first field is the handle, the second is the timestamp (e.g., 1159807590L)
		"""
		selectStr = """SELECT `handle`,`timestamp` 
			FROM `handles` 
			WHERE `handle` = '%s' AND `idx` = '1'""" % handle
		results = self.doSelect (selectStr)
		if results:
			return results[0][1]
		
if __name__ == "__main__":
	# print WebTestDB().doCount(None)
	db = HandlesDB()
	
	foo = db.getTimestamp('2200/20061002124629267T')
	print foo, type(foo)

