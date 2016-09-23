"""
Update Metadata Records having Dares Authors that have a upid (these are Employees, 
as opposed to Visitors)

from jamaica:
	we know that all records for Jeff Anderson, Glen Romine, and Hui Liu should be
	updates with a DAReS affiliation. Hui's will be hard, as he's not the only H Liu
	at NCAR.
	
	The collections affected are AMS, OSGC, and PUBS not FY10.
	
	For Jeff and Glen's records, you can go ahead and update the affiliations. For
	Hui, I think it's probably best to do a dump of record ID, title type, pub type,
	coauthors, fiscal year, and collection, and then manually determine which are
	his and which are not.


APPROACH
start with
- a spreadsheet of records for a particular author
- a DaresAuthor instance 
read the spreadsheet in using xls


"""


import os, sys
from xls import WorksheetEntry, XslWorksheet
from authors import DaresAuthors, getAuthorEntry
from ncar_lib.peopledb import InternalPerson, getInstDivisionVocab
from ncar_lib.repository.record_manager import CachingRecordManager, CachedRecordError

import ncar_lib
ncar_lib_dir = os.path.dirname (ncar_lib.__file__)

"""
Use search service to retrieve a batch of records and then process them
"""

class DaresXlsRecord (WorksheetEntry):
	
	def __init__ (self, textline, schema):
		WorksheetEntry.__init__ (self, textline, schema)
		self.recId = self['recId']

class DaresXls (XslWorksheet):
	linesep = "\n"
	
	def __init__ (self, xls_path):
		XslWorksheet.__init__(self,entry_class=DaresXlsRecord)
		self.read (xls_path)
	
class DaresUpdater:
	"""
	for each record listed in the spreadsheet (at xls_path),
	call self.updateRecord
	"""
	
	dowrites = 1
	
	def __init__ (self, xls_path, daresAuthor):
		worksheet = DaresXls(xls_path)
		print '%d records read' % len(worksheet)
		
		metadata_cache = os.path.join (ncar_lib_dir, 'repository/reports/dares/records')
		searchBaseUrl = "http://nldr.library.ucar.edu/schemedit/services/ddsws1-1"
		
		self.record_manager = CachingRecordManager(searchBaseUrl=searchBaseUrl, baseCachePath=metadata_cache)
		
		self.upid = daresAuthor['author'].upid
		self.instDiv = daresAuthor['instDiv']
		
		self.internalPerson = InternalPerson(self.upid)
		self.instDivisionVocab = getInstDivisionVocab(self.instDiv)
		
		if 1:
			print "\n%s" % self.internalPerson
			# print self.instDivisionVocab
		
		for rec in worksheet:
			matchStrength = rec['matchStrength']
			print '\n', rec['recId'], rec['collection'],matchStrength
			
			# required_matchStrength = ['certain', 'strong']
			required_matchStrength = ['certain'] # use for names that may not be unique (e.g. H Liu)
			
			if not matchStrength in required_matchStrength:
				print ' .... skipping based on matchStrength'
				continue
			try:
				self.updateRecord (rec)
			except:
				raise Exception, 'Could not update record for %s: %s' % (rec.recId, sys.exc_info()[1])
				
			# print "halting ...."
			# sys.exit()
			
			
			
	def updateRecord (self, xlsRecord):
		"""
		- update author information from peopledb.internalPerson response
		- update the exsting instDiv (or add a new one) to reflect the
			instDiv value for the daresAuthor
		"""
		# print '\nupdateRecord: %s' % xlsRecord.recId
		# osmRecord = getDiskRecord (xlsRecord.recId)
		osmRecord = self.record_manager.getRecord (xlsRecord.recId)
		if not osmRecord:
			raise Exception, 'OsmRecord not found'
			
		osmAuthor = self.getOsmAuthor (osmRecord, xlsRecord)
		if not osmAuthor:
			raise Exception, 'Author not found for %s' % (xlsRecord.recId)

		self.updateOsmAuthor (osmAuthor)
		osmAuthor.orderElements()
		
		if self.dowrites:
			# osmRecord.write()
			self.record_manager.cacheRecord(osmRecord)
			print "wrote ", osmRecord.getId()
		else:
			print 'WOULD have written', osmRecord.getId()
		
		# print osmAuthor.element.toxml()
		# osmRecord.write("updated.xml");
		# print osmRecord
		
	def getOsmAuthor (self, osmRecord, xlsRecord):
		"""
		find the OsmRecord.ContributorPerson field matching date from the xlsRecord
		- as sanity check, require that all osmAuthor fields from xlsRecord (which represent
			the "best author match" from the record, match
		"""
		
		match_fields = ['lastName', 'firstName', 'middleName', 'upid']
		
		matched_author = None
		
		candidates = osmRecord.getContributorPeople()
		# print '\nChecking %d candidates' % len(candidates)
		for author in candidates:
			for field in match_fields:
				if getattr (author, field) != xlsRecord[field]:
					# print "no match for %s: %s vs %s" % (field, getattr (author, field), xlsRecord[field])
					break
				#print "MATCH FOUND"
				return author
		
	def updateOsmAuthor (self, osmAuthor):
		"""
		update the osmAuthor in the OsmRecord with data from the peopleDB (self.internalPerson)
		"""
		
		attrs = [ 'firstName', 'middleName','lastName', 'upid']
		
		for attr in attrs:
			val = self.internalPerson[attr] or ""
			if val:
				setattr (osmAuthor, attr, str(val))
			
		if self.internalPerson['nameSuffix']:
			setattr (osmAuthor, 'suffix', self.internalPerson['nameSuffix'])
			
		osmAuthor.updateElement() # update the osmAuthor element in the instance Record
			
		email = self.internalPerson['email']
		if email:
			osmAuthor.setEmail (email)

		ucarAffiliation = osmAuthor.getUcarAffiliation()
		if not ucarAffiliation:
			print 'UCAR affiliation not found'
		ucarAffiliation.addInstDivVocab (self.instDivisionVocab)
		ucarAffiliation.sortInstDivs()
			
def tester():	
	data = "reports/Glen_Romine.txt"
	authorEntry = getAuthorEntry ('Glen Romine')
	DaresUpdater (data, authorEntry)

def batch_updater():
	for fullName in DaresAuthors.dares_authors.keys():
		update_for_author (fullName)
		
def update_for_author (fullName):
	splits = map (lambda x:x.strip(), fullName.split(' '))
	data = "reports/%s_%s.txt" % (splits[0], splits[1])
	if not os.path.exists(data):
		raise IOError, 'data file not exist at %s' % data
	authorEntry = getAuthorEntry(fullName)
	DaresUpdater (data, authorEntry)

	
if __name__ == '__main__':
	full_time_dares = ['Jeffrey Anderson',
			   'Glen Romine',
			   'Hui Liu']
	update_for_author(full_time_dares[2])
