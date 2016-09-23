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
from ncar_lib.osm.wos import Author
from ncar_lib.peopledb import InternalPersonSearch
from UserDict import UserDict
from JloXml import XmlUtils

InternalPersonSearch.verbose = 0

class PeopleDBPerson (UserDict):
	
	attrs = ['lastName', 'firstName', 'middleName', 'secondMiddleName', 'upid', 'internalOrg',
			 'preferredName', 'active', 'email', 'location']
	
	def __init__ (self, data):
		UserDict.__init__ (self, data)
		for attr in self.attrs:
			setattr (self, attr, self[attr])
		
	def __getitem__ (self, key):
		if self.data.has_key(key):
			return self.data[key]
		else:
			return ""
			
	def __repr__ (self):
		"""
		display a name in human readable form.
		
		rules regarding periods in first, middle, and secondMiddleNames:
			display should add a period only when the name is a single letter,
			otherwise, no periods ..
		"""
		s = self.lastName
		if self.firstName or self.middleName:
			s = s + ","
		if self.firstName:
			s = "%s %s" % (s, self.firstName)
			# if len(self.firstName) == 1:
			if self.isAbreviation(self.firstName):
				s = s + '.'
		if self.middleName:
			s = "%s %s" % (s, self.middleName)
			# if len(self.middleName) == 1:
			if self.isAbreviation(self.middleName):
				s = s + '.'
		if self.secondMiddleName:
			s = "%s %s" % (s, self.secondMiddleName)
			#if len(self.secondMiddleName) == 1:
			if self.isAbreviation(self.secondMiddleName):
				s = s + '.'				
			
		s = "%s - #%s - %s" % (s, self.upid, self.internalOrg)
		return s
		
	def isAbreviation (self, s):
		return len(s) == 1
		
class AuthorLookup:
	
	def __init__ (self, author):
		"""

		"""
		self.author = author
		searchParams = {
			'lastName' : self.author.lastName,
			'internalOnly' : 'true',
			'searchType' : 'quickSearch'
		}
		
		self.hits = map (PeopleDBPerson, InternalPersonSearch (searchParams, 2))
		self.lastNameMatches = filter (lambda x:x.lastName == self.author.lastName, self.hits)
		# self.firstInitialMatches = self.getFirstInitialMatches(self.lastNameMatches)
		
	# def getFirstInitialMatches(self, pool):
		# matches = []
		# for hit in pool:
			# if len(hit.firstName) == len(self.author.lastName) == 1:
				# if hit.firstName[0] != self.author.firstName[0]:
					# continue:
			
		
	def report (self):
		print '\n%s' % self.author.data
		print '----------'
		print '%d hits' % len(self.hits)
		print '%d lastNameMatches' % len(self.lastNameMatches)
		for m in self.lastNameMatches:
			print m
		print '\n'

if __name__ == '__main__':
	name = 'Ma, Ruiping'
	name = 'Ha, S.-Y.'
	name = 'Zhang, M.'
	# name = 'Thompson, Greg'
	author = Author (name)
	lookup = AuthorLookup (author)
	lookup.report()


