"""
Gap plugger - update input/accessionNumberMappings.xml with the results of the gap analysis.

read the data from the gap analysis ("input/gap_dr_analysis.txt").
make 2 mappings:
	handMappings - these go from DR num to RecordID and can be incorporated in the accessionNumberMappings as is
	drMappings - these map from DR to DR

"""
import os, sys, re, time
from line_data_reader import LineDataReader
from UserDict import UserDict
from JloXml import XmlRecord, XmlUtils
import utils

class SortedUserDict (UserDict):
			
	def keys(self):
		sorted = self.data.keys()
		sorted.sort()
		return sorted
		
class GapAnalysisMappings (SortedUserDict):
	def __init__ (self):
		self.handMappings = SortedUserDict()
		self.drMappings = SortedUserDict()
		self.unMapped = SortedUserDict()
		UserDict.__init__ (self)
		lines = LineDataReader ("input/gap_dr_analysis.txt")
		# lines.report()
		for line in lines:
			splits = line.split(' - ')
			drNum = splits[0].strip()
			data = splits[1].strip()
			if self.isDrNum (data):
				self.drMappings[drNum] = self.mkDrNum(data)
			elif self.isRecordId (data):
				self.handMappings[drNum] = data
			else:
				self.unMapped[drNum] = data
				pass
			self[drNum] = data	
			
	def isDrNum (self, s):
		try:
			int(s)
			return 1
		except:
			pass
		return 0
		
	def mkDrNum (self, s):
		return "DR%06d" % int(s)
		
	recordIdPat = re.compile ("(.*?)-[0-9]{3}-[0-9]{3}-[0-9]{3}-[0-9]{3}")

	def isRecordId(self, s):
		return self.recordIdPat.match (s)

class GapPlugger (SortedUserDict):
	
	def __init__ (self):
		self.errors = []
		SortedUserDict.__init__ (self)
		self.gappers = GapAnalysisMappings()
		self.initializeFromBaseMappings()
		## must update baseMappings from gaps.handMappings before updateing with gapDrs
		self.updateWithGapHandMappings()
		self.updateWithGapDrs()
		
	def initializeFromBaseMappingsBOG(self):
		baseRec = XmlRecord(path="input/accessionNumberMappings.xml")
		mappingEls = baseRec.selectNodes(baseRec.dom, 'accessionNumberMappings:mapping')
		for mappingEl in mappingEls:
			drNum = mappingEl.getAttribute ('drNumber')
			queryString = mappingEl.getAttribute ('queryString')
			self[drNum] = queryString
		print '%d base mappings found' % len (self)
		
	def initializeFromBaseMappings(self):
		baseRec = XmlRecord(path="output/dr_2_recId_mappings.xml")
		mappingEls = baseRec.selectNodes(baseRec.dom, 'dr_2_recId_mappings:mapping')
		for mappingEl in mappingEls:
			drNum = mappingEl.getAttribute ('drNumber')
			recId = mappingEl.getAttribute ('recordID')
			self[drNum] = recId
		print '%d base mappings found' % len (self)
		
	def updateWithGapHandMappings (self):
		"""
		self.gappers.handMappings are taken verbatim and added to the baseMappings
		"""
		handMap = self.gappers.handMappings
		for key in handMap.keys():
			if self.has_key (key):
				self.errors.add ("handmapping key already in basemappings: %s (%s)" % (key))
				continue
			self[key] = handMap[key]
		
	def updateWithGapDrs (self):
		"""
		self.gappers.drMappings is of form:
			gapDrNum : mappedDrNum
		we expect the the mappedDrNum to be a key in self, and we assign
		the value of mappedDrNum (which is a recordId) to the gapDrNum
		"""
		drMap = self.gappers.drMappings
		for drNum in drMap.keys():
			if self.has_key(drNum):
				self.errors.append ("gappers.drMapping has mapped drNum!: %s" % drNum)
				continue
			mappedDrNum = drMap[drNum]
			if not self.has_key(mappedDrNum):
				self.errors.append ("did not find mappedDrNum: %s" % mappedDrNum)
				continue
			recordId = self[mappedDrNum]
			# queryString = "collId=%s&itemId=%s" % (utils.getCollectionFromId(recId), recId)
			self[drNum] = recordId
			# print "%s : %s" % (drNum, recordId)
			
	def asXml (self):
		rec = XmlRecord (xml="<accessionNumberMappings />")
		root = rec.doc
		root.setAttribute ("date", time.asctime())
		for drNum in self.keys():
			mappingEl = rec.addElement (root, "mapping")
			self.populateMappingElement (mappingEl, drNum)
		
		return rec
		
			
	def populateMappingElement (self, element, drNum):
		element.setAttribute ("drNumber", drNum)
		recId = self[drNum]
		queryString = "collId=%s&itemId=%s" % (utils.getCollectionFromId(recId), recId)
		element.setAttribute ("queryString", queryString)
			
					
if __name__ == '__main__':
	g = GapPlugger()
	if g.errors:
		print "\nERRORS"
		for err in g.errors:
			print err
	g.asXml().write("output/FINAL-accessionNumberMappings.xml")
