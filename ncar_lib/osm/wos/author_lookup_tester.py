import sys, os, re
from ncar_lib.peopledb import InternalPersonSearch
from UserDict import UserDict
from wos_author import Author
from JloXml import XmlUtils

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
	
	def __init__ (self, author):
		"""
		first try last name only
		- if more than 1 result, try initials
		  - if no results, try first initials
		  - if more than 1 result, try full names
		"""
		params = {
			'searchScope' : 'all',
			'includeActive' : 'true',
			'includeInactive'  : 'true',
			'searchType' : 'advancedSearch'
		}
		
		params['lastName'] = author.lastName
		
		for attr in ['firstName', 'middleName']:
			value = getattr(author, attr)
			if value:
				params[attr] = value[0]
		self.results = map (PeopleDBPerson, InternalPersonSearch (params, 2))
		

if __name__ == '__main__':
	author = Author ('Ostwald, J.')
	# author = Author ('Attie, J. -R.')
	print '%s (%s)' % (author, author.data)
	
	results = Lookup (author).results
	print '%d results found' % len(results)
	for result in results:
		print result

