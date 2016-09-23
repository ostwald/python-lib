import sys, os, re
from wos_xls import WosXlsReader
from UserList import UserList

class UniqueList (UserList):
	
	def append (self, item):
		if not item in self.data:
			self.data.append(item)

# Sandu, Adrian
# firstAndLast = re.compile ('[A-Za-z]{2,}, [A-Za-z^]{2,}')
firstAndLast = re.compile ('.*?, [A-Za-z^]{2,}')
firstAndLastAndInitial = re.compile ('[A-Za-z]{2,}, [A-Za-z^]{2,} [A-Z]\.')

data_path = 'real_data/wos_ncar-ucar_fy11.txt'
reader = WosXlsReader(data_path)

all_items = UniqueList()
firstAndLast_items = UniqueList()
firstAndLastAndInitial_items = UniqueList()

def isFirstAndLast (author):
	m = firstAndLast.match(author)
	return m and m.group() == author

def isFirstAndLastAndInitial (author):
	m = firstAndLastAndInitial.match(author)
	return m and m.group() == author
	
for item in reader:
	data = item['author full name']
	if data:
		authors = map (lambda x:x.strip(), data.split(';'))
		for author in authors:
			all_items.append(author)
			if isFirstAndLast(author):
				firstAndLast_items.append(author)
			elif isFirstAndLastAndInitial(author):
				firstAndLastAndInitial_items.append(author)
				
print "%d total items" % len(all_items)
print "\nfirstAndLast items (%d)" % len (firstAndLast_items)
print "\nfirstAndLastAndInitial items (%d)" % len (firstAndLastAndInitial_items)

others = UniqueList()
for author in all_items:
	if (not author in firstAndLast_items) and (not author in firstAndLastAndInitial_items):
		others.append(author)
		
print "\nOTHERS (%d)" % len (others)
for a in others:
	print a
