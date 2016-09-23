"""
docDiff - compare two XML Records and produce a list of all the xpaths where
the two docs are different (including missing)
"""
from JloXml import XmlUtils, XmlRecord
from UserList import UserList



class DocDiff(UserList):
	
	def __init__ (self, doc1, doc2):
		self.data = []
		self.doc1 = doc1
		self.doc2 = doc2
		self.comparePath (doc1.doc.tagName)
		
	def comparePath (self, path):
		print "\ncomparing %s" % path
		
		if self.doc1.getTextAtPath (path) != self.doc2.getTextAtPath(path):
			self.append(path)
		
		doc1Siblings = self.doc1.selectNodes (self.doc1.dom, path)
		if len(doc1Siblings) > 1:
			print "mulitple doc1 siblings at %s!!" % path
			return
		
		doc1Children = self.doc1.getElements (doc1Siblings[0])
		if not doc1Children:
			print "no doc1 children at %s" % path
			return
		print "%d doc1 children at %s" % (len(doc1Children), path)
		for child in doc1Children:
			self.comparePath (path+"/"+child.tagName)
			
if __name__ == '__main__':
	# from utils import getDiskRecord
	# docA = getDiskRecord ("PUBS-000-000-000-400")
	# docB = getDiskRecord ("PUBS-NOT-FY2010-000-000-000-734")	
	XmlRecord.xpath_delimiter = "/"
	docA = XmlRecord(path="cmp-docs/doc1.xml")	
	docB = XmlRecord(path="cmp-docs/doc2.xml")	
	dd = DocDiff (docA, docB)
	print "\n-------------\ndiff paths"
	for path in dd:
		print path
