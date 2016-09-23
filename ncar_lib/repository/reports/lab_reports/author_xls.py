"""
MMM Authors 
	Reads author data from a spreadsheet written by "author_xls_writer"
"""
import os, sys
from xls import WorksheetEntry, XslWorksheet
from ncar_lib.repository.author_search import Author

## "normalized" used to be mmm_type
author_fields = ['firstName', 'nickname', 'middleName', 'lastName', 'upid', 'normalized'] 

class AuthorEntry (WorksheetEntry):
	
	def __repr__ (self):
		author_data = map (lambda x:self[x], self.schema)
		return ', '.join(author_data)
		
	def asSearchAuthor(self):
		firstname = self['nickname'] or self['firstName']
		return Author(self['lastName'], 
						 firstname, 
						 self['middleName'], 
						 self['upid'])

class AuthorWorksheet(XslWorksheet):
	
	linesep = "\n"
	
	def __init__ (self, path):
		XslWorksheet.__init__ (self, entry_class=AuthorEntry)
		self.read(path)
		
	def report(self):
		for rec in self:
			print rec
		
def getSearchAuthors (path):
	AuthorWorksheet.linesep = '\n'
	return map (lambda x:x.asSearchAuthor(), AuthorWorksheet(path))


def get_ACD_authors():
	return getSearchAuthors('data/ACD/ACD-authors.txt')
	
def get_GCD_authors():
	return getSearchAuthors('data/GCD/GCD-authors.txt')
	
def get_MMM_authors ():
	return getSearchAuthors('data/MMM/mmm_authors.txt')


if __name__ == '__main__':
	# authors = AuthorWorksheet('data/ACD/ACD-authors.txt')
	# authors.report ()
	authors = get_ACD_authors()
	a = authors[0]
	print a.lastname
