import os, sys
import util
from StdDocument import StdDocument

class AsnFileTester (StdDocument):
	
	writeBadFiles = False
	
	def __init__ (self, path):
		self.path = path
		StdDocument.__init__ (self, path)
		self.missingStandards = self.getMissingNodes()
		
		print "\n%s" % os.path.basename (path)
		if self.missingStandards:
			if self.writeBadFiles:
				self.write ()
			print "\t%d MISSING standards" % len(self.missingStandards)
			for m in self.missingStandards:
				print "\t",m	
		else:
			print "\tOK"
	
	def getMissingNodes (self):
		missing = []
		for id in self.keys():
			std = self[id]
			if std.children:
				# print "%s (%d)" % (id, len(std.children))
				for childId in std.children:
					# print "\t%s" % childId
					if not self[childId]:
						missing.append (childId)
		return missing
		
	missing_by_traversal = []
		
	def checkNodeStructure (self):
		self.visit (self.root.id)
		return self.missing_by_traversal
	
	def visit (self, id):
		std = self[id]
		if std.children:
			# print "%s (%d)" % (id, len(std.children))
			for childId in std.children:
				# print "\t%s" % childId
				if not self[childId]:
					self.missing_by_traversal.append (childId)
				else:
					self.visit (childId)
					
	def write (self):
		path = self.asnRecord.path
		util.beautify (path, os.path.join ("badDocs", os.path.basename(path)))
					
		
def dirTest (dir):
	print "\nChecking %s\n" % dir
	for filename in os.listdir (dir):
		if not filename.lower().endswith (".xml"): continue
		path = os.path.join (dir, filename)
		tester = AsnFileTester (path)
			
def fileTest ():
	dir = "/Documents/Work/DLS/ASN/globe/"
	# filename = "1.4.1Math-2000-National Council of Teachers of Mathematics (NCTM)-Principles and Standards for School.xml"
	filename = "Math-2000-National Council of Teachers of Mathematics (NCTM)-Principles and Standards for School.xml"
	path = os.path.join (dir, filename)
	print "\nChecking %s\n" % path
	AsnFileTester (path)

	
if __name__ == '__main__':
	# fileTest()
	dirTest ("/Documents/Work/DLS/ASN/globe/")
