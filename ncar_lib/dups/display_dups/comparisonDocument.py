from HyperText.HTML40 import *
from html import HtmlDocument
from termCompareGroup import TermCompareGroup, getTermCompareGroup
# from cmpRecHtml import CmpRecord
from comparisonRecord import ComparisonRecord, ComparisonTable

class RecordCompareHtml:

	def __init__ (self, termMapEntryComp):
		self.title = "Record Comparison"
		self.termMapEntryComp = termMapEntryComp

	def makeHtmlDoc (self):
		"""
		Generate the html document as string
		"""
		## title = os.path.splitext(self.filename)[0]
		title=self.title
		doc = HtmlDocument (title=title, stylesheet="resources/styles.css")
		# doc.body["onload"] = "init();"
		
		# <meta http-equiv="Content-Type" content="text/html; charset=iso-8859-1">
		
		doc.head.append (META(http_equiv="Content-Type",
                          content="text/html; charset=utf-8"))
		
		doc.addJavascript ("resources/prototype.js")
		doc.append (DIV (id="debug"))
		doc.append (H1 (title))
		
		# doc.append (self.getXmlRecord());  # old school
		doc.append (self.getComparisonTable());
		
		# doc.append (self.html)
		return doc
		
	def getComparisonTable (self):
		return ComparisonTable (self.termMapEntryComp).html
		
	def getXmlRecord (self):
		"""
		grab some XML and see how it presents
		"""
		search_results = self.termMapEntryComp
		records = map (lambda x:x.payload, search_results)
		xml = TABLE()
		hdr = TR(valign='top')
		xml.append(hdr)
		for result in search_results:
			hdr.append(TD (result.collectionName, klass='collection-name'))
		
		row = TR(valign='top');xml.append(row)
		for record in records:
			row.append (TD (ComparisonRecord (record).html, width='%d%%' % (100/len(records))))
		return xml
		
	def write (self, path=None):
		if path is None:
			path = 'html/comp.html'
		fp = open(path, 'w')
		fp.write (self.makeHtmlDoc().__str__())
		fp.close()
		print 'wrote to ', path
		
if __name__ == '__main__':
	rch = RecordCompareHtml (getTermCompareGroup())
	rch.write()
