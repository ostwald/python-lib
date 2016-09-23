"""
test authors returned by GetAuthors vs ASN Jusrisdictions
"""

from getAuthors import getAuthors
from getTopics import getTopics
from asn.util import asnHelper

 
asnAuthors = asnHelper.authors.values()
asnTopics = asnHelper.topics.values()

catAuthors = getAuthors()
catTopics = getTopics()

def asnJurisTest ():
	print "ASN Authors"
	for author in asnAuthors.values():
		print author

def catAuthorTest():
	print "Cat Authors"
	for author in catAuthors:
		print author
		
class Comparer:

	asnValues = None
	catValues = None
	name = None
	
	def __init__ (self):
		self.asnValues.sort()
		self.catValues.sort()
	
	def compare (self):
		print "FOUND"
		for catVal in self.catValues:
			if catVal in self.asnValues:
				# print catVal
				pass
		print "\n-------------------\n"
		print "NOT FOUND"
		for catVal in self.catValues:
			if not catVal in self.asnValues:
				print catVal
				
	def showAsnValues(self):
		print "ASN", self.name
		for val in self.asnValues:
			print val
			
	def showCatValues(self):
		print "CAT", self.name
		for val in self.catValues:
			print val
			
	def showValues(self):
		self.showCatValues()
		print "========"
		self.showAsnValues()
				
class AuthorComparer (Comparer):
	asnValues = asnAuthors
	catValues = catAuthors
	name = "Authors"
	
class TopicComparer (Comparer):
	asnValues = asnTopics
	catValues = catTopics
	name = "Topics"
	
if __name__ == '__main__':
	AuthorComparer().compare()
	# TopicComparer().compare()
