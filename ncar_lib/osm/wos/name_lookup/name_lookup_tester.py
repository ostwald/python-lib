"""
name lookup tester -

populate cells of spreadsheeet (name_data.txt) with number of results obtained for different
name critieria.

GOAL: find algorithm for matching name data to peopleDB

e.g., something like: 		

	first try last name only
		- if more than 1 result, try initials
		  - if no results, try first initials
		  - if more than 1 result, try full names

"""

import sys, os, re
from xls import WorksheetEntry, XslWorksheet
from ncar_lib.peopledb import InternalPersonSearch
from UserDict import UserDict
from JloXml import XmlUtils

InternalPersonSearch.verbose = 0

class PeopleDBPerson (UserDict):
	
	attrs = ['lastName', 'firstName', 'middleName', 'secondMiddleName', 'upid', 'internalOrg',
			 'preferredName', 'active', 'email', 'location']
	
	def __init__ (self, data):
		UserDict.__init__ (self, data)
		
		
	def __getitem__ (self, key):
		if self.data.has_key(key):
			return self.data[key]
		else:
			return ""

class Lookup:
	
	def __init__ (self, params):
		"""

		"""
		searchParams = {
			'searchScope' : 'all',
			'includeActive' : 'true',
			'includeInactive'  : 'true',
			'searchType' : 'advancedSearch'
		}
		
		searchParams.update (params)
		self.results = map (PeopleDBPerson, InternalPersonSearch (searchParams, 2))
		
class QuickInternalLookup:
	
	def __init__ (self, name):
		"""

		"""
		searchParams = {
			'lastName' : name,
			'internalOnly' : 'true',
			'searchType' : 'quickSearch'
		}
		
		self.results = map (PeopleDBPerson, InternalPersonSearch (searchParams, 2))
		
class NameRecord (WorksheetEntry):
	pass

class NameXlsReader (XslWorksheet):
	
	verbose = 1
	linesep = '\r\n' # windows
	encoding = 'utf-8'
	path = 'name_data.xls'
	
	def __init__ (self):
		XslWorksheet.__init__ (self, entry_class=NameRecord)
		self.read (self.path)
		
	def addField (self, field):
		if field in self.schema:
			raise KeyError, 'field (%s) already exists in schema' % field
		self.schema.append(field)
		for rec in self:
			rec.setSchema (self.schema)
			rec.data.append ('')
	
	def lastNameLookup (self):
		self.addField ("lastNameLookup")
		for rec in self.data:
			results = Lookup ({'lastName':rec['lastName']}).results
			rec["lastNameLookup"] = str(len(results))
			print '%s (%d)' % (rec['fullName'], len(results))
			
	def quickNameLookup (self):
		self.addField ("quickNameLookup")
		for rec in self.data:
			results = QuickInternalLookup (rec['lastName']).results
			rec["quickNameLookup"] = str(len(results))
			print '%s (%d)' % (rec['fullName'], len(results))
			
	def write (self, path=None):
		if path is None:
			path = self.path
		XslWorksheet.write(self, path)
			
def lookupTest (params):
	pass

if __name__ == '__main__':
	
	reader = NameXlsReader()
	if 0:
		# active and inactive, scope: all
		reader.lastNameLookup ()
		reader.write ()
		
	if 1:
		# quicksearch, internal only
		reader.quickNameLookup ()
		reader.write ()
		
	# print reader[0]
	# results = Lookup (author).results
	# print '%d results found' % len(results)
	# for result in results:
		# print result

