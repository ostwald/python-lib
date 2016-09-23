"""
record change info

- use web service to compile lists (rendered as XML docs) of metadata
records to be updated.
"""

import sys, os
from pubNamesWorksheet import PubNamesWorkSheet, data_worksheeet_path
from JloXml import XmlRecord, XmlUtils
from ncar_lib.osm import OsmRecord
from dds_getRecord import GetRecord
from dds_pubName_search import PubNameRecordGetter
from UserList import UserList

local_repo = 'home/ostwald/Documents/NCAR Library/OpenSky/pubName 2010-11-24/records'

repo_path = local_repo
osm_dir = os.path.join (repo_path, 'osm')

dowrites = 1

class PubNameSpec:
	"""
	contains information necessary to update the pubName field of a single metadata record
	- term (pubName value)
	- recId
	- collection (key)
	- xmlFormat
	"""
	def __init__ (self, term, recId, collection, xmlFormat, pubType="Proceedings"):
		self.term = term
		self.recId = recId
		self.collection = collection
		self.xmlFormat = xmlFormat
		self.pubType = pubType
		
	def __repr__ (self):
		s=[];add=s.append
		for attr in ['term', 'recId', 'collection', 'xmlFormat', 'pubType']:
			add ("%s: %s" % (attr, getattr(self, attr)))
		return ', '.join (s)
		
	def __cmp__ (self, other):
		return cmp (self.recId, other.recId)
		
	def asElement (self):
		"""
		render this PubNameSpec as an XML element so it can be put in an XML
		document containing multiple change PubNameSpecs
		"""
		element = XmlUtils.createElement ("pubNameSpec")
		for attr in ['recId', 'collection', 'xmlFormat', 'pubType']: 
			element.setAttribute (attr, getattr(self, attr))
			XmlUtils.setText (element, self.term)
		return element
		
class RecordModInfo (UserList):
	"""
	Abstract class for compiling a list of Record Modification specs
	- can be output as XML Document
	"""	
	
	rootElementName = "NO_NAME"
	
	def __init__ (self,path=data_worksheeet_path):
		UserList.__init__(self)
		self.ws = PubNamesWorkSheet (path)
		self.errors = []
		print "%d worksheet records read" % len(self.ws)
		self.populate()
		self.reportErrors()
		
	def reportErrors(self):
		"""
		report any errors encountered while building list
		"""
		print "\nERRORS (%d)" % len(self.errors)
		for error in self.errors:
			print error
			
	def asXML (self):
		rec = XmlRecord (xml="<" + self.rootElementName + "/>")
		for spec in self:
			rec.doc.appendChild (spec.asElement())
		return rec
		
	def write (self):
		rec = self.asXML()
		outpath = "output/%s.xml" % self.rootElementName
		rec.write (outpath)
		print "wrote to %s" % outpath
		
	def report (self):
		"""
		print out information from each spec
		"""
		self.sort()
		for spec in self:
			print "%s %s (%s)" % (spec.recId, spec.term, spec.pubType)
		
class ToAddInfo (RecordModInfo):
	"""
	compiles a list of PubNameSpecs from the OSM data spreadsheet. 
	for each recordID in the "addto" field, a PubNameSpec is created by
	using dds.GetRecord to obtain necessary info about record
	
	errors include the IDs that could not be found by GetRecord
	"""
	rootElementName = "PubNamesToAddInfo"
	
	def __init__ (self,path=data_worksheeet_path):
		RecordModInfo.__init__(self, path)

	def populate (self):
		for rec in self.ws:
			if rec.addto:
				# print 'add "%s" to these records' % rec.term
				for recId in rec.addto:
					# print ' - ', recId
					try:
						result = GetRecord(recId).result
					except:
						self.errors.append(sys.exc_info()[1])
						continue
					spec = PubNameSpec (rec.term, recId, result.collection, result.xmlFormat, rec.pubType)
					self.append (spec)
			
					
class ToChangeInfo (RecordModInfo):
	"""
	Uses dds.Search to find all records with the "Incorrect" terms listed in the OSM data spreadsheet.
	Each record having an "incorrect" pubname results in a PubNameSpec containing the Correct term
	and information about the record(s) to be modified
	
	errors include ...
	"""
	
	rootElementName = "PubNamesToChangeInfo"
	
	def populate (self):
		for item in self.ws:
			if item.badterm:
				results = []
				try:
					results = PubNameRecordGetter(item.badterm).results
				except:
					self.errors.append("%s (%s)" % (sys.exc_info()[1], item.badterm))
					continue
				print "%d results found for '%s'" % (len (results), item.badterm)
				for result in results:
					spec = PubNameSpec (item.term, result.recId, result.collection, result.xmlFormat, item.pubType)
					self.append (spec)

def setPubName (recId, collection, pubName):
	path = os.path.join (osm_dir, recId+'.xml')
	rec = OsmRecord(path=path)
	rec.setPubName (pubName, "Proceedings")
	if dowrites:
		rec.write()
		print "wrote to %s (%s)" % (recId, collection)
	else:
		print "WOULD'VE WRITTEN to %s (%s)" % (recId, collection)

def saveToAddInfo():
	info = ToAddInfo()
	if 1:
		rec = info.asXML()
		# print rec
		info.report()
	else:
		info.write ()
	
def saveToChangeInfo():
	info = ToChangeInfo()
	if 1:
		rec = info.asXML()
		# print rec
		info.report()
	else:
		info.write ()
		
if __name__ == '__main__':
	# saveToAddInfo()
	saveToChangeInfo()
