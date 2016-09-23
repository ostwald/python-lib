import sys, os, re
from wos_xls import WosXlsReader
from UserDict import UserDict
from wos_author import Author,AuthorParseException
from author_lookup_tester import Lookup



class All_Authors (UserDict):
	
	def __init__ (self):
		self.data = {}
		data_path = 'real_data/wos_ncar-ucar_fy11.txt'
		reader = WosXlsReader(data_path)
		for item in reader:
			data = item['author full name']
			if data:
				authors = map (lambda x:x.strip(), data.split(';'))
				for authorStr in authors:
					try:
						author = Author (authorStr)
						self.add(author)
					except AuthorParseException, msg:
						print 'could not process "%s" (%s)' % (authorStr, msg)	

	def add (self, author):
		key = str(author)
		if not self.has_key (key):
			self[key] = author
			
	def values (self):
		keys = self.keys()
		keys.sort()
		return map (lambda x:self.data[x], keys)
		
	def toTabDelimited (self):
		fields = ['fullName', 'lastName', 'firstName', 'middleName', 'secondMiddleName']
		recs = []
		recs.append (fields)
		for author in self.values():
			rec = [str(author)] + map (lambda x:getattr(author, x), fields[1:])
			recs.append(rec)
		content = '\n'.join (map (lambda x:'\t'.join(x), recs))
		fp = open ("FOOBERRY.xls", 'w')
		fp.write (content)
		fp.close()
		
		
if __name__ == '__main__':

	all_authors = All_Authors()	
	if 1:
		all_authors.toTabDelimited()
	elif 0:
		print '\n\n-------------------------------\n'
		for author in all_authors.values():
			print '\n---'
			results = Lookup(author).results
			print '%s (%s) - %d results' % (author, author.data, len(results))
			
				
