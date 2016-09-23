# from JloXml import XmlRecord, XmlUtils
from xls import WorksheetEntry, XslWorksheet
from misc.titlecase import titlecase

"""
- read a bunch of titles from a spreadsheet.
- title case them
- write them as <xs:enumeration value="Publicly available"/> elements
"""

data = 'pubNames-for-NCAR-authored-books.txt'

class BookPubNameVocab (XslWorksheet):
	linesep = "\r\n"
	def __init__ (self):
		XslWorksheet.__init__ (self)
		self.read (data)
		
	def makePubName (self, entry):
		raw = entry['Title']
		title = titlecase (raw.strip().lower())
		return '<xs:enumeration value="%s"/>' % title
			
	def writeVocab (self, path):
		s=[];addme=s.append
		for entry in self.data:
			line = self.makePubName (entry)
			print line
			addme (line)
		fp = open (path, 'w')
		fp.write ("\n".join (s))
		fp.close()
		print "wrote to %s" % path
		
	
if __name__ == "__main__":
	vocab = BookPubNameVocab()
	vocab.writeVocab ("bookPubNames.xsd")
