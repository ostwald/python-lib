import os, sys, time
from HyperText.HTML40 import *
from html import HtmlDocument
# from termCompareGroup import TermCompareGroup, getTermCompareGroup
# from cmpRecHtml import CmpRecord
from side_by_side_HTML import SideBySideDisplay
import comparisonText

class RecordCompareHtml:
	"""
	displays comparison information for the provided DupGroup
		see comparisonManager module
	- dupGroup is a list of RecordInfo instances
	"""
	
	def __init__ (self, dupGroup, name, returnUrl=None):
		self.name = name
		self.dupGroup = dupGroup
		self.title = "Record Group #%s" % self.dupGroup.groupNum
		self.returnUrl = returnUrl

	def makeHtmlDoc (self):
		"""
		Generate the html document as string
		"""
		## title = os.path.splitext(self.filename)[0]
		title=self.title
		doc = HtmlDocument (title=title, stylesheet="../resources/record-compare-styles.css")
		# doc.body["onload"] = "init();"
		
		# <meta http-equiv="Content-Type" content="text/html; charset=iso-8859-1">
		
		doc.head.append (META(http_equiv="Content-Type",
                          content="text/html; charset=utf-8"))
		
		doc.addJavascript ("../resources/prototype.js")
		doc.addJavascript ("../resources/record-compare-scripts.js")
		if self.returnUrl:
			label = comparisonText.getTitle (self.name)
			doc.append (DIV (Href (self.returnUrl, "back to " + label), id="return-link"))
		doc.append (H1 (title))
		
		doc.append (DIV ("this page was generated %s" % time.asctime(time.localtime()), id="page-date"))
		
		blurb = comparisonText.getBlurb ("RecordComparison");
		if blurb:
			doc.append (DIV (blurb, id='blurb'))
		
		sideBySideDisplay = SideBySideDisplay (self.dupGroup)
		doc.append (sideBySideDisplay.html);
		
		return doc
		
	def write (self, path=None):
		if path is None:
			path = 'html/comp.html'
		fp = open(path, 'w')
		fp.write (self.makeHtmlDoc().__str__())
		fp.close()
		print 'wrote to ', path
		
def getDupGroup(key=None):
	from comparisonManager import ComparisonManager
	cm = ComparisonManager()
	if key is None:
		return cm.values()[2]
	return cm[key]
		
if __name__ == '__main__':
	dupGroup = getDupGroup('womeninmeteorology')
	rch = RecordCompareHtml (dupGroup)
	rch.write()
