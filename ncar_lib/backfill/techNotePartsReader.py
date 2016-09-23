import sys, os, time, math
from ncar_lib.lib import globals, webcatUtils
from UserDict import UserDict
from spreadSheetReader import SpreadSheetReader, Entry

class TNEntry (Entry):
	key_field = "DR Number"

	def getIssue (self):
		return self.getFieldValue ("TN ISSUE")
		
	def getDrNum (self):
		return self.getFieldValue ("DR Number")
	
class TNFolder (TNEntry):
	
	def __init__ (self, line, schema):
		Entry.__init__ (self, line, schema)
		# issue = self.getFieldValue ("TN ISSUE").strip()
		issue = self.getIssue()
		if not issue.lower().endswith ("folder"):
			raise Exception, issue
		self.name = issue[:-len("folder")].strip()
		# print self.name
		self.children = []

	def cmp (self, other):
		return webcatUtils.tnCmp (self.name, other.name)

		
class TNSheetReader (SpreadSheetReader):

	key_field = "DR Number"
	issueNames = []
	drMap = UserDict()
	
	def processLines (self, lines):
		"""
		each successfully processed line is a Payment (if a date cannot be parsed,
		an Exception is raised and that line is not processed)
		"""
		folder = None
		uniqueIssues = []
		for line in lines:
			try:
				entry = TNEntry (line, self.schema)
				drNum = entry.getDrNum()
				self.drMap[drNum] = entry
				issue = entry.getFieldValue("TN ISSUE")
				if issue in uniqueIssues:
					msg = "dup issue (%s)" % issue
				uniqueIssues.append (issue)
				if issue.lower().endswith ("folder"):
					folder = TNFolder (line, self.schema)
					self[folder.name] = folder
				else:
					# key = entry.getFieldValue (entry.key_field)
					# if folder.has_key (key):
						# msg = "duplicate key (%s)" % key
						# raise Exception, msg
					folder.children.append(entry)

			except "ValueError":
				# print sys.exc_info()[0], sys.exc_info()[1], sys.exc_info()[2]
				print sys.exc_info()[0], sys.exc_info()[1]
				print line
				pass
		self.issueNames = uniqueIssues
		
	def getFolders (self):
		folders = self.values()
		folders.sort(TNFolder.cmp)
		return folders

def showFolders (reader):
	print "%d folders read" % len(reader.getFolders())
	for f in reader.getFolders():
		print f.name
		
def showDrMap (reader):
	print "DR Number Map"
	drMap = reader.drMap
	keys = drMap.keys()
	keys.sort()
	for drNum in keys:
		entry = drMap[drNum]
		print "%s %s" % (drNum, entry.getIssue())
		
if __name__ == "__main__":
	
	path = os.path.join (globals.docBase, "backfill/DR numbers for TN parts.txt")
	reader = TNSheetReader (path)
	showDrMap (reader)
