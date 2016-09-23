"""
Tools for comparing duplicates (by pubId) accross pubs-ref and not-fy10 collections

how many dups are there?

look at a few and see if any patterns emerge
- test assumptions by writing scripts (e.g., are all not-fy10 items different from their pubs-ref counterparts
in the same way?)
"""
import os, sys, time
from HyperText.HTML40 import *
from html import HtmlDocument
from UserDict import UserDict
from UserList import UserList
from JloXml import XmlRecord, XmlUtils
from grouping_data import RecordInfo
from recordCompareHTML import RecordCompareHtml
from ncar_lib.dups.utils import getCollectionKey, getPrettyTimeStr
import comparisonText

class DupGroup (UserList):
	"""
	- key - the grouping key for this group
	- UserList API exposes RecordInfo instances as items
	"""
	def __init__ (self, element):
		self.data = []
		self.key = element.getAttribute('key')
		self.groupNum = element.getAttribute('groupNum')
		map (self.append, map (RecordInfo, XmlUtils.getChildElements(element)))

	def getDiff (self):
		"""
		display hints for Display
		for now - contains paths where there is a difference
		between two docs
		"""
		paths = []
		return paths
		
	def asListingHtml (self):
		allfields = ['title', 'pubName', 'recId', 'status']
		fields = ['title', 'pubName', 'status']
		groupTable = TABLE(klass='dup-group')
		hdr = TR ()
		map (lambda x:hdr.append(TH (x)), fields)
		groupTable.append (hdr)
		for recInfo in self:
			recordRow = TR()
			map (lambda x:recordRow.append(TD (x)), 
				 map(lambda x:getattr(recInfo, x), fields))

			
			groupTable.append(recordRow)
		return groupTable

class ComparisonManager (UserDict):
	"""
	reads cached comparison info from disk
	"""
	
	grouping_data_dir = 'grouping_data'
	max_dups = 5000
	
	def __init__(self, grouping):
		self.data = {}
		path = os.path.join (self.grouping_data_dir, grouping+'Map.xml')
		self.rec = XmlRecord(path=path)
		groupNodes = self.rec.selectNodes (self.rec.dom, 'dupGroups:group')
		print '%d dup nodes found' % len(groupNodes)
		for groupNode in groupNodes[:self.max_dups]:
			dupGroup = DupGroup (groupNode)
			key = dupGroup.key
			self[key] = dupGroup
		print 'comparisonManager ingested %d dupGroups' % len(self.keys())
		
	def writeListingHtml (self):
		"""
		create an html document that shows the groups and provides access to
		side-by-side display
		"""
		datapath = self.rec.path
		root, ext = os.path.splitext(os.path.basename (datapath))
		self.name = root
		htmlDoc = DuplicateGroupListingHTML(self, self.name)
		htmlDoc.write()
		
	def writeComparisonPages (self):
		baseDir = os.path.join ('html', self.name+'_data')
		if not os.path.exists(baseDir):
			os.mkdir (baseDir)
			
		for key in self.keys():
			returnUrl = '../%s.html?groupNum=%s' % (self.name, self[key].groupNum)
			compareHtml = RecordCompareHtml(self[key], self.name, returnUrl)
			compareHtml.write (os.path.join (baseDir, self[key].groupNum+'.html'))
		
	def keys (self):
		sorted = self.data.keys()
		sorted.sort()
		return sorted

class DuplicateGroupListingHTML:
	
	def __init__ (self, dupMap, title):
		
		self.name = title
		self.dupMap = dupMap
	
	def makeHtmlDoc (self):
		"""
		Generate the html document as string
		"""
		## title = os.path.splitext(self.filename)[0]
		title = comparisonText.getTitle(self.name)
		doc = HtmlDocument (title=title, stylesheet="resources/dup-listing-styles.css")
		# doc.body["onload"] = "init();"
		
		# <meta http-equiv="Content-Type" content="text/html; charset=iso-8859-1">
		
		doc.head.append (META(http_equiv="Content-Type",
                          content="text/html; charset=utf-8"))
		
		doc.addJavascript ("resources/prototype.js")
		doc.addJavascript ("resources/listing-scripts.js")
		doc.append (DIV (id="debug"))
		doc.append (H1 (title))
		
		doc.append (DIV ("this page was generated %s" % time.asctime(time.localtime()), id="page-date"))
		
		blurb = comparisonText.getBlurb(self.name)
		if blurb:
			doc.append (DIV (blurb, id='blurb'))
		
		doc.append (self.makeDupGroupsHtml())
		
		return doc	

	def makeDupGroupsHtml(self):
		html = DIV ()
		for key in self.dupMap.keys():
			dupGroup = self.dupMap[key]
			table = TABLE()
			row = TR()
			numberCell = TD (DIV(dupGroup.groupNum, klass="listing-group-num"))
			numberCell.append (IMG (src="resources/compare.png", border=0, 
							   id=dupGroup.groupNum, klass="compare-button"))
			row.append(numberCell)
			row.append(TD(dupGroup.asListingHtml()))
			table.append(row)
			html.append(table)
			
		return html
			
	def write (self, path=None):
		if path is None:
			path = 'html/%s' % self.name+'.html'
		fp = open(path, 'w')
		fp.write (self.makeHtmlDoc().__str__())
		fp.close()
		print 'wrote to ', path
		
if __name__ == '__main__':
	for group in ['TitlePubName', 'TitleGrouping']:
		cm = ComparisonManager(group)
		cm.writeListingHtml()
		cm.writeComparisonPages()

		
