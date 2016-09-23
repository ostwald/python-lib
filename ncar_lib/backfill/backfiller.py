import os, sys, re
from UserDict import UserDict
from JloXml import XmlRecord, XmlUtils
from filler_imports import *
from ncar_lib.lib.frameworks import LibraryDCRec, NCARRec


# mapper maps from accessionNum to ID (e.g., id = mapper[num])
mapper = accessionNumMappings.AccessNumMapping(globals.mappingDataPath)
verbose = True

class DrMap (UserDict):
	"""
	obtains (normalized) issue from tnNote spreadsheet for given DR number
	"""
	from techNotePartsReader import TNSheetReader
	
	path = os.path.join (globals.docBase, "backfill/DR numbers for TN parts.txt")
	reader = TNSheetReader (path)
	
	def __init__ (self):
		UserDict.__init__ (self, self.reader.drMap.data)
	
	def getIssue(self, dr):
		return self.normalize (self[dr].getIssue())
		
	def normalize (self, issue):
		for pat in ['Pt.', 'part', 'Pt', 'pt.', 'pt']:
			if pat in issue:
				issue = issue.replace (pat, 'Part')
				break
		return issue
		
drMap = DrMap()

class CategoryRecord (NCARRec):
	"""
	encapsulates xml record representing a FolderRecord, which was
	created by "FolderScraper", which created WebCatFolder instances 
	(using data from the webcat folder metadata and also from the WebCat
	hierarchy of nodes)
	
	in particular, each CategoryRecord holds information about its children,
	which we will use to grab the library_dc records and populate their
	fields with data from the CategoryRecord, such as:
		- issue
		- creators
		- contributors
	"""
	rootElementName = 'record'
	updating = 0
	
	def __init__ (self, path):
		XmlRecord.__init__ (self, path=path)
		self.children = self._get_children()
		self.creators = self.getFieldValues ("creator")
		self.contributors = self.getFieldValues ("contributor")
		self.title = self.getFieldValue ("title")
		self.issue = self.getFieldValue ("tn_isssue")
		self.accessionNum = self.getFieldValue ("accessionNum")
		
		self.creators.sort()
		self.contributors.sort()
			
	def _get_children (self):
		children = []
		nodes = self.selectNodes (self.dom, "children/child")
		# print "%d children found" % len (nodes)
		for node in nodes:
			# children.append (XmlUtils.getText (node))
			try:
				children.append (Child (node))
			except:
				print sys.exc_info()[1]
				print self.path
				sys.exit()
		return children
		
	def cmp (self, other):
		return webcatUtils.tnCmp (self.issue, other.issue)
		
	def updateChildren (self):
		# for child in self.children:
			# self.updateChild (child)
		map (self.updateChild, self.children)
		
	def updateChild (self, child):
		"""
		compare issue, creator and contributor fields with specified child
		"""
		diff = False
		s = [];add=s.append
		# if not child.issue or (child.issue and (self.issue != child.issue)):
			# add ("issue: %s (%s)" % (child.issue, self.issue))
			
		normalizedIssue = drMap.getIssue (child.accessionNum)
		
		if self.updating:
			child.setIssue (normalizedIssue)
			if (child.getIssue() != normalizedIssue):
				raise Exception, "issue not normalized for %s" % child.accessionNum
		else:
			# diagnostic (no longer used)
			if child.getIssue() and not normalizedIssue.startswith (child.getIssue()):
				raise Exception, "normalized: '%s'  child: %s" % (normalizedIssue, child.getIssue())
			add ("Issue: '%s' (was: '%s')" % (normalizedIssue, child.getIssue()))
			
		# add ("Title: '%s'" % child.rec.getTitle())
			
		if self.updating:
			for attr in ["creators", "contributors"]:
				self.updateDcMultiField (child, attr)
		
		for attr in ["creators", "contributors"]:
			dcField = "dc:"+attr[:-1]  # take off the "s"
			parentVals = getattr (self, attr)
			childVals = child.rec.getFieldValues (dcField)
			if parentVals != childVals:
				missing = []
				for val in parentVals:
					if not val in childVals:
						missing.append (val)
				if missing:
					add ("missing %s" % attr)
					for val in missing:
						add ("\t%s" % val)

		if s:
			print "\n%s (%s)" % (child.recId, child.accessionNum)
			print "\n".join(s)
			
		if self.updating:
			try:
				child.rec.orderFields()
			except:
				print "couldn't update %s: %s" % (child.recId, sys.exc_info()[1])
				return
			# print child.rec
			child.rec.write()
			print 'updated %s' % child.rec.path
		
	def updateDcMultiField (self, child, attr):
		parentVals = getattr (self, attr)
		dcField = "dc:"+attr[:-1]  # take off the "s"
		childVals = child.rec.getFieldValues (dcField)
		if parentVals != childVals:
			missing = []
			for val in parentVals:
				if not val in childVals:
					missing.append (val)
			if missing:
				print ("adding missing %s" % attr)
				for val in missing:
					print ("\t%s" % val)
					child.rec.addFieldValue (dcField, val)
					
	def report (self):
		"""
		report this folder in a way that can be compared with spreadsheet
		"""
		s=[];add=s.append
		add ("%s\t%s folder\t%s" % (self.accessionNum, self.issue, self.title))
		for child in self.children:
			add ("%s\t%s\t%s" % (child.accessionNum, child.getIssue(), child.title))
		return '\n'.join (s)
		
