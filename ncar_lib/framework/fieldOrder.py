

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

class FieldOrder (UserDict):
	"""
	UserDict used to store information about field/term counts, keyed by field
	name
	"""
	def __init__ (self, dir):
		UserDict.__init__ (self)
		self.dir = dir
		self.recordCount = 0
		self.processDir ()
		self.writeOrders()
		self.report()

	def processDir (self):
		for filename in os.listdir (self.dir):
			path = os.path.join (self.dir, filename)
			rec = XmlRecord (path=path)
			order = self.processRecord (rec)
			key = self.makeKey (order)
			if not self.has_key (key):
				self[key] = 0
			self[key] = self[key] + 1

	def makeKey (self, list):
		return ','.join (list)

	def processRecord (self, rec):
		"""
		tally the fields. first make a map of occurrances for the record, then
		merge record map into global map
		"""
		elementOrder = []
		for element in XmlUtils.getChildElements (rec.doc):
			tag = element.tagName
			if not elementOrder or (tag != elementOrder[-1]):
				elementOrder.append (tag)

		self.recordCount = self.recordCount + 1
		return elementOrder

	def writeOrders (self):
		path = "elementOrders.txt"
		fp = open (path, 'w')
		fp.write ('\n'.join (self.keys()))
		fp.close()
		print "wrote to %s" % path

	def report (self):
		"""
		report the tally
		"""
		print "Report - %d different orders for %d records" % (len (self.keys()), self.recordCount)
		
		for key in self.keys():
			# print key
			pass
		threshold = 17
		print "orders having at least %d members" % threshold
		for key in self.getLongest (threshold):
			print key

	def getLongest (self, threshold):
		longest = []
		for key in self.keys():
			length = len(key.split(','))
			# print "length: %d" % length
			if length >= threshold:
				longest.append (key)
		return longest
	
			
def tester ():
	fc = FieldOrder (technotesDir)
	rec = XmlRecord (path=os.path.join (technotesDir, "DR000537.xml"))
	order = fc.processRecord (rec)
	print order

if __name__ == "__main__":
	## tester()
	fc = FieldOrder (technotesDir)

