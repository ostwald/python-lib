"""
API - getCollection (archon_db_coll_id) - returns ArchonDBCollection instance
"""
import os, sys, re
# from mysql import GenericDB, TableRow
# import MySQLdb
from archonDB import ArchonDB
from mysql import TableRow

class ArchonDBCollection ():
	"""
	exposes the following from archon database
	- collection (a TableRow instance) for collection record
	- title
	- items (list of TableRow instances)
	"""
	def __init__ (self, archon_db, coll_id):
		self.db = archon_db
		self.coll_id = coll_id
		self.collection = self.getCollectionRec()
		self.items = self.getContentItems()
		self.title = self.collection and self.collection['Title'] or None
			
	def getCollectionRec (self, schema=None):
		table_name = 'tblCollections_Collections'
		if schema is None:
			schema = self.db.getSchema(table_name)
			q_fields = '*'
		else:
			q_fields = ','.join(schema)
			
		queryStr = """SELECT %s 
					  FROM %s 
					  WHERE ID=%s;""" % (q_fields, table_name, self.coll_id)
		
		rows = self.db.doSelect (queryStr)
		if len(rows) > 0:
			return TableRow (rows[0], schema)
			
	def getContentItems (self, schema=None):
		"""
		gets all content items for this collection as a list
		of TableRow instances
		"""
		table_name = 'tblCollections_Content'
		if schema is None:
			schema = self.db.getSchema(table_name)
			q_fields = '*'
		else:
			q_fields = ','.join(schema)
	
		queryStr = """SELECT %s FROM %s 
					where CollectionId=%s;""" % (q_fields, table_name, self.coll_id)
					
		rows = self.db.doSelect (queryStr)
		results = []
		for row in rows:
			results.append (TableRow (row, schema))
		return results
		
	def getContentChildren (self, parent_id, schema=None):
		"""
		gets children items for given parent_id as a list
		of TableRow instances
		"""
		table_name = 'tblCollections_Content'
		if schema is None:
			schema = self.db.getSchema(table_name)
			q_fields = '*'
		else:
			q_fields = ','.join(schema)
	
		queryStr = """SELECT %s FROM %s 
					WHERE CollectionId=%s AND ParentID=%s;""" % (q_fields, table_name, self.coll_id, parent_id)
					
		rows = self.db.doSelect (queryStr)
		results = []
		for row in rows:
			results.append (TableRow (row, schema))
		return results

def getCollection (coll_id):
	db = ArchonDB()
	return ArchonDBCollection (db, coll_id)

def contentChildrenTester():
	coll_id = 3	
	collection = getCollection (coll_id)
	schema = ['ID','Title','ParentID']

	parent_id = '0'
	recs = collection.getContentChildren(parent_id, schema)
	print '%d recs returned' % len(recs)
	print recs[0]
	
def collectionContentTester():
	coll_id = 3	
	collection = getCollection (coll_id)
	schema = ['ID','Title','ParentID']
	recs = collection.getContentItems(schema)
	print '%d recs returned' % len(recs)
	print recs[0]
	
	
def contentRecsTester():
	coll_id = 3	
	collection = getCollection (coll_id)
	schema = ['ID','Title','ParentID']
	recs = db.getCollectionContent(coll_id, schema)
	print '%d recs returned' % len(recs)
	print recs[0]
	
def getCollectionRecTester():
	coll_id = 3	
	collection = getCollection (coll_id)
	schema = ['ID','CollectionIdentifier', 'Title']
	rec = collection.getCollectionRec(schema)
	print rec
	
if __name__ == "__main__":
	# contentChildrenTester()
	# collectionContentTester()
	# getCollectionRecTester()
	
	collection = getCollection(3)
	print 'collection: ', collection.title
