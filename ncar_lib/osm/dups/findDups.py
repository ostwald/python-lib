"""
findDups - scan records and collect into Dups (where dups are identified by some predicate
that takes two records and returns true if they are dups).

Dup - a set of records that are dups of each other
"""

import os, sys
from UserDict import UserDict
from JloXml import XmlUtils
from ncar_lib import OsmRecord

pubsdata = '/home/ostwald/Documents/NCAR Library/showcase/pubs-ref'

class DupFinder (UserDict):
	"""
	keys are values that are used to determine dups
	"""
	
	def __init__ (self, datadir):
		UserDict.__init__ (self)
		self.datadir = datadir
		self.max_recs = 200000
		self._load ()
		
	def _load (self):
		for i, filename in enumerate (os.listdir(self.datadir)):
			if i >= self.max_recs: break
			if filename.endswith (".xml"):
				rec = OsmRecord (path=os.path.join (self.datadir, filename))
				# title = rec.get('title')
				# print rec.getId(), title
				# print "   " + squashTitle (title)
				# key = squashTitle (rec.get('title'))
				self._add (rec)
				
				
	def _add (self, rec):
		key = squashTitle (rec.get('title'))
		
		values = self.has_key(key) and self[key] or []
		
		if values:
			print 'dup found'

		values.append(rec)
		self[key] = values
		
	def report (self):
		for key in self.keys():
			values = self[key]
			if len(values) > 1:
				print "\n", key
				for rec in values:
					# print "-%s - %s" % (rec.getId(), rec.get('title'))
					showRec(rec)
				
def showRec (rec):
	print "\n", rec.getId()
	print "- ", rec.get('title')
	authors = rec.getAuthors()
	if authors:
		authors.sort (lambda a, b: cmp(XmlUtils.getChildText (a, "lastName"), XmlUtils.getChildText (b, "lastName")))
		# print "- authors"
		authorList = []
		for author in authors:
			authorList.append ("%s, %s" % (XmlUtils.getChildText (author, "lastName"),
										  XmlUtils.getChildText (author, "firstName")))
		print "-  " + ", ".join (authorList)
		# for author in authors:
			# print "  - %s, %s" % (XmlUtils.getChildText (author, "lastName"),
								  # XmlUtils.getChildText (author, "firstName"))
		print "-  " + rec.get('pubName')
			
	
					
def squashTitle (title):
	squashed = ""
	for ch in title.lower():
		if ((ord(ch) >= ord('a') and ord(ch) <= ord('z')) or 
			(ord(ch) >= ord('0') and ord(ch) <= ord('9'))):
			squashed += ch
	return squashed
				
if __name__ == '__main__':
	DupFinder(pubsdata).report()
			
