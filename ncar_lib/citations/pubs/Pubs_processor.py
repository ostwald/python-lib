
"""
process data from PUBs database to create Citation records
"""
import os, sys
from ncar_lib.citations import GenericProcessor
from ncar_lib.citations import Author
from ncar_lib.citations import Citation
from mysql import PubsDB, PublicationRec
from author import AuthorList
		
class PubsProcessor (GenericProcessor):
	"""
	a processor for PUBS data
	"""
	destDir = "PUBS_other_metadata"
	id_prefix = "PUBS"
	
	optimizeAuthorData = 0
	# query used to obtain citations (published AND refereed)
	select_query = "pubstatus = 'published' AND class = 'refereed'"	
	
	def __init__ (self, startid=None, limit=None, write=1):
		"""
		populate self.records from PubsDB and then call process records
		"""
		GenericProcessor.__init__ (self, startid, limit, write)
		self.db = PubsDB() 
		self.records = self.db.getPubs(where=self.select_query)
		print "about to process %d records" % min (self.limit, len (self.records))
		self.processRecords()
		
	def makeDataDict (self, rec):
		"""
		make the dictionary from which the Citation record will be built
		"""
		data = {}
		data['title'] = rec['title']
		data['year'] = rec['year']
		data['pubname'] = self.db.getPubname (rec['pubname_id'])
		data['editor'] = rec['editor']
		data['volume'] = rec['volume']
		data['pages'] = rec['pages']

		data['pubstatus'] = rec['pubstatus']
		data['statusdate'] = rec['statusdate']

		data['type'] = rec['type']
		# data['authors'] = self.makeAuthorList (rec)
		data['authors'] = AuthorList (self.db, rec['pub_id'], self.optimizeAuthorData)
		
		## ---- pubs-specific fields
		data['pub_id'] = rec['pub_id']
		data['publisher'] = self.db.getPublisher (rec['publisher_id'])
		data['doi'] = rec['doi']
		data['url'] = rec['url']
		data['meetstartdate'] = rec['meetstartdate'] 
		data['meetenddate'] = rec['meetenddate'] 
		data['class'] = rec['class'] 
		data['meetcity'] = rec['meetcity'] 
		data['meetstateprov'] = rec['meetstateprov'] 
		data['meetcountrycode'] = rec['meetcountrycode'] 
		data['collaboration'] = rec['collaboration'] 
		data['meetdate'] = rec['meetdate'] 
		return data
	
class PubsOtherProcessor (PubsProcessor):
	"""
	a processor for all PUBS data OTHER than than citations
	"""
	destDir = "PUBS_other_metadata"
	id_prefix = "PUBS-OTHER"
	
	optimizeAuthorData = 0
	
	# query used to obtain all other records  (!published OR !refereed)
	select_query = "pubstatus != 'published' OR class != 'refereed'"	
		
class PubsSingleRecordProcessor (PubsProcessor):
	"""
	a processor for all PUBS data OTHER than than citations
	"""
	destDir = "PUBS_other_metadata"
	id_prefix = "PUBS-OTHER"
	
	optimizeAuthorData = 0
	
	# query used to obtain all other records  (!published OR !refereed)
	select_query = "pub_id = 200981"		
	
class FY2010Pubs (PubsProcessor):
	"""
	a processor that plucks FYI 2010 records
	"""
	destDir = "PUBS_2010_metadata"
	id_prefix = "FY2010"
	# where_clause = "`statusdate` >  '2009-10-01'"
	select_query = "`year` = 2010 or `statusdate` > '2009-10-01'"
	optimizeAuthorData = 0
	
if __name__ == '__main__':
	
	## foo = PubsProcessor (startid=None, limit=None)
	# foo = PubsOtherProcessor (startid=None, limit=None)
	# foo = PubsSingleRecordProcessor (startid=None, limit=None, write=1)
	foo = FY2010Pubs (startid=None, limit=None, write=1)
