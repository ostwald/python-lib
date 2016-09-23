"""
Functionality for populating HandleResolution mySQL database with NSDL handle-mapping info.

HrsDB - the class for interacting with the HRS Database on rs1
ResourceMappingTable - table in HrsDB containing resourceHandle, resourceUrl
MetadataMappingTable - table containing metadataHandle, partnerId, setspec
"""

import time
from mysql import GenericDB
from HandlesDB import HandlesDB
import MySQLdb

class HrsDB (GenericDB):
	
	host = "nsdl-rs1.nsdldev.org"
	user = "rsadmin"
	password = "dls*mysql4us"
	db = "handleResolution"
	
	def __init__ (self, host=None, user=None, password=None, db=None):
		# GenericDB.__init__ (self, host=self.host, user=self.user, password=self.password, db=self.db)
		GenericDB.__init__ (self)
		self.handlesDB = HandlesDB()
		
	def getConnection (self):
		return MySQLdb.connect(host=self.host, user=self.user, passwd=self.password, db=self.db)
		
class HrsDBTable:
			
	name = None
	
	def __init__ (self, db):
		self.db = db
		self.handlesDB = HandlesDB()
		
	def empty (self):
		"""
		 TRUNCATE TABLE `resource`
		"""
		self.db.doEmptyTable(self.name)
		
	def insert (self, *list, **args):
		raise Exception, "insert not implemented for %s" % self.__class__.__name__ 

class ResourceMappingTable(HrsDBTable):
	
	name = 'resource'
	
	def insert (self, handle, resource_url):
		"""
		INSERT INTO resource (
			`handle` ,
			`resource_url` ,
			`timestamp`
			)
		VALUES (
			'2200/934948T', 'http://google.com', '12345678'
			);
		"""
		
		if 0: # get timestamp from LHS DB
			timestamp = self.handlesDB.getTimestamp(handle)
			if timestamp is None:
				raise Exception, "handle not in master DB: %s" % handle
		else:
			timestamp = int (time.time())
			
		query = """INSERT INTO resource (
			`handle` ,
			`resource_url` ,
			`timestamp`
			)
		VALUES (
			'%s', '%s', '%d'
			);""" % (handle, resource_url, timestamp)
			
		self.db.doInsert(query)
		
class MetadataMappingTable(HrsDBTable):
	
	name = 'metadata'
	
	def insert (self, handle, partner_id, setspec):
		"""
		Example query:
		INSERT INTO metadata (
			`handle` ,
			`partner_id` ,
			`setspec` ,
			`timestamp`
			)
		VALUES (
			'2200/934948T', 'http://google.com', 'BEN', '12345678'
			);
		"""
		
		if 0: # get timestamp from LHS DB
			timestamp = self.handlesDB.getTimestamp(handle)
			if timestamp is None:
				raise Exception, "handle not in master DB: %s" % handle
		else:
			timestamp = int (time.time())
		
		query = """INSERT INTO metadata (
			`handle` ,
			`partner_id` ,
			`setspec` ,
			`timestamp`
			)
		VALUES (
			'%s', '%s', '%s', '%d'
			);""" % (handle, partner_id, setspec, timestamp)
			
		self.db.doInsert(query)

def resourcesTableTester ():
	resourcesTable = ResourceMappingTable (HrsDB())
	resourcesTable.insert ("2200/20061002124629267T", "http://fooberry")
	
if __name__ == "__main__":
	# print WebTestDB().doCount(None)
	metadataTable = MetadataMappingTable (HrsDB())
	metadataTable.insert ("2200/20101027210925545T", "partnerId:8373467230", 'setspec:BEN')

