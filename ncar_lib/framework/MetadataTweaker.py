

"""
traverse all the technote metadata and tweak records so they can play in the DCS:
	- noNamespaceSchemaLocation="http://www.dls.ucar.edu/people/ostwald/Metadata/webcat/webcat-record.xsd">
	- ID (base on AccessionNum)
	- URL (also based on AccessionNum) http://www.library.ucar.edu/uhtbin/hyperion-image/<AccessionNum>
"""

import os
from JloXml import XmlRecord, XmlUtils

technotesDir = "../NCAR Technical Notes"

def makeId (accessionNum):
	idNum = int (accessionNum[2:])
	thousands = idNum / 1000
	## print "thousands: %d" % thousands
	ones = idNum % 1000
	## print "ones: %d" % ones
	id = "TECH-NOTE-000-000-%03d-%03d" % (thousands, ones)
	return id

class MetadataTweaker:
	"""
	UserDict used to store information about field/term counts, keyed by field
	name
	"""
	def __init__ (self, dir):
		self.dir = dir
		self.recordCount = 0
		self.processDir ()
		# self.report()

	def processDir (self):
		for filename in os.listdir (self.dir):
			path = os.path.join (self.dir, filename)
			rec = XmlRecord (path=path)
			self.processRecord (rec)

		
	def processRecord (self, rec):
		"""
			add namespace info
			add RecordID, Url elements
		"""
		
		rec.doc.setAttribute ("xmlns:"+rec.schema_instance_namespace, \
								rec.SCHEMA_INSTANCE_URI)
		rec.setNoNamespaceSchemaLocation ( \
			"http://www.dls.ucar.edu/people/ostwald/Metadata/webcat/webcat-record.xsd")
		
		accessionNum = self.getAccessionNum (rec)
		# print "%d (%s)" % (idNum, type(idNum))
		# print accessionNum, id
		
		url = "http://www.library.ucar.edu/uhtbin/hyperion-image/" + accessionNum
		urlElement = rec.dom.createElement ("Url")
		XmlUtils.setText(urlElement, url)
		
		id = makeId (accessionNum)
		idElement = rec.dom.createElement ("RecordID")
		XmlUtils.setText(idElement, id)
		
		children = XmlUtils.getChildElements (rec.doc)
		rec.doc.insertBefore (urlElement, children[0])
		rec.doc.insertBefore (idElement, urlElement)
		
		# print rec
		rec.write ()
		print accessionNum
		
	def getAccessionNum (self, rec):
		return XmlUtils.getChildText (rec.doc, "AccessionNum")
				
		self.recordCount = self.recordCount + 1


	def report (self):
		"""
		report the tally
		"""
		print "Report (%d records)" % self.recordCount
			

def tester ():
	fc = MetadataTweaker (technotesDir)
	rec = XmlRecord (path=os.path.join (technotesDir, "DR000537.xml"))
	fc.processRecord (rec)
	# fc.report ()

if __name__ == "__main__":
	fc = MetadataTweaker (technotesDir)
	# tester()

