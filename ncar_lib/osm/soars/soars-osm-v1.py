"""
convert from spreadsheets of Soars metadata data to OSM
records.
"""
import os, sys, time
from JloXml import XmlUtils
from ncar_lib.osm.osmRecord import OsmRecord
from xls import XslWorksheet, WorksheetEntry
from soars_assets import SoarsAssetsFromTextFile
from mapping_maker import MappingMaker

class SoarsRecord (OsmRecord):

	template = "data/SOARS-OSM-TEMPLATE.xml"
	id_prefix = "SOARS"

	def __init__ (self, idnum):
		OsmRecord.__init__ (self, path=self.template)
		self.setId (self.makeId(idnum))
		self.set ('recordDate', "2009-XXXX")
		
	def setUrl (self, url):
		asset = self.selectSingleNode (self.dom, 'record/general/asset');
		if asset:
			asset.setAttribute ("url", url)
		
class SoarsXls (XslWorksheet):
	linesep = "\n"
	verbose = 1
	path = None # must be overridden by subclass

	def __init__ (self):
		XslWorksheet.__init__ (self)
		self.read (self.path)	

class SoarsProtegeInfo (SoarsXls):
	path = "data/ProtegePersonalInfo-kg.txt"

	def __init__ (self):
		SoarsXls.__init__ (self)
		self.idmap = {}
		for entry in self:
			self.idmap[entry['ProtegeID']] = entry

	def getEntry (self, id):
		return self.idmap[id]

class SoarsPapers (SoarsXls):
	path = "data/SummerResearch.txt"

class SoarsRecordMaker:
	
	soarsURL = "http://nldr.library.ucar.edu/collections/soars/"
	metadata = "metadata"  # name of directory where metadata will be written
	doWrite = 1
	
	def __init__ (self, paperID=None):
		"""
		when paperID is supplied, only that paper is processed.
		otherwise, all papers are processed
		"""
		
		if self.doWrite and not os.path.exists (self.metadata):
			os.mkdir (self.metadata)
		self.papers = SoarsPapers()
		self.people = SoarsProtegeInfo()
		self.assets = SoarsAssetsFromTextFile()
		self.handMappings = MappingMaker()
		if paperID:
			paper = self.papers.find ("ResearchID", paperID)
			if paper is None:
				raise KeyError, "Paper not found for '%s'" % paperID
			self.process_paper (paper)
		else:
			self.process()
		
	def process (self):
		print "%d papers" % len (self.papers)
		for i, paper in enumerate(self.papers):
			self.process_paper (paper)
			
	def getAsset (self, lastName, firstName, year):
		# first consult the hand mappings
			
		# now try look up
		found = self.assets.findAsset (lastName, year=year)
		if len(found) > 1:
			raise Exception, 'getAsset: more than one asset found for "%s, %s (%s)"' % (lastName, firstName, year)
		if len(found) == 0:
			raise Exception, 'getAsset: no asset found for "%s, %s (%s)"' % (lastName, firstName, year)
		return found[0]
			
	def process_paper (self, paper):
		researchID = paper['ResearchID']
		protegeID = paper['ProtegeID']
		paperTitle = paper['PaperTitle']
		paperYear = paper['Year']
		peopleEntry = self.people.getEntry (protegeID)
		if not peopleEntry:
			raise KeyError, "people entry not found for protegeID='%s'" % protegeID
		
		# print peopleEntry
			
		firstName = peopleEntry['FirstName']
		lastName = peopleEntry['LastName']
		middleName = peopleEntry['MiddleName']
		suffix = peopleEntry['Sufix'] #(sic)

		# first consult hand-mappings		
		if self.handMappings.has_key(researchID):
			assetID = "%s%s" % (self.soarsURL, self.handMappings.getAssetID (researchID))
		else:
		
			try:
				asset = self.getAsset (lastName, firstName, paperYear)
				if not asset:
					raise Exception, 'Asset Not found for "%s, %s (%s)"' % (lastName, firstName, paperYear)
				assetID = "%s%s" % (self.soarsURL, asset.id)
			except:
				errmsg = str(sys.exc_info()[1])
				print "\n%s : %s" % (researchID, paperTitle)
				print "\t%s" % (errmsg)
				print "\tassetID: "
				splits = errmsg.split(':')
				assetID = splits[-1]
		
		# print "%s, %s" % (lastName, firstName)
		now = time.strftime("%Y-%m-%d", time.localtime())
		
		rec = SoarsRecord(researchID)
		rec.set ('recordDate', now)
		rec.set ('title', paperTitle)
		rec.set ('lastName', lastName)
		rec.set ('firstName', firstName)
		rec.set ('middleName', middleName)
		rec.set ('suffix', suffix)
		rec.set ('coverageDate', paperYear)
		
		rec.setUrl (assetID)
		
		# print rec
		
		if self.doWrite:
			path = os.path.join (self.metadata, rec.getId()+'.xml')
			rec.write(path)
			print "wrote %s" % rec.getId()	
		else:
			# print rec.__repr__().encode ("utf-8")
			# print "processed %s" % rec.getId()
			pass
			
	def showXlsRec (self, rec):
		"""
		debugging: see the fields and values of a spreadsheet record
		"""
		for field in rec.schema:
			print "%s: %s" % (field, rec[field])
			
def peopleTester ():
	info = SoarsProtegeInfo ()
	entry = info.getEntry ("119")
	print entry['LastName']	
	
def mmTest ():
	mm = MappingMaker()
	mm.report()
	print mm.getAssetID(170)	
	
if __name__ == '__main__':
	SoarsRecordMaker()


