
"""
processes PUS data in search of hyphen name handling
"""
import os, sys, re
from Pubs_processor import PubsProcessor
from ncar_lib.citations import Author
from ncar_lib.citations import Citation
from mysql.PubsDB import PubsDB, PublicationRec
from author import AuthorData
		
class AuthorProcessor (PubsProcessor):
	"""
	a processor for PUBS data that emphasizes authors
	"""
	destDir = "PUBS_metadata"
	id_prefix = "PUBS"
		
	def processRecords (self):
		for rec in self.records:
			data = self.makeDataDict (rec)
			
			citation = Citation (data, self.makeId(self.idcounter))
			if self.write:
				citation.write (os.path.join (self.destDir, citation.id+'.xml'))
			else:
				print citation
			# print citation
			self.idcounter = self.idcounter + 1
			self.reccounter = self.reccounter + 1
			if self.reccounter >= self.limit: break
			
class HypenatedNameFinder:
	
	# hyphenRe = re.compile("[\S]*\.\-[\S]")  # matches .-
	hyphenRe = re.compile("[\S]*\-[\S]")
	name_fields = [] # defined in subclass
	
	def __init__ (self):
		self.authorRecs = self.getAuthorRecs ()
		print "%d author recs found" % len (self.authorRecs)
		self.hyphenNames = self.getHyphenNames()
		
		print "\nthere are %d names containing hyphens" % len (self.hyphenNames)
		for name in self.hyphenNames:
			print name	
	
	def getHyphenNames (self):
		"""
		construct list of unique names containing a hyphen pattern in first or middle names
		"""
		hyphenNames = []
		for rec in self.authorRecs:
			if self.isHyphenName (rec):
				name = self.getFullName(rec)
				if not name in hyphenNames:
					hyphenNames.append (name)
		hyphenNames.sort()
		return hyphenNames
		
	def getFullName (self, rec):
		"""
		abstract - implemented by subclass
		"""
		return ""
		
	def sameName (self, rec1, rec2):
		for field in self.name_fields:
			if getattr (rec1, field) != getattr (rec2, field):
				return 0
		return 1	
		
	def getAuthorRecs (self):
		"""
		abstract - implemented by subclass
		"""
		return []
		
	def isHyphenName (self, rec):
		for field in self.name_fields[1:]:
			val = getattr (rec, field)
			if val and self.hyphenRe.search(val):
				return 1
		return 0
	
class Essl_Author_H_Names (HypenatedNameFinder):
	
	name_fields = ['lastname', 'firstname', 'middlename']
	
	def getAuthorRecs (self):
		
		from mysql.essl_record_types import AuthorRec
		rows = PubsDB().getRows ("author")
		authorRecs = map (AuthorRec, rows)
		return authorRecs
		
	def isHyphenNameX (self, rec):
		return self.hyphenRe.search (rec.firstname) or self.hyphenRe.search (rec.middlename)
		
	def getFullName (self, rec):
		return rec.getFullName()
		
class People_H_Names (HypenatedNameFinder):
	
	name_fields = ['name_last', 'name_first', 'name_middle', 'nickname']
	
	def getAuthorRecs (self):
		
		from mysql.PeopleDB import PeopleDB
		return PeopleDB().getPeople()
		
	def getFullName (self, rec):
		fullname = rec.name_last
		if rec.name_first:
			fullname = "%s, %s" % (fullname, rec.name_first)
		if rec.name_middle:
			fullname = "%s %s" % (fullname, rec.name_middle)
			
		if rec.nickname:
			fullname = "%s (%s)" % (fullname, rec.nickname)
			
		fullname = "%s -- #%d" % (fullname, rec.upid)
		return fullname
		
	def isHyphenName (self, rec):
		
		return (rec.name_first and self.hyphenRe.search (rec.name_first)) or \
			   (rec.name_middle and self.hyphenRe.search (rec.name_middle))
		
if __name__ == '__main__':
	
	Essl_Author_H_Names()
	# People_H_Names()
