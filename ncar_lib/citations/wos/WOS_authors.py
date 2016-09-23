"""
ultimately want to have enough info to produce "AMS/ASR format (as specified by Pubs) ..."
"""

import sys, os, time, re

from UserList import UserList
from UserDict import UserDict
from misc.titlecase import titlecase
from ncar_lib.citations.Author import WOSAuthor
from WOS_reader import WOSXlsReader

		
def filterByTitle (item, findstring):
	## findstring = "DETERMINING MAJOR SAR-ARC PROPERTIES FROM A FEW MEASURABLE PARAMETERS"
	title = item._getTitle().lower()
	return title.find (findstring.lower()) != -1
	
def filterByAuthor (item, findstring):
	return item['authors'].lower().find (findstring.lower()) != -1
	
dotAuthorRe = re.compile("[\S]*\.[\S]")
	
def filterByDotAuthor (item):
	m = dotAuthorRe.search (item['authors'])
	if m:
		# print item['authors']
		return 1
	else:
		return 0
		
hyphenAuthorRe = re.compile("[\S]*\.\-[\S]")
		
def filterByHyphenAuthor (item):
	m = hyphenAuthorRe.search (item['authors'])
	if m:
		# print item['authors']
		return 1
	else:
		return 0		
		
def filterWosFile (path, filterFn):
	wos = WOSXlsReader(path)
	
	# fn = lambda a:(a._getTitle().lower().find (findstring) != -1)
	return filter (filterFn, wos)
	
def batchFilterWosFile (filterFn, basedir=None):
	basedir = basedir or "WOS_data_files"
	items = []
	for filename in os.listdir (basedir):
		if not filename.endswith(".txt"):
			continue
		print filename
		path = os.path.join (basedir, filename)
		filtereditems = filterWosFile (path, filterFn)
		print "%d filtered items" % len (filtereditems)
		items = items + filtereditems
	return items
		
def showHyphenAuthors ():
	items = batchFilterWosFile (filterByHyphenAuthor)
	print "\n%d hypehn-authors found" % len(items)
	for item in items:
		for author in item['authors'].split(';'):
			if 0 or hyphenAuthorRe.search (author):
				print "%s" % str(author).strip()
			
def showFoundAuthors (findstr):
	"""
	print all names found containing "findstr"
	"""
	items = batchFilterWosFile (lambda item: 1)
	print "\n%d authors found" % len(items)
	for item in items:
		for author in item['authors'].split(';'):
			# print "%s" % str(author).strip()
			if author.lower().find (findstr.lower()) != -1:
				print "%s" % str(author).strip()
				
if __name__ == '__main__':
	path = "WOS_data_files/WOS_11501-11816.txt"
	# filterWosFile (path, filterByHyphenAuthor)
	# filterWosFile (path, filterByDotAuthor)
	# showHyphenAuthors()
	showFoundAuthors ("Xie")
	
		
