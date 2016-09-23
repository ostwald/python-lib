"""
Data Filter - filter the inCites data (author records) to contain only record 
having unique combo of fullname + address

"""
import os, sys
from tabdelimited import TabDelimitedFile, TabDelimitedRecord
from UserDict import UserDict
from find_person import resolveFullName, PersonFinder
# to be executed on acorn

class AuthorRecord (TabDelimitedRecord):
	def __init__ (self, data, parent):
		TabDelimitedRecord.__init__ (self, data, parent)
		self.fullname = self['author_full name']
		self.address = self['address']
		self.key = self.fullname + self.address
	
class UniquePeople (UserDict):
	"""
	a dict, mapping KEYS (fullname + self.address)
				to AuthorRecord see above
				
	
	"""
	def __init__ (self, records):
		"""
		records are a list of AuthorRecord from the spreadsheet
		"""
		self.data = {}
		for record in records:
			self.add (record)
		
	def add (self, record):
		"""
		only add if there is a unique combo of full name + address
		"""
		fullname = record.fullname
		uniques = []
		if self.has_key(fullname):
			uniques = self[fullname]
			
		for val in uniques:
			if val.key == record.key:
				return
			
		uniques.append(record)
		self[fullname] = uniques	
		
	def keys(self):
		sorted = self.data.keys()
		sorted.sort(lambda x, y:cmp(x.lower(), y.lower()))
		return sorted
		
class FilteredAuthorData (TabDelimitedFile):
	"""
	extend XslWorksheet to overwrite methods such as 'accept'
	- specify the entry class constructor
	
	self.data - a list of all records in the spreadsheet (as AuthorRecord)
	self.people - a UniquePeople instance
	"""
	
	default_path = "/home/ostwald/Documents/NCAR Library/inCitesAuthors/NCARinitialauthorUTlist_4.5.12Update.txt"
	
	def __init__ (self, path=None):
		self.path = path or self.default_path
		TabDelimitedFile.__init__ (self, entry_class=AuthorRecord)
		self.read (self.path)
		self.people = UniquePeople(self.data)
		
	def findPeople(self):
		errors = []
		notes = []
		total = 0
		for fullname in self.people.keys():
			try:
				size = len(self.people[fullname])
				
				finder = PersonFinder (fullname)
				candidates = finder.candidates
				if len(candidates) == 1:
					continue
					
				## print '\n%s (%d)' % (fullname, size)
				print "\n%d candidates found for '%s' (%s | %s)" % \
					(len(finder.candidates), 
					 finder.fullname, 
					 finder.lastName, 
					 finder.firstName)
					 
				for person in candidates:
					print '- ', person
			except Exception, e:
				errors.append(fullname + ": " + str(e))
			total += size
		# print "---------\n%d total records" % total
		if errors:
			print '\nNames that could not be parsed'
			for error in errors:
				print error
		if notes:
			print '\nNotes'
			for note in notes:
				print note		

	def reportPeople(self):
		errors = []
		notes = []
		total = 0
		for key in self.people.keys():
			try:
				size = len(self.people[key])
				print '%s (%d)' % (key, size)
				first, middle, last, note = resolveFullName (key)
				print ' - %s | %s | %s' % (last, first, middle)
				if note:
					notes.append (note)
			except Exception, e:
				errors.append(key + ": " + str(e))
			total += size
		print "---------\n%d total records" % total
		print '\nNames that could not be parsed'
		for error in errors:
			print error
		print '\nNotes'
		for note in notes:
			print note			
		
if __name__ == '__main__':
	xslPath = "/home/ostwald/Documents/NCAR Library/inCitesAuthors/NCARinitialauthorUTlist_4.5.12Update.txt"
	authors = FilteredAuthorData(xslPath)
	print "%d authors read" % len(authors)
	print "%d unique poeple" % len(authors.people.keys())
	authors.findPeople()
	
