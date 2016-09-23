

"""
traverse all the metadata and make a report of what fields there are, and how
many times each field occurs per record
"""


import os
from JloXml import XmlRecord, XmlUtils
from UserDict import UserDict

technotesDir = "../NCAR Technical Notes"

class Entry:

	def __init__ (self, tag, count=0):
		self.tag = tag
		self.count = count
		self.max = -1
		self.maxRec = ""
		self.min = 1000

class FieldCounter (UserDict):
	"""
	UserDict used to store information about field/term counts, keyed by field
	name
	"""
	def __init__ (self, dir):
		UserDict.__init__ (self)
		self.dir = dir
		self.recordCount = 0
		self.processDir ()
		self.report()

	def processDir (self):
		for filename in os.listdir (self.dir):
			path = os.path.join (self.dir, filename)
			rec = XmlRecord (path=path)
			self.processRecord (rec)


	def processRecord (self, rec):
		"""
		tally the fields. first make a map of occurrances for the record, then
		merge record map into global map
		"""
		recordData = {}
		for element in XmlUtils.getChildElements (rec.doc):
			tag = element.tagName
			text = XmlUtils.getText(element).strip()
			if not recordData.has_key (tag):
				recordData[tag] = 0
			recordData[tag] = recordData[tag] + 1

		## now enter data into global tally
		for tag in recordData.keys():
			if not self.has_key(tag):
				self[tag] = Entry (tag)
			entry = self[tag]
			entry.count = entry.count + recordData[tag]
			entry.max = max (entry.max, recordData[tag])
			if entry.max == recordData[tag]:
				entry.maxRec = os.path.split (rec.path)[1]
			entry.min = min (entry.min, recordData[tag])

		for entry in self.values():
			if entry.tag in recordData.keys():
				continue
			entry.min = 0
				
		self.recordCount = self.recordCount + 1


	def report (self):
		"""
		report the tally
		"""
		print "Report (%d records)" % self.recordCount
		for entry in self.values():
			print "%s: %d (%0.2f) max: %d min: %d" % (entry.tag,\
											  entry.count, \
											  float(entry.count)/self.recordCount, \
											  entry.max, entry.min)
			
			

def tester ():
	fc = FieldCounter (technotesDir)
	rec = XmlRecord (path=os.path.join (technotesDir, "DR000537.xml"))
	fc.processRecord (rec)
	fc.report ()

if __name__ == "__main__":
	fc = FieldCounter (technotesDir)

