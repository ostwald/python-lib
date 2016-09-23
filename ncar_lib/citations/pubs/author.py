import sys
from UserList import UserList
from ncar_lib.citations import Author		

class AuthorData:
	"""
	db is PubsDB instance
	authorRec is a record from the Pubs.Author table
	""" 
	# NOT a good idea to assign class variables like this!!!
	# lastname = firstname = middlename = authororder = person_id = upid = suffix = None
		
	def __init__ (self, db, authorRec):
		"""
		Class to hold the best data we can find in association with a particular author
			- db -- PubsDB instance
			- authorRec -- record from the essl_publications.author table
		"""
		self.db = db
		self.authorRec = authorRec
		self.lastname = authorRec.lastname
		self.firstname = authorRec.firstname
		self.middlename = authorRec.middlename
		self.authororder = authorRec.authororder
		self.person_id = authorRec.person_id
		self.upid = None
		self.suffix = None
		
		if (self.person_id):
			try:
				self._update_from_essl_peopleDB (self.person_id)
			except KeyError:
				errors.append ("%s (%s)" % (self, sys.exc_info()[1]))
		
		
		# self.upid = self._get_upid ()
		# if (self.upid):
			# try:
				# self._update_from_peopleDB (self.upid)
			# except:
				# errors.append ("%s (%s)" % (self, sys.exc_info()[1]))
				
	def _update_from_essl_peopleDB (self, person_id):
		"""
		we assume the info in the essl_person db is best, so we override
		info from the authorRec with that from the essl_person rec having the 
		same person_id
		"""
		personRec = self.db.essl_peopleDB.getPerson (person_id)
		if not personRec:
			raise KeyError, 'Record not found for %s' % person_id
		self.lastname = personRec.lastname
		self.firstname = personRec.firstname
		self.middlename = personRec.middlename
		self.suffix = personRec.suffix
		self.upid = personRec.upid
	
	def _get_upid (self):
		"""
		NOT USED FOR NOW - INSTEAD WE USE THE PERSON_ID AND TAKE THE UPID FROM THERE
		get the upid for this author, ensuring that pubs and peopleDB information is
		consistent
		"""
		essl_upid = self.db.essl_peopleDB.getUpid (self.authorRec.person_id)
	
		# use authorRec to find match in poepleDB - NOTE: would we do better to 
		# use essl_people.person record (which has full names)?? (maybe if candidates != 1)
		candidates = self.db.peopleDB.pubsSearch (name_last=self.lastname, 
											 	  name_first=self.firstname+"%", 
												  name_middle=self.middlename+"%")
		
		if (len(candidates) > 1):
			errors.append ("%s (more than one PeopleDB candidates found using initials for search)" % self)
												  
		# print "\t%d candidates found" % len (candidates)
		people_upid = len(candidates) == 1 and candidates[0]['upid'] or None
		
		# raise an error if people_upid and essl_upid are not consistent
		if people_upid and essl_upid and people_upid != essl_upid:
			errors.append ("%s (upid mismatch: peopleDB=%s, essl=%s)" % (self, people_upid, essl_upid))
			upid = people_upid
			
		return (people_upid or essl_upid) or None
		
	def _update_from_peopleDB (self, upid):
		"""
		NOT CURRENTLY USED ... for now essl_person table is authority
		we assume the info in the peopleDB is best, so we draw author names from peopleDB
		"""
		peopleRec = self.db.peopleDB.getPerson (upid)
		if not peopleRec:
			raise KeyError, "PersonDB entry not found for upid: %s" % upid
		self.lastname = peopleRec['name_last']
		self.firstname = peopleRec['name_first']
		self.middlename = peopleRec['name_middle']
	
	def __repr__ (self):
		"""
		make a string representation of this author showing name, upid, etc
		"""
		
		name = '%s, %s. %s.' % (self.lastname, self.firstname, self.middlename)
		info = 'person_id: %s, order: %d, upid: %s' % (self.authorRec.person_id, \
													   self.authororder, \
													   self.upid)
		notes = ""
		# if candidates: notes = " ... %d PeopleDB matches found" % len(candidates)
		
		return '%s -- %s' % (name, info) 	
	
class AuthorList (UserList):
	"""
	create a list of Author instances for provided pub
	- get authorRecs for specified pub (by pub_id)
	  - authors are represented by id, so for each id get a record from the AuthorDB
	 - if "optimize", we try to improve the author information from either:
		 - the essl people table, OR
		 - the PeopleDB
    (NOTE: we generally do not use "optimize" because the hyphenation of asian names is
	 better in the "author" table, and there are sometimes mulitple entries for the same person
	 in the people tables. The drawback of not optimizing is that the author table lists only
	 first and middle initials, with no suffix information at all).
	"""
	
	def __init__ (self, db, pub_id, optimize=0):
		UserList.__init__(self)	
		self.pub_id = pub_id
		authorRecs = db.getAuthorRecs(pub_id)
		for authorRec in authorRecs:
			if optimize:
				try:
					authorData = AuthorData (db, authorRec)
				except:
					print "Author Data Error: %s" % sys.exc_info()[1]
					authorData = authorRec
			else:
				authorData = authorRec
			lastname = authorData.lastname
			firstname = authorData.firstname
			middlename = authorData.middlename
			suffix = hasattr (authorData, 'suffix') and authorData.suffix or None
			order = authorData.authororder
			person_id = authorData.person_id
			upid = authorData.upid
			self.append (Author (lastname, firstname, middlename, suffix, order, person_id, upid))
		self.sort()
	
	def sort (self):
		self.data.sort (lambda a, b: cmp (a.authororder, b.authororder))
			
	def __repr__ (self):
		s=[];add=s.append
		add ("AuthorList for pub_id: %s" % self.pub_id)
		for author in self:
			add (str(author))
		return '\n'.join (s)
			
		
if __name__ == '__main__':
	from mysql.PubsDB import PubsDB, AuthorRec
	
	pub_id = 106827
	db = PubsDB()
	rec = db.getPub (pub_id)
	print "non-optimized"
	print AuthorList (db, pub_id)
	print "\noptimized"
	print AuthorList (db, pub_id, 1)

	
