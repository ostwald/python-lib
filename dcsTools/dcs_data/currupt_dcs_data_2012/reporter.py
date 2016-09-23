"""
Corrupt record report
"""
import os, sys, re, urllib
from html import HtmlDocument
from HyperText.HTML import *
from JloXml import XmlRecord, XmlUtils, StatusElement, DcsDataRecord
from dcsTools.dcs_data.dcs_data_repo_scanner import threshold
from collection_info import *

host = os.environ['HOST']
print 'host', host

if host == 'acornvm':
	base_dir = '/users/Home/ostwald/python-lib/dcsTools/dcs_data'
else:
	raise Exception, "unknown host: %s" % host
data_dir = os.path.join (base_dir, 'currupt_dcs_data_2012')

repo_config = {
	"nsdl" : {
		'baseUrl': 'http://ncs.nsdl.org/mgr',
		'collectionOfCollections': '1201216476279',
		'collection_info_constructor' : NSDLCollectionInfo,
		'data': 'data/nsdl.xml'
		},
	"ncar_lib": {
		'baseUrl': 'http://nldr.library.ucar.edu/schemedit',
		'collectionOfCollections': 'collections',
		'collection_info_constructor' : NcarLibCollectionInfo,
		'data' : 'data/ncar_lib.xml'
		},
	"dlese": {
		'baseUrl': 'http://dcs.dlese.org/schemedit',
		'collectionOfCollections': 'dcr',
		'collection_info_constructor' : DleseCollectionInfo,
		'data' : 'data/dlese.xml'
		}
}

current_repo = "dlese"

class Node:
	
	child_constructor = None
	child_selector = None
	my_css_class = None
	
	def __init__ (self, element):
		self.element = element
		try:
			self.name = element.getAttribute('name')
		except AttributeError, msg:
			print "could not get name attribute: %s" % msg
			print self.element.toxml()
		self.children = self.getChildren()
		
	def __cmp__ (self, other):
		return cmp(self.name, other.name)
		
	def getChildren (self):
		"""
		this method will raise Exception because constructor and selector are
		not defined.
		"""
		children = map (self.child_constructor, 	
					self.element.getElementsByTagName (self.child_selector))
		children.sort()
		return children

	def getRecordIds(self):
		ids = []
		for child in self.children:
			ids += child.getRecordIds()
		return ids
					
	def showChildren(self, indent=None):
		if indent is None:
			indent = ''
		for child in self.children:
			if child.isBarren():
				continue
			if not hasattr(child, 'name'):
				print "no name!"
				print child.element.toxml()
				print '%s- %s' % (indent, "NoNAME")
			else:
				# print '%s- %s' % (indent, child.name)
				print '%s- %s (%s)' % (indent, child.name, child.__class__.__name__)
			
			child.showChildren(indent+'  ')
			
	def getEditLink(self):
		return None
			
	def getHtmlHeader(self):
		content = self.getEditLink() or self.name
		if self.__class__ != Record:
			content = "%s (%d)" % (content, len(self.getRecordIds()))
		return DIV (content, klass=self.my_css_class, id=self.name)
			
	def render (self, parent):
		if self.isBarren(): return
		header = self.getHtmlHeader()
		if (header):
			parent.append(header)
		body = DIV(klass="indent")
		parent.append(body)
		for child in self.children:
			child.render(body)
			
	def isBarren (self):
		"""
		has no Records as descendents
		"""
		for child in self.children:
			if not child.isBarren():
				return False
				
		return True