class RecNotFound (Exception):
	pass
		
class Child:
	def __init__ (self, element):
		self.accessionNum = element.getAttribute ("accessionNum")
		if (not self.accessionNum):
			raise Exception, "accessionNum not found: %s" % element.toxml()
		
		self.rec = getLibraryDCRec (self.accessionNum)

		if (not self.rec):
			raise RecNotFound, "library_dc rec not found for %s" % self.accessionNum
			
		self.recId = self.rec.getId()
		self.title = self.rec.getTitle()
		# self.issue = self.rec.getIssue()
		# self.creators = self.rec.getCreators()
		# self.contributors = self.rec.getContributors()
		
	def getCreators (self):
		ret = self.rec.getCreators()
		ret.sort()
		return ret
		
	def getContributors (self):
		ret = self.rec.getContributors()
		ret.sort()
		return ret
		
	def getIssue (self):
		return self.rec.getIssue()
		
	def setIssue (self, val):
		return self.rec.setIssue(val)
		
def getLibraryDCRec(accessionNum):
	"""
	get library_dc record from accessionNum
	"""
	id = drNum2RecId(accessionNum)
	
	path =  webcatUtils.getRecordPath (id)
	if not os.path.exists (path):
		raise RecNotFound, "File does not exist at '%s'" % path
		
	rec = LibraryDCRec (path)
	# print rec
	return rec
	
class BackFiller:
	"""
	records are CategoryRecord instances, children are LibraryDCRec instances
	"""
	def __init__ (self, dirname="NCAR Technical Notes"):
		self.drNumMap = DrMap()
		self.dataDir = os.path.join (globals.develBase, 'backfill/WebCatFolderData', dirname)
		self.records = self.read()
		
	def read (self):
		records = []
		for filename in os.listdir(self.dataDir):
			if filename[0] == '.': continue
			path = os.path.join (self.dataDir, filename)
			rec = CategoryRecord (path=path)
			if "NCAR Technical Notes" in rec.title:
				if verbose:
					print "Skipping '%s'" % rec.title
			else:
				records.append (rec)
		records.sort(CategoryRecord.cmp)
		return records
	
	def report (self, reclist=None, reporter=None):
		"""
		make a display that can be compared with spreadsheet
		"""
		reclist = reclist or self.records
		for rec in reclist:
			# print "%s -> %s" % (rec.issue, rec.title)
			if not reporter:
				print "\n", rec.report()
			else:
				reporter(rec)
				
	def select (self, fn):
		selected = []
		for rec in self.records:
			if fn(rec):
				selected.append (rec)
		selected.sort (CategoryRecord.cmp)
		return selected
		
	def query (self, filter, reporter=None):
		selected = self.select (filter)
		self.report (selected, reporter)
		
	def updateRecordChildren (self):
		for rec in self.records:
			rec.updateChildren()
		
def reporter (rec):
	print '%15s %25s\t%s' % (rec.accessionNum or "no DR Number", rec.issue, rec.title)
	
def isPdfTitle (title):	
	if title[-1] == '.': title = title[:-1]
	if title.lower().endswith ("pdf"):
		return 1
		
def pdfTitleFilter (rec):
	for child in rec.children:
		title = child.rec.getTitle()
		if isPdfTitle (title):
			return 1
		
def pdfTitleReporter (rec):
	for child in rec.children:
		title = child.rec.getTitle()
		if isPdfTitle (title):
			print "\n%s\n\t%s" % (child.recId, child.rec.getTitle())
			
def recordTester ():
	filename = '17.xml'
	dirname = 'NCAR Technical Notes'
	path = os.path.join (globals.develBase, 'backfill/WebCatFolderData', dirname, filename)
	rec = CategoryRecord (path=path)
	rec.updateChildren()
		
if __name__ == '__main__':
	if 0:
		recordTester ()
	elif 1:
		bf = BackFiller()
		bf.updateRecordChildren()
	else:
		bf = BackFiller()
		bf.query (pdfTitleFilter, pdfTitleReporter)
		
