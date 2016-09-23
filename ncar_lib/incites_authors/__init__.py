"""
Attached is the author's list as supplied by Thomson-Reuters.
I did some minor clean up of obvious non-NCAR people, but have left all the various variations of the author names in the document.
Let me know how the run against the PeopleSearch DB goes. 

"""
import os, sys
from tabdelimited import TabDelimitedFile, TabDelimitedRecord
from UserDict import UserDict
# to be executed on acorn

class AuthorRecord (TabDelimitedRecord):
	def __init__ (self, data, parent):
		TabDelimitedRecord.__init__ (self, data, parent)
		self.fullname = self['author_full name']
		self.address = self['address']
	
class UniquePeople (UserDict):
	
	def keys(self):
		sorted = self.data.keys()
		sorted.sort(lambda x, y:cmp(x.lower(), y.lower()))
		return sorted
		
class AuthorData (TabDelimitedFile):
	"""
	extend XslWorksheet to overwrite methods such as 'accept'
	- specify the entry class constructor
	"""
	def __init__ (self, path):
		TabDelimitedFile.__init__ (self, entry_class=AuthorRecord)
		self.read (path)
		self.people = self.get_unique_people()
		
	def get_unique_people (self):
		"""
		build a map from unique fullname to records having that name
		"""
		people = UniquePeople()
		for record in self:
			fullname = record.fullname
			values = people.has_key(fullname) and people[fullname] or []
			values.append (record)
			people[fullname] = values
		return people
		
	def reportPeople(self):
		total = 0
		for key in self.people.keys():
			size = len(self.people[key])
			print '%s (%d)' % (key, size)
			total += size
		print "---------\n%d total records" % total
		
if __name__ == '__main__':
	xslPath = "/home/ostwald/Documents/NCAR Library/inCitesAuthors/NCARinitialauthorUTlist_4.5.12Update.txt"
	authors = AuthorData(xslPath)
	print "%d authors read" % len(authors)
	print "%d unique poeple" % len(authors.people.keys())
	authors.reportPeople()
