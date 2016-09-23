"""

Analyze info in the author and person tables to determine the best data to extract.

"""
import sys
from UserDict import UserDict
from PubsDB import PubsDB
from EsslPeopleDB import EsslPeopleDB
from essl_record_types import AuthorRec

class AuthorRecException (Exception):
	pass
	
class PersonRecException (Exception):
	pass
	
def getDistinctPersonIds ():
	"""
	return a list of DISTINCT person_id values from the author table
	"""
	person_ids = []
	query = "SELECT DISTINCT person_id FROM author WHERE person_id is not NULL and person_id != 0"
	authorRows = PubsDB().doSelect (query)
	print "%d distinct person_id values found" % len(authorRows)
	person_ids = map (lambda x: x[0], authorRows)
	return person_ids

class AuthorIntegrityCheck (UserDict):
	"""
	verify that all names and upids associated with records for given person_id are the same
	"""
	
	def __init__ (self):
		UserDict.__init__(self)
		self.errors = []
		self.pubsDB = PubsDB()
		self.esslPeopleDB = EsslPeopleDB()
		self.authorRecs = self._get_authorRecs()
		self.init()
		
		print '%d author recs found' % len(self.authorRecs)
		print '%d unique person_ids found' % len(self)

		self.reportErrors()
		
	def _makeAuthorKey (self, rec):
		return "%s_%s" % (rec.pub_id, rec.person_id)
		
	def keys (self):
		sorted = self.data.keys()
		sorted.sort
		return sorted
		
	def init (self):
		"""
		get all the non-NULL and non-0 person_ids
		"""
		
		for rec in self.authorRecs:
			person_id = rec.person_id
			if not person_id:
				continue
			elif self.has_key(person_id):
				try:
					ref = self[person_id]
					self.authorRecDiff (ref, rec)
				except AuthorRecException:
					self.errors.append ("%s: %s (%s)" % (sys.exc_info()[1],
										   self._makeAuthorKey(ref), 
										   self._makeAuthorKey(rec)))
				except PersonRecException:
					print sys.exc_info()[1]
				continue
			else:
				self[person_id] = rec
		
	def reportErrors (self):
		print "\nError Report (%d errors)" % len (self.errors)
		for error in self.errors:
			print error
				
	def authorRecDiff (self, reference, other):
		"""
		compare selected fields of two authorRecs: a reference and another rec
		"""
		## fields = ['lastname', 'firstname', 'middlename', 'upid']
		fields = ['firstname']
		for field in fields:
			ref_val = getattr (reference, field)
			other_val = getattr (other, field)
			if  ref_val != other_val:
				if 0:
					# simple - just report the mismatching values
					raise AuthorRecException, '%s mismatch ("%s" vs "%s")' % (field, ref_val, other_val)
				else:
					# get the value from the person table
					person_val = self.getPersonRecordField (reference.person_id, field)
					raise AuthorRecException, '%s mismatch ("%s" vs "%s") --> %s' % \
						(field, ref_val, other_val, person_val)
				
	def getPersonRecordField (self, person_id, field):
		personRec = self.esslPeopleDB.getPerson (person_id)
		if not personRec:
			raise PersonRecException, 'Record not found for %s' % person_id
		if field == 'lastname' and personRec.suffix:
			return "%s %s" % (personRec.lastname, personRec.suffix)
		else:
			return getattr (personRec, field)
					
	def _get_authorRecs (self):
		"""
		returns list of all AuthorRecs in the Pubs database corresponding to specified
		"""
		rows = self.pubsDB.getRows ("author")
		return map (AuthorRec, rows)
		
	def compareTables (self):
		"""
		compare the records associated with the person_ids
		"""

if __name__ == '__main__':
	AuthorIntegrityCheck()

