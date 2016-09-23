"""
connector for local archon database
"""
from mysql import GenericDB, TableRow
import MySQLdb

class ArchonDB (GenericDB):
	host = "localhost"
	user = "root"
	password = "lydick"
	db = "archon"
	name = "WhatEver"
	
	def __init__ (self):
		GenericDB.__init__ (self, host=self.host, user=self.user, password=self.password, db=self.db)		
	

	
if __name__ == "__main__":
	pass