class Record (Node):
	
	child_constructor = StatusElement
	child_selector = 'statusEntry'
	my_css_class = 'record'
	
	def __init__ (self, element):
		"""
		element is the statusEntries element from a DcsDataRecord,
		with the recordId represented as an attribute
		e.g., 
		<statusEntries recordId="NASA-Edmall-640">
          <statusEntry>
            <status>Needs QA</status>
			...
		"""
		Node.__init__(self, element)
		self.id = self.element.getAttribute ('recordId')
		self.name = self.id
	
	def getChildren (self):
		"""
		this method will raise Exception because constructor and selector are
		not defined.
		"""
		# return map (self.child_constructor, 	
					# self.element.getElementsByTagName (self.child_selector))
		children = Node.getChildren(self)
		# print "unsorted"
		# for child in children:
			# print ' - %s (%d)' % (child.changeDate, child.timeStamp)
		children.sort (cmp=lambda x, y: self.statusEntryCompare(x,y))
		# print "sorted"
		# for child in children:
			# print ' - %s (%d)' % (child.changeDate, child.timeStamp)
		# children.sort (cmp=lambda x, y: cmp(x.timeStamp, y.timeStamp))
		return children
		
	def statusEntryCompare (self, s1, s2):
		d1 = s1.timeStamp
		d2 = s2.timeStamp
		if d1 < d2: return 1
		if d1 > d2: return -1
		return 0
		
	def isBarren(self):
		"""
		a Record is not barren by definition
		"""
		return False
	
	def getRecordIds(self):
		return [self.id]
		
	def getCurrentStatus (self):
		"""
		last element in the list is current
		"""
		if not self.children: return None
		return self.children[0]
	
	def getBogusStatus(self):
		for status in self.children:
			if status.timeStamp < threshold:
				return status
		
	def getFinalStatuses(self):
		finals=[];add=finals.append
		for child in self.children:
			if child.status.startswith("_|-final-"):
				add(child)
		return finals
				
	def showChild (self, child, indent=None):
		if indent is None:
			indent = ''
		statusFlag = child.status.startswith("_|-final-") and "Done" or child.status
		print '%s- %s (%s) - %s' % (indent, child.changeDate, child.editor, statusFlag)
		print '%s "%s"' % (indent, child.statusNote)
	
	def showChildren(self, indent=None):
		if indent is None:
			indent = ''
		# for status in self.children:
			# self.showChild (status, indent+'  ')
		self.showChild (self.getCurrentStatus(),  indent+'  ')
		self.showChild (self.getBogusStatus(),  indent+'  ')
		
	def getEditLink (self):
		"""
		do a search for this record
		https://ncs.nsdl.org/mgr/browse/query.do?s=0&searchMode=id&q=MATH-PATH-000-000-001-370&vld=&resultsPerPage=10
		"""
		href = "%s//browse/query.do?s=0&searchMode=id&q=%s" % (repo_config[current_repo]['baseUrl'], self.name)
		# href = "%s/editor/edit.do?command=edit&recId=%s" % (repo_config[current_repo]['baseUrl'], self.name)
		return Href (href, self.name, target="_edit")
		
	def render (self, parent):
		"""
		render html for this Record
		- header is the recordId, linked to the repository
		- current status
		- corrupt Status
		"""
		header = self.getHtmlHeader()
		if (header):
			parent.append(header)
		body = DIV()
		parent.append(body)
		currentStatus = self.getCurrentStatus()
		if currentStatus is None:
			print 'current status not found'
			print self.element.toxml()
		
		bogusStatus = self.getBogusStatus()
		if bogusStatus is None:
			print 'bogus status not found'
			print self.element.toxml()
			
		finalStatuses = filter (lambda x:x != bogusStatus and x != currentStatus, self.getFinalStatuses())
			
		wrapper = DIV(klass="status-entry")
		wrapper.append( SPAN("current status: ", klass="current-status"))
		body.append (wrapper)
		self.renderStatus (currentStatus, wrapper)
		
		if finalStatuses:
			for finalStatus in finalStatuses:
				wrapper = DIV(klass="status-entry")
				wrapper.append( SPAN("final status: ", klass="final-status"))
				body.append (wrapper)
				self.renderStatus (finalStatus, wrapper)
				
		wrapper = DIV(klass="status-entry")
		wrapper.append( SPAN("corrupt status: ", klass="corrupt-status"))
		body.append (wrapper)
		self.renderStatus (bogusStatus, wrapper)

	def renderStatus (self, entry, parent):
		"""
		create html for the provided statusEntry
		"""
		# parent.append(wrapper)
		changeDate = SPAN(entry.changeDate, klass="changeDate")
		editor = SPAN(entry.editor, klass="editor")
		statusFlag = entry.status.startswith("_|-final-") and "Done" or entry.status
		status = SPAN(statusFlag, klass="status")
		statusNote = DIV(entry.statusNote, klass="statusNote")
		parent.append(SPAN ('%s (%s) - %s' % (changeDate, editor, status)))
		parent.append(statusNote)
			

