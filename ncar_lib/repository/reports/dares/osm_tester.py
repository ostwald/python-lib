"""
osm tester

we want to verify that the instName and instDivision stuff works
"""

import os, sys
from JloXml import XmlUtils
from ncar_lib.peopledb import InternalPerson, getInstDivisionVocab
from ncar_lib import OsmRecord
from authors import DaresAuthors, getAuthorEntry

class Tester:
	
	def __init__ (self, path, daresAuthor):
		self.osmRecord = OsmRecord (path=path)
		self.author = daresAuthor['author']
		self.instDiv = daresAuthor['instDiv']
		self.instDivisionVocab = getInstDivisionVocab(self.instDiv)
		print 'instDiv: %s\n' % self.instDivisionVocab
		
		self.internalPerson = InternalPerson(self.author.upid)
		
		self.osmAuthor = self.getOsmAuthor()
		if not self.osmAuthor:
			raise Exception, "osmAuthor not found for %s" % self.author
		
		print "BEFORE\n%s" % self.osmAuthor.element.toprettyxml()
			
		self.updateRecord()
				
		#print self.osmRecord
		
	def updateRecord (self):
		attrs = [ 'firstName', 'middleName','lastName', 'upid']
		
		for attr in attrs:
			# print "%s -> %s" % (attr, osmAuthorAttrs[i])
			val = self.internalPerson[attr] or ""
			print "%s: %s" % (attr, val)
			if val:
				setattr (self.osmAuthor, attr, str(val))
		self.osmAuthor.updateElement()
		print (self.osmAuthor.element.toxml())	
		
	def updateRecordFromAuthor (self):
		"""
		update from Author attributes
		"""
		osmAuthorAttrs = [ 'firstName', 'middleName','lastName', 'upid']
		authorAttrs = ['firstname', 'middlename', 'lastname', 'upid']
		
		for i, attr in enumerate(authorAttrs):
			# print "%s -> %s" % (attr, osmAuthorAttrs[i])
			setattr (self.osmAuthor, osmAuthorAttrs[i], getattr(self.author, attr))
		self.osmAuthor.updateElement()
		print (self.osmAuthor.element.toxml())
		
	def updateRecord0 (self):
		ucarAffiliation = self.osmAuthor.getUcarAffiliation()
		if not ucarAffiliation:
			raise Exception, 'UCAR affiliation not found'

		ucarAffiliation.addInstDivVocab (self.instDivisionVocab)
			
		
	def write (self, path='validate-me.xml'):
		self.osmRecord.write (path)
		
	def getOsmAuthor (self):
		"""
		find the OsmRecord.ContributorPerson field matching date from the xlsRecord
		- as sanity check, require that all relevant fields from xlsRecord match
		"""
		
		candidates = self.osmRecord.getContributorPeople()
		# print '\nChecking %d candidates' % len(candidates)
		for osmAuthor in candidates:
			if osmAuthor.lastName == self.author.lastname:
				return osmAuthor		
			
			
if __name__ == '__main__':
	div = "MMM"
	auth = getAuthorEntry ('Glen Romine')
	
	# path = "test-record.xml"
	path = "OSGC-000-000-000-017.xml"
	# path = 'validate-me.xml'
	tester = Tester (path, auth)
	# tester.write ('validate-me.xml')