class Collection (Node):
	
	child_selector = 'statusEntries' # this selects records
	child_constructor = Record
	my_css_class = "collection"
	
	def __init__ (self, element):
		Node.__init__(self, element)
		self.key = element.getAttribute('key')
		self.name = self.key
		
	def getEditLink (self):
		repository_context = repo_config[current_repo]['baseUrl']
		baseHref = "%s/browse/query.do" % repository_context # ?command=edit&recId=%s" % (repository_context, self.name)
		params = {
			's' : '0',
			'searchMode' : 'id',
			'q' : ' OR '.join(self.getRecordIds())
			}
		href = baseHref + '?' + urllib.urlencode(params)
		try:
			collectionName = HELPER.getCollectionInfo(self.name).title
		except:
			collectionName = self.name
		return Href (href, collectionName, target="_edit")
	# https://ncs.nsdl.org/mgr/browse/query.do?s=0&searchMode=id&q=MATH-PATH-000-000-000-179%20OR%20MATH-PATH-000-000-000-078&vld=&resultsPerPage=10

class Format (Node):
	
	child_selector = 'collection' # this selects records
	child_constructor = Collection
	my_css_class = "format"
	
	def getChildren(self):
		children = map (self.child_constructor, 	
					self.element.getElementsByTagName (self.child_selector))
		return filter (lambda x:x.name != repo_config[current_repo]['collectionOfCollections'], children)
	
class Repository (Node):
	
	child_selector = 'format' # this selects records
	child_constructor = Format
	my_css_class = "repository"
	
	def getHtmlReport (self):
		title = self.name + " report"
		javascript = ["prototype.js", "report_script.js"]
		stylesheet = 'styles.css'
		doc = HtmlDocument (title=title, javascript=javascript, stylesheet=stylesheet)
		doc.body.append (H1(title))
		self.render(doc.body)
		dest = "html/%s.html" % self.name
		print "dest", dest
		fp = open(dest, 'w')
		fp.write (doc.__str__())
		fp.close()
		print "wrote report to ", dest
		
class ReporterHelper:
	
	def __init__ (self):
		self.config = repo_config[current_repo]
		CollectionInfoSearcher.collection_info_constructor = self.config['collection_info_constructor']
		self.searcher = CollectionInfoSearcher(self.config['collectionOfCollections'], "", self.config['baseUrl']+'/services/ddsws1-1')
		
	def getCollectionInfo (self, key):
		return self.searcher.getCollectionInfo (key)
		
HELPER = None
		
def collectionTester (record, format, collectionKey):
	collections = record.selectNodes (record.dom, 'repository:format:collection')
	for collectionEl in collections:
		if collectionEl.getAttribute('key') == collectionKey:
			return Collection (collectionEl)
	return None

def formatTester(record, formatToShow=None):
	formats = record.selectNodes (record.dom, 'repository:format')
	print "%d formats found" % len(formats)
	# format = Format(formats[0])
	for formatElement in formats:
		format = Format (formatElement)
		# print 'format %s has %d children' % (format.name, len (format.children))
		if formatToShow == None or format.name == formatToShow:	
			format.showChildren()

def recordTester (path):
	dcsData = DcsDataRecord (path=path)
	element = dcsData.entriesElement
	element.setAttribute("recordId", dcsData.getId());
	# print element.toxml()
	rec = Record(element)
	# parent = DIV()
	# rec.render(parent)
	# print parent
	print "\nrecordTeter"
	for child in rec.children:
		print "- %s (%s)" %(child.changeDate, child.timeStamp)
			
if __name__ == '__main__':
	data = os.path.join(data_dir, repo_config[current_repo]['data'])
	record = XmlRecord(path=data)
	if 0:
		reporter = Reporter('mgr')
		print "%d collections" % len(reporter.searcher.collections)
		
	if 1:
		HELPER = ReporterHelper()
		repository = Repository(record.doc)
		# repository.showChildren()
		root = DIV()
		# repository.render(root)
		repository.getHtmlReport()
		
	if 0:
		col = collectionTester (record, 'math_path', '1278566073520')
		if col.isBarren():
			print "BARREN"
		else:
			print "NOT barren"
	if 0:
		path = "/users/Home/ostwald/tmp/corrupt_dcs_data_11_2012/lib_dcs_data/osm/osgc/OSGC-000-000-000-063.xml"
		recordTester (path)
		
